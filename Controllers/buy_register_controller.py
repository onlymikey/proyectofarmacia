from Models.cart_model import Cart
from Services.buy_register_service import BuyRegisterService
class BuyRegisterController:
    def __init__(self):
        self.buy_register_service = BuyRegisterService()

    def add_buy_register(self, buy_suppliers_folio: str, cart: Cart) -> dict:
        """Agrega un registro de compra"""
        msg = {
            'status': False,
            'type': 'Error',
            'message': ''
        }
        if self.buy_register_service.add_buy_register(buy_suppliers_folio, cart):
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Registro de compra agregado exitosamente'
        else:
            msg['message'] = 'Error en el servicio de registro de compra'
        return msg

    def get_products_by_folio(self, buy_suppliers_folio: str) -> dict:
        """Obtiene los productos de un registro de compra"""
        products = self.buy_register_service.get_products_by_folio(buy_suppliers_folio)
        if products:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Productos encontrados',
                'data': products
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Productos no encontrados'
        }