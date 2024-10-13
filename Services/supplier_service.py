from Models.supplier_model import Supplier
from Daos.supplier_dao import SupplierDAO
from typing import Optional, List, Dict

class SupplierService:
    @staticmethod
    def create_supplier(iup: str, companyName: str) -> Optional[int]:
        supplier = Supplier(iup=iup, companyName=companyName)
        return SupplierDAO.create_supplier(supplier)

    @staticmethod
    def get_supplier_by_iup(iup: str) -> Optional[Dict]:
        return SupplierDAO.get_supplier_by_iup(iup)

    @staticmethod
    def get_all_suppliers() -> List[Dict]:
        return SupplierDAO.get_all_suppliers()

    @staticmethod
    def update_supplier(iup: str, companyName: str) -> bool:
        supplier = Supplier(iup=iup, companyName=companyName)
        return SupplierDAO.update_supplier(supplier)

    @staticmethod
    def delete_supplier(iup: str) -> bool:
        return SupplierDAO.delete_supplier(iup)