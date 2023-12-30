from typing import Optional

import attr

from data_pipelines.sport_monks.downloaders.entities.entity_base import DownloaderEntityBase


@attr.s(auto_attribs=True)
class Country(DownloaderEntityBase):
    """
    Entity that represents a country in sportmonks API
    """

    id: int
    continent_id: int
    name: str
    official_name: str
    fifa_name: str
    iso2: str
    iso3: str
    latitude: str
    longitude: str
    borders: Optional[list[str]]
    image_path: str

    @staticmethod
    def get_middle_endpoint() -> str:
        return "core"
