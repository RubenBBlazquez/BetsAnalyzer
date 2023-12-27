from abc import ABC, abstractmethod

from pydantic import BaseModel


class IEntity(ABC, BaseModel):
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
        pass
