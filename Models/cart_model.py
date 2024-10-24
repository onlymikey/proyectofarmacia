from Models.cart_item_model import CartItem

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, upc_product: str, quantity: int, price: float):
        for item in self.items:
            if item.upc_product == upc_product:
                item.quantity += quantity
                return
        self.items.append(CartItem(upc_product, quantity, price))

    def calculate_subtotal(self):
        """Calcular el subtotal de los productos en el carrito."""
        subtotal = sum(item.price * item.quantity for item in self.items)
        return subtotal
    
    def get_items(self):
        return self.items

    def remove_item(self, upc_product: str):
        self.items = [item for item in self.items if item.upc_product != upc_product]

    def clear_cart(self):
        self.items = []