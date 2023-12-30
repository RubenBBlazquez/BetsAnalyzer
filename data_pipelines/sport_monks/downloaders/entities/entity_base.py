from copy import deepcopy

import attr
import cattrs
from common.entity_base import IEntity


@attr.s(auto_attribs=True)
class DownloaderEntityBase(IEntity):
    """
    Base Entity class
    """

    @staticmethod
    def get_includes() -> list[str]:
        """
        method to obtain includes in sportMonks for each entity

        Returns
        -------
        list of includes
        """
        return []

    def to_dict(self) -> dict:
        """
        method to convert entity to dict

        Returns
        -------
        dict representation of entity
        """
        return attr.asdict(self)

    @classmethod
    def from_dict(cls, dict_: dict) -> IEntity:
        """
        method to cast dict to entity

        Returns
        -------
        entity
        """
        converter = deepcopy(cattrs.global_converter)
        return converter.structure(dict_, cls)

    @staticmethod
    def get_middle_endpoint() -> str:
        """
        middle endpoint to obtain data in sportMonks for each entity

        Returns
        -------
        middle endpoint
        """
        return "football"
