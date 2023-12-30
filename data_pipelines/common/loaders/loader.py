from abc import ABC

import attr


@attr.s(auto_attribs=True)
class ILoader(ABC):
    """
    Base Loader class
    """

    @staticmethod
    def load() -> None:
        """
        method to load data
        """
        raise NotImplementedError()
