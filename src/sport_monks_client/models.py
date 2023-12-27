import os

import attr

from src.common.api_client_base import ApiClientBase


@attr.s(auto_attribs=True, frozen=True)
class SportMonksClient(ApiClientBase):
    """
    Class for SportMonks API client
    """

    def get_players(self):
        """
        Method to get players from SportMonks API
        """
        api_key = os.getenv("SPORT_MONKS_API_KEY", default="")
        api_url = os.getenv("SPORT_MONKS_BASE_URL", default="")

        return self.get(url=f"{api_url}/football/players", params={"api_token": api_key})["data"]
