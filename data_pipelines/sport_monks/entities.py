from __future__ import annotations

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


@attr.s(auto_attribs=True)
class Leagues(EntityBase):
    """
    Entity that represents a league in sportmonks API
    """

    id: int
    sport_id: int
    country_id: int
    name: str
    active: bool
    short_code: str
    image_path: str
    type: str
    sub_type: str
    last_played_at: str
    category: Optional[int]
    has_jerseys: bool


@attr.s(auto_attribs=True)
class TeamPlayer(EntityBase):
    """
    Entity that represents a Team Player in sportmonks API
    """

    id: int
    transfer_id: Optional[int]
    player_id: int
    team_id: int
    position_id: Optional[int]
    detailed_position_id: Optional[int]
    start: str
    end: str
    captain: bool
    jersey_number: Optional[int]


@attr.s(auto_attribs=True)
class Teams(EntityBase):
    """
    Entity that represents a Team in sportmonks API
    """

    id: int
    sport_id: int
    country_id: Optional[int]
    venue_id: Optional[int]
    gender: bool
    name: str
    short_code: str
    image_path: str
    founded: Optional[int]
    type: str
    placeholder: bool
    last_played_at: str
    players: list[TeamPlayer]

    @staticmethod
    def includes() -> list[str]:
        """
        method to obtain includes in sportMonks for each entity

        Returns
        -------
        list of includes
        """
        return ["players"]
