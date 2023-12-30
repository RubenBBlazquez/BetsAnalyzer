import os
from enum import Enum
from typing import Any, Iterator

import attr
from sport_monks.downloaders.entities.country import Country
from sport_monks.downloaders.entities.entity_base import DownloaderEntityBase
from sport_monks.downloaders.entities.league import League
from sport_monks.downloaders.entities.match import Match
from sport_monks.downloaders.entities.player import Player
from sport_monks.downloaders.entities.team import Team
from sport_monks.downloaders.entities.type import Type

from data_pipelines.common.api_client_base import ApiClientBase


class SportMonksEndpoints(Enum):
    """
    Enum for SportMonks API endpoints to get and download data
    """

    PLAYERS = "players"
    TEAMS = "teams"
    LEAGUES = "leagues"
    MATCHES = "fixtures"
    COUNTRIES = "countries"
    TYPES = "types"


DATABASE_NAME = "sport_monks"

RAW_DATA_COLLECTIONS_SWITCHER = {
    SportMonksEndpoints.PLAYERS: "raw_data_players",
    SportMonksEndpoints.LEAGUES: "raw_data_leagues",
    SportMonksEndpoints.TEAMS: "raw_data_teams",
    SportMonksEndpoints.MATCHES: "raw_data_matches",
    SportMonksEndpoints.COUNTRIES: "raw_data_countries",
    SportMonksEndpoints.TYPES: "raw_data_types",
}

DOWNLOADER_ENTITY_SWITCHER = {
    SportMonksEndpoints.PLAYERS: Player,
    SportMonksEndpoints.LEAGUES: League,
    SportMonksEndpoints.TEAMS: Team,
    SportMonksEndpoints.MATCHES: Match,
    SportMonksEndpoints.COUNTRIES: Country,
    SportMonksEndpoints.TYPES: Type,
}


@attr.s(auto_attribs=True)
class SportMonksClient(ApiClientBase):
    """
    Class for SportMonks API client
    """

    def __attrs_post_init__(self):
        self.api_key = os.getenv("SPORT_MONKS_API_KEY", default="")
        self.api_url = os.getenv("SPORT_MONKS_BASE_URL", default="")

    def get_data_in_batches(self, entity: DownloaderEntityBase) -> Iterator[Any]:
        has_more_pages = True
        page = 1
        per_page = 50

        while has_more_pages:
            response = self.get(
                url=f"{self.api_url}/{entity.get_middle_endpoint()}/{entity.get_endpoint()}",
                params={
                    "api_token": self.api_key,
                    "page": page,
                    "per_page": per_page,
                    "include": ";".join(entity.get_includes()),
                },
            )

            has_more_pages = response["pagination"]["has_more"]
            page += 1

            yield [entity.from_dict(data) for data in response["data"]]
