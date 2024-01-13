from sport_monks.downloaders.entities.country import CountriesDownloader
from sport_monks.downloaders.entities.league import LeaguesDownloader
from sport_monks.downloaders.entities.match import MatchesDownloader
from sport_monks.downloaders.entities.player import (
    EnglandPlayersDownloader,
    GermanyPlayersDownloader,
    PlayersDownloader,
    SpainPlayersDownloader,
)
from sport_monks.downloaders.entities.season import SeasonsDownloader
from sport_monks.downloaders.entities.sport_monks_type import SportMonksTypesDownloader
from sport_monks.downloaders.entities.team import TeamsDownloader
from sport_monks.downloaders.sport_monks_client import SportMonksEndpoints

RAW_DATA_PLAYERS = f"raw_data_{SportMonksEndpoints.PLAYERS.value}"
RAW_DATA_LEAGUES = f"raw_data_{SportMonksEndpoints.LEAGUES.value}"
RAW_DATA_TEAMS = f"raw_data_{SportMonksEndpoints.TEAMS.value}"
RAW_DATA_MATCHES = f"raw_data_{SportMonksEndpoints.MATCHES.name.lower()}"
RAW_DATA_COUNTRIES = f"raw_data_{SportMonksEndpoints.COUNTRIES.value}"
RAW_DATA_TYPES = f"raw_data_{SportMonksEndpoints.TYPES.value}"
RAW_DATA_SEASONS = f"raw_data_{SportMonksEndpoints.SEASONS.value}"

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
}

DOWNLOADER_ENTITY_SWITCHER = {
    SportMonksEndpoints.PLAYERS: PlayersDownloader(),
    SportMonksEndpoints.PLAYERS_ENGLAND: EnglandPlayersDownloader(),
    SportMonksEndpoints.PLAYERS_GERMANY: GermanyPlayersDownloader(),
    SportMonksEndpoints.PLAYERS_SPAIN: SpainPlayersDownloader(),
    SportMonksEndpoints.LEAGUES: LeaguesDownloader(),
    SportMonksEndpoints.TEAMS: TeamsDownloader(),
    SportMonksEndpoints.MATCHES: MatchesDownloader(),
    SportMonksEndpoints.COUNTRIES: CountriesDownloader(),
    SportMonksEndpoints.TYPES: SportMonksTypesDownloader(),
    SportMonksEndpoints.SEASONS: SeasonsDownloader(),
}
