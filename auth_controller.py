from database import create_connection

class AuthController:
    def __init__(self):
        self.connection = create_connection()

    def login(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return {
                'status': True,
                'user': user
            }
        else:
            return {
                'status': False,
                'message': 'Usuario o contraseña incorrectos'
            }
