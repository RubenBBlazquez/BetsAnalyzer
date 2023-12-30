from __future__ import annotations

from copy import deepcopy

import attr
import cattrs


@attr.s(auto_attribs=True)
class DownloaderEntityBase:
    """
    Base Downloader Entity information
    """

    def to_dict(self) -> dict:
        """
        method to convert entity to dict

        Returns
        -------
        dict representation of entity
        """
        return attr.asdict(self)

    @classmethod
    def from_dict(cls, dict_: dict) -> DownloaderEntityBase:
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

    @staticmethod
    def get_endpoint() -> str:
        """
        middle endpoint to obtain data in sportMonks for each entity

        Returns
        -------
        middle endpoint
        """
        raise NotImplementedError()

    @staticmethod
    def get_includes() -> list[str]:
        """
        method to obtain includes in sportMonks for each entity

        Returns
        -------
        list of includes
        """
        return []
