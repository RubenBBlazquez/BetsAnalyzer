from datetime import datetime

import attr
from airflow.models.dag import DAG
from common.downloader_base import Downloader
from downloaders.sport_monks.builder import get_sport_monks_downloaders

from data_pipelines.common.dag_builder import DagCollector, IDagBuilder


@attr.s(auto_attribs=True)
class DownloaderDagBuilder(IDagBuilder):
    """
    Class for building DAG for downloading data from SportMonks API

    Attributes
    -----------
    _downloader: Downloader
        entity  that contains all the information necessary
        to download data

    """

    _downloader: Downloader

    def build(self):
        today = datetime.today()
        entity = self._downloader.entity
        dag = DAG(
            dag_id=f"Downloader_{entity.dag_name}",
            schedule=entity.schedule,
            start_date=datetime(today.year, today.month, today.day),
        )

        for task in self._downloader.get_downloader_tasks():
            dag.add_task(task)

        return dag


def build_sports_monks_dags(dag_collector: DagCollector):
    """
    Method to build sport monks DAGs
    """
    for sport_monks_downloader in get_sport_monks_downloaders():
        dag_collector.add_builder(DownloaderDagBuilder(sport_monks_downloader))


def build_downloader_dags() -> list[DAG]:
    """
    Method to build DAGs for downloading data from SportMonks API
    """
    dag_collector = DagCollector()

    build_sports_monks_dags(dag_collector)

    return dag_collector.collect()
