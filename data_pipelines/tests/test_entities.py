from sport_monks.entities import Leagues, Player, Teams

player_data = {
    "id": 1,
    "sport_id": 100,
    "country_id": 50,
    "nationality_id": 55,
    "city_id": 500,
    "position_id": 10,
    "detailed_position_id": 15,
    "type_id": 5,
    "common_name": "John Doe",
    "firstname": "John",
    "lastname": "Doe",
    "name": "John Doe",
    "display_name": "J. Doe",
    "image_path": "path/to/image.jpg",
    "height": 180,
    "weight": 75,
    "date_of_birth": "1990-01-01",
    "gender": "M",
}

league_data = {
    "id": 2,
    "sport_id": 100,
    "country_id": 60,
    "name": "Premier League",
    "active": True,
    "short_code": "EPL",
    "image_path": "path/to/league/image.jpg",
    "type": "Football",
    "sub_type": "Professional",
    "last_played_at": "2023-05-20",
    "category": 1,
    "has_jerseys": True,
}

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
}


def test_player_to_dict():
    player = Player(**player_data)
    player_dict = player.to_dict()
    assert player_dict == player_data


def test_league_to_dict():
    league = Leagues(**league_data)
    league_dict = league.to_dict()
    assert league_dict == league_data


def test_teams_to_dict():
    teams = Teams(**teams_data)
    teams_dict = teams.to_dict()
    assert teams_dict == teams_data


def test_player_from_dict():
    player = Player.from_dict(player_data)
    assert isinstance(player, Player)
    assert player.firstname == "John"


def test_league_from_dict():
    league = Leagues.from_dict(league_data)
    assert isinstance(league, Leagues)
    assert league.name == "Premier League"


def test_teams_from_dict():
    teams = Teams.from_dict(teams_data)
    assert isinstance(teams, Teams)
    assert teams.name == "City Eagles"
