import mysql.connector
from database import get_connection
from Models.cart_model import Cart
from typing import List, Dict

class SalesRegisterDAO:
    @staticmethod
    def create_sales_register(folio_venta: str, cart: Cart) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            for item in cart.items:
                query = "INSERT INTO sales_register (folio_venta, upc_product, quantity) VALUES (%s, %s, %s)"
                cursor.execute(query, (folio_venta, item.upc_product, item.quantity))
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
    def get_products_by_folio(folio_venta: str) -> List[Dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT upc_product, quantity FROM sales_register WHERE folio_venta = %s"
            cursor.execute(query, (folio_venta,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()