# *-* airflow DAG script *-*

from sport_monks.etl_management.etl_dag_builder import build_sport_monks_dags

for dag in build_sport_monks_dags():
    globals()[dag.dag_id] = dag
