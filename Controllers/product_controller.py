from Services.product_service import ProductService

class ProductController:
    def __init__(self):
        self.product_service = ProductService()

    @staticmethod
    def validate_product_data(upc: str, name: str, description: str, price: float) -> dict:
        """Valida los datos de un producto"""
        msg = {
            'status': False,
            'type': 'Error',
            'message': ''
        }
        # 1. Validar todos los campos obligatorios
        if not upc or not name  or not description or not price:
            msg['message'] = 'Todos los campos son obligatorios'
            return msg

        # 2. Validar que el upc sea un string de máximo 12 caracteres
        if len(upc) > 12:
            msg['message'] = 'El upc debe ser un string de máximo 12 caracteres'
            return msg

        # 3. Validar que el nombre sea un string de máximo 100 caracteres
        if len(name) > 100:
            msg['message'] = 'El nombre debe ser un string de máximo 100 caracteres'
            return msg

        # 5. Validar que la descripción sea un string de máximo 200 caracteres
        if len(description) > 200:
            msg['message'] = 'La descripción debe ser un string de máximo 200 caracteres'
            return msg

        # 6. Validar que el precio sea un número positivo
        if not price >= 0:
            msg['message'] = 'El precio debe ser un número positivo'
            return msg

        # Si todos los datos son válidos
        msg['status'] = True
        msg['type'] = 'Success'
        return msg

    def create_product(self, upc: str, name: str, stock:int, description: str, price: float) -> dict:
        """Crea un producto"""
        msg = self.validate_product_data(upc, name, description, price)
        if not msg['status']:
            return msg
        created = self.product_service.create_product(upc, name, stock, description, price)
        if created is not None:
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Producto creado exitosamente'
        else:
            msg['message'] = 'Error en el servicio de creación de producto'
        return msg

    def get_product_by_upc(self, upc: str) -> dict:
        """Obtiene un producto por upc"""
        product = self.product_service.get_product_by_upc(upc)
        if product:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Producto encontrado',
                'data': product
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Producto no encontrado'
        }

    def get_product_by_name(self, name: str) -> dict:
        """Obtiene un producto por nombre"""
        product = self.product_service.get_product_by_name(name)
        if product:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Producto encontrado',
                'data': product
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Producto no encontrado'
        }

    def get_all_products(self) -> dict:
        """Obtiene todos los productos"""
        products = self.product_service.get_all_products()
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

    def update_product(self, upc: str, name: str, stock: int, description: str, price: float) -> dict:
        """Actualiza un producto"""
        msg = self.validate_product_data(upc, name, description, price)
        if not msg['status']:
            return msg
        if self.product_service.update_product(upc, name, stock, description, price):
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Producto actualizado exitosamente'
        else:
            msg['message'] = 'Error en el servicio de actualización de producto'
        return msg

    def delete_product(self, upc: str) -> dict:
        """Elimina un producto"""
        if self.product_service.delete_product(upc):
            return {
                'status': True,
                'type': 'Success',
                'message': 'Producto eliminado exitosamente'
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Error en el servicio de eliminación de producto'
        }