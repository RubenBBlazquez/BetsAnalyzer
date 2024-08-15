import attr


@attr.s(auto_attribs=True)
class BaseCacheClient:
    """
    Base Cache Client class
    """

    def get(self, key: str) -> str:
        """
        method to get data from cache

        Parameters
        ----------
        key: str
            key to get data

        Returns
        -------
        data
        """
        raise NotImplementedError()

    def set(self, key: str, value: str):
        """
        method to set data in cache

        Parameters
        ----------
        key: str
            key to set data
        value: str
            value to set
        """
        raise NotImplementedError()
