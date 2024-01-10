import os
import subprocess

import pytest
from common.db_client.mongo_db_client import MongoDBConnection
from pymongo import MongoClient
from sport_monks.downloaders.constants import (
    RAW_DATA_COUNTRIES,
    RAW_DATA_LEAGUES,
    RAW_DATA_MATCHES,
    RAW_DATA_PLAYERS,
    RAW_DATA_SEASONS,
    RAW_DATA_TEAMS,
    RAW_DATA_TYPES,
)

DOCKER_COMPOSE_FILE = os.path.join(os.path.dirname(__file__), "docker-compose.yaml")


@pytest.fixture
def mongo_db_conn():
    return MongoDBConnection().db_conn


def pytest_addoption(parser):
    parser.addoption("--with-docker-compose", action="store", default=False)


def pytest_sessionstart(session):
    use_docker_compose = session.config.getoption("--with-docker-compose")
    os.environ.update(
        {
            "MONGO_HOST": "localhost",
            "MONGO_PORT": "27017",
            "MONGO_USER": "admin",
            "MONGO_PASSWORD": "root",
            "MONGO_AUTH_DATABASE": "admin",
            "PROJECT_DATABASE": "sport_monks",
        }
    )

    if use_docker_compose:
        subprocess.run(
            ["docker-compose", "-f", DOCKER_COMPOSE_FILE, "up", "-d", "--build"], check=True
        )
        populate_test_database(MongoDBConnection().db_conn)


def pytest_sessionfinish(session, exitstatus):
    use_docker_compose = session.config.getoption("--with-docker-compose")

    if use_docker_compose:
        MongoDBConnection().db_conn.drop_database("sport_monks_prueba")
        subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "down", "-v"], check=True)


def populate_test_database(db_conn: MongoClient):
    seasons = [
        {
            "id": 1,
            "name": "2022/2023",
            "league_id": 1,
            "starting_at": "2020-08-22",
            "ending_at": "2021-05-23",
        },
        {
            "id": 2,
            "name": "2022/2023",
            "league_id": 2,
            "starting_at": "2020-08-22",
            "ending_at": "2021-05-23",
        },
        {
            "id": 3,
            "name": "2021/2022",
            "league_id": 2,
            "starting_at": "2020-08-21",
            "ending_at": "2021-05-22",
        },
    ]
    leagues = [
        {
            "id": 2,
            "sport_id": 1,
            "country_id": 2,
            "name": "La Liga",
            "active": True,
            "short_code": "EPL",
            "image_path": "path/to/league/image.jpg",
            "type": "Football",
            "sub_type": "Professional",
            "last_played_at": "2023-05-20",
            "category": 1,
            "has_jerseys": True,
        },
    ]
    countries = [
        {
            "id": 1,
            "name": "England",
            "fifa_name": "ENG",
        },
        {
            "id": 2,
            "name": "Spain",
            "fifa_name": "SP",
        },
    ]
    players = [
        {
            "id": 1,
            "name": "Pierre-Emerick Aubameyang",
            "image_path": "https://cdn.sportmonks.com/images/soccer/players/1/1.png",
            "height": 187,
            "weight": 80,
            "gender": "male",
        },
        {
            "id": 2,
            "name": "Lionel Messi",
            "image_path": "https://cdn.sportmonks.com/images/soccer/players/1/1.png",
            "height": 187,
            "weight": 80,
            "gender": "male",
        },
        {
            "id": 3,
            "name": "Enry Kane",
            "image_path": "https://cdn.sportmonks.com/images/soccer/players/1/1.png",
            "height": 187,
            "weight": 80,
            "gender": "male",
        },
        {
            "id": 4,
            "name": "Robert Lewandowski",
            "image_path": "https://cdn.sportmonks.com/images/soccer/players/1/1.png",
            "height": 187,
            "weight": 80,
            "gender": "male",
        },
    ]

    teams = [
        {
            "name": "Arsenal",
            "image_path": "https://cdn.sportmonks.com/images/soccer/teams/1/1.png",
            "country_id": 1,
            "id": 1,
            "venue_id": 1,
            "players": [
                {
                    "player_id": 1,
                    "team_id": 1,
                    "position_id": 1,
                    "detailed_position_id": 1,
                    "transfer_id": 1,
                    "start": "2020-01-01",
                    "end": "2023-01-01",
                },
                {
                    "player_id": 2,
                    "team_id": 1,
                    "position_id": 2,
                    "detailed_position_id": 2,
                    "transfer_id": 2,
                    "start": "2020-01-01",
                    "end": "2023-01-01",
                },
            ],
        },
        {
            "name": "Barcelona",
            "image_path": "https://cdn.sportmonks.com/images/soccer/teams/1/1.png",
            "country_id": 2,
            "id": 2,
            "venue_id": 2,
            "players": [
                {
                    "player_id": 3,
                    "team_id": 2,
                    "position_id": 1,
                    "detailed_position_id": 1,
                    "transfer_id": 3,
                    "start": "2020-01-01",
                    "end": "2023-01-01",
                },
                {
                    "player_id": 4,
                    "team_id": 2,
                    "position_id": 2,
                    "detailed_position_id": 2,
                    "transfer_id": 4,
                    "start": "2020-01-01",
                    "end": "2023-01-01",
                },
            ],
        },
        {
            "name": "Madrid",
            "image_path": "https://cdn.sportmonks.com/images/soccer/teams/1/1.png",
            "country_id": 2,
            "id": 3,
            "venue_id": 3,
            "players": [
                {
                    "player_id": 1,
                    "team_id": 3,
                    "position_id": 1,
                    "detailed_position_id": 1,
                    "transfer_id": 5,
                    "start": "2020-01-01",
                    "end": "2023-01-01",
                },
                {
                    "player_id": 2,
                    "team_id": 3,
                    "position_id": 2,
                    "detailed_position_id": 2,
                    "transfer_id": 6,
                    "start": "2020-01-01",
                    "end": "2023-01-01",
                },
            ],
        },
    ]
    matches = [
        {
            "id": 1,
            "league_id": 2,
            "season_id": 2,
            "venue_id": 1,
            "name": "Madrid vs Barcelona",
            "starting_at": "2021-01-03",
            "starting_at_timestamp": "1111111111",
            "result_info": "Game ended in draw",
            "weather_report": None,
            "length": 90,
            "scores": [
                {
                    "id": 1,
                    "fixture_id": 1,
                    "type_id": 1,
                    "participant_id": 3,
                    "score": {"goals": 0, "participant": "home"},
                    "description": "1ST_HALF",
                },
                {
                    "id": 2,
                    "fixture_id": 1,
                    "type_id": 2,
                    "participant_id": 3,
                    "score": {"goals": 1, "participant": "home"},
                    "description": "2ND_HALF",
                },
                {
                    "id": 1,
                    "fixture_id": 1,
                    "type_id": 1,
                    "participant_id": 2,
                    "score": {"goals": 0, "participant": "away"},
                    "description": "1ST_HALF",
                },
                {
                    "id": 2,
                    "fixture_id": 1,
                    "type_id": 2,
                    "participant_id": 2,
                    "score": {"goals": 1, "participant": "away"},
                    "description": "2ND_HALF",
                },
            ],
            "venue": {
                "id": 2,
                "name": "Santiago Bernabéu",
                "latitude": "51.509865",
                "longitude": "-0.118092",
                "capacity": 5000,
                "image_path": "https://cdn.sportmonks.com/images/soccer/venues/17/209.png",
                "city_name": "Madrid",
                "surface": "grass",
            },
            "lineups": [],
        },
        {
            "id": 2,
            "league_id": 2,
            "season_id": 3,
            "venue_id": 1,
            "name": "Madrid vs Barcelona",
            "starting_at": "2021-01-01",
            "starting_at_timestamp": "1111111111",
            "result_info": "Game ended in draw",
            "weather_report": None,
            "length": 90,
            "scores": [
                {
                    "id": 1,
                    "fixture_id": 2,
                    "type_id": 1,
                    "participant_id": 2,
                    "score": {"goals": 2, "participant": "home"},
                    "description": "1ST_HALF",
                },
                {
                    "id": 2,
                    "fixture_id": 2,
                    "type_id": 2,
                    "participant_id": 2,
                    "score": {"goals": 1, "participant": "home"},
                    "description": "2ND_HALF",
                },
                {
                    "id": 1,
                    "fixture_id": 2,
                    "type_id": 1,
                    "participant_id": 3,
                    "score": {"goals": 0, "participant": "away"},
                    "description": "1ST_HALF",
                },
                {
                    "id": 2,
                    "fixture_id": 2,
                    "type_id": 2,
                    "participant_id": 3,
                    "score": {"goals": 1, "participant": "away"},
                    "description": "2ND_HALF",
                },
            ],
            "venue": {
                "id": 2,
                "name": "Santiago Bernabéu",
                "latitude": "51.509865",
                "longitude": "-0.118092",
                "capacity": 5000,
                "image_path": "https://cdn.sportmonks.com/images/soccer/venues/17/209.png",
                "city_name": "Madrid",
                "surface": "grass",
            },
            "lineups": [],
        },
    ]
    types = [
        {
            "id": 1,
            "name": "1st Half",
            "code": "1st-half",
            "developer_name": "1ST_HALF",
            "model_type": "period",
            "stat_group": None,
        },
        {
            "id": 2,
            "name": "2nd Half",
            "code": "2nd-half",
            "developer_name": "2ND_HALF",
            "model_type": "period",
            "stat_group": None,
        },
    ]
    database_name = os.getenv("PROJECT_DATABASE", "sport_monks_prueba")
    db = db_conn.get_database(database_name)
    db.get_collection(RAW_DATA_SEASONS).insert_many(seasons)
    db.get_collection(RAW_DATA_LEAGUES).insert_many(leagues)
    db.get_collection(RAW_DATA_COUNTRIES).insert_many(countries)
    db.get_collection(RAW_DATA_PLAYERS).insert_many(players)
    db.get_collection(RAW_DATA_TEAMS).insert_many(teams)
    db.get_collection(RAW_DATA_MATCHES).insert_many(matches)
    db.get_collection(RAW_DATA_TYPES).insert_many(types)
