class Buy:
    def __init__(self, folio:str, user_id:int, iup_supplier:str, total:float, date:str):
        #el date debe seguir el formato de la db de tipo dateTime (o pertenecer a una biblioteca que lo haga)
        self.folio = folio
        self.user_id = user_id
        self.iup_supplier = iup_supplier
        self.total = total
        self.date = date