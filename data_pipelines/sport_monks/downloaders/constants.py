from sport_monks.downloaders.entities.country import Country
from sport_monks.downloaders.entities.league import League
from sport_monks.downloaders.entities.match import Match
from sport_monks.downloaders.entities.player import (
    EnglandPlayers,
    GermanyPlayers,
    Player,
    SpainPlayers,
)
from sport_monks.downloaders.entities.season import Season
from sport_monks.downloaders.entities.team import Team
from sport_monks.downloaders.entities.type import Type
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
    SportMonksEndpoints.PLAYERS: Player,
    SportMonksEndpoints.PLAYERS_ENGLAND: EnglandPlayers,
    SportMonksEndpoints.PLAYERS_GERMANY: GermanyPlayers,
    SportMonksEndpoints.PLAYERS_SPAIN: SpainPlayers,
    SportMonksEndpoints.LEAGUES: League,
    SportMonksEndpoints.TEAMS: Team,
    SportMonksEndpoints.MATCHES: Match,
    SportMonksEndpoints.COUNTRIES: Country,
    SportMonksEndpoints.TYPES: Type,
    SportMonksEndpoints.SEASONS: Season,
}
