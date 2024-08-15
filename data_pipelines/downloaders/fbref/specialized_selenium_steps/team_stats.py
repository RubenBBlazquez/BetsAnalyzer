import logging

import pandas as pd
from attrs import define
from bs4 import BeautifulSoup
from common.selenium.common_steps import GoToStep
from common.selenium.selenium_client import (
    DownloaderSeleniumStep,
    SeleniumStep,
    SeleniumStepsGenerator,
)
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


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
                    GoToStep(
                        url=f"https://fbref.com/en/comps/12/{season}/{season}-La-Liga-Stats",
                    ),
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

        for index in range(0, n_teams):
            soup = BeautifulSoup(all_team_stats_rows.get_attribute("outerHTML"), "html.parser")
            soup = soup.find("tr", {"data-row": index})

            finish_position = soup.find("th", {"data-stat": "rank"}).text
            finish_position = int(finish_position) if finish_position else None
            top_player_name = soup.select_one("td[data-stat='top_team_scorers'] > a").text
            top_player_name = top_player_name if top_player_name else None
            top_player_score = soup.select_one("td[data-stat='top_team_scorers'] > span").text
            top_player_score = int(top_player_score) if top_player_score else None

            home_away_team_stats_rows = driver.find_element(
                By.ID, f"results{self.season}121_home_away"
            )
            soup = BeautifulSoup(
                home_away_team_stats_rows.get_attribute("outerHTML"), "html.parser"
            )
            soup = soup.find("tr", {"data-row": index})

            team_name = soup.select_one("td[data-stat='team'] > a").text
            home_games = soup.find("td", {"data-stat": "home_games"}).text
            home_games = int(home_games) if home_games else None
            home_wins = soup.find("td", {"data-stat": "home_wins"}).text
            home_wins = int(home_wins) if home_wins else None
            home_draws = soup.find("td", {"data-stat": "home_ties"}).text
            home_draws = int(home_draws) if home_draws else None
            home_losses = soup.find("td", {"data-stat": "home_losses"}).text
            home_losses = int(home_losses) if home_losses else None
            home_goals_for = soup.find("td", {"data-stat": "home_goals_for"}).text
            home_goals_for = int(home_goals_for) if home_goals_for else None
            home_goals_against = soup.find("td", {"data-stat": "home_goals_against"}).text
            home_goals_against = int(home_goals_against) if home_goals_against else None
            home_goals_diff = soup.find("td", {"data-stat": "home_goal_diff"}).text
            home_goals_diff = int(home_goals_diff) if home_goals_diff else None
            home_points = soup.find("td", {"data-stat": "home_points"}).text
            home_points = int(home_points) if home_points else None
            home_points_avg = soup.find("td", {"data-stat": "home_points_avg"}).text
            home_points_avg = float(home_points_avg) if home_points_avg else None
            away_games = soup.find("td", {"data-stat": "away_games"}).text
            away_games = int(away_games) if away_games else None
            away_wins = soup.find("td", {"data-stat": "away_wins"}).text
            away_wins = int(away_wins) if away_wins else None
            away_draws = soup.find("td", {"data-stat": "away_ties"}).text
            away_draws = int(away_draws) if away_draws else None
            away_losses = soup.find("td", {"data-stat": "away_losses"}).text
            away_losses = int(away_losses) if away_losses else None
            away_goals_for = soup.find("td", {"data-stat": "away_goals_for"}).text
            away_goals_for = int(away_goals_for) if away_goals_for else None
            away_goals_against = soup.find("td", {"data-stat": "away_goals_against"}).text
            away_goals_against = int(away_goals_against) if away_goals_against else None
            away_goals_diff = soup.find("td", {"data-stat": "away_goal_diff"}).text
            away_goals_diff = int(away_goals_diff) if away_goals_diff else None
            away_points = soup.find("td", {"data-stat": "away_points"}).text
            away_points = int(away_points) if away_points else None
            away_points_avg = soup.find("td", {"data-stat": "away_points_avg"}).text
            away_points_avg = float(away_points_avg) if away_points_avg else None

            general_team_stats_rows = driver.find_element(By.ID, f"stats_squads_standard_for")
            soup = BeautifulSoup(general_team_stats_rows.get_attribute("outerHTML"), "html.parser")
            soup = soup.find("tr", {"data-row": index})

            n_players_used = soup.find("td", {"data-stat": "players_used"}).text
            n_players_used = int(n_players_used) if n_players_used else None
            avg_age = soup.find("td", {"data-stat": "avg_age"}).text
            avg_age = float(avg_age) if avg_age else None
            goals = soup.find("td", {"data-stat": "goals"}).text
            goals = int(goals) if goals else None
            assists = soup.find("td", {"data-stat": "assists"}).text
            assists = int(assists) if assists else None
            goals_plus_assists = soup.find("td", {"data-stat": "goals_assists"}).text
            goals_plus_assists = int(goals_plus_assists) if goals_plus_assists else None
            yellow_cards = soup.find("td", {"data-stat": "cards_yellow"}).text
            yellow_cards = int(yellow_cards) if yellow_cards else None
            red_cards = soup.find("td", {"data-stat": "cards_red"}).text
            red_cards = int(red_cards) if red_cards else None
            goals_per_90 = soup.find("td", {"data-stat": "goals_per90"}).text
            goals_per_90 = float(goals_per_90) if goals_per_90 else None
            assists_per_90 = soup.find("td", {"data-stat": "assists_per90"}).text
            assists_per_90 = float(assists_per_90) if assists_per_90 else None
            goal_assists_per_90 = soup.find("td", {"data-stat": "goals_assists_per90"}).text
            goal_assists_per_90 = float(goal_assists_per_90) if goal_assists_per_90 else None

            team_shots_stats_rows = driver.find_element(By.ID, f"stats_squads_shooting_for")
            soup = BeautifulSoup(team_shots_stats_rows.get_attribute("outerHTML"), "html.parser")
            soup = soup.find("tr", {"data-row": index})

            shots_on_target_pct = soup.find("td", {"data-stat": "shots_on_target_pct"}).text
            shots_on_target_pct = float(shots_on_target_pct) / 100 if shots_on_target_pct else None
            shots_total = soup.find("td", {"data-stat": "shots"}).text
            shots_total = int(shots_total) if shots_total else None
            shots_on_target = soup.find("td", {"data-stat": "shots_on_target"}).text
            shots_on_target = int(shots_on_target) if shots_on_target else None

            try:
                team_passing_stats_rows = driver.find_element(By.ID, f"stats_squads_passing_for")
                soup = BeautifulSoup(
                    team_passing_stats_rows.get_attribute("outerHTML"), "html.parser"
                )

                passing_completion_pct = soup.find("td", {"data-stat": "passes_pct"}).text
                passing_completion_pct = (
                    float(passing_completion_pct) / 100 if passing_completion_pct else None
                )
                passed_completed = soup.find("td", {"data-stat": "passes_completed"}).text
                passed_completed = int(passed_completed) if passed_completed else None
                passes_attempted = soup.find("td", {"data-stat": "passes"}).text
                passes_attempted = int(passes_attempted) if passes_attempted else None
            except NoSuchElementException:
                passing_completion_pct = None
                passed_completed = None
                passes_attempted = None

            team_fouls_stats_rows = driver.find_element(By.ID, f"stats_squads_misc_for")
            soup = BeautifulSoup(team_fouls_stats_rows.get_attribute("outerHTML"), "html.parser")
            soup = soup.find("tr", {"data-row": index})

            fouls = soup.find("td", {"data-stat": "fouls"}).text
            fouls = int(fouls) if fouls else None
            fouled = soup.find("td", {"data-stat": "fouled"}).text
            fouled = int(fouled) if fouled else None
            offsides = soup.find("td", {"data-stat": "offsides"}).text
            offsides = int(offsides) if offsides else None
            crosses = soup.find("td", {"data-stat": "crosses"}).text
            crosses = int(crosses) if crosses else None
            tackles_won = soup.find("td", {"data-stat": "tackles_won"}).text
            tackles_won = int(tackles_won) if tackles_won else None
            interceptions = soup.find("td", {"data-stat": "interceptions"}).text
            interceptions = int(interceptions) if interceptions else None
            own_goals = soup.find("td", {"data-stat": "own_goals"}).text
            own_goals = int(own_goals) if own_goals else None
            ball_recoveries = soup.find("td", {"data-stat": "ball_recoveries"})
            ball_recoveries = int(ball_recoveries.text) if ball_recoveries else None
            aerials_won = soup.find("td", {"data-stat": "aerials_won"})
            aerials_won = int(aerials_won.text) if aerials_won else None
            aerials_lost = soup.find("td", {"data-stat": "aerials_lost"})
            aerials_lost = int(aerials_lost.text) if aerials_lost else None
            aerials_won_pct = soup.find("td", {"data-stat": "aerials_won_pct"})
            aerials_won_pct = float(aerials_won_pct.text) / 100 if aerials_won_pct else None
            second_yellow_cards = soup.find("td", {"data-stat": "cards_yellow_red"}).text
            second_yellow_cards = int(second_yellow_cards) if second_yellow_cards else None

            goal_keeper_stats_rows = driver.find_element(By.ID, f"stats_squads_keeper_for")
            soup = BeautifulSoup(goal_keeper_stats_rows.get_attribute("outerHTML"), "html.parser")
            soup = soup.find("tr", {"data-row": index})

            goal_keeper_saves_pct = soup.find("td", {"data-stat": "gk_save_pct"}).text
            goal_keeper_saves_pct = (
                float(goal_keeper_saves_pct) / 100 if goal_keeper_saves_pct else None
            )
            goal_keeper_clean_sheets_pct = soup.find(
                "td", {"data-stat": "gk_clean_sheets_pct"}
            ).text
            goal_keeper_clean_sheets_pct = (
                float(goal_keeper_clean_sheets_pct) / 100 if goal_keeper_clean_sheets_pct else None
            )
            penalty_kick_saves_pct = soup.find("td", {"data-stat": "gk_pens_save_pct"}).text
            penalty_kick_saves_pct = (
                float(penalty_kick_saves_pct) / 100 if penalty_kick_saves_pct else None
            )

            result.append(
                pd.DataFrame(
                    [
                        {
                            "season": self.season,
                            "home_games": home_games,
                            "home_wins": home_wins,
                            "home_draws": home_draws,
                            "home_losses": home_losses,
                            "home_goals_for": home_goals_for,
                            "home_goals_against": home_goals_against,
                            "home_goals_diff": home_goals_diff,
                            "home_points": home_points,
                            "home_points_avg": home_points_avg,
                            "team_name": team_name,
                            "away_games": away_games,
                            "away_wins": away_wins,
                            "away_draws": away_draws,
                            "away_losses": away_losses,
                            "away_goals_for": away_goals_for,
                            "away_goals_against": away_goals_against,
                            "away_goals_diff": away_goals_diff,
                            "away_points": away_points,
                            "away_points_avg": away_points_avg,
                            "finish_position": finish_position,
                            "top_player_name": top_player_name,
                            "top_player_score": top_player_score,
                            "n_players_used": n_players_used,
                            "avg_age": avg_age,
                            "goals": goals,
                            "assists": assists,
                            "goals_plus_assists": goals_plus_assists,
                            "yellow_cards": yellow_cards,
                            "red_cards": red_cards,
                            "goals_per_90": goals_per_90,
                            "assists_per_90": assists_per_90,
                            "goal_assists_per_90": goal_assists_per_90,
                            "shots_on_target_pct": shots_on_target_pct,
                            "shots_total": shots_total,
                            "shots_on_target": shots_on_target,
                            "passing_completion_pct": passing_completion_pct,
                            "passed_completed": passed_completed,
                            "passes_attempted": passes_attempted,
                            "fouls": fouls,
                            "fouled": fouled,
                            "offsides": offsides,
                            "crosses": crosses,
                            "tackles_won": tackles_won,
                            "interceptions": interceptions,
                            "own_goals": own_goals,
                            "ball_recoveries": ball_recoveries,
                            "aerials_won": aerials_won,
                            "aerials_lost": aerials_lost,
                            "aerials_won_pct": aerials_won_pct,
                            "second_yellow_cards": second_yellow_cards,
                            "goal_keeper_saves_pct": goal_keeper_saves_pct,
                            "goal_keeper_clean_sheets_pct": goal_keeper_clean_sheets_pct,
                            "penalty_kick_saves_pct": penalty_kick_saves_pct,
                        }
                    ],
                )
            )

        return pd.concat(result, ignore_index=True)
