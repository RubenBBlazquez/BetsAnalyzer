import attr

from src.common.entity import IEntity


class Player(IEntity):
    """
    Entity that represents a player in sportmonks API
    """

    id: int
    sport_id: int
    country_id: int
    nationality_id: int
    city_id: int
    position_id: int
    detailed_position_id: int
    type_id: int
    common_name: str
    firstname: str
    lastname: str
    name: str
    display_name: str
    image_path: str
    height: int
    weight: int
    date_of_birth: str
    gender: str

    def to_dict(self) -> dict:
        return attr.asdict(self)
