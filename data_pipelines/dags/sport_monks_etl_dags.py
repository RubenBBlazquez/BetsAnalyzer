# *-* airflow DAG script *-*

from etl_management.etl_dag_builder import build_etl_dags

for dag in build_etl_dags():
    globals()[dag.dag_id] = dag
