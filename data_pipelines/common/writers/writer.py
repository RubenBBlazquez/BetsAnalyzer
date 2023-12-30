from abc import ABC

import pandas as pd


class IWriter(ABC):
    """
    Interface for writer
    """

    def write(self, entities: pd.DataFrame, collection: str):
        """
        Abstract method to write data in some database/storage

        Parameters
        ----------
        entities: pd.DataFrame
            List of entities to write
        collection: str
            Name of collection/table to write data
        """
        raise NotImplementedError()
