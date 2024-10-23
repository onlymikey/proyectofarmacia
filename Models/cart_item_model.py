class CartItem:
    #para el carrito de compras
    def __init__(self, upc_product: str, quantity: int):
        self.upc_product = upc_product
        self.quantity = quantity