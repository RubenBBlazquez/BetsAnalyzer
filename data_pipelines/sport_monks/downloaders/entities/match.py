from typing import Optional

import attr

from data_pipelines.sport_monks.downloaders.entities.entity_base import DownloaderEntityBase


@attr.s(auto_attribs=True)
class MatchWeatherReportTemperature:
    """
    Entity that represents a Match Weather Report Temperature in sportmonks API
    """

    day: float
    morning: float
    evening: float
    night: float


@attr.s(auto_attribs=True)
class MatchWeatherReportWind:
    """
    Entity that represents a Match Weather Report Wind in sportmonks API
    """

    speed: float
    direction: float


@attr.s(auto_attribs=True)
class MatchWeatherReport:
    """
    Entity that represents a Match Weather Report in sportmonks API
    """

    id: int
    fixture_id: int
    venue_id: int
    temperature: MatchWeatherReportTemperature
    feels_like: MatchWeatherReportTemperature
    wind: MatchWeatherReportWind
    humidity: str
    pressure: int
    clouds: str
    description: str
    icon: str
    type: str
    metric: str
    current: Optional[str]


@attr.s(auto_attribs=True)
class MatchLineup:
    """
    Entity that represents a Match Lineup in sportmonks API
    """

    id: int
    sport_id: int
    fixture_id: int
    player_id: Optional[int]
    team_id: int
    position_id: Optional[int]
    formation_field: Optional[str]
    type_id: int
    formation_position: Optional[int]
    player_name: str
    jersey_number: int


@attr.s(auto_attribs=True)
class MatchStadium:
    """
    Entity that represents a Match Stadium in sportmonks API
    """

    id: int
    country_id: Optional[int]
    city_id: Optional[int]
    name: str
    address: Optional[str]
    zipcode: Optional[str]
    latitude: str
    longitude: str
    capacity: Optional[int]
    image_path: Optional[str]
    city_name: str
    surface: Optional[str]
    national_team: bool


@attr.s(auto_attribs=True)
class MatchScore:
    """
    Entity that represents a Match Score in sportmonks API
    """

    goals: int
    participant: str


@attr.s(auto_attribs=True)
class MatchScores:
    """
    Entity that represents Match Scores in sportmonks API
    """

    id: int
    fixture_id: int
    type_id: int
    participant_id: int
    score: MatchScore
    description: str


@attr.s(auto_attribs=True)
class MatchFormations:
    """
    Entity that represents a Match Formation in sportmonks API
    """

    id: int
    fixture_id: int
    participant_id: int
    formation: str
    location: str


@attr.s(auto_attribs=True)
class Match(DownloaderEntityBase):
    """
    Entity that represents a Match in sportmonks API
    """

    id: int
    league_id: int
    season_id: int
    stage_id: int
    group_id: Optional[int]
    aggregate_id: Optional[int]
    round_id: Optional[int]
    state_id: int
    venue_id: Optional[int]
    name: Optional[str]
    starting_at: Optional[str]
    result_info: Optional[str]
    leg: str
    details: Optional[str]
    length: Optional[int]
    placeholder: bool
    has_odds: bool
    starting_at_timestamp: int
    formations: list[MatchFormations]
    scores: list[MatchScores]
    venue: Optional[MatchStadium]
    lineups: list[MatchLineup]
    weatherreport: Optional[MatchWeatherReport]

    @staticmethod
    def includes() -> list[str]:
        """
        method to obtain includes in sportMonks for each entity

        Returns
        -------
        list of includes
        """
        return ["formations", "scores", "venue", "lineups", "weatherReport"]
