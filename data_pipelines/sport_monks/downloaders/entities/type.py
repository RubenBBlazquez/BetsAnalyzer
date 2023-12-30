from typing import Optional

import attr

from data_pipelines.sport_monks.downloaders.entities.entity_base import DownloaderEntityBase


@attr.s(auto_attribs=True)
class Type(DownloaderEntityBase):
    """
    Entity that represents a type in sportmonks API
    """

    id: int
    name: str
    code: str
    developer_name: str
    model_type: str
    stat_group: Optional[str]

    @staticmethod
    def get_middle_endpoint() -> str:
        return "core"
