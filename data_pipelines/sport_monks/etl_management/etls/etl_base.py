from __future__ import annotations

import attr
import pandas as pd
from airflow import Dataset
from common.extractors.base import BaseExtractor
from common.writers.base import IWriter


@attr.s(auto_attribs=True)
class ETL:
    """
    Base ETL Entity information

    Attributes
    -----------
    name: str
        name of the ETL
    schedule: str | Dataset
        schedule to run the ETL
    _writer: IWriter
        writer to insert data
    _extractor: BaseExtractor
        extractors to obtain data from a service
    _transform: callable
        function to transform data
    """

    name: str
    schedule: str | list[Dataset]
    _writer: IWriter
    _extractor: BaseExtractor
    _transform: callable

    def extract(self) -> dict[str, pd.DataFrame]:
        """
        method to extract data
        """
        return self._extractor.extract()

    def transform(self, raw_data: dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        method to transform data
        """
        return self._transform(raw_data)

    def load(self, information: pd.DataFrame) -> None:
        """
        method to load data
        """
        self._writer.write(information)
