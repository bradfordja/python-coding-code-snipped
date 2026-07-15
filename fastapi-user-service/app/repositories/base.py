from abc import ABC, abstractmethod
from typing import Generic, TypeVar


EntityType = TypeVar("EntityType")


class BaseRepository(ABC, Generic[EntityType]):
    @abstractmethod
    def find_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[EntityType]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, entity_id: int) -> EntityType | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        raise NotImplementedError