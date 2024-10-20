from Models.sale_model import Sale
from Daos.sale_dao import SaleDAO
from typing import Optional, List, Dict

class SaleService:
    @staticmethod
    def create_sale(folio: str, client_id: int, user_id: int, date: str, total: float) -> Optional[int]:
        sale = Sale(folio=folio, client_id=client_id, user_id=user_id, date=date, total=total)
        return SaleDAO.create_sale(sale)

    @staticmethod
    def get_sale_by_folio(folio: str) -> Optional[Dict]:
        return SaleDAO.get_sale_by_folio(folio)

    @staticmethod
    def get_all_sales() -> List[Dict]:
        return SaleDAO.get_all_sales()

    @staticmethod
    def update_sale(folio: str, client_id: int, user_id: int, date: str, total: float) -> bool:
        sale = Sale(folio=folio, client_id=client_id, user_id=user_id, date=date, total=total)
        return SaleDAO.update_sale(sale)

    @staticmethod
    def delete_sale(folio: str) -> bool:
        return SaleDAO.delete_sale(folio)