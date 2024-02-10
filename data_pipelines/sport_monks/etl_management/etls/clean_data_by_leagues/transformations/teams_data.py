import pandas as pd


def transform_team_data(transformed_data: pd.DataFrame, teams: pd.DataFrame):
    """
    Method to transform team data

    Parameters
    ----------
    transformed_data: pd.DataFrame
        transformed data
    teams: pd.DataFrame
        teams data
    """
    teams.rename(columns={"id": "team_id"}, inplace=True)

    transformed_data["team"] = teams["name"]
    transformed_data["team_id"] = teams["team_id"]

    return transformed_data
