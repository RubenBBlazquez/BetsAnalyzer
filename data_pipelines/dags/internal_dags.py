import json
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from common.cache_client.redis_client import RedisCacheClient
from common.extractors.base import ExtractorConfig
from common.extractors.mongo_db import MongoDBExtractor
from downloaders.fbref.factories import RAW_DATA_COLLECTIONS_SWITCHER, TEAM_STATS_FB_REF_KEY

with DAG(
    dag_id="download_and_save_in_cache",
    schedule="30 * * * *",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    def download_data_and_save():
        extractors_config = [
            ExtractorConfig(collection="raw_data_teams"),
            ExtractorConfig(collection="raw_data_seasons"),
            ExtractorConfig(collection="raw_data_leagues"),
            ExtractorConfig(collection=RAW_DATA_COLLECTIONS_SWITCHER[TEAM_STATS_FB_REF_KEY]),
        ]
        extractor = MongoDBExtractor(
            extractors_config, os.getenv("PROJECT_DATABASE", "bets_analyzer")
        )
        data = extractor.extract()
        cache_client = RedisCacheClient()

        for collection, df in data.items():
            df.drop("_id", axis=1, inplace=True)
            cache_client.set(collection, json.dumps(df.to_dict("records")))

    PythonOperator(task_id="download_data_and_save", python_callable=download_data_and_save)
