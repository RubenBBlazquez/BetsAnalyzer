import os
from typing import Optional, Type

import attr
from common.extractors.base import ExtractorConfig
from common.extractors.mongo_db import MongoDBExtractor
from sport_monks.downloaders.sport_monks_client import SportMonksEndpoints

from data_pipelines.sport_monks.downloaders.entities.entity_base import (
    DownloaderEntityBase,
    SportMonksEntityBase,
)

RAW_DATA_SEASONS = f"raw_data_{SportMonksEndpoints.SEASONS.value}"


@attr.s(auto_attribs=True)
class TopScorerType:
    id: int
    name: str
    code: str
    developer_name: str
    model_type: str
    stat_group: str


@attr.s(auto_attribs=True)
class TopScorerPlayer:
    id: int
    sport_id: int
    country_id: Optional[int]
    nationality_id: Optional[int]
    city_id: Optional[int]
    position_id: Optional[int]
    detailed_position_id: Optional[int]
    type_id: Optional[int]
    common_name: str
    firstname: str
    lastname: str
    name: str
    display_name: str
    image_path: str
    height: Optional[int]
    weight: Optional[int]
    date_of_birth: str
    gender: str


@attr.s(auto_attribs=True)
class TopScorer(SportMonksEntityBase):
    """
    Entity that represents a player in sportmonks API
    """

    id: int
    season_id: int
    player_id: int
    type_id: int
    position: int
    total: int
    participant_id: int
    player: TopScorerPlayer
    type: TopScorerType


class TopScorersDownloader(DownloaderEntityBase):
    """
    Entity that represents the information to create a top scorers downloader dag
    """

    @property
    def endpoint_entity_wrapper(self) -> Type[SportMonksEntityBase]:
        return TopScorer

    @property
    def includes(self) -> list[str]:
        return ["player", "type"]

    @property
    def dag_name(self) -> str:
        return "player_statistics_by_season"

    @property
    def endpoints(self) -> list[str]:
        database_name = os.getenv("PROJECT_DATABASE", "sport_monks")
        seasons = MongoDBExtractor([ExtractorConfig(RAW_DATA_SEASONS)], database_name).extract()[
            RAW_DATA_SEASONS
        ]

        for season in seasons.itertuples(index=False):
            yield f"topscorers/seasons/{str(season.id)}"
