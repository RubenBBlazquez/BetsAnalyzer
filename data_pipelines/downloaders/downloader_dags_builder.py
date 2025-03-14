from datetime import datetime
from typing import Iterable

from airflow.models.dag import DAG
from common.downloader_base import Downloader
from downloaders.fbref.builder import get_fb_ref_downloaders
from downloaders.sport_monks.builder import get_sport_monks_downloaders


def build_downloader_dag(downloader: Downloader) -> DAG:
    """
    Method to build a DAG for a downloader
    """
    today = datetime.today()
    entity = downloader.entity

    dag = DAG(
        dag_id=f"Downloader_{entity.dag_name}",
        schedule=entity.schedule,
        start_date=datetime(today.year, today.month, today.day),
        catchup=False,
    )

    for task in downloader.get_downloader_tasks():
        dag.add_task(task)

    return dag


def build_sports_monks_dags() -> Iterable[DAG]:
    """
    Method to build sport monks DAGs
    """
    for sport_monks_downloader in get_sport_monks_downloaders():
        yield build_downloader_dag(sport_monks_downloader)


def build_fb_ref_dags() -> list[DAG]:
    """
    Method to build Selenium DAGs
    """
    for fb_ref_downloader in get_fb_ref_downloaders():
        yield build_downloader_dag(fb_ref_downloader)


def build_downloader_dags() -> list[DAG]:
    """
    Method to build DAGs for downloading data from SportMonks API
    """
    sport_monks_dags = build_sports_monks_dags()
    fb_ref_dags = build_fb_ref_dags()

    return [*sport_monks_dags, *fb_ref_dags]
