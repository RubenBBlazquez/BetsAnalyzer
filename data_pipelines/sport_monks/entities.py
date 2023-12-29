from __future__ import annotations

from typing import Optional

import attr

from data_pipelines.common.entity import IEntity


@attr.s(auto_attribs=True)
class Player(IEntity):
    """
    Entity that represents a player in sportmonks API
    """

    id: Optional[int]
    sport_id: Optional[int]
    country_id: Optional[int]
    nationality_id: Optional[int]
    city_id: Optional[int]
    position_id: Optional[int]
    detailed_position_id: Optional[int]
    type_id: Optional[int]
    common_name: str
    firstname: str
    lastname: str
    name: str
    display_name: str
    image_path: str
    height: Optional[int]
    weight: Optional[int]
    date_of_birth: str
    gender: str

    def to_dict(self) -> dict:
        return attr.asdict(self)
