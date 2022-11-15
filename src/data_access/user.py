from src.data_access.sqlalchemy import SQLAlchemyAsyncDataAccess
from src.models.user import User


class UserDataAccess(SQLAlchemyAsyncDataAccess):
    def _model(self) -> User:
        return User
