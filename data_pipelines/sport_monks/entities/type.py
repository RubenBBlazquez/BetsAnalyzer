from typing import Optional

import attr
from common.entity import EntityBase


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
