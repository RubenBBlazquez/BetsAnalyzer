import pandas as pd
from airflow import Dataset
from common.extractors.base import ExtractorConfig
from common.extractors.mongo_db import MongoDBExtractor
from common.writers.mongo_db import MongoDBWriter
from sport_monks.downloaders.sport_monks_client import SportMonksEndpoints
from sport_monks.etl_management.etls.etl_base import ETL

OUTPUT_COLLECTION = "clean_data_by_leagues"
INPUT_COLLECTIONS = [
    ExtractorConfig(f"raw_data_{SportMonksEndpoints.LEAGUES.value}"),
    ExtractorConfig(f"raw_data_{SportMonksEndpoints.MATCHES.value}"),
    ExtractorConfig(f"raw_data_{SportMonksEndpoints.PLAYERS.value}"),
    ExtractorConfig(f"raw_data_{SportMonksEndpoints.COUNTRIES.value}"),
    ExtractorConfig(f"raw_data_{SportMonksEndpoints.TYPES.value}"),
]
DATABASE_NAME = "sport_monks"


def transform(raw_data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return raw_data[INPUT_COLLECTIONS[4].collection]


def etl_create_data_by_leagues():
    """
    Method to create ETL to create clean data by leagues
    """

    writer = MongoDBWriter(DATABASE_NAME, OUTPUT_COLLECTION)
    extractor = MongoDBExtractor(extractors_config=INPUT_COLLECTIONS, database_name=DATABASE_NAME)

    return ETL(
        name="create_data_by_leagues",
        schedule=[Dataset(extractor_config.collection) for extractor_config in INPUT_COLLECTIONS],
        writer=writer,
        extractor=extractor,
        transform_=transform,
    )
