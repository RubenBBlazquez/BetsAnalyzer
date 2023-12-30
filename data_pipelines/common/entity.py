from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy

import attr
import cattrs


class IEntity(ABC):
    """
    Interface that represents an entity that will be used in the application
    to represent data and insert it into the database if its necessary
    """

    @abstractmethod
    def to_dict(self) -> dict:
        """
        method to convert entity to dict

        Returns
        -------
        dict representation of entity
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_: dict) -> IEntity:
        """
        method to cast dict to entity

        Returns
        -------
        entity
        """
        raise NotImplementedError()


@attr.s(auto_attribs=True)
class EntityBase(ABC):
    """
    Base Entity class
    """

    def to_dict(self) -> dict:
        """
        method to convert entity to dict

        Returns
        -------
        dict representation of entity
        """
        return attr.asdict(self)

    @classmethod
    def from_dict(cls, dict_: dict) -> IEntity:
        """
        method to cast dict to entity

        Returns
        -------
        entity
        """
        converter = deepcopy(cattrs.global_converter)
        return converter.structure(dict_, cls)
