from abc import ABC, abstractmethod

import attr
import requests


class IApiClient(ABC):
    """
    Interface that represents an api client base methods
    """

    @abstractmethod
    def get(self, url: str, params: dict = None, headers: dict = None) -> dict:
        """
        method to make GET request:

        Parameters
        ----------
        url: str
            url to make request
        params: dict
            parameters to pass to request
        headers: dict
            headers to pass to request
        """
        pass

    @abstractmethod
    def post(self, url: str, params: dict = None, body: dict = None, headers: dict = None) -> dict:
        """
        method to make POST request:

        Parameters
        ----------
        url: str
            url to make request
        params: dict
            parameters to pass to request
        body: dict
            body to pass to request
        headers: dict
            headers to pass to request
        """
        pass

    @abstractmethod
    def put(self, url: str, params: dict = None, body: dict = None, headers: dict = None) -> dict:
        """
        method to make PUT request:

        Parameters
        ----------
        url: str
            url to make request
        params: dict
            parameters to pass to request
        body: dict
            body to pass to request
        headers: dict
            headers to pass to request
        """
        pass

    @abstractmethod
    def delete(
        self, url: str, params: dict = None, body: dict = None, headers: dict = None
    ) -> dict:
        """
        method to make DELETE request:

        Parameters
        ----------
        url: str
            url to make request
        params: dict
            parameters to pass to request
        body: dict
            body to pass to request
        headers: dict
            headers to pass to request
        """

        pass


@attr.s(auto_attribs=True)
class ApiClientBase(IApiClient):
    """
    Base class for api clients
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
