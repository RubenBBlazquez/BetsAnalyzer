import os

import pandas as pd
from airflow import Dataset
from common.extractors.base import ExtractorConfig
from common.extractors.mongo_db import MongoDBExtractor
from common.writers.mongo_db import MongoDBWriter
from sport_monks.downloaders.constants import (
    RAW_DATA_LEAGUES,
    RAW_DATA_MATCHES,
    RAW_DATA_PLAYERS,
    RAW_DATA_SEASONS,
    RAW_DATA_TEAMS,
    RAW_DATA_TYPES,
)
from sport_monks.downloaders.entities.league import League
from sport_monks.downloaders.sport_monks_client import (
    DEFAULT_ENGLAND_COUNTRY_ID,
    DEFAULT_GERMANY_COUNTRY_ID,
    DEFAULT_SPAIN_COUNTRY_ID,
    SportMonksEndpoints,
)
from sport_monks.etl_management.etls.clean_data_by_leagues.transformations.player_data import (
    transform_players_data,
)
from sport_monks.etl_management.etls.etl_base import ETL


def _transform_matches_data(
    transformed_data: pd.DataFrame,
    matches: pd.DataFrame,
    teams: pd.DataFrame,
    players: pd.DataFrame,
) -> pd.DataFrame:
    """
    Method to clean matches data

    Parameters
    ----------
    transformed_data: pd.DataFrame
        final transformed data
    matches: pd.DataFrame
        matches data
    teams: pd.DataFrame
        teams data

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        tuple of clean data for home and away matches
    """
    match_scores = matches[["match_id", "scores"]]
    scores = match_scores["scores"].apply(pd.DataFrame).to_list()
    scores = pd.concat(scores).reset_index(drop=True).drop(columns=["id", "type_id"])
    match_scores = match_scores.merge(scores, left_on="match_id", right_on="fixture_id")
    match_scores.drop(columns=["scores", "fixture_id"], inplace=True)
    match_scores[["goals", "participant"]] = match_scores["score"].apply(pd.Series)
    match_scores.drop(columns=["score"], inplace=True)
    match_scores = (
        match_scores.groupby(["match_id", "participant_id", "participant"]).sum().reset_index()
    )

    match_teams = matches[["match_id", "name"]]
    match_teams[["team_1", "team_2"]] = match_teams["name"].str.split(" vs ", expand=True)
    match_teams.drop(columns="name", inplace=True)
    match_teams = match_teams.melt(
        id_vars=["match_id"], value_vars=["team_1", "team_2"], value_name="team_name"
    ).drop(columns="variable")
    match_teams = match_teams.merge(
        teams[["team_id", "name"]], left_on="team_name", right_on="name"
    )
    match_teams.drop(columns="name", inplace=True)

    match_scores = match_scores.merge(
        match_teams, left_on=["participant_id", "match_id"], right_on=["team_id", "match_id"]
    )
    match_scores.drop(columns=["participant_id"], inplace=True)

    home_match_scores = match_scores[match_scores["participant"] == "home"].drop(
        columns=["participant"]
    )
    away_match_scores = match_scores[match_scores["participant"] == "away"].drop(
        columns=["participant"]
    )
    match_scores = pd.merge(
        home_match_scores, away_match_scores, on="match_id", suffixes=("_home", "_away")
    )

    clean_data_matches = matches[
        [
            "match_id",
            "season_id",
            "league_id",
            "starting_at",
            "starting_at_timestamp",
            "length",
            "weatherreport",
            "lineups",
        ]
    ]
    clean_data_matches.rename(
        columns={
            "starting_at": "date",
            "starting_at_timestamp": "date_timestamp",
            "length": "duration",
        },
        inplace=True,
    )
    clean_data_matches = clean_data_matches.merge(match_scores, on="match_id")

    clean_data_home_matches = (
        clean_data_matches.groupby(["season_id", "league_id", "team_id_home"])
        .apply(
            lambda row: pd.DataFrame(row)
            .drop(columns=["season_id", "league_id"])
            .to_dict("records")
        )
        .reset_index()
        .rename(columns={0: "home_matches", "team_id_home": "team_id"})
    )
    clean_data_away_matches = (
        clean_data_matches.groupby(["season_id", "league_id", "team_id_away"])
        .apply(
            lambda row: pd.DataFrame(row)
            .drop(columns=["season_id", "league_id"])
            .to_dict("records")
        )
        .reset_index()
        .rename(columns={0: "away_matches", "team_id_away": "team_id"})
    )

    transformed_data = transformed_data.merge(
        clean_data_home_matches, on=["season_id", "league_id", "team_id"], how="outer"
    )
    transformed_data = transformed_data.merge(
        clean_data_away_matches, on=["season_id", "league_id", "team_id"], how="outer"
    )

    transformed_data.loc[:, "home_matches"] = transformed_data.loc[:, "home_matches"].apply(
        lambda x: [] if not isinstance(x, list) and pd.isna(x) else x
    )
    transformed_data.loc[:, "away_matches"] = transformed_data.loc[:, "away_matches"].apply(
        lambda x: [] if not isinstance(x, list) and pd.isna(x) else x
    )

    return transformed_data


def _transform_team_data(
    transformed_data: pd.DataFrame, teams: pd.DataFrame, players: pd.DataFrame
):
    """
    Method to transform team data

    Parameters
    ----------
    transformed_data: pd.DataFrame
        transformed data
    teams: pd.DataFrame
        teams data
    players: pd.DataFrame
        players data
    """
    teams.rename(columns={"id": "team_id"}, inplace=True)

    transformed_data["team"] = teams["name"]
    transformed_data["team_id"] = teams["team_id"]

    return transformed_data


def _transform_season_data(transformed_data: pd.DataFrame, seasons: pd.DataFrame):
    # we create an aux index to be able to get the teams by seasons
    # so if we have 2 seasons, we will have 2 rows for each team
    transformed_data["aux_index"] = 1
    seasons["aux_index"] = 1
    seasons.rename(columns={"id": "season_id", "name": "season"}, inplace=True)

    transformed_data = transformed_data.merge(
        seasons[["aux_index", "season", "season_id"]], on="aux_index"
    )
    transformed_data.drop(columns="aux_index", inplace=True)

    return transformed_data


def _transform_league_data(transformed_data: pd.DataFrame, league: pd.Series):
    transformed_data["league"] = league["name"]
    transformed_data["league_id"] = league["id"]

    return transformed_data


def transform(raw_data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    transformed_data = pd.DataFrame()

    seasons = raw_data[RAW_DATA_SEASONS]
    matches = raw_data[RAW_DATA_MATCHES].rename(columns={"id": "match_id"})
    players = raw_data[RAW_DATA_PLAYERS]
    teams = raw_data[RAW_DATA_TEAMS]
    league = raw_data[RAW_DATA_LEAGUES].iloc[0]

    transformed_data = _transform_team_data(transformed_data, teams, players)
    transformed_data = _transform_season_data(transformed_data, seasons)
    transformed_data = transform_players_data(transformed_data, players, teams, seasons, matches)
    transformed_data = _transform_league_data(transformed_data, league)
    transformed_data = _transform_matches_data(transformed_data, matches, teams, players)

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
    extracted_leagues = (
        leagues_extractor.extract()[f"raw_data_{SportMonksEndpoints.LEAGUES.value}"]
        .drop(columns="_id")
        .to_dict("records")
    )

    return [League.from_dict(league) for league in extracted_leagues]


def get_extractors_configuration(league: League):
    return [
        ExtractorConfig(
            RAW_DATA_MATCHES,
            query={"league_id": league.id},
        ),
        ExtractorConfig(RAW_DATA_TEAMS, query={"country_id": league.country_id}),
        ExtractorConfig(RAW_DATA_SEASONS, query={"league_id": league.id}),
        ExtractorConfig(RAW_DATA_TYPES, query={}),
        ExtractorConfig(RAW_DATA_PLAYERS, query={}),
        ExtractorConfig(RAW_DATA_LEAGUES, query={"id": league.id}),
    ]


def etl_clean_data_by_leagues():
    """
    Method to create ETLs that creates clean data by leagues
    """
    etl_s = []
    database_name = os.getenv("PROJECT_DATABASE", "sport_monks")

    for league in get_leagues():
        output_collection = f"clean_data_league_{league.name.lower()}"
        input_collections = get_extractors_configuration(league)

        writer = MongoDBWriter(database_name, output_collection)
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
                transform_=transform,
            )
        )

    return etl_s
