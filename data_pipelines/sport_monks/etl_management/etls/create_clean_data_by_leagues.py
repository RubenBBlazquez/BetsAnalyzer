import os

import pandas as pd
from airflow import Dataset
from common.extractors.base import ExtractorConfig
from common.extractors.mongo_db import MongoDBExtractor
from common.writers.mongo_db import MongoDBWriter
from sport_monks.downloaders.entities.league import League
from sport_monks.downloaders.sport_monks_client import SportMonksEndpoints
from sport_monks.etl_management.etls.etl_base import ETL


def transform(raw_data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return pd.DataFrame()


def etl_clean_data_by_leagues():
    """
    Method to create ETL to create clean data by leagues
    """
    database_name = os.getenv("PROJECT_DATABSAE", "sport_monks")
    leagues_extractor = MongoDBExtractor(
        extractors_config=[ExtractorConfig(f"raw_data_{SportMonksEndpoints.LEAGUES.value}")],
        database_name=database_name,
    )
    leagues = [
        League.from_dict(league)
        for league in leagues_extractor.extract()[f"raw_data_{SportMonksEndpoints.LEAGUES.value}"]
    ]
    etls = []
    for league in leagues:
        output_collection = f"clean_data_league_{league.name.lower()}"
        input_collections = [
            ExtractorConfig(
                f"raw_data_{SportMonksEndpoints.MATCHES.value}",
                query={"league_id": league.id},
            ),
            ExtractorConfig(f"raw_data_{SportMonksEndpoints.PLAYERS.value}", query={}),
            ExtractorConfig(
                f"raw_data_{SportMonksEndpoints.TEAMS.value}",
                query={"country_id": league.country_id},
            ),
            ExtractorConfig(f"raw_data_{SportMonksEndpoints.COUNTRIES.value}", query={}),
            ExtractorConfig(f"raw_data_{SportMonksEndpoints.TYPES.value}", query={}),
        ]

        writer = MongoDBWriter(database_name, output_collection)
        extractor = MongoDBExtractor(
            extractors_config=input_collections, database_name=database_name
        )

        etls.append(
            ETL(
                name=f"ETL_create_clean_data_{league.name.lower()}",
                schedule=[
                    Dataset(extractor_config.collection) for extractor_config in input_collections
                ],
                writer=writer,
                extractor=extractor,
                transform_=transform,
            )
        )

    return etls
