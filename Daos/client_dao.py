import mysql.connector
from database import get_connection
from Models.client_model import Client
from typing import List, Optional

class ClientDAO:
    @staticmethod
    def create_client(client: Client) -> Optional[int]:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "INSERT INTO clients (name, email, phone, points) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (client.name, client.email, client.phone, client.points))
            connection.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_client_by_id(client_id: int) -> Optional[dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM clients WHERE id = %s"
            cursor.execute(query, (client_id,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_clients() -> List[dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM clients"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_client(client: Client) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "UPDATE clients SET name = %s, email = %s, phone = %s, points = %s WHERE id = %s"
            cursor.execute(query, (client.name, client.email, client.phone, client.points, client.id))
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
    def delete_client(client_id: int) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "DELETE FROM clients WHERE id = %s"
            cursor.execute(query, (client_id,))
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
    def get_next_client_id() -> int:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "SELECT MAX(id) FROM clients"
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] + 1 if result[0] else 1
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 1
        finally:
            cursor.close()
            connection.close()