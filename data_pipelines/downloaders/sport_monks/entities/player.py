from typing import Optional, Type

import attr
from common.utils import EntityWrapper
from downloaders.sport_monks.entities.entity_base import SportMonksDownloaderEntityBase


@attr.s(auto_attribs=True)
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


@attr.s(auto_attribs=True)
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


@attr.s(auto_attribs=True)
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
class Player(EntityWrapper):
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


class PlayersSportMonksDownloader(SportMonksDownloaderEntityBase):
    """
    Entity that represents the information to create a players downloader dag
    """

    @property
    def endpoint_entity_wrapper(self) -> Type[EntityWrapper]:
        return Player

    @property
    def includes(self) -> list[str]:
        return ["position", "teams", "transfers"]

    @property
    def endpoints(self) -> list[str]:
        return ["players"]


class SpainPlayersDownloader(PlayersSportMonksDownloader):
    """
    Entity that represents the information to create a spain players downloader dag
    """

    @property
    def endpoints(self) -> list[str]:
        return ["players/countries/32"]

    @property
    def dag_name(self) -> str:
        return "SportMonks_spain_players"


class EnglandPlayersDownloader(PlayersSportMonksDownloader):
    """
    Entity that represents the information to create a england players downloader dag
    """

    @property
    def endpoints(self) -> list[str]:
        return ["players/countries/462"]

    @property
    def dag_name(self) -> str:
        return "SportMonks_england_players"


class GermanyPlayersDownloader(PlayersSportMonksDownloader):
    """
    Entity that represents the information to create a germany players downloader dag
    """

    @property
    def endpoints(self) -> list[str]:
        return ["players/countries/11"]

    @property
    def dag_name(self) -> str:
        return "SportMonks_germany_players"
