import logging
from dataclasses import dataclass

import pandas as pd
from attrs import define
from bs4 import BeautifulSoup
from common.selenium.common_steps import GoToStep
from common.selenium.selenium_client import (
    DownloaderSeleniumStep,
    SeleniumStep,
    SeleniumStepsGenerator,
)
from common.selenium.utils import get_stat
from selenium import webdriver
from selenium.webdriver.common.by import By


@dataclass
class TeamStats:
    season: str
    team_name: str
    home_games: int
    home_wins: int
    home_draws: int
    home_losses: int
    home_goals_for: int
    home_goals_against: int
    home_goals_diff: int
    home_points: int
    home_points_avg: float
    away_games: int
    away_wins: int
    away_draws: int
    away_losses: int
    away_goals_for: int
    away_goals_against: int
    away_goals_diff: int
    away_points: int
    away_points_avg: float
    finish_position: int
    top_player_name: str
    top_player_score: int
    n_players_used: int
    avg_age: float
    goals: int
    assists: int
    goals_plus_assists: int
    yellow_cards: int
    red_cards: int
    goals_per_90: float
    assists_per_90: float
    goal_assists_per_90: float
    shots_on_target_pct: float
    shots_total: int
    shots_on_target: int
    passing_completion_pct: float
    passed_completed: int
    passes_attempted: int
    fouls: int
    fouled: int
    offsides: int
    crosses: int
    tackles_won: int
    interceptions: int
    own_goals: int
    ball_recoveries: int
    aerials_won: int
    aerials_lost: int
    aerials_won_pct: float
    second_yellow_cards: int
    goal_keeper_saves_pct: float
    goal_keeper_clean_sheets_pct: float
    penalty_kick_saves_pct: float

    @classmethod
    def create_from_downloaded_hit(cls, **columns):
        columns = {
            column: columns.get(column, None)
            for column in cls.__annotations__.keys()
        }

        return cls(**columns)



class TeamStatsDownloaderStepsGenerator(SeleniumStepsGenerator):
    """
    Class to generate the steps to download the team stats from the fbref page
    """

    seasons: list[str] = [
        "2000-2001",
        "2001-2002",
        "2002-2003",
        "2003-2004",
        "2004-2005",
        "2005-2006",
        "2006-2007",
        "2007-2008",
        "2008-2009",
        "2009-2010",
        "2010-2011",
        "2011-2012",
        "2012-2013",
        "2013-2014",
        "2014-2015",
        "2015-2016",
        "2016-2017",
        "2017-2018",
        "2018-2019",
        "2019-2020",
        "2020-2021",
        "2021-2022",
        "2022-2023",
        "2023-2024",
    ]

    def generate_steps(self) -> list[SeleniumStep]:
        steps = []
        for season in self.seasons:
            steps.extend(
                [
                    GoToStep(url=f"https://fbref.com/en/comps/12/{season}/{season}-La-Liga-Stats"),
                    DownloadSeasonTeamStatsStep(season),
                ]
            )
        return steps


@define(auto_attribs=True)
class DownloadSeasonTeamStatsStep(DownloaderSeleniumStep):
    """
    Step to download the team stats from the fbref page

    Attributes:
    -----------
    season: str
    """

    season: str

    def execute(self, driver: webdriver.Remote) -> pd.DataFrame:
        logging.info(f"Downloading team stats for season {self.season}")
        result = []

        all_team_stats_rows = driver.find_element(By.ID, f"results{self.season}121_overall")
        soup = BeautifulSoup(all_team_stats_rows.get_attribute("outerHTML"), "html.parser")
        n_teams = len(soup.select("[data-row]"))

        for index in range(n_teams):
            team_stats = self.extract_team_stats(soup, driver, index)
            result.append(pd.DataFrame([team_stats.__dict__]))

        return pd.concat(result, ignore_index=True)

    def extract_team_stats(self, soup, driver, index) -> TeamStats:
        """
        Extracts team stats from the soup object and returns a TeamStats instance.
        """
        team_row = soup.find("tr", {"data-row": index})

        finish_position = get_stat(team_row, "rank", int)
        top_player_name = get_stat(team_row, "top_team_scorers", str, True)
        top_player_score = get_stat(team_row, "top_team_scorers", int, True)

        home_away_team_stats_rows = driver.find_element(By.ID, f"results{self.season}121_home_away")
        home_away_soup = BeautifulSoup(
            home_away_team_stats_rows.get_attribute("outerHTML"), "html.parser"
        )
        home_away_row = home_away_soup.find("tr", {"data-row": index})

        team_name = get_stat(home_away_row, "team", str, True)
        home_stats = self.extract_home_away_stats(home_away_row)

        general_team_stats_rows = driver.find_element(By.ID, f"stats_squads_standard_for")
        general_soup = BeautifulSoup(
            general_team_stats_rows.get_attribute("outerHTML"), "html.parser"
        )
        general_row = general_soup.find("tr", {"data-row": index})

        general_stats = self.extract_general_stats(general_row)

        team_stats = TeamStats.create_from_downloaded_hit(
            season=self.season,
            team_name=team_name,
            finish_position=finish_position,
            top_player_name=top_player_name,
            top_player_score=top_player_score,
            **home_stats,
            **general_stats,
        )

        return team_stats

    def extract_home_away_stats(self, row) -> dict:
        """
        Extracts home and away stats from the row and returns them as a dictionary.
        """
        return {
            "home_games": get_stat(row, "home_games", int),
            "home_wins": get_stat(row, "home_wins", int),
            "home_draws": get_stat(row, "home_ties", int),
            "home_losses": get_stat(row, "home_losses", int),
            "home_goals_for": get_stat(row, "home_goals_for", int),
            "home_goals_against": get_stat(row, "home_goals_against", int),
            "home_goals_diff": get_stat(row, "home_goal_diff", int),
            "home_points": get_stat(row, "home_points", int),
            "home_points_avg": get_stat(row, "home_points_avg", float),
            "away_games": get_stat(row, "away_games", int),
            "away_wins": get_stat(row, "away_wins", int),
            "away_draws": get_stat(row, "away_ties", int),
            "away_losses": get_stat(row, "away_losses", int),
            "away_goals_for": get_stat(row, "away_goals_for", int),
            "away_goals_against": get_stat(row, "away_goals_against", int),
            "away_goals_diff": get_stat(row, "away_goal_diff", int),
            "away_points": get_stat(row, "away_points", int),
            "away_points_avg": get_stat(row, "away_points_avg", float),
        }

    def extract_general_stats(self, row) -> dict:
        """
        Extracts general stats from the row and returns them as a dictionary.
        """
        return {
            "n_players_used": get_stat(row, "players_used", int),
            "avg_age": get_stat(row, "avg_age", float),
            "goals": get_stat(row, "goals", int),
            "assists": get_stat(row, "assists", int),
            "goals_plus_assists": get_stat(row, "goals_assists", int),
            "yellow_cards": get_stat(row, "cards_yellow", int),
            "red_cards": get_stat(row, "cards_red", int),
            "goals_per_90": get_stat(row, "goals_per90", float),
            "assists_per_90": get_stat(row, "assists_per90", float),
            "goal_assists_per_90": get_stat(row, "goals_assists_per90", float),
            "shots_on_target_pct": get_stat(row, "shots_on_target_pct", float) / 100,
            "shots_total": get_stat(row, "shots", int),
            "shots_on_target": get_stat(row, "shots_on_target", int),
        }
