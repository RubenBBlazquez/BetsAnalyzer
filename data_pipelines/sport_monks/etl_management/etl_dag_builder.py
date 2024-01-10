from datetime import datetime

import attr
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from sport_monks.etl_management.etls.clean_data_by_leagues.create_clean_data_by_leagues import (
    etl_clean_data_by_leagues,
)
from sport_monks.etl_management.etls.etl_base import ETL

from data_pipelines.common.dag_builder import DagCollector, IDagBuilder


@attr.s(auto_attribs=True)
class SportMonksETLDagBuilder(IDagBuilder):
    """
    Class for building DAG for downloading data from SportMonks API
    """

    _etl: ETL

    def _etl_task(self):
        """
        Method to execute ETL
        """
        raw_data = self._etl.extract()
        transformed_data = self._etl.transform(raw_data)
        self._etl.load(transformed_data)

    def build(self):
        today = datetime.today()
        dag = DAG(
            dag_id=f"ETL_SportMonks_{self._etl.name.capitalize()}",
            schedule=self._etl.schedule,
            start_date=datetime(today.year, today.month, today.day),
        )

        with dag:
            PythonOperator(
                python_callable=self._etl_task,
                task_id="etl_task",
            )

        return dag


def build_sport_monks_dags() -> list[DAG]:
    """
    Method to build DAGs for downloading data from SportMonks API
    """
    dag_collector = DagCollector()

    etl_s = [
        *etl_clean_data_by_leagues(),
    ]

    for etl in etl_s:
        dag_collector.add_builder(SportMonksETLDagBuilder(etl))

    return dag_collector.collect()
