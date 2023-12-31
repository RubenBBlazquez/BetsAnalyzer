import os

from pymongo import MongoClient
from sport_monks.etl_management.etls.create_clean_data_by_leagues import etl_clean_data_by_leagues


def populate_test_database(db_conn: MongoClient):
    """ """
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
    ]
    leagues = [
        {
            "id": 1,
            "country_id": 1,
            "name": "Premier League",
            "image_path": "https://cdn.sportmonks.com/images/soccer/leagues/20/564.png",
        },
        {
            "id": 2,
            "country_id": 2,
            "name": "La Liga",
            "image_path": "https://cdn.sportmonks.com/images/soccer/leagues/20/564.png",
        },
    ]
    countries = [
        {
            "name": "England",
            "fifa_name": "ENG",
            "country_id": 1,
        },
        {
            "name": "Spain",
            "country_id": 2,
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
            "team_id": 1,
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
            "team_id": 2,
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
            "team_id": 3,
            "venue_id": 3,
            "players": [
                {
                    "player_id": 5,
                    "team_id": 3,
                    "position_id": 1,
                    "detailed_position_id": 1,
                    "transfer_id": 5,
                    "start": "2020-01-01",
                    "end": "2023-01-01",
                },
                {
                    "player_id": 6,
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
            "season_id": 1,
            "venue_id": 1,
            "name": "Madrid vs Barcelona",
            "starting_at": "2021-01-01",
            "result_info": "Game ended in draw",
            "length": 90,
            "scores": [
                {
                    "id": 1,
                    "fixture_id": 1,
                    "type_id": 1,
                    "participant_id": 6,
                    "score": {"goals": 0, "participant": "home"},
                    "description": "1ST_HALF",
                },
                {
                    "id": 2,
                    "fixture_id": 1,
                    "type_id": 2,
                    "participant_id": 6,
                    "score": {"goals": 0, "participant": "home"},
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
        }
    ]
    database_name = os.getenv("PROJECT_DATABASE", "sport_monks_prueba")
    db_conn.get_database(database_name).get_collection("raw_data_seasons").insert_many(seasons)
    db_conn.get_database(database_name).get_collection("raw_data_leagues").insert_many(leagues)
    db_conn.get_database(database_name).get_collection("raw_data_countries").insert_many(countries)
    db_conn.get_database(database_name).get_collection("raw_data_players").insert_many(players)
    db_conn.get_database(database_name).get_collection("raw_data_teams").insert_many(teams)
    db_conn.get_database(database_name).get_collection("raw_data_matches").insert_many(matches)


def test_etl_clean_data_by_leagues(mongo_db_conn):
    populate_test_database(mongo_db_conn)
    etl_clean_data_by_leagues()
