from abc import ABC

from data_pipelines.common.entity import IEntity


class IWriter(ABC):
    """
    Interface for writer
    """

    def write(self, entities: list[IEntity]):
        """
        Abstract method to write data in some database/storage

        Parameters
        ----------
        entities: list[IEntity]
            List of entities to write
        """
        raise NotImplementedError()
