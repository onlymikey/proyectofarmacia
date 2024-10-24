class Client:
    def __init__(self, id:int, name:str, email:str, phone:str, points:int):
        self.id = id #identificador unico de cliente
        self.name = name
        self.phone = phone
        self.email = email
        self.points = points