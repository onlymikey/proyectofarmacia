from Services.client_service import ClientService
import re
class ClientController:
    def __init__(self):
        self.client_service = ClientService()
    @staticmethod
    def validate_client_data(name: str, email: str, phone: str) -> dict:
        """Valida los datos de un cliente"""
        msg = {
            'status': False,
            'type': 'Error',
            'message': ''
        }
        # 1. Validar todos los campos obligatorios
        if not name or not email or not phone:
            msg['message'] = 'Todos los campos son obligatorios'
            return msg

        # 2. Validar que el nombre sea un string de máximo 50 caracteres
        if len(name) > 50:
            msg['message'] = 'El nombre debe ser un string de máximo 50 caracteres'
            return msg

        # 3. Validar que el email sea un string de máximo 50 caracteres
        if len(email) > 50:
            msg['message'] = 'El email debe ser un string de máximo 50 caracteres'
            return msg

        # 4. Validar que el teléfono sea un string de máximo 14 caracteres
        if len(phone) > 14:
            msg['message'] = 'El teléfono debe ser un string de máximo 14 caracteres'
            return msg

        # 6. Validar que el email tenga el formato correcto
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            msg['message'] = 'El email debe tener un formato válido'
            return msg

        # 7. Validar que el teléfono tenga el formato correcto
        if not re.match(r'^\+\d{1,3}\s\d{10}$', phone):
            msg['message'] = 'El teléfono debe tener un formato válido'
            return msg

        # Si todos los datos son válidos
        msg['status'] = True
        msg['type'] = 'Success'
        return msg


    def create_client(self, name: str, email: str, phone: str) -> dict:
        """Crea un cliente"""
        msg = self.validate_client_data(name, email, phone)
        if not msg['status']:
            return msg
        if self.client_service.create_client(name, email, phone):
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Cliente creado exitosamente'
        else:
            msg['message'] = 'Error en el servicio de creación de cliente'
        return msg

    def get_client_by_id(self, client_id: int) -> dict:
        """Obtiene un cliente por id"""
        client = self.client_service.get_client_by_id(client_id)
        if client:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Cliente encontrado',
                'data': client
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Cliente no encontrado'
        }

    def get_all_clients(self) -> dict:
        """Obtiene todos los clientes"""
        clients = self.client_service.get_all_clients()
        if clients:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Clientes encontrados',
                'data': clients
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Clientes no encontrados'
        }

    def update_client(self, client_id: int, name: str, email: str, phone: str, points:int) -> dict:
        """Actualiza un cliente"""
        msg = self.validate_client_data(name, email, phone)
        if not msg['status']:
            return msg
        if self.client_service.update_client(client_id, name, email, phone, points):
            return {
                'status': True,
                'type': 'Success',
                'message': 'Cliente actualizado exitosamente'
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Error en el servicio de actualización de cliente'
        }

    def delete_client(self, client_id: int) -> dict:
        """Elimina un cliente"""
        if self.client_service.delete_client(client_id):
            return {
                'status': True,
                'type': 'Success',
                'message': 'Cliente eliminado exitosamente'
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Error en el servicio de eliminación de cliente'
        }

    def get_next_client_id(self) -> int:
        """Obtiene el siguiente id de cliente"""
        next_client_id = self.client_service.get_next_client_id()
        return next_client_id