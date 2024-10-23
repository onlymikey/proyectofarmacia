from Services.sales_register_service import SalesRegisterService
from Models.cart_model import Cart
from Controllers.product_controller import ProductController
class SalesRegisterController:
    def __init__(self):
        self.sales_register_service = SalesRegisterService()
        self.product_controller = ProductController()

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

    # def get_data_products_sale(self, products):
    #     #iteramos la funcion get_product_by_upc para obtener los datos de los productos
    #     product_data_list = []
    #     for product in products:
    #         product_data_controller = self.product_controller.get_product_by_upc(product['upc_product'])
    #         if product_data_controller['status']:
    #             product_data_list.append(product_data_controller['data'])

    #     return product_data_list
            