import mysql.connector
from database import get_connection
from Models.user_model import User
from typing import Optional, List

class UserDAO:
    @staticmethod
    def create_user(user: User) -> Optional[int]:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "INSERT INTO users (name, username, password, profile) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user.name, user.username, user.password, user.profile))
            connection.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_users() -> List[dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_user(user: User) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "UPDATE users SET name = %s, username = %s, password = %s, profile = %s WHERE id = %s"
            cursor.execute(query, (user.name, user.username, user.password, user.profile, user.id))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_user(user_id: int) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def verify_user(username: str, password: str) -> Optional[dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_next_user_id() -> int:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "SELECT MAX(id) FROM users"
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] + 1 if result[0] else 1
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 1
        finally:
            cursor.close()
            connection.close()