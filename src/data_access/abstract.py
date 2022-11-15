from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from pydantic import BaseModel

PK = TypeVar("PK")
Model = TypeVar("Model", bound=BaseModel)


class AbstractAsyncDataAccess(Generic[PK, Model], ABC):
    @property
    @abstractmethod
    def _model(self) -> Type[Model]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, pk: PK) -> Model:
        raise NotImplementedError

    @abstractmethod
    async def persist(self, model: Model) -> Model:
        raise NotImplementedError

    @abstractmethod
    async def persist_many(self, models: list[Model]) -> list[Model]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, model: Model) -> None:
        raise NotImplementedError
