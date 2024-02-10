import os

import pandas as pd
from airflow import Dataset
from common.etl_base import ETL
from common.extractors.base import ExtractorConfig
from common.extractors.mongo_db import MongoDBExtractor
from common.writers.mongo_db import MongoDBWriter
from sport_monks.downloaders.entities.league import League
from sport_monks.downloaders.factories import (
    DEFAULT_ENGLAND_COUNTRY_ID,
    DEFAULT_GERMANY_COUNTRY_ID,
    DEFAULT_SPAIN_COUNTRY_ID,
    RAW_DATA_LEAGUES,
    RAW_DATA_MATCHES,
    RAW_DATA_PLAYERS,
    RAW_DATA_SEASONS,
    RAW_DATA_TEAMS,
    RAW_DATA_TOP_SCORERS,
    RAW_DATA_TYPES,
)
from sport_monks.downloaders.sport_monks_client import SportMonksEndpoints
from sport_monks.etl_management.etls.clean_data_by_leagues.transformations.matches_data import (
    transform_matches_data,
)
from sport_monks.etl_management.etls.clean_data_by_leagues.transformations.player_data import (
    transform_players_data,
)
from sport_monks.etl_management.etls.clean_data_by_leagues.transformations.seasons_data import (
    transform_season_data,
)
from sport_monks.etl_management.etls.clean_data_by_leagues.transformations.teams_data import (
    transform_team_data,
)


def _transform_league_data(transformed_data: pd.DataFrame, league: pd.Series):
    """
    Method to transform league data

    Parameters
    ----------
    transformed_data: pd.DataFrame
        clean data
    league: pd.Series
        league data
    """
    transformed_data["league"] = league["name"]
    transformed_data["league_id"] = league["id"]

    return transformed_data


def transform(raw_data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Method to transform raw data

    Parameters
    ----------
    raw_data: dict[str, pd.DataFrame]
        raw data

    Returns
    -------
    pd.DataFrame
        clean data by leagues
    """
    pd.options.mode.chained_assignment = None
    transformed_data = pd.DataFrame()

    seasons = raw_data[RAW_DATA_SEASONS].rename(columns={"id": "season_id", "name": "season"})
    matches = raw_data[RAW_DATA_MATCHES].rename(columns={"id": "match_id"})
    players = raw_data[RAW_DATA_PLAYERS]
    player_statistics = raw_data[RAW_DATA_TOP_SCORERS]
    teams = raw_data[RAW_DATA_TEAMS]
    types = raw_data[RAW_DATA_TYPES]
    league = raw_data[RAW_DATA_LEAGUES].iloc[0]
    league_seasons = seasons[seasons["league_id"] == league["id"]]

    transformed_data = transform_team_data(transformed_data, teams)
    transformed_data = transform_season_data(transformed_data, league_seasons)
    transformed_data = transform_players_data(
        transformed_data, players, player_statistics, teams, seasons, league_seasons, matches
    )
    transformed_data = _transform_league_data(transformed_data, league)
    transformed_data = transform_matches_data(transformed_data, matches, teams, types)

    return transformed_data


def get_leagues() -> list[League]:
    """
    Method to get leagues from MongoDB

    Returns
    -------
    list[League]
        list of leagues
    """
    leagues_query = {
        "country_id": {
            "$in": [
                DEFAULT_SPAIN_COUNTRY_ID,
                DEFAULT_ENGLAND_COUNTRY_ID,
                DEFAULT_GERMANY_COUNTRY_ID,
            ]
        }
    }
    leagues_extractor = MongoDBExtractor(
        extractors_config=[ExtractorConfig(RAW_DATA_LEAGUES, query=leagues_query)],
        database_name=os.getenv("PROJECT_DATABASE", "sport_monks"),
    )
    leagues = leagues_extractor.extract()[f"raw_data_{SportMonksEndpoints.LEAGUES.value}"]

    if leagues.empty:
        raise ValueError(
            "No leagues found in MongoDB, "
            "we cant create the ETLs of create_clean_data_by_leagues"
        )

    extracted_leagues = leagues.drop(columns="_id").to_dict("records")

    return [League.from_dict(league) for league in extracted_leagues]


def get_extractors_configuration(league: League):
    """
    Method to get extractors configuration

    Parameters
    ----------
    league: League
        league where we want to filter the data
    """
    return [
        ExtractorConfig(
            RAW_DATA_MATCHES,
            query={"league_id": league.id},
        ),
        ExtractorConfig(RAW_DATA_TEAMS, query={"country_id": league.country_id}),
        ExtractorConfig(RAW_DATA_SEASONS, query={}),
        ExtractorConfig(RAW_DATA_TYPES, query={}),
        ExtractorConfig(RAW_DATA_PLAYERS, query={}),
        ExtractorConfig(RAW_DATA_LEAGUES, query={"id": league.id}),
        ExtractorConfig(RAW_DATA_TOP_SCORERS, query={}),
    ]


def etl_clean_data_by_leagues():
    """
    Method to create ETLs that creates clean data by leagues
    """
    etl_s = []
    database_name = os.getenv("PROJECT_DATABASE", "sport_monks")

    for league in get_leagues():
        output_collection = f"clean_data_league_{league.name.lower().replace(' ', '_')}"
        input_collections = get_extractors_configuration(league)

        writer = MongoDBWriter(
            database_name, output_collection, update_fields=["league_id", "season_id", "team_id"]
        )
        extractor = MongoDBExtractor(
            extractors_config=input_collections, database_name=database_name
        )

        etl_name = f"clean_data_" f"{league.name.lower().replace(' ', '_').replace('-', '_')}"
        etl_s.append(
            ETL(
                name=etl_name,
                schedule=[
                    Dataset(extractor_config.collection) for extractor_config in input_collections
                ],
                writer=writer,
                extractor=extractor,
                transform=transform,
            )
        )

    return etl_s
