"""
Adidas Bat Purchase Module
Handles the purchase flow for an Adidas cricket/baseball bat
"""

class Product:
    def __init__(self, product_id, name, brand, price, stock):
        self.product_id = product_id
        self.name = name
        self.brand = brand
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.brand} {self.name} - ${self.price:.2f} (Stock: {self.stock})"


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity=1):
        if product.stock >= quantity:
            self.items.append({"product": product, "quantity": quantity})
            product.stock -= quantity
            print(f"✓ Added {quantity} x {product.name} to cart")
            return True
        else:
            print(f"✗ Insufficient stock. Only {product.stock} available.")
            return False

    def get_total(self):
        return sum(item["product"].price * item["quantity"] for item in self.items)

    def display_cart(self):
        if not self.items:
            print("Cart is empty")
            return

        print("\n=== Shopping Cart ===")
        for item in self.items:
            product = item["product"]
            quantity = item["quantity"]
            subtotal = product.price * quantity
            print(f"{product.name} x{quantity} - ${subtotal:.2f}")
        print(f"\nTotal: ${self.get_total():.2f}")
        print("=" * 30)


class Purchase:
    def __init__(self, user_name, shipping_address):
        self.user_name = user_name
        self.shipping_address = shipping_address
        self.cart = ShoppingCart()

    def process_payment(self, payment_method, card_number=None):
        total = self.cart.get_total()

        if total == 0:
            print("Cart is empty. Cannot process payment.")
            return False

        print(f"\nProcessing payment of ${total:.2f}...")
        print(f"Payment method: {payment_method}")

        if payment_method == "credit_card" and card_number:
            masked_card = f"****-****-****-{card_number[-4:]}"
            print(f"Card: {masked_card}")

        # Simulate payment processing
        print("✓ Payment successful!")
        return True

    def complete_purchase(self):
        print("\n" + "=" * 50)
        print("PURCHASE CONFIRMATION")
        print("=" * 50)
        print(f"Customer: {self.user_name}")
        print(f"Shipping Address: {self.shipping_address}")
        self.cart.display_cart()
        print("\n✓ Order confirmed! Your items will be shipped soon.")
        print("Thank you for your purchase!")
        print("=" * 50)


def purchase_adidas_bat():
    """Main function to purchase an Adidas bat"""

    # Available Adidas bats
    adidas_bats = [
        Product("BAT001", "XT Bat", "Adidas", 89.99, 15),
        Product("BAT002", "Incurza Bat", "Adidas", 129.99, 10),
        Product("BAT003", "Libro Bat", "Adidas", 149.99, 8),
    ]

    print("=" * 50)
    print("WELCOME TO ADIDAS BAT STORE")
    print("=" * 50)

    # Display available bats
    print("\nAvailable Adidas Bats:")
    for i, bat in enumerate(adidas_bats, 1):
        print(f"{i}. {bat}")

    # Get user information
    user_name = input("\nEnter your name: ")
    shipping_address = input("Enter shipping address: ")

    # Create purchase instance
    purchase = Purchase(user_name, shipping_address)

    # Select bat
    while True:
        try:
            choice = int(input("\nSelect bat number (1-3): "))
            if 1 <= choice <= len(adidas_bats):
                selected_bat = adidas_bats[choice - 1]
                break
            else:
                print("Invalid choice. Please select 1-3.")
        except ValueError:
            print("Please enter a valid number.")

    # Select quantity
    while True:
        try:
            quantity = int(input(f"Enter quantity (Available: {selected_bat.stock}): "))
            if quantity > 0:
                break
            else:
                print("Quantity must be at least 1.")
        except ValueError:
            print("Please enter a valid number.")

    # Add to cart
    if purchase.cart.add_item(selected_bat, quantity):
        # Display cart
        purchase.cart.display_cart()

        # Payment
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

        # Process payment
        if purchase.process_payment(payment_method, card_number):
            # Complete purchase
            purchase.complete_purchase()
        else:
            print("Payment failed. Please try again.")
    else:
        print("Unable to add item to cart.")


if __name__ == "__main__":
    purchase_adidas_bat()
