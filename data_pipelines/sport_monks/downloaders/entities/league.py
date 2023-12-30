from typing import Optional

import attr

from data_pipelines.sport_monks.downloaders.entities.entity_base import DownloaderEntityBase


@attr.s(auto_attribs=True)
class League(DownloaderEntityBase):
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

    @staticmethod
    def get_endpoint() -> str:
        return "leagues"
