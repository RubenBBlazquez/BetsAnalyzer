import os

import attr
import pandas as pd
from airflow.models import Operator
from airflow.operators.python import PythonOperator
from common.downloader_base import Downloader
from common.writers.mongo_db import MongoDBWriter
from downloaders.sport_monks.entities.entity_base import SportMonksDownloaderEntityBase
from downloaders.sport_monks.factories import (
    DOWNLOADER_ENTITY_SWITCHER,
    RAW_DATA_COLLECTIONS_SWITCHER,
)
from downloaders.sport_monks.sport_monks_client import SportMonksClient, SportMonksEndpoints


@attr.s(auto_attribs=True)
class SportMonksDownloader(Downloader):
    """
    Class for downloading data from the Sport Monks API.
    This class implements the downloading logic for Sport Monks data.
    """

    def _download_and_save_data(self):
        """
        Method to download and save data from the Sport Monks API.
        """
        if not isinstance(self._entity, SportMonksDownloaderEntityBase):
            raise ValueError(
                "Sport Monks Downloader entity must be an instance of SportMonksDownloaderEntityBase"
            )

        sport_monks_client = SportMonksClient()
        iterator = sport_monks_client.get_data_in_batches(self._entity)

        for data in iterator:
            if not len(data):
                continue

            self._writer.write(pd.DataFrame([entity.to_dict() for entity in data]))

    def get_downloader_tasks(self) -> list[Operator]:
        """
        Method to get downloader tasks for Airflow.

        Returns
        -------
        list[Operator]
            List of Airflow operators for downloading tasks.
        """
        return [
            PythonOperator(
                python_callable=self._download_and_save_data,
                task_id="download_and_save_data",
            )
        ]


def get_sport_monks_downloaders():
    """
    Method to get Sport Monks downloaders.

    Yields
    ------
    SportMonksDownloader
        Instances of SportMonksDownloader for each endpoint.
    """
    for endpoint in SportMonksEndpoints:
        entity = DOWNLOADER_ENTITY_SWITCHER[endpoint]
        raw_data_collection = RAW_DATA_COLLECTIONS_SWITCHER[endpoint]
        writer = MongoDBWriter(
            os.getenv("PROJECT_DATABASE", ""),
            raw_data_collection,
            update_fields=entity.update_fields,
        )

        yield SportMonksDownloader(entity=entity, writer=writer)
