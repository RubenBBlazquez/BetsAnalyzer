import logging
from dataclasses import dataclass
import pandas as pd
from attrs import define
from bs4 import BeautifulSoup
from common.selenium.common_steps import GoToStep
from common.selenium.selenium_client import (
    DownloaderSeleniumStep,
    SeleniumStep,
    SeleniumStepsGenerator, NormalSeleniumStepException,
)
from common.selenium.utils import get_stat
from selenium import webdriver
from selenium.webdriver.common.by import By


@dataclass
class PlayerStats:
    season: str
    player_name: str
    team_name: str
    goals: int
    assists: int
    yellow_cards: int
    red_cards: int
    goals_per_90: float
    assists_per_90: float


class PlayerStatsDownloaderStepsGenerator(SeleniumStepsGenerator):
    """
    Class to generate the steps to download player stats from the fbref page
    """

    seasons: list[str] = [
        "2000-2001", "2001-2002", "2002-2003", "2003-2004", "2004-2005",
        "2005-2006", "2006-2007", "2007-2008", "2008-2009", "2009-2010",
        "2010-2011", "2011-2012", "2012-2013", "2013-2014", "2014-2015",
        "2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020",
        "2020-2021", "2021-2022", "2022-2023", "2023-2024",
    ]

    def generate_steps(self) -> list[SeleniumStep]:
        steps = []
        for season in self.seasons:
            steps.extend([
                GoToStep(url=f"https://fbref.com/en/comps/12/{season}/{season}-La-Liga-Stats"),
                DownloadSeasonPlayerStatsStep(season),
            ])
        return steps


@define(auto_attribs=True)
class DownloadSeasonPlayerStatsStep(DownloaderSeleniumStep):
    """
    Step to download player stats from the fbref page

    Attributes:
    -----------
    season: str
    """

    season: str

    def execute(self, driver: webdriver.Remote) -> pd.DataFrame:
        logging.info(f"Downloading player stats for season {self.season}")
        result = []

        try:
            all_player_stats_rows = driver.find_element(By.ID, f"results{self.season}121_overall")
        except Exception as e:
            raise NormalSeleniumStepException(f"Could not find any player stats for season {self.season}")

        soup = BeautifulSoup(all_player_stats_rows.get_attribute("outerHTML"), "html.parser")
        n_players = len(soup.select("[data-row]"))

        for index in range(n_players):
            player_stats = self.extract_player_stats(soup, driver, index)
            result.append(pd.DataFrame([player_stats.__dict__]))

        return pd.concat(result, ignore_index=True)

    def extract_player_stats(self, soup, driver, index) -> PlayerStats:
        """
        Extracts player stats from the soup object and returns a PlayerStats instance.
        """
        player_row = soup.find("tr", {"data-row": index})

        player_name = get_stat(player_row, "player", str, True)
        team_name = get_stat(player_row, "team", str, True)
        goals = get_stat(player_row, "goals", int)
        assists = get_stat(player_row, "assists", int)
        yellow_cards = get_stat(player_row, "cards_yellow", int)
        red_cards = get_stat(player_row, "cards_red", int)
        goals_per_90 = get_stat(player_row, "goals_per90", float)
        assists_per_90 = get_stat(player_row, "assists_per90", float)

        player_stats = PlayerStats(
            season=self.season,
            player_name=player_name,
            team_name=team_name,
            goals=goals,
            assists=assists,
            yellow_cards=yellow_cards,
            red_cards=red_cards,
            goals_per_90=goals_per_90,
            assists_per_90=assists_per_90,
        )

        return player_stats
