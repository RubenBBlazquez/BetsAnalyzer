from typing import Optional, Type

import attr
from downloaders.sport_monks.entities.entity_base import DownloaderEntityBase, SportMonksEntityBase


@attr.s(auto_attribs=True)
class League(SportMonksEntityBase):
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


class LeaguesDownloader(DownloaderEntityBase):
    """
    Entity that represents the information to create a leagues downloader dag
    """

    @property
    def endpoint_entity_wrapper(self) -> Type[SportMonksEntityBase]:
        return League

    @property
    def endpoints(self) -> list[str]:
        return ["leagues"]
