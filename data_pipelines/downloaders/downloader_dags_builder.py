import os
from datetime import datetime

import attr
import pandas as pd
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from common.writers.mongo_db import MongoDBWriter
from downloaders.sport_monks.entities.entity_base import SportMonksDownloaderEntityBase
from downloaders.sport_monks.factories import (
    DOWNLOADER_ENTITY_SWITCHER,
    RAW_DATA_COLLECTIONS_SWITCHER,
)
from downloaders.sport_monks.sport_monks_client import SportMonksClient, SportMonksEndpoints

from data_pipelines.common.dag_builder import DagCollector, IDagBuilder
from data_pipelines.common.writers.base import IWriter


@attr.s(auto_attribs=True)
class DownloaderDagBuilder(IDagBuilder):
    """
    Class for building DAG for downloading data from SportMonks API

    Attributes
    -----------
    _entity: SportMonksDownloaderEntityBase
        entity for downloading data
    _writer: IWriter
        writer for saving data
    _downloader_tasks: list
        list of downloader tasks
    """

    _entity: SportMonksDownloaderEntityBase
    _writer: IWriter
    _downloader_tasks: list

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

        with dag:
            PythonOperator(
                python_callable=self._download_and_save_data,
                task_id="download_and_save_data",
            )

        return dag


def build_sports_monks_dags(dag_collector: DagCollector):
    """
    Method to build sport monks DAGs
    """
    for endpoint in SportMonksEndpoints:
        entity = DOWNLOADER_ENTITY_SWITCHER[endpoint]
        raw_data_collection = RAW_DATA_COLLECTIONS_SWITCHER[endpoint]
        writer = MongoDBWriter(
            os.getenv("PROJECT_DATABASE", ""),
            raw_data_collection,
            update_fields=entity.update_fields,
        )

        dag_collector.add_builder(DownloaderDagBuilder(entity, writer, []))


def build_downloader_dags() -> list[DAG]:
    """
    Method to build DAGs for downloading data from SportMonks API
    """
    dag_collector = DagCollector()

    build_sports_monks_dags(dag_collector)

    return dag_collector.collect()
