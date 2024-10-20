import mysql.connector
from database import get_connection
from Models.buy_model import Buy
from typing import List, Dict, Optional

class BuyDAO:
    @staticmethod
    def create_buy(buy: Buy) -> Optional[int]:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "INSERT INTO buys (folio, user_id, iup_supplier, total, date) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (buy.folio, buy.user_id, buy.iup_supplier, buy.total, buy.date))
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
    def get_buy_by_folio(folio: str) -> Optional[Dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM buys WHERE folio = %s"
            cursor.execute(query, (folio,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_buys() -> List[Dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM buys"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_buy(buy: Buy) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "UPDATE buys SET user_id = %s, iup_supplier = %s, total = %s, date = %s WHERE folio = %s"
            cursor.execute(query, (buy.user_id, buy.iup_supplier, buy.total, buy.date, buy.folio))
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
    def delete_buy(folio: str) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "DELETE FROM buys WHERE folio = %s"
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