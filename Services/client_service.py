from Models.client_model import Client
from Daos.client_dao import ClientDAO
from typing import Optional, List, Dict

class ClientService:
    @staticmethod
    def create_client(name: str, email: str, phone: str, points: int) -> Optional[int]:
        client = Client(id=None, name=name, email=email, phone=phone, points=points)
        return ClientDAO.create_client(client)

    @staticmethod
    def get_client_by_id(client_id: int) -> Optional[Dict]:
        return ClientDAO.get_client_by_id(client_id)

    @staticmethod
    def get_all_clients() -> List[Dict]:
        return ClientDAO.get_all_clients()

    @staticmethod
    def update_client(client_id: int, name: str, email: str, phone: str, points:int) -> bool:
        print(points)
        client = Client(id=client_id, name=name, email=email, phone=phone, points=points)
        return ClientDAO.update_client(client)

    @staticmethod
    def delete_client(client_id: int) -> bool:
        return ClientDAO.delete_client(client_id)
    
    @staticmethod
    def get_next_client_id() -> int:
        return ClientDAO.get_next_client_id()