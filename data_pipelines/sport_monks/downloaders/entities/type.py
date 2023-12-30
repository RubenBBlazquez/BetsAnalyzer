from typing import Optional

import attr
from sport_monks.downloaders.entities.entity_base import EntityBase


@attr.s(auto_attribs=True)
class Type(EntityBase):
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
