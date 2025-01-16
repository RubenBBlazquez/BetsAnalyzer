import attr


@attr.s(auto_attribs=True)
class BaseCacheClient:
    """
    Base Cache Client class.
    This class defines the interface for cache clients.
    """

    def get(self, key: str) -> str:
        """
        Method to get data from cache.

        Parameters
        ----------
        key: str
            Key to get data from the cache.

        Returns
        -------
        data
            The data retrieved from the cache.
        """
        raise NotImplementedError()

    def set(self, key: str, value: str):
        """
        Method to set data in cache.

        Parameters
        ----------
        key: str
            Key to set data in the cache.
        value: str
            Value to set in the cache.
        """
        raise NotImplementedError()
