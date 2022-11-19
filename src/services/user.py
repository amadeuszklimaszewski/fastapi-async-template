from src.data_access import UserAsyncDataAccess
from src.models import User
from src.schemas import RegisterSchema
from src.services.exceptions import AlreadyExists, InvalidCredentials
from src.utils import pwd_context


class UserService:
    def __init__(self, data_access: UserAsyncDataAccess) -> None:
        self.data_access = data_access

    @classmethod
    def _hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    async def register_user(self, schema: RegisterSchema) -> User:
        user_data = schema.dict(exclude="repeat_password")

        if await self.data_access.get_many(email=user_data["email"]):
            raise AlreadyExists("User with given email already exists")

        user_data["password"] = self._hash_password(user_data["password"])
        new_user = User(**schema.dict())

        return await self.data_access.persist(new_user)

    async def authenticate(self, email: str, password: str) -> User:
        users = await self.data_access.get_many(email=email)
        if not users or not pwd_context.verify(password, users[0].password):
            raise InvalidCredentials("Invalid credentials provided")
        return users[0]
