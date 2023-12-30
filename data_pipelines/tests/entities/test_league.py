from sport_monks.entities.league import Leagues

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


def test_league_to_dict():
    league = Leagues(**league_data)
    league_dict = league.to_dict()
    assert league_dict == league_data


def test_league_from_dict():
    league = Leagues.from_dict(league_data)
    assert isinstance(league, Leagues)
    assert league.name == "Premier League"
