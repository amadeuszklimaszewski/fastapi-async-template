from src.data_access import UserAsyncDataAccess
from src.models.user import User
from src.schemas.user import RegisterSchema
from src.utils import pwd_context


class UserService:
    def __init__(self, data_access: UserAsyncDataAccess) -> None:
        self.data_access = data_access

    @classmethod
    async def _hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    async def register_user(self, schema: RegisterSchema) -> User:
        new_user = User(**schema.dict())
        return await self.data_access.persist(new_user)

    async def authenticate(self, email: str, password: str) -> User:
        ...
