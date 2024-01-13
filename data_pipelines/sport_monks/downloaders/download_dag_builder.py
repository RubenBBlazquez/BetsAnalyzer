import os
from datetime import datetime

import attr
import pandas as pd
from airflow import Dataset
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from sport_monks.downloaders.constants import (
    DOWNLOADER_ENTITY_SWITCHER,
    RAW_DATA_COLLECTIONS_SWITCHER,
)
from sport_monks.downloaders.entities.entity_base import DownloaderEntityBase
from sport_monks.downloaders.sport_monks_client import SportMonksClient, SportMonksEndpoints

from data_pipelines.common.dag_builder import DagCollector, IDagBuilder
from data_pipelines.common.writers.base import IWriter
from data_pipelines.common.writers.mongo_db import MongoDBWriter


@attr.s(auto_attribs=True)
class SportMonksDownloadDagBuilder(IDagBuilder):
    """
    Class for building DAG for downloading data from SportMonks API

    Attributes
    -----------
    _entity: DownloaderEntityBase
        entity for downloading data
    _writer: IWriter
        writer for saving data
    """

    _entity: DownloaderEntityBase
    _writer: IWriter

    def _download_and_save_data(self):
        """
        Method to download and save data
        """
        sport_monks_client = SportMonksClient()
        iterator = sport_monks_client.get_data_in_batches(self._entity)

        for data in iterator:
            if not len(data):
                continue

            self._writer.write(pd.DataFrame([entity.to_dict() for entity in data]))

    def build(self):
        today = datetime.today()
        dag = DAG(
            dag_id=f"Downloader_SportMonks_{self._entity.dag_name}",
            schedule="@daily",
            start_date=datetime(today.year, today.month, today.day),
        )

        endpoint = SportMonksEndpoints(self._entity.endpoint)
        dataset = RAW_DATA_COLLECTIONS_SWITCHER[endpoint]

        with dag:
            PythonOperator(
                python_callable=self._download_and_save_data,
                task_id="download_and_save_data",
                outlets=[Dataset(dataset)],
            )

        return dag


def build_sport_monks_dags() -> list[DAG]:
    """
    Method to build DAGs for downloading data from SportMonks API
    """
    dag_collector = DagCollector()

    for endpoint in SportMonksEndpoints:
        entity = DOWNLOADER_ENTITY_SWITCHER[endpoint]
        raw_data_collection = RAW_DATA_COLLECTIONS_SWITCHER[endpoint]
        writer = MongoDBWriter(os.getenv("PROJECT_DATABASE", "sport_monks"), raw_data_collection)

        dag_collector.add_builder(SportMonksDownloadDagBuilder(entity, writer))

    return dag_collector.collect()
