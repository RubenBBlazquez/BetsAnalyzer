import os

import attr

from src.common.api_client_base import ApiClientBase


@attr.s(auto_attribs=True)
class SportMonksClient(ApiClientBase):
    """
    Class for SportMonks API client
    """

    def __attrs_post_init__(self):
        self.api_key = os.getenv("SPORT_MONKS_API_KEY", default="")
        self.api_url = os.getenv("SPORT_MONKS_BASE_URL", default="")

    def get_players(self):
        """
        Method to get players from SportMonks API
        """

        return self.get(url=f"{self.api_url}/football/players", params={"api_token": self.api_key})[
            "data"
        ]
