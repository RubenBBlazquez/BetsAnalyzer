from typing import Optional

import attr

from data_pipelines.sport_monks.downloaders.entities.entity_base import DownloaderEntityBase


@attr.s(auto_attribs=True)
class TeamPlayer(DownloaderEntityBase):
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
class Teams(DownloaderEntityBase):
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
