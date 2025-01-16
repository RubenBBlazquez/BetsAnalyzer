from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from common.etl_base import ETL
from etl_management.sport_monks.create_clean_data_by_leagues import etl_clean_data_by_leagues


def build_etl_task(etl: ETL) -> None:
    """
    Method to execute ETL.

    Parameters
    ----------
    etl: ETL
        ETL entity to execute.
    """
    raw_data = etl.extract()
    transformed_data = etl.transform(raw_data)
    etl.load(transformed_data)


def build_etl_dag(etl: ETL) -> DAG:
    """
    Method to build a DAG for an ETL.

    Parameters
    ----------
    etl: ETL
        ETL entity to build the DAG for.

    Returns
    -------
    DAG
        The constructed DAG for the ETL process.
    """
    today = datetime.today()
    dag = DAG(
        dag_id=f"ETL_SportMonks_{etl.name.capitalize()}",
        schedule=etl.schedule,
        start_date=datetime(today.year, today.month, today.day),
    )

    with dag:
        PythonOperator(
            python_callable=build_etl_task,
            task_id="etl_task",
            op_kwargs={"etl": etl},
        )

    return dag


def build_etl_dags() -> list[DAG]:
    """
    Method to build ETL DAGs.

    Returns
    -------
    list[DAG]
        List of constructed DAGs for ETL processes.
    """
    etl_s = [
        *etl_clean_data_by_leagues(),
    ]

    return [build_etl_dag(etl) for etl in etl_s]
