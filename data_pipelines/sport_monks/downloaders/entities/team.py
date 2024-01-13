from typing import Optional, Type

import attr

from data_pipelines.sport_monks.downloaders.entities.entity_base import (
    DownloaderEntityBase,
    SportMonksEntityBase,
)


@attr.s(auto_attribs=True)
class TeamPlayer:
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
class Team(SportMonksEntityBase):
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


class TeamsDownloader(DownloaderEntityBase):
    """
    Entity that represents the information to create a teams downloader dag
    """

    @property
    def endpoint_entity_wrapper(self) -> Type[SportMonksEntityBase]:
        return Team

    @property
    def includes(self) -> list[str]:
        return ["players"]

    @property
    def endpoints(self) -> list[str]:
        return ["teams"]
