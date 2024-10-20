class Product:
    #para registrar productos en la db
    def __init__(self, upc:str, name:str, stock:int, description:str, price:float):
        self.upc = upc #universal product code (como su id)
        self.name = name
        self.stock = stock
        self.description = description
        self.price = price