from src.data_access import UserAsyncDataAccess
from src.models import User
from src.schemas import RegisterSchema
from src.services.exceptions import AlreadyExists
from src.utils import get_password_hash


async def register_user(
    data_access: UserAsyncDataAccess, schema: RegisterSchema
) -> User:
    user_data = schema.dict(exclude={"repeat_password"})

    if await data_access.get_many(email=user_data["email"]):
        raise AlreadyExists("User with given email already exists")

    user_data["password"] = get_password_hash(user_data["password"])
    new_user = User(**user_data)

    return await data_access.persist(new_user)
