# *-* airflow DAG script *-*

from data_pipelines.sport_monks.download_dag_builder import build_sport_monks_dags

for dag in build_sport_monks_dags():
    globals()[dag.dag_id] = dag
