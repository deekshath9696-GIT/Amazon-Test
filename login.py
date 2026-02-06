"""
Amazon Store - Login and Purchase System
Integrated login functionality with Adidas bat purchase
"""

from purchase_bat import Product, Purchase


class User:
    def __init__(self, username, password, full_name, address):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.address = address
        self.purchase_history = []

    def verify_password(self, password):
        return self.password == password


class UserDatabase:
    def __init__(self):
        # Pre-registered users (in real app, this would be a database)
        self.users = {
            "john_doe": User("john_doe", "password123", "John Doe", "123 Main St, New York, NY 10001"),
            "jane_smith": User("jane_smith", "pass456", "Jane Smith", "456 Oak Ave, Los Angeles, CA 90001"),
        }

    def register_user(self, username, password, full_name, address):
        if username in self.users:
            return False, "Username already exists"

        self.users[username] = User(username, password, full_name, address)
        return True, "Registration successful"

    def authenticate(self, username, password):
        if username in self.users:
            user = self.users[username]
            if user.verify_password(password):
                return True, user
        return False, None


class AmazonStore:
    def __init__(self):
        self.user_db = UserDatabase()
        self.current_user = None
        self.adidas_bats = [
            Product("BAT001", "XT Bat", "Adidas", 89.99, 15),
            Product("BAT002", "Incurza Bat", "Adidas", 129.99, 10),
            Product("BAT003", "Libro Bat", "Adidas", 149.99, 8),
        ]

    def display_menu(self):
        print("\n" + "=" * 50)
        print("AMAZON STORE - ADIDAS BATS")
        print("=" * 50)
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        print("=" * 50)

    def login(self):
        print("\n=== LOGIN ===")
        username = input("Username: ")
        password = input("Password: ")

        success, user = self.user_db.authenticate(username, password)
        if success:
            self.current_user = user
            print(f"\n✓ Welcome back, {user.full_name}!")
            return True
        else:
            print("\n✗ Invalid username or password")
            return False

    def register(self):
        print("\n=== REGISTER NEW ACCOUNT ===")
        username = input("Choose username: ")
        password = input("Choose password: ")
        full_name = input("Full name: ")
        address = input("Shipping address: ")

        success, message = self.user_db.register_user(username, password, full_name, address)
        print(f"\n{message}")

        if success:
            print("You can now login with your credentials.")

        return success

    def display_products(self):
        print("\n=== AVAILABLE ADIDAS BATS ===")
        for i, bat in enumerate(self.adidas_bats, 1):
            print(f"{i}. {bat}")
        print()

    def shop(self):
        if not self.current_user:
            print("\n✗ Please login first")
            return

        # Create purchase instance with logged-in user info
        purchase = Purchase(self.current_user.full_name, self.current_user.address)

        while True:
            print("\n" + "=" * 50)
            print("SHOPPING MENU")
            print("=" * 50)
            print("1. View Adidas Bats")
            print("2. Add to Cart")
            print("3. View Cart")
            print("4. Checkout")
            print("5. Return to Main Menu")
            print("=" * 50)

            choice = input("Select option (1-5): ")

            if choice == "1":
                self.display_products()

            elif choice == "2":
                self.display_products()
                try:
                    bat_choice = int(input("Select bat number (1-3): "))
                    if 1 <= bat_choice <= len(self.adidas_bats):
                        selected_bat = self.adidas_bats[bat_choice - 1]
                        quantity = int(input(f"Enter quantity (Available: {selected_bat.stock}): "))

                        if quantity > 0:
                            purchase.cart.add_item(selected_bat, quantity)
                        else:
                            print("Quantity must be at least 1")
                    else:
                        print("Invalid bat selection")
                except ValueError:
                    print("Please enter valid numbers")

            elif choice == "3":
                purchase.cart.display_cart()

            elif choice == "4":
                if len(purchase.cart.items) == 0:
                    print("\n✗ Your cart is empty")
                    continue

                purchase.cart.display_cart()

                confirm = input("\nProceed to checkout? (y/n): ")
                if confirm.lower() == 'y':
                    print("\nPayment Options:")
                    print("1. Credit Card")
                    print("2. Debit Card")
                    print("3. PayPal")

                    payment_choice = input("Select payment method (1-3): ")
                    payment_methods = {
                        "1": "credit_card",
                        "2": "debit_card",
                        "3": "paypal"
                    }

                    payment_method = payment_methods.get(payment_choice, "credit_card")

                    if payment_choice in ["1", "2"]:
                        card_number = input("Enter card number: ")
                    else:
                        card_number = None

                    if purchase.process_payment(payment_method, card_number):
                        purchase.complete_purchase()
                        self.current_user.purchase_history.append(purchase)
                        return
                    else:
                        print("Payment failed")

            elif choice == "5":
                break

            else:
                print("Invalid option")

    def run(self):
        print("\n" + "=" * 50)
        print("WELCOME TO AMAZON STORE")
        print("=" * 50)

        while True:
            if not self.current_user:
                self.display_menu()
                choice = input("Select option (1-3): ")

                if choice == "1":
                    if self.login():
                        self.shop()
                        self.current_user = None  # Logout after shopping

                elif choice == "2":
                    self.register()

                elif choice == "3":
                    print("\nThank you for visiting Amazon Store!")
                    break

                else:
                    print("Invalid option")
            else:
                self.shop()


if __name__ == "__main__":
    store = AmazonStore()
    store.run()
