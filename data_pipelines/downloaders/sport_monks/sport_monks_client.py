import logging
import os
from enum import Enum
from typing import Any, Iterator

import attr
from downloaders.sport_monks.entities.entity_base import DownloaderEntityBase

from data_pipelines.common.api_client_base import ApiClientBase


class SportMonksEndpoints(Enum):
    """
    Enum for SportMonks API endpoints to get and download data
    """

    PLAYERS = "players"
    PLAYERS_SPAIN = "spain_players"
    PLAYERS_ENGLAND = "england_players"
    PLAYERS_GERMANY = "germany_players"
    TEAMS = "teams"
    LEAGUES = "leagues"
    MATCHES = "fixtures"
    COUNTRIES = "countries"
    TYPES = "types"
    SEASONS = "seasons"
    TOP_SCORERS = "top_scorers"


@attr.s(auto_attribs=True)
class SportMonksClient(ApiClientBase):
    """
    Class for SportMonks API client
    """

    def __attrs_post_init__(self):
        self.api_key = os.getenv("SPORT_MONKS_API_KEY", default="")
        self.api_url = os.getenv("SPORT_MONKS_BASE_URL", default="")

    def get_data_in_batches(self, entity: DownloaderEntityBase) -> Iterator[Any]:
        per_page = 50
        endpoints = entity.endpoints

        for endpoint in endpoints:
            page = 1
            has_more_pages = True
            endpoint_url = f"{self.api_url}/{entity.middle_endpoint}/{endpoint}"
            logging.info(f"-------------------------------------------")
            logging.info(f"downloading data from endpoint: {endpoint_url} ")

            while has_more_pages:
                response = self.get(
                    url=endpoint_url,
                    params={
                        "api_token": self.api_key,
                        "page": page,
                        "per_page": per_page,
                        "include": ";".join(entity.includes),
                    },
                )

                response_data = response.get("data")

                if not response_data:
                    logging.info(
                        f"there's no information with request: {endpoint}, "
                        f"message: {response.get('message', 'no_message')}"
                    )
                    has_more_pages = False
                    continue

                has_more_pages = response["pagination"]["has_more"]
                page += 1

                entity_wrapper = entity.endpoint_entity_wrapper
                yield [entity_wrapper.from_dict(data) for data in response_data]
