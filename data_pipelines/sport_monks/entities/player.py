from typing import Optional

import attr

from data_pipelines.common.entity import EntityBase


@attr.s(auto_attribs=True)
class Player(EntityBase):
    """
    Entity that represents a player in sportmonks API
    """

    id: int
    sport_id: int
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

    @staticmethod
    def includes() -> list[str]:
        """
        method to obtain includes in sportMonks for each entity

        Returns
        -------
        list of includes
        """
        return ["position", "teams", "latest"]
