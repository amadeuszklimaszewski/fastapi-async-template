import asyncio

from sqlalchemy import select
import datetime
from src.adapters.orm import mapper_registry, UserDAO
from src.data_access.sqlalchemy import SQLAlchemyAsyncDataAccess
from src.database.connection import async_session, engine
from src.models.user import User


class UserDataAccess(SQLAlchemyAsyncDataAccess):
    @property
    def _dao(self) -> UserDAO:
        return UserDAO

    @property
    def _model(self) -> User:
        return User


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
        await conn.run_sync(mapper_registry.metadata.create_all)


async def main():
    # await init_models()
    async with async_session() as session:
        # user1 = UserDAO(email="testt@gmail.com", password="test")
        # print(user1)
        # user1.updated_at = datetime.datetime.now()
        user_da = UserDataAccess(session)
        # print(user1.id)
        # await user_da.persist(user1)
        # await user_da.refresh_from_db(user1)
        # print(user1.id)
        user = await user_da.get(pk="ea810928-cfba-4c4a-bdf5-bb2f8e576477")
        # print(user.email)
        # user.email = "changedk111@email.com"
        # await user_da.persist(user)
        print(user.updated_at)
        # print(user_da._model)
        # rs = (await session.scalars(select(User))).all()
        # print(rs)


if __name__ == "__main__":

    asyncio.run(main())
