from typing import Optional, Type

import attr

from data_pipelines.sport_monks.downloaders.entities.entity_base import (
    DownloaderEntityBase,
    SportMonksEntityBase,
)


@attr.s(auto_attribs=True)
class Country(SportMonksEntityBase):
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


class CountriesDownloader(DownloaderEntityBase):
    """
    Entity that represents the information to create a countries downloader dag
    """

    @property
    def endpoint_entity_wrapper(self) -> Type[SportMonksEntityBase]:
        return Country

    @property
    def middle_endpoint(self) -> str:
        return "core"

    @property
    def endpoint(self) -> str:
        return "countries"
