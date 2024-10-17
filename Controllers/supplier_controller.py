from Services.supplier_service import SupplierService

class SupplierController:
    def __init__(self):
        self.supplier_service = SupplierService()

    @staticmethod
    def validate_supplier_data(iup: str, companyName: str) -> dict:
        """Valida los datos de un proveedor"""
        msg = {
            'status': False,
            'type': 'Error',
            'message': ''
        }
        # 1. Validar todos los campos obligatorios
        if not iup or not companyName:
            msg['message'] = 'Todos los campos son obligatorios'
            return msg

        # 2. Validar que el iup sea un string de máximo 20 caracteres
        if len(iup) > 20:
            msg['message'] = 'El iup debe ser un string de máximo 20 caracteres'
            return msg

        # 3. Validar que el nombre de la empresa sea un string de máximo 50 caracteres
        if len(companyName) > 50:
            msg['message'] = 'El nombre de la empresa debe ser un string de máximo 50 caracteres'
            return msg

        # Si todos los datos son válidos
        msg['status'] = True
        msg['type'] = 'Success'
        return msg


    def create_supplier(self, iup: str, companyName: str) -> dict:
        """Crea un proveedor"""
        msg = self.validate_supplier_data(iup, companyName)
        if not msg['status']:
            return msg
        if self.supplier_service.create_supplier(iup, companyName):
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Proveedor creado exitosamente'
        else:
            msg['message'] = 'Error en el servicio de creación de proveedor'
        return msg

    def get_supplier_by_iup(self, iup: str) -> dict:
        """Obtiene un proveedor por iup"""
        supplier = self.supplier_service.get_supplier_by_iup(iup)
        if supplier:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Proveedor encontrado',
                'data': supplier
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Proveedor no encontrado'
        }

    def get_all_suppliers(self) -> dict:
        """Obtiene todos los proveedores"""
        suppliers = self.supplier_service.get_all_suppliers()
        if suppliers:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Proveedores encontrados',
                'data': suppliers
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'No hay proveedores registrados'
        }

    def update_supplier(self, iup: str, companyName: str) -> dict:
        """Actualiza un proveedor"""
        msg = self.validate_supplier_data(iup, companyName)
        if not msg['status']:
            return msg
        if self.supplier_service.update_supplier(iup, companyName):
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Proveedor actualizado exitosamente'
        else:
            msg['message'] = 'Error en el servicio de actualización de proveedor'
        return msg

    def delete_supplier(self, iup: str) -> dict:
        """Elimina un proveedor"""
        if self.supplier_service.delete_supplier(iup):
            return {
                'status': True,
                'type': 'Success',
                'message': 'Proveedor eliminado exitosamente'
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Error en el servicio de eliminación de proveedor'
        }