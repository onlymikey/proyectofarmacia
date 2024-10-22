from Services.user_service import UserService
import re
class UserController:
    def __init__(self):
        self.user_service = UserService()

    @staticmethod
    def validate_user_data(name: str, username: str, password: str, profile: str) -> dict:
        """Valida los datos de un usuario"""
        msg = {
            'status': False,
            'type': 'Error',
            'message': ''
        }
        # 1. Validar todos los campos obligatorios
        if not name or not username or not password or not profile:
            msg['message'] = 'Todos los campos son obligatorios'
            return msg

        # 2. Validar que el nombre sea un string de máximo 50 caracteres
        if len(name) > 50:
            msg['message'] = 'El nombre debe ser un string de máximo 50 caracteres'
            return msg

        # 3. Validar que el nombre de usuario sea un string de máximo 50 caracteres
        if len(username) > 50:
            msg['message'] = 'El nombre de usuario debe ser un string de máximo 50 caracteres'
            return msg

        # 4. Validar que la contraseña contenga al menos un número, una letra mayúscula y un carácter especial ademas de tener una longitud de 8 a 50 caracteres
        if not re.match(r'^(?=.*[A-ZÑ])(?=.*\d)(?=.*[@$!%*?&])[A-Za-zÑñ\d@$!%*?&]{8,50}$', password):
            msg['message'] = 'La contraseña debe contener al menos un número, una letra mayúscula y un carácter especial'
            return msg

        # 5. Validar que el perfil sea un string de máximo 50 caracteres
        if len(profile) > 50:
            msg['message'] = 'El perfil debe ser un string de máximo 50 caracteres'
            return msg

        # Si todos los datos son válidos
        msg['status'] = True
        msg['type'] = 'Success'
        return msg

    def create_user(self, name: str, username: str, password: str, profile: str) -> dict:
        """Crea un usuario"""
        msg = self.validate_user_data(name, username, password, profile)
        if not msg['status']:
            return msg
        if self.user_service.create_user(name, username, password, profile):
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Usuario creado exitosamente'
        else:
            msg['message'] = 'Error en el servicio de creación de usuario'
        return msg

    def get_user_by_id(self, user_id: int) -> dict:
        """Obtiene un usuario por id"""
        user = self.user_service.get_user_by_id(user_id)
        if user:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Usuario encontrado',
                'data': user
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Usuario no encontrado'
        }

    def get_all_users(self) -> dict:
        """Obtiene todos los usuarios"""
        users = self.user_service.get_all_users()
        if users:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Usuarios encontrados',
                'data': users
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Usuarios no encontrados'
        }

    def update_user(self, user_id: int, name: str, username: str, password: str, profile: str) -> dict:
        """Actualiza un usuario"""
        msg = self.validate_user_data(name, username, password, profile)
        if not msg['status']:
            return msg
        if self.user_service.update_user(user_id, name, username, password, profile):
            msg['status'] = True
            msg['type'] = 'Success'
            msg['message'] = 'Usuario actualizado exitosamente'
        else:
            msg['message'] = 'Error en el servicio de actualización de usuario'
        return msg

    def delete_user(self, user_id: int) -> dict:
        """Elimina un usuario"""
        if self.user_service.delete_user(user_id):
            return {
                'status': True,
                'type': 'Success',
                'message': 'Usuario eliminado exitosamente'
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'Error en el servicio de eliminación de usuario'
        }

    def verify_user(self, username: str, password: str) -> dict:
        """Verifica un usuario para login"""
        user = self.user_service.verify_user(username, password)
        if user:
            return {
                'status': True,
                'type': 'Success',
                'message': 'Usuario verificado',
                'data': user
            }
        return {
            'status': False,
            'type': 'Error',
            'message': 'El usuario no existe o la contraseña es incorrecta'
        }

    def get_next_user_id(self) -> int:
        """Obtiene el siguiente id de usuario"""
        next_user_id = self.user_service.get_next_user_id()
        return next_user_id

