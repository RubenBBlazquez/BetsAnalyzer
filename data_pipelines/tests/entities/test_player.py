from sport_monks.downloaders.entities.player import Player

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


def test_player_to_dict():
    player = Player(**player_data)
    player_dict = player.to_dict()
    assert player_dict == player_data


def test_player_from_dict():
    player = Player.from_dict(player_data)
    assert isinstance(player, Player)
    assert player.firstname == "John"
