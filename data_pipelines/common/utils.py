from __future__ import annotations

from copy import deepcopy

import attr
import cattrs


@attr.s(auto_attribs=True)
class EntityWrapper:
    """
    Wrapper class for entities.
    This class provides methods to convert entities to and from dictionaries.
    """

    def to_dict(self) -> dict:
        """
        Method to convert entity to dictionary.

        Returns
        -------
        dict
            Representation of the entity as a dictionary.
        """
        return attr.asdict(self)

    @classmethod
    def from_dict(cls, dict_: dict) -> EntityWrapper:
        """
        Method to cast dictionary to entity.

        Returns
        -------
        EntityWrapper
            The entity created from the dictionary.
        """
        converter = deepcopy(cattrs.global_converter)
        return converter.structure(dict_, cls)
