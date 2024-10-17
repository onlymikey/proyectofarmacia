from Services.buy_service import BuyService
import datetime
class BuyController:
    def __init__(self):
        self.buy_service = BuyService()

    @staticmethod
    def validate_buy_data(folio: str, user_id: int, iup_supplier: str, total: float, date: str) -> dict:
        """Valida los datos de una compra"""
        msg = {
            'status': False,
            'type': 'Error',
            'message': ''
        }
        # 1. Validar todos los campos obligatorios
        if not folio or not user_id or not iup_supplier or not total or not date:
            msg['message'] = 'Todos los campos son obligatorios'
            return msg

        # 2. Validar que el folio sea un string de maximo 20 caracteres
        if not folio.isdigit() or len(folio) > 20:
            msg['message'] = 'El folio debe ser un número de máximo 20 caracteres'
            return msg

        # 3. Validar que el id de usuario sea un entero positivo
        if not user_id > 0:
            msg['message'] = 'El id de usuario debe ser un entero positivo'
            return msg

        # 4. Validar que el iup del proveedor sea un string de máximo 20 caracteres
        if len(iup_supplier) > 20:
            msg['message'] = 'El iup del proveedor debe ser un string de máximo 20 caracteres'
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

    def create_buy(self, folio: str, user_id: int, iup_supplier: str, total: float, date: str) -> dict:
        """Crea una compra"""
        msg = self.validate_buy_data(folio, user_id, iup_supplier, total, date)
        if msg['status']:
            return msg
        if self.buy_service.create_buy(folio, user_id, iup_supplier, total, date):
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Compra creada exitosamente'
        else:
            msg['message'] = 'Error en el servicio de creación de compra'
        return msg

    def get_buy_by_folio(self, folio: str) -> dict:
        """Obtiene una compra por folio"""
        buy = self.buy_service.get_buy_by_folio(folio)
        if buy:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Compra encontrada',
                'data': buy
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Compra no encontrada'
        }

    def get_all_buys(self) -> dict:
        """Obtiene todas las compras"""
        buys = self.buy_service.get_all_buys()
        if buys:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Compras encontradas',
                'data': buys
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'No se encontraron compras'
        }

    def update_buy(self, folio: str, user_id: int, iup_supplier: str, total: float, date: str) -> dict:
        """Actualiza una compra"""
        msg = self.validate_buy_data(folio, user_id, iup_supplier, total, date)
        if msg['status']:
            return msg
        if self.buy_service.update_buy(folio, user_id, iup_supplier, total, date):
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Compra actualizada exitosamente'
        else:
            msg['message'] = 'Error en el servicio de actualización de compra'
        return msg

    def delete_buy(self, folio: str) -> dict:
        """Elimina una compra"""
        if self.buy_service.delete_buy(folio):
            return {
                'status': True,
                'type': 'Success',
                'message': 'Compra eliminada exitosamente'
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Error en el servicio de eliminación de compra'
        }