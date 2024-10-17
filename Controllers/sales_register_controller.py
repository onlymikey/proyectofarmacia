from Services.sales_register_service import SalesRegisterService
from Models.cart_model import Cart
class SalesRegisterController:
    def __init__(self):
        self.sales_register_service = SalesRegisterService()

    def create_sales_register(self, folio_venta: str, cart: Cart) -> dict:
        """Crea un registro de ventas"""
        msg = {
            'status': False,
            'type': 'Error',
            'message': ''
        }
        if self.sales_register_service.create_sales_register(folio_venta, cart):
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Registro de ventas creado exitosamente'
        else:
            msg['message'] = 'Error en el servicio de creación de registro de ventas'
        return msg

    def get_products_by_folio(self, folio_venta: str) -> dict:
        """Obtiene los productos de un registro de ventas"""
        products = self.sales_register_service.get_products_by_folio(folio_venta)
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