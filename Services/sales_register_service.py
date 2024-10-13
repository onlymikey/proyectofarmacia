from Models.cart_model import Cart
from Daos.sales_register_dao import SalesRegisterDAO
from typing import List, Dict

class SalesRegisterService:
    @staticmethod
    def create_sales_register(folio_venta: str, cart: Cart) -> bool:
        return SalesRegisterDAO.create_sales_register(folio_venta, cart)

    @staticmethod
    def get_products_by_folio(folio_venta: str) -> List[Dict]:
        return SalesRegisterDAO.get_products_by_folio(folio_venta)