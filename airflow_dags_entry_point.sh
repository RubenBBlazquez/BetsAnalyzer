#!/bin/bash

rm -f /opt/airflow/dags/sport_monks_downloader_dags.py
ln -sf "/opt/airflow/data_pipelines/dags/sport_monks_downloader_dags.py" "/opt/airflow/dags/sport_monks_downloader_dags.py"

rm -f /opt/airflow/dags/sport_monks_etl_dags.py
ln -sf "/opt/airflow/data_pipelines/dags/sport_monks_etl_dags.py" "/opt/airflow/dags/sport_monks_etl_dags.py"

pip install -e /opt/airflow/data_pipelines
rm -f /opt/airflow/data_pipelines/data_pipelines.egg-info

exec airflow "$@"
