from Models.cart_item_model import CartItem

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, upc_product: str, quantity: int):
        for item in self.items:
            if item.upc_product == upc_product:
                item.quantity += quantity
                return
        self.items.append(CartItem(upc_product, quantity))

    def remove_item(self, upc_product: str):
        self.items = [item for item in self.items if item.upc_product != upc_product]

    def clear_cart(self):
        self.items = []