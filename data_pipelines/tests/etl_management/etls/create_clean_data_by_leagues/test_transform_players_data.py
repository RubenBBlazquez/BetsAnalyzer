import pandas as pd

RAW_DATA_PLAYERS = pd.DataFrame([])

RAW_DATA_TEAMS = pd.DataFrame(
    [
        {
            "team_id": 528,
            "sport_id": 1,
            "country_id": 32,
            "venue_id": 89,
            "gender": True,
            "name": "Espanyol",
            "short_code": "ESY",
            "image_path": "https://cdn.sportmonks.com/images/soccer/teams/16/528.png",
            "founded": 1900,
            "type": "domestic",
            "placeholder": False,
            "last_played_at": "2023-12-19 20:30:00",
            "players": [
                {
                    "id": 11217,
                    "transfer_id": None,
                    "player_id": 110226,
                    "team_id": 528,
                    "position_id": 26,
                    "detailed_position_id": 150,
                    "start": "2020-08-01",
                    "end": "2024-06-30",
                    "captain": False,
                    "jersey_number": 21,
                },
                {
                    "id": 370694,
                    "transfer_id": 10500,
                    "player_id": 129727,
                    "team_id": 528,
                    "position_id": 26,
                    "detailed_position_id": 153,
                    "start": "2022-08-08",
                    "end": "2027-06-30",
                    "captain": False,
                    "jersey_number": 20,
                },
            ],
        },
        {
            "team_id": 214,
            "sport_id": 1,
            "country_id": 32,
            "venue_id": 9240,
            "gender": True,
            "name": "Valencia",
            "short_code": "VAL",
            "image_path": "https://cdn.sportmonks.com/images/soccer/teams/22/214.png",
            "founded": 1919,
            "type": "domestic",
            "placeholder": False,
            "last_played_at": "2023-12-19 18:00:00",
            "players": [
                {
                    "id": 11079,
                    "transfer_id": 26154,
                    "player_id": 186635,
                    "team_id": 214,
                    "position_id": 25,
                    "detailed_position_id": 148,
                    "start": "2017-08-18",
                    "end": "2024-06-30",
                    "captain": False,
                    "jersey_number": 5,
                },
                {
                    "id": 386653,
                    "transfer_id": 11242,
                    "player_id": 793,
                    "team_id": 214,
                    "position_id": 26,
                    "detailed_position_id": 153,
                    "start": "2022-08-25",
                    "end": "2028-06-30",
                    "captain": False,
                    "jersey_number": 10,
                },
            ],
        },
    ]
)

RAW_DATA_SEASON = pd.DataFrame(
    [
        {
            "season_id": 16036,
            "name": "2020/2021",
            "league_id": 271,
            "is_current_season": True,
            "current_round_id": 183973,
            "current_stage_id": 77443861,
            "live_standings": True,
            "coverage": {
                "predictions": True,
                "topscorer_goals": True,
                "topscorer_assists": True,
                "topscorer_cards": True,
            },
        },
    ]
)
