from abc import ABC, abstractmethod
from typing import Type
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data_access.abstract import AbstractAsyncDataAccess
from src.data_access.exceptions import DoesNotExistError
from src.models.abstract import UUIDBaseModel


class SQLAlchemyAsyncDataAccess(AbstractAsyncDataAccess[UUID, UUIDBaseModel], ABC):
    def __init__(self, async_session: AsyncSession) -> None:
        self._async_session = async_session

    @property
    @abstractmethod
    def _model(self) -> Type[UUIDBaseModel]:
        raise NotImplementedError

    async def get(self, pk: UUID) -> UUIDBaseModel:
        result = (
            await self._async_session.scalars(
                select(self._model).where(self._model.id == pk)
            )
        ).first()
        if not result:
            raise DoesNotExistError(
                f"{self.__class__.__name__} could not find {self._model.__name__} with given PK - {pk}"
            )
        return result

    # TODO implement get_many method, add support for where clause
    async def get_many(self) -> list[UUIDBaseModel]:
        ...

    async def persist(self, model: UUIDBaseModel) -> UUIDBaseModel:
        await self._async_session.add(model)
        return model

    async def persist_many(self, models: list[UUIDBaseModel]) -> list[UUIDBaseModel]:
        await self._async_session.add_all(models)
        return models

    async def delete(self, model: UUIDBaseModel) -> None:
        await self._async_session.delete(model)
        return None
