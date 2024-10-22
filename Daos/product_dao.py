import mysql.connector
from database import get_connection
from Models.product_model import Product
from typing import List, Optional

class ProductDAO:
    @staticmethod
    def create_product(product: Product) -> Optional[int]:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "INSERT INTO products (upc, name, stock, description, price) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (product.upc, product.name, product.stock, product.description, product.price))
            connection.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

    #verificar si el producto existe, por medio de su upc
    @staticmethod
    def product_exists(upc: str) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "SELECT COUNT(*) FROM products WHERE upc = %s"
            cursor.execute(query, (upc,))
            return cursor.fetchone()[0] > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_product_by_upc(upc: str) -> Optional[dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM products WHERE upc = %s"
            cursor.execute(query, (upc,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_product_by_name(name: str) -> Optional[dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM products WHERE name = %s"
            cursor.execute(query, (name,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_products() -> List[dict]:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM products"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_product(product: Product) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "UPDATE products SET name = %s, stock = %s, description = %s, price = %s WHERE upc = %s"
            cursor.execute(query, (product.name, product.stock, product.description, product.price, product.upc))
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
    def delete_product(upc: str) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            query = "DELETE FROM products WHERE upc = %s"
            cursor.execute(query, (upc,))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()
