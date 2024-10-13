from Models.buy_model import Buy
from Daos.buy_dao import BuyDAO
from typing import Optional, List, Dict

class BuyService:
    @staticmethod
    def create_buy(folio: str, user_id: int, iup_supplier: str, total: float, date: str) -> Optional[int]:
        buy = Buy(folio=folio, user_id=user_id, iup_supplier=iup_supplier, total=total, date=date)
        return BuyDAO.create_buy(buy)

    @staticmethod
    def get_buy_by_folio(folio: str) -> Optional[Dict]:
        return BuyDAO.get_buy_by_folio(folio)

    @staticmethod
    def get_all_buys() -> List[Dict]:
        return BuyDAO.get_all_buys()

    @staticmethod
    def update_buy(folio: str, user_id: int, iup_supplier: str, total: float, date: str) -> bool:
        buy = Buy(folio=folio, user_id=user_id, iup_supplier=iup_supplier, total=total, date=date)
        return BuyDAO.update_buy(buy)

    @staticmethod
    def delete_buy(folio: str) -> bool:
        return BuyDAO.delete_buy(folio)