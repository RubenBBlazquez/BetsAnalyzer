from __future__ import annotations

import attr
import pandas as pd
from airflow import Dataset
from common.extractors.base import BaseExtractor
from common.writers.base import IWriter


@attr.s(auto_attribs=True)
class ETL:
    """
    Base ETL Entity information.

    Attributes
    -----------
    name: str
        Name of the ETL.
    schedule: str | Dataset
        Schedule to run the ETL.
    _writer: IWriter
        Writer to insert data.
    _extractor: BaseExtractor
        Extractor to obtain data from a service.
    _transform: callable
        Function to transform data.
    """

    name: str
    schedule: str | list[Dataset]
    _writer: IWriter
    _extractor: BaseExtractor
    _transform: callable

    def extract(self) -> dict[str, pd.DataFrame]:
        """
        Method to extract data.
        """
        return self._extractor.extract()

    def transform(self, raw_data: dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Method to transform data.

        Parameters
        ----------
        raw_data: dict[str, pd.DataFrame]
            Raw data extracted from the source.

        Returns
        -------
        pd.DataFrame
            Transformed data.
        """
        return self._transform(raw_data)

    def load(self, information: pd.DataFrame) -> None:
        """
        Method to load data.

        Parameters
        ----------
        information: pd.DataFrame
            Data to be loaded.
        """
        self._writer.write(information)
