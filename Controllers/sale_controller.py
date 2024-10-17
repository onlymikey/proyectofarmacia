from Services.sale_service import SaleService
import datetime

class SaleController:
    def __init__(self):
        self.sale_service = SaleService()

    @staticmethod
    def validate_sale_data(folio: str, client_id: int , user_id: int, date: str, total: float) -> dict:
        """Valida los datos de una venta"""
        msg = {
            'status': False,
            'type': 'Error',
            'message': ''
        }
        # 1. Validar todos los campos obligatorios
        if not folio or not user_id or not total or not date:
            msg['message'] = 'Todos los campos son obligatorios'
            return msg

        # 2. Validar que el folio sea un string de maximo 20 caracteres
        if not folio.isdigit() or len(folio) > 20:
            msg['message'] = 'El folio debe ser un número de máximo 20 caracteres'
            return msg

        # 3. Validar que el id de cliente sea un entero positivo
        if not client_id > 0:
            msg['message'] = 'El id de cliente debe ser un entero positivo'
            return msg

        # 4. Validar que el id de usuario sea un entero positivo
        if not user_id > 0:
            msg['message'] = 'El id de usuario debe ser un entero positivo'
            return msg

        # 5. Validar que el total sea un número positivo
        if not total >= 0:
            msg['message'] = 'El total debe ser un número positivo'
            return msg

        # 6. Validar que la fecha siga el formato DD-MM-YYYY
        try:
            datetime.datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
            msg['message'] = 'La fecha debe seguir el formato DD-MM-YYYY'
            return msg

        # Si todos los datos son válidos
        msg['status'] = True
        msg['type'] = 'Success'
        return msg

    def create_sale(self, folio: str, client_id: int, user_id: int, date: str, total: float) -> dict:
        """Crea una venta"""
        msg = self.validate_sale_data(folio, client_id, user_id, date, total)
        if not msg['status']:
            return msg
        if self.sale_service.create_sale(folio, client_id, user_id, date, total):
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Venta creada exitosamente'
        else:
            msg['message'] = 'Error en el servicio de creación de venta'
        return msg

    def get_sale_by_folio(self, folio: str) -> dict:
        """Obtiene una venta por folio"""
        sale = self.sale_service.get_sale_by_folio(folio)
        if sale:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Venta encontrada',
                'data': sale
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Venta no encontrada'
        }

    def get_all_sales(self) -> dict:
        """Obtiene todas las ventas"""
        sales = self.sale_service.get_all_sales()
        if sales:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Ventas encontradas',
                'data': sales
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Ventas no encontradas'
        }

    def update_sale(self, folio: str, client_id: int, user_id: int, date: str, total: float) -> dict:
        """Actualiza una venta"""
        msg = self.validate_sale_data(folio, client_id, user_id, date, total)
        if not msg['status']:
            return msg
        if self.sale_service.update_sale(folio, client_id, user_id, date, total):
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Venta actualizada exitosamente'
        else:
            msg['message'] = 'Error en el servicio de actualización de venta'
        return msg

    def delete_sale(self, folio: str) -> dict:
        """Elimina una venta"""
        if self.sale_service.delete_sale(folio):
            return {
                'status': True,
                'type': 'Success',
                'message': 'Venta eliminada exitosamente'
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Error en el servicio de eliminación de venta'
        }