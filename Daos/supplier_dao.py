import mysql.connector
from database import get_connection
from Models.supplier_model import Supplier
from typing import List, Dict, Optional

class SupplierDAO:
    @staticmethod
    def create_supplier(supplier: Supplier) -> Optional[int]:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "INSERT INTO suppliers (iup, companyName) VALUES (%s, %s)"
            cursor.execute(query, (supplier.iup, supplier.companyName))
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
    def get_supplier_by_iup(iup: str) -> Optional[Dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM suppliers WHERE iup = %s"
            cursor.execute(query, (iup,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_suppliers() -> List[Dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM suppliers"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_supplier(supplier: Supplier) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "UPDATE suppliers SET companyName = %s WHERE iup = %s"
            cursor.execute(query, (supplier.companyName, supplier.iup))
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
    def delete_supplier(iup: str) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "DELETE FROM suppliers WHERE iup = %s"
            cursor.execute(query, (iup,))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()