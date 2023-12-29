from datetime import datetime, timedelta

import attr
from airflow import Dataset
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

from data_pipelines.common.dag_builder import IDagBuilder
from data_pipelines.common.writers.writer import IWriter
from data_pipelines.sport_monks.sport_monks_client import SportMonksClient, SportMonksGetEndpoints

DOWNLOAD_SWITCHER = {
    SportMonksGetEndpoints.PLAYERS: SportMonksClient.get_players,
}


@attr.s(auto_attribs=True)
class SportMonksDownloadDagBuilder(IDagBuilder):
    """
    Class for building DAG for downloading data from SportMonks API
    """

    _type: SportMonksGetEndpoints
    _writer: IWriter

    def _download_and_save_data(self):
        """
        Method to download and save data
        """
        for data in DOWNLOAD_SWITCHER[self._type]():
            print(data)

    def build(self):
        dag = DAG(
            dag_id=f"Downloader_SportMonks_Get_{self._type.value}",
            schedule="@daily",
            start_date=datetime.now() - timedelta(days=2),
        )

        with dag:
            PythonOperator(
                python_callable=self._download_and_save_data,
                task_id="download_and_save_data",
                outlets=[Dataset(f"SportMonks_Get_{self._type.value}")],
            )

        return dag
