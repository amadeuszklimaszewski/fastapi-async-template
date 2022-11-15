# from sqlalchemy.ext.asyncio.session import AsyncSession

from src.models.user import User
from src.schemas.user import RegisterSchema
from src.utils import pwd_context


class UserService:
    @classmethod
    async def _hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    @classmethod
    async def register_user(cls, schema: RegisterSchema) -> User:
        return User(**schema.dict())

    @classmethod
    async def authenticate(cls, email: str, password: str) -> User:
        ...
