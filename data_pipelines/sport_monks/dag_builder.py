from datetime import datetime, timedelta

import attr
from airflow import Dataset
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

from data_pipelines.common.dag_builder import DagCollector, IDagBuilder
from data_pipelines.common.writers.mongodb_writer import MongoDBWriter
from data_pipelines.common.writers.writer import IWriter
from data_pipelines.sport_monks.sport_monks_client import SportMonksClient, SportMonksCollections


def get_sport_monks_downloader(collection: SportMonksCollections) -> callable:
    """
    Function to get downloader callable for SportMonks API

    Parameters
    ----------
    collection: SportMonksCollections
        collection where want to download data
    """
    sport_monks_client = SportMonksClient()

    switcher = {
        SportMonksCollections.PLAYERS: sport_monks_client.get_players,
    }

    return switcher[collection]


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
        downloader_callable = get_sport_monks_downloader(self._collection)

        for data in downloader_callable():
            self._writer.write(data, self._collection.value)

    def build(self):
        dag = DAG(
            dag_id=f"Downloader_SportMonks_Get_{self._collection.value}",
            schedule="@daily",
            start_date=datetime.now() - timedelta(days=2),
        )

        with dag:
            PythonOperator(
                python_callable=self._download_and_save_data,
                task_id="download_and_save_data",
                outlets=[Dataset(f"SportMonks_Get_{self._collection.value}")],
            )

        return dag


def build_sport_monks_dags() -> list[DAG]:
    """
    Method to build DAGs for downloading data from SportMonks API
    """
    dag_collector = DagCollector()
    writer = MongoDBWriter("sport_monks")

    for type_ in SportMonksCollections:
        dag_collector.add_builder(SportMonksDownloadDagBuilder(type_, writer))

    return dag_collector.collect()
