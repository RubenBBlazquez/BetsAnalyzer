from downloaders.sport_monks.entities.country import CountriesSportMonksDownloader
from downloaders.sport_monks.entities.league import LeaguesSportMonksDownloader
from downloaders.sport_monks.entities.match import MatchesSportMonksDownloader
from downloaders.sport_monks.entities.player import (
    EnglandPlayersDownloader,
    GermanyPlayersDownloader,
    PlayersSportMonksDownloader,
    SpainPlayersDownloader,
)
from downloaders.sport_monks.entities.season import SeasonsSportMonksDownloader
from downloaders.sport_monks.entities.sport_monks_type import SportMonksTypesSportMonksDownloader
from downloaders.sport_monks.entities.team import TeamsSportMonksDownloader
from downloaders.sport_monks.entities.top_scorer import TopScorersSportMonksDownloader
from downloaders.sport_monks.sport_monks_client import SportMonksEndpoints

DEFAULT_ENGLAND_COUNTRY_ID = 462
DEFAULT_GERMANY_COUNTRY_ID = 11
DEFAULT_SPAIN_COUNTRY_ID = 32

RAW_DATA_PLAYERS = f"raw_data_{SportMonksEndpoints.PLAYERS.value}"
RAW_DATA_LEAGUES = f"raw_data_{SportMonksEndpoints.LEAGUES.value}"
RAW_DATA_TEAMS = f"raw_data_{SportMonksEndpoints.TEAMS.value}"
RAW_DATA_MATCHES = f"raw_data_{SportMonksEndpoints.MATCHES.name.lower()}"
RAW_DATA_COUNTRIES = f"raw_data_{SportMonksEndpoints.COUNTRIES.value}"
RAW_DATA_TYPES = f"raw_data_{SportMonksEndpoints.TYPES.value}"
RAW_DATA_SEASONS = f"raw_data_{SportMonksEndpoints.SEASONS.value}"
RAW_DATA_TOP_SCORERS = f"raw_data_top_scorers"

RAW_DATA_COLLECTIONS_SWITCHER = {
    SportMonksEndpoints.PLAYERS: RAW_DATA_PLAYERS,
    SportMonksEndpoints.PLAYERS_SPAIN: RAW_DATA_PLAYERS,
    SportMonksEndpoints.PLAYERS_ENGLAND: RAW_DATA_PLAYERS,
    SportMonksEndpoints.PLAYERS_GERMANY: RAW_DATA_PLAYERS,
    SportMonksEndpoints.LEAGUES: RAW_DATA_LEAGUES,
    SportMonksEndpoints.TEAMS: RAW_DATA_TEAMS,
    SportMonksEndpoints.MATCHES: RAW_DATA_MATCHES,
    SportMonksEndpoints.COUNTRIES: RAW_DATA_COUNTRIES,
    SportMonksEndpoints.TYPES: RAW_DATA_TYPES,
    SportMonksEndpoints.SEASONS: RAW_DATA_SEASONS,
    SportMonksEndpoints.TOP_SCORERS: RAW_DATA_TOP_SCORERS,
}

DOWNLOADER_ENTITY_SWITCHER = {
    SportMonksEndpoints.PLAYERS: PlayersSportMonksDownloader(),
    SportMonksEndpoints.PLAYERS_ENGLAND: EnglandPlayersDownloader(),
    SportMonksEndpoints.PLAYERS_GERMANY: GermanyPlayersDownloader(),
    SportMonksEndpoints.PLAYERS_SPAIN: SpainPlayersDownloader(),
    SportMonksEndpoints.LEAGUES: LeaguesSportMonksDownloader(),
    SportMonksEndpoints.TEAMS: TeamsSportMonksDownloader(),
    SportMonksEndpoints.MATCHES: MatchesSportMonksDownloader(),
    SportMonksEndpoints.COUNTRIES: CountriesSportMonksDownloader(),
    SportMonksEndpoints.TYPES: SportMonksTypesSportMonksDownloader(),
    SportMonksEndpoints.SEASONS: SeasonsSportMonksDownloader(),
    SportMonksEndpoints.TOP_SCORERS: TopScorersSportMonksDownloader(),
}
