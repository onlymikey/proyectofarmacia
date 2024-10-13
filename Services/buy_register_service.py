from Models.cart_model import Cart
from Daos.buy_register_dao import BuyRegisterDAO
from typing import List, Dict

class BuyRegisterService:
    @staticmethod
    def add_buy_register(buy_suppliers_folio: str, cart: Cart) -> bool:
        return BuyRegisterDAO.add_buy_register(buy_suppliers_folio, cart)

    @staticmethod
    def get_products_by_folio(buy_suppliers_folio: str) -> List[Dict]:
        return BuyRegisterDAO.get_products_by_folio(buy_suppliers_folio)