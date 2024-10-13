import mysql.connector
from database import get_connection
from typing import List, Dict, Optional
from Models.cart_model import Cart

class BuyRegisterDAO:
    @staticmethod
    def add_buy_register(buy_suppliers_folio: str, cart: Cart) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            for item in cart.items:
                query = "INSERT INTO buy_register (buy_suppliers_folio, upc_product, quantity) VALUES (%s, %s, %s)"
                cursor.execute(query, (buy_suppliers_folio, item.upc_product, item.quantity))
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
    def get_products_by_folio(buy_suppliers_folio: str) -> List[Dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT upc_product, quantity FROM buy_register WHERE buy_suppliers_folio = %s"
            cursor.execute(query, (buy_suppliers_folio,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()