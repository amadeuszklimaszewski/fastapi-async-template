from abc import ABC, abstractmethod
from typing import Type
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.orm import SQLAlchemyDAO
from src.core.exceptions import DoesNotExist
from src.data_access.abstract import AbstractAsyncDataAccess
from src.models.abstract import BaseUUIDModel


class SQLAlchemyAsyncDataAccess(
    AbstractAsyncDataAccess[UUID, SQLAlchemyDAO, BaseUUIDModel], ABC
):
    def __init__(self, async_session: AsyncSession) -> None:
        self._async_session = async_session

    @property
    @abstractmethod
    def _model(self) -> Type[BaseUUIDModel]:
        raise NotImplementedError

    @property
    @abstractmethod
    def _dao(self) -> Type[SQLAlchemyDAO]:
        raise NotImplementedError

    def _map_to_dao(self, model: BaseUUIDModel) -> SQLAlchemyDAO:
        return self._dao.from_model(model)

    async def _commit(self) -> None:
        await self._async_session.commit()

    async def get(self, pk: UUID) -> BaseUUIDModel:
        result = (
            await self._async_session.scalars(
                select(self._dao).where(self._dao.id == pk)
            )
        ).first()
        if not result:
            raise DoesNotExist(
                f"{self.__class__.__name__} could not find {self._model.__name__} with given PK - {pk}"
            )
        return self._model.from_orm(result)

    async def get_many(self, **kwargs) -> list[BaseUUIDModel]:
        args = [getattr(self._dao, k) == v for k, v in kwargs.items()]
        stmt = select(self._model).where(True, *args)
        result = (await self._async_session.scalars(stmt)).all()
        return [self._model.from_orm(dao) for dao in result]

    async def persist(self, model: BaseUUIDModel) -> BaseUUIDModel:
        self._async_session.add(self._map_to_dao(model))
        await self._commit()

        return model

    async def persist_many(self, models: list[BaseUUIDModel]) -> list[BaseUUIDModel]:
        self._async_session.add_all([self._map_to_dao(model) for model in models])
        await self._commit()
        return models

    async def delete(self, model: BaseUUIDModel) -> None:
        await self._async_session.delete(self._map_to_dao(model))
        await self._commit()

        return None
