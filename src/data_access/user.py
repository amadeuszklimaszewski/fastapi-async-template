from src.adapters.orm import UserDAO
from src.data_access import SQLAlchemyAsyncDataAccess
from src.models import User


class UserAsyncDataAccess(SQLAlchemyAsyncDataAccess):
    @property
    def _dao(self) -> UserDAO:
        return UserDAO

    @property
    def _model(self) -> User:
        return User
