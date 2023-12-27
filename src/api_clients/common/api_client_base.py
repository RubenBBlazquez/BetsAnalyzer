from abc import ABC, abstractmethod


class ApiClientBase(ABC):

    @abstractmethod
    def get(self, url: str, params: dict = None) -> dict:
        """
        method to make GET request:

        Parameters
        ----------
        url: str
            url to make request
        params: dict
            parameters to pass to request
        """
        pass

    @abstractmethod
    def post(self, url: str, params: dict = None) -> dict:
        """
        method to make POST request:

        Parameters
        ----------
        url: str
            url to make request
        params: dict
            parameters to pass to request
        """
        pass

    @abstractmethod
    def put(self, url: str, params: dict = None) -> dict:
        """
        method to make PUT request:

        Parameters
        ----------
        url: str
            url to make request
        params: dict
            parameters to pass to request
        """
        pass

    @abstractmethod
    def delete(self, url: str, params: dict = None) -> dict:
        """
        method to make DELETE request:

        Parameters
        ----------
        url: str
            url to make request
        params: dict
            parameters to pass to request
        """

        pass
