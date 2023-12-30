from sport_monks.downloaders.entities.team import Team

team_players = [
    {
        "id": 1,
        "transfer_id": 100,
        "player_id": 200,
        "team_id": 300,
        "position_id": 10,
        "detailed_position_id": 15,
        "start": "2021-01-01",
        "end": "2022-01-01",
        "captain": True,
        "jersey_number": 10,
    },
    {
        "id": 1,
        "transfer_id": 100,
        "player_id": 200,
        "team_id": 300,
        "position_id": 10,
        "detailed_position_id": 15,
        "start": "2021-01-01",
        "end": "2022-01-01",
        "captain": True,
        "jersey_number": 10,
    },
]

teams_data = {
    "id": 101,
    "sport_id": 200,
    "country_id": 45,
    "venue_id": 300,
    "gender": True,
    "name": "City Eagles",
    "short_code": "CE",
    "image_path": "path/to/team/image.jpg",
    "founded": 1985,
    "type": "Professional",
    "placeholder": False,
    "last_played_at": "2023-04-15",
    "players": team_players,
}


def test_teams_to_dict():
    teams = Team(**teams_data)
    teams_dict = teams.to_dict()
    assert teams_dict == teams_data


def test_teams_from_dict():
    teams = Team.from_dict(teams_data)
    assert isinstance(teams, Team)
    assert teams.name == "City Eagles"
    assert len(teams.players) == 2
