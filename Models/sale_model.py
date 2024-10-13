class Sale:
    def __init__(self, folio, client_id, user_id, date, total):
        self.folio = folio #folio de la venta (id)
        self.client_id = client_id
        self.user_id = user_id
        self.date = date
        self.total = total