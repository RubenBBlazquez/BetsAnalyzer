from common.etl_utils import build_etl_dag
from common.etl_base import ETL
from etl_management.sport_monks.create_clean_data_by_leagues import etl_clean_data_by_leagues


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
