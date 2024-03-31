from typing import Optional, Type

import attr
from common.utils import EntityWrapper
from downloaders.sport_monks.entities.entity_base import SportMonksDownloaderEntityBase


@attr.s(auto_attribs=True)
class Country(EntityWrapper):
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


class CountriesSportMonksDownloader(SportMonksDownloaderEntityBase):
    """
    Entity that represents the information to create a countries downloader dag
    """

    @property
    def endpoint_entity_wrapper(self) -> Type[EntityWrapper]:
        return Country

    @property
    def middle_endpoint(self) -> str:
        return "core"

    @property
    def endpoints(self) -> list[str]:
        return ["countries"]
