from typing import Optional, Type

import attr
from common.utils import EntityWrapper
from downloaders.sport_monks.entities.entity_base import SportMonksDownloaderEntityBase


@attr.s(auto_attribs=True)
class League(EntityWrapper):
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


class LeaguesSportMonksDownloader(SportMonksDownloaderEntityBase):
    """
    Entity that represents the information to create a leagues downloader dag
    """

    @property
    def endpoint_entity_wrapper(self) -> Type[EntityWrapper]:
        return League

    @property
    def endpoints(self) -> list[str]:
        return ["leagues"]
