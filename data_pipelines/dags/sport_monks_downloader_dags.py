# *-* airflow DAG script *-*

from downloaders.downloader_dags_builder import build_downloader_dags

for dag in build_downloader_dags():
    globals()[dag.dag_id] = dag
