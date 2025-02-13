from dataclasses import field
from typing import Any, TypeVar
from pydantic import BaseModel

EntityType = TypeVar("EntityType", bound="Entity")


class Entity():
    id: int = field(init=False)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)


class Aggregate(Entity):
    """
    An entry point of aggregate.
    """
    pass


class AggregateRoot(Entity):
    """
    An entry point of aggregate.
    """
    pass