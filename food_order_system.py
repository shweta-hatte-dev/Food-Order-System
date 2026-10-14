
from collections import deque

# Food menu
menu = {
    1: {"name": "Burger", "price": 60},
    2: {"name": "Pizza", "price": 120},
    3: {"name": "Sandwich", "price": 50},
    4: {"name": "French Fries", "price": 70},
    5: {"name": "Cold Coffee", "price": 60}
}

# Queue and order records
order_queue = deque()
preparing_orders = []
completed_orders = []
order_counter = 1


# Display food menu
def display_menu():
    print("\n========== FOOD MENU ==========")
    for number, item in menu.items():
        print(f"{number}. {item['name']} - Rs. {item['price']}")
    print("================================")


# Place a new order
def place_order():
    global order_counter

    customer = input("Enter customer name: ").strip()

    if not customer:
        print("Error: Customer name cannot be empty.")
        return

    display_menu()

    try:
        choice = int(input("Select food item number: "))

        if choice not in menu:
            print("Error: Invalid food item.")
            return

        quantity = int(input("Enter quantity: "))

        if quantity <= 0:
            print("Error: Quantity must be greater than zero.")
            return

    except ValueError:
        print("Error: Please enter a valid number.")
        return

    food = menu[choice]

    order = {
        "order_id": order_counter,
        "customer": customer,
        "food": food["name"],
        "quantity": quantity,
        "price": food["price"] * quantity,
        "status": "Pending"
    }

    # ENQUEUE: Add order to the rear of the queue
    order_queue.append(order)

    print("\nOrder placed successfully!")
    print("Order Number:", order["order_id"])
    print("Customer:", order["customer"])
    print("Food:", order["food"])
    print("Quantity:", order["quantity"])
    print("Total Bill: Rs.", order["price"])
    print("Status:", order["status"])

    order_counter += 1


# View pending orders
def view_pending_orders():
    print("\n========== PENDING ORDERS ==========")

    if not order_queue:
        print("No pending orders.")
        return

    for order in order_queue:
        print(
            f"Order No: {order['order_id']} | "
            f"Customer: {order['customer']} | "
            f"Food: {order['food']} | "
            f"Quantity: {order['quantity']} | "
            f"Bill: Rs. {order['price']} | "
            f"Status: {order['status']}"
        )


# Start preparing the oldest pending order
def prepare_next_order():
    if not order_queue:
        print("\nNo pending orders to prepare.")
        return

    # DEQUEUE: Remove the oldest order
    order = order_queue.popleft()
    order["status"] = "Preparing"
    preparing_orders.append(order)

    print("\nOrder moved to preparation!")
    print("Order Number:", order["order_id"])
    print("Customer:", order["customer"])
    print("Food:", order["food"])
    print("Status:", order["status"])


# View orders being prepared
def view_preparing_orders():
    print("\n========== ORDERS BEING PREPARED ==========")

    if not preparing_orders:
        print("No orders are being prepared.")
        return

    for order in preparing_orders:
        print(
            f"Order No: {order['order_id']} | "
            f"Customer: {order['customer']} | "
            f"Food: {order['food']} | "
            f"Status: {order['status']}"
        )


# Complete an order
def complete_order():
    if not preparing_orders:
        print("\nNo orders are currently being prepared.")
        return

    view_preparing_orders()

    try:
        order_id = int(input("Enter order number to complete: "))
    except ValueError:
        print("Error: Enter a valid order number.")
        return

    for order in preparing_orders:
        if order["order_id"] == order_id:
            order["status"] = "Completed"
            preparing_orders.remove(order)
            completed_orders.append(order)

            print("\nOrder completed successfully!")
            print("Order Number:", order["order_id"])
            print("Customer:", order["customer"])
            print("Food:", order["food"])
            print("Final Bill: Rs.", order["price"])
            print("Status:", order["status"])
            return

    print("Error: Order not found in the preparation list.")


# View completed orders and total sales
def view_completed_orders():
    print("\n========== COMPLETED ORDERS ==========")

    if not completed_orders:
        print("No completed orders.")
        return

    total_sales = 0

    for order in completed_orders:
        print(
            f"Order No: {order['order_id']} | "
            f"Customer: {order['customer']} | "
            f"Food: {order['food']} | "
            f"Quantity: {order['quantity']} | "
            f"Bill: Rs. {order['price']} | "
            f"Status: {order['status']}"
        )
        total_sales += order["price"]

    print("---------------------------------------")
    print("Total Sales: Rs.", total_sales)


# Main application
def main():
    while True:
        print("\n========================================")
        print("     FOOD ORDER PROCESSING SYSTEM")
        print("========================================")
        print("1. Display Food Menu")
        print("2. Place an Order")
        print("3. View Pending Orders")
        print("4. Prepare Next Order")
        print("5. View Orders Being Prepared")
        print("6. Complete an Order")
        print("7. View Completed Orders")
        print("8. Exit")
        print("========================================")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Error: Please enter a number from 1 to 8.")
            continue

        if choice == 1:
            display_menu()
        elif choice == 2:
            place_order()
        elif choice == 3:
            view_pending_orders()
        elif choice == 4:
            prepare_next_order()
        elif choice == 5:
            view_preparing_orders()
        elif choice == 6:
            complete_order()
        elif choice == 7:
            view_completed_orders()
        elif choice == 8:
            print("\nThank you for using the Food Order System!")
            break
        else:
            print("Invalid choice. Please select 1 to 8.")


# Run the application
if __name__ == "__main__":
    main()
