from abc import ABC, abstractmethod

import attr
import requests


class IApiClient(ABC):
    """
    Interface that represents an API client base methods.
    This class defines the structure for any API client implementation.
    """

    @abstractmethod
    def get(self, url: str, params: dict = None, headers: dict = None) -> dict:
        """
        Method to make a GET request.

        Parameters
        ----------
        url: str
            URL to make the request to.
        params: dict
            Parameters to pass to the request.
        headers: dict
            Headers to pass to the request.
        """
        pass

    @abstractmethod
    def post(self, url: str, params: dict = None, body: dict = None, headers: dict = None) -> dict:
        """
        Method to make a POST request.

        Parameters
        ----------
        url: str
            URL to make the request to.
        params: dict
            Parameters to pass to the request.
        body: dict
            Body to pass to the request.
        headers: dict
            Headers to pass to the request.
        """
        pass

    @abstractmethod
    def put(self, url: str, params: dict = None, body: dict = None, headers: dict = None) -> dict:
        """
        Method to make a PUT request.

        Parameters
        ----------
        url: str
            URL to make the request to.
        params: dict
            Parameters to pass to the request.
        body: dict
            Body to pass to the request.
        headers: dict
            Headers to pass to the request.
        """
        pass

    @abstractmethod
    def delete(
        self, url: str, params: dict = None, body: dict = None, headers: dict = None
    ) -> dict:
        """
        Method to make a DELETE request.

        Parameters
        ----------
        url: str
            URL to make the request to.
        params: dict
            Parameters to pass to the request.
        body: dict
            Body to pass to the request.
        headers: dict
            Headers to pass to the request.
        """
        pass


@attr.s(auto_attribs=True)
class ApiClientBase(IApiClient):
    """
    Base class for API clients that implements the IApiClient interface.
    This class provides default implementations for the API methods.
    """

    def get(self, url: str, params: dict = None, headers: dict = None) -> dict:
        params, headers = params or {}, headers or {}
        return requests.get(url, params=params, headers=headers).json()

    def post(self, url: str, params: dict = None, body: dict = None, headers: dict = None) -> dict:
        params, headers, body = params or {}, headers or {}, body or {}
        return requests.post(url, data=body, params=params, headers=headers).json()

    def put(self, url: str, params: dict = None, body: dict = None, headers: dict = None) -> dict:
        params, headers, body = params or {}, headers or {}, body or {}
        return requests.put(url, data=body, params=params, headers=headers).json()

    def delete(
        self, url: str, params: dict = None, body: dict = None, headers: dict = None
    ) -> dict:
        params, headers, body = params or {}, headers or {}, body or {}
        return requests.get(url, data=body, params=params, headers=headers).json()
