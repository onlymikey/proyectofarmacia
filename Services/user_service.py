from Models.user_model import User
from typing import Optional, List
from Daos.user_dao import UserDAO

class UserService:
    @staticmethod
    def create_user(name: str, username: str, password: str, profile: str) -> Optional[int]:
        user = User(id=None, name=name, username=username, password=password, profile=profile)
        return UserDAO.create_user(user)

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[dict]:
        return UserDAO.get_user_by_id(user_id)

    @staticmethod
    def get_all_users() -> List[dict]:
        return UserDAO.get_all_users()

    @staticmethod
    def update_user(user_id: int, name: str, username: str, password: str, profile: str) -> bool:
        user = User(id=user_id, name=name, username=username, password=password, profile=profile)
        return UserDAO.update_user(user)

    @staticmethod
    def delete_user(user_id: int) -> bool:
        return UserDAO.delete_user(user_id)

    @staticmethod
    def verify_user(username: str, password: str) -> Optional[dict]:
        return UserDAO.verify_user(username, password)

    @staticmethod
    def get_next_user_id() -> int:
        return UserDAO.get_next_user_id()