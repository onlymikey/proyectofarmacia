import mysql.connector
from database import get_connection
from Models.sale_model import Sale
from typing import List, Dict, Optional

class SaleDAO:
    @staticmethod
    def create_sale(sale: Sale) -> Optional[int]:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "INSERT INTO sales (folio, client_id, user_id, date, total) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (sale.folio, sale.client_id, sale.user_id, sale.date, sale.total))
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
    def get_sale_by_folio(folio: int) -> Optional[Dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM sales WHERE folio = %s"
            cursor.execute(query, (folio,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_sales() -> List[Dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM sales"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_sale(sale: Sale) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "UPDATE sales SET client_id = %s, user_id = %s, date = %s, total = %s WHERE folio = %s"
            cursor.execute(query, (sale.client_id, sale.user_id, sale.date, sale.total, sale.folio))
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
    def delete_sale(folio: int) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "DELETE FROM sales WHERE folio = %s"
            cursor.execute(query, (folio,))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()