from Models.product_model import Product
from Daos.product_dao import ProductDAO
from typing import Optional, List, Dict

class ProductService:
    @staticmethod
    def create_product(upc: str, name: str, stock: int, description: str, price: float) -> Optional[int]:
        product = Product(upc=upc, name=name, stock=stock, description=description, price=price)
        return ProductDAO.create_product(product)
    
    @staticmethod
    def product_exists(upc: str) -> bool:
        return ProductDAO.product_exists(upc)

    @staticmethod
    def get_product_by_upc(upc: str) -> Optional[Dict]:
        return ProductDAO.get_product_by_upc(upc)

    @staticmethod
    def get_product_by_name(name: str) -> Optional[Dict]:
        return ProductDAO.get_product_by_name(name)

    @staticmethod
    def get_all_products() -> List[Dict]:
        return ProductDAO.get_all_products()

    @staticmethod
    def update_product(upc: str, name: str, stock: int, description: str, price: float) -> bool:
        product = Product(upc=upc, name=name, stock=stock, description=description, price=price)
        return ProductDAO.update_product(product)
    @staticmethod
    def delete_product(upc: str) -> bool:
        return ProductDAO.delete_product(upc)