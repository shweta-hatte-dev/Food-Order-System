
from collections import deque
from itertools import count

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "queuebite-local-demo-key"

MENU = {
    1: {
        "name": "Classic Burger",
        "description": "Grilled patty and house sauce",
        "price": 60,
        "emoji": "🍔"
    },
    2: {
        "name": "Cheese Pizza",
        "description": "Cheese, herbs and tomato",
        "price": 120,
        "emoji": "🍕"
    },
    3: {
        "name": "Veg Sandwich",
        "description": "Fresh vegetables and chutney",
        "price": 50,
        "emoji": "🥪"
    },
    4: {
        "name": "French Fries",
        "description": "Golden crispy potato fries",
        "price": 70,
        "emoji": "🍟"
    },
    5: {
        "name": "Cold Coffee",
        "description": "Chilled creamy coffee",
        "price": 60,
        "emoji": "🥤"
    },
    6: {
        "name": "Chocolate Donut",
        "description": "Soft donut with chocolate",
        "price": 45,
        "emoji": "🍩"
    }
}

# Queue: oldest pending order is processed first.
pending_orders = deque()

# Orders that have left the queue but are not yet completed.
preparing_orders = []

# Completed order history.
completed_orders = []

order_ids = count(1001)


@app.template_filter("money")
def money(amount):
    return f"₹{amount:.2f}"


@app.get("/")
def index():
    total_sales = sum(
        order["total"] for order in completed_orders
    )

    total_orders = (
        len(pending_orders)
        + len(preparing_orders)
        + len(completed_orders)
    )

    return render_template(
        "index.html",
        menu=MENU,
        pending_orders=list(pending_orders),
        preparing_orders=preparing_orders,
        completed_orders=list(reversed(completed_orders)),
        total_sales=total_sales,
        total_orders=total_orders
    )


@app.post("/place-order")
def place_order():
    customer = request.form.get("customer", "").strip()
    item_value = request.form.get("item", "")
    quantity_value = request.form.get("quantity", "")

    if not customer:
        flash("Please enter the customer name.", "error")
        return redirect(url_for("index"))

    try:
        item_id = int(item_value)
        quantity = int(quantity_value)
    except (ValueError, TypeError):
        flash("Please select a food item and valid quantity.", "error")
        return redirect(url_for("index"))

    if item_id not in MENU:
        flash("Invalid food item selected.", "error")
        return redirect(url_for("index"))

    if not 1 <= quantity <= 50:
        flash("Quantity must be between 1 and 50.", "error")
        return redirect(url_for("index"))

    food = MENU[item_id]

    order = {
        "id": next(order_ids),
        "customer": customer,
        "food": food["name"],
        "emoji": food["emoji"],
        "quantity": quantity,
        "unit_price": food["price"],
        "total": food["price"] * quantity,
        "status": "Pending"
    }

    # ENQUEUE: Add a new order to the rear.
    pending_orders.append(order)

    flash(
        f"Order #{order['id']} added to the queue successfully!",
        "success"
    )
    return redirect(url_for("index"))


@app.post("/prepare-next")
def prepare_next():
    if not pending_orders:
        flash("There are no pending orders to prepare.", "error")
        return redirect(url_for("index"))

    # DEQUEUE: Remove the oldest pending order from the front.
    order = pending_orders.popleft()
    order["status"] = "Preparing"
    preparing_orders.append(order)

    flash(
        f"Order #{order['id']} is now being prepared.",
        "success"
    )
    return redirect(url_for("index"))


@app.post("/complete-order/<int:order_id>")
def complete_order(order_id):
    for index, order in enumerate(preparing_orders):
        if order["id"] == order_id:
            order["status"] = "Completed"
            completed_orders.append(preparing_orders.pop(index))

            flash(
                f"Order #{order_id} has been completed!",
                "success"
            )
            return redirect(url_for("index"))

    flash("Preparing order not found.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
