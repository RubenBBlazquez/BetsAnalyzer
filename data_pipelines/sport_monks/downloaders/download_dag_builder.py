from datetime import datetime

import attr
from airflow import Dataset
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from sport_monks.downloaders.sport_monks_client import (
    ENTITY_SWITCHER,
    SportMonksClient,
    SportMonksCollections,
)

from data_pipelines.common.dag_builder import DagCollector, IDagBuilder
from data_pipelines.common.writers.mongodb_writer import MongoDBWriter
from data_pipelines.common.writers.writer import IWriter


@attr.s(auto_attribs=True)
class SportMonksDownloadDagBuilder(IDagBuilder):
    """
    Class for building DAG for downloading data from SportMonks API
    """

    _collection: SportMonksCollections
    _writer: IWriter

    def _download_and_save_data(self):
        """
        Method to download and save data
        """
        sport_monks_client = SportMonksClient()
        entity = ENTITY_SWITCHER[self._collection]
        iterator = sport_monks_client.get_data_in_batches(self._collection, entity)

        for data in iterator:
            self._writer.write(data, f"raw_data_{self._collection.name.lower()}")

    def build(self):
        today = datetime.today()
        dag = DAG(
            dag_id=f"Downloader_SportMonks_{self._collection.name.capitalize()}",
            schedule="@daily",
            start_date=datetime(today.year, today.month, today.day),
        )

        with dag:
            PythonOperator(
                python_callable=self._download_and_save_data,
                task_id="download_and_save_data",
                outlets=[Dataset(f"SportMonks_Get_{self._collection.name.lower()}")],
            )

        return dag


def build_sport_monks_dags() -> list[DAG]:
    """
    Method to build DAGs for downloading data from SportMonks API
    """
    dag_collector = DagCollector()
    writer = MongoDBWriter("sport_monks")

    for collection in SportMonksCollections:
        dag_collector.add_builder(SportMonksDownloadDagBuilder(collection, writer))

    return dag_collector.collect()
