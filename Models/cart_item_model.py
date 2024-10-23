class CartItem:
    #para el carrito de compras
    def __init__(self, upc_product: str, quantity: int, price: float):
        self.upc_product = upc_product
        self.quantity = quantity
        self.price = price