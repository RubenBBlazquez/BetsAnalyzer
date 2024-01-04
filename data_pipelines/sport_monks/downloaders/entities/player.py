from typing import Optional

import attr

from data_pipelines.sport_monks.downloaders.entities.entity_base import DownloaderEntityBase


class PlayerPosition:
    """
    Entity that represents a position in sportmonks API Players endpoint
    """

    id: int
    name: str
    code: str
    developer_name: str
    model_type: str
    stat_group: Optional[str]


class PlayerTransfer:
    """
    Entity that represents a transfer in sportmonks API Players endpoint
    """

    id: int
    sport_id: int
    player_id: int
    type_id: int
    from_team_id: int
    to_team_id: int
    position_id: Optional[int]
    detailed_position_id: Optional[int]
    date: str
    career_ended: bool
    completed: bool
    amount: Optional[int]


class PlayerTeam:
    """
    Entity that represents a team in sportmonks API Players endpoint
    """

    id: int
    transfer_id: Optional[int]
    player_id: int
    team_id: int
    position_id: Optional[int]
    detailed_position_id: Optional[int]
    start: Optional[str]
    end: Optional[str]
    captain: Optional[bool]
    jersey_number: Optional[int]


@attr.s(auto_attribs=True)
class Player(DownloaderEntityBase):
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
    teams: Optional[list[PlayerTeam]]
    transfers: Optional[list[PlayerTransfer]]
    position: Optional[PlayerPosition]

    @staticmethod
    def includes() -> list[str]:
        """
        method to obtain includes in sportMonks for each entity

        Returns
        -------
        list of includes
        """
        return ["position", "teams", "transfers"]

    @staticmethod
    def get_endpoint() -> str:
        return "players"


@attr.s(auto_attribs=True)
class SpainPlayers(Player):
    """
    Entity that represents a spain players in sportmonks API
    """

    @staticmethod
    def get_endpoint() -> str:
        return "players/countries/32"


@attr.s(auto_attribs=True)
class EnglandPlayers(Player):
    """
    Entity that represents a spain players in sportmonks API
    """

    @staticmethod
    def get_endpoint() -> str:
        return "players/countries/462"


@attr.s(auto_attribs=True)
class GermanyPlayers(Player):
    """
    Entity that represents a spain players in sportmonks API
    """

    @staticmethod
    def get_endpoint() -> str:
        return "players/countries/11"
