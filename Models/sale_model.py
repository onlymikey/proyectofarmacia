class Sale:
    def __init__(self, folio:str, client_id:int, user_id:int, date:str, total:float):
        ##el date debe seguir el formato de la db de tipo dateTime (o pertenecer a una biblioteca que lo haga)
        self.folio = folio #folio de la venta (id)
        self.client_id = client_id
        self.user_id = user_id
        self.date = date
        self.total = total