from typing import Optional, Type

import attr
from downloaders.sport_monks.entities.entity_base import DownloaderEntityBase, SportMonksEntityBase


@attr.s(auto_attribs=True)
class SportMonksType(SportMonksEntityBase):
    """
    Entity that represents a type in sportmonks API
    """

    id: int
    name: str
    code: str
    developer_name: str
    model_type: str
    stat_group: Optional[str]


class SportMonksTypesDownloader(DownloaderEntityBase):
    """
    Entity that represents the information to create a types downloader dag
    """

    @property
    def endpoint_entity_wrapper(self) -> Type[SportMonksEntityBase]:
        return SportMonksType

    @property
    def middle_endpoint(self) -> str:
        return "core"

    @property
    def endpoints(self) -> list[str]:
        return ["types"]
