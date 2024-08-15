import logging
from abc import ABC

import attr
import pandas as pd


@attr.s(auto_attribs=True)
class IWriter(ABC):
    """
    Interface for writer
    """

    def write(self, entities: pd.DataFrame):
        """
        Abstract method to write data in some database/storage

        Parameters
        ----------
        entities: pd.DataFrame
            List of entities to write
        """
        raise NotImplementedError()


class DummyWriter(IWriter):
    """
    Dummy writer that does nothing
    """

    def write(self, entities: pd.DataFrame):
        logging.info("Dummy writer does nothing")
