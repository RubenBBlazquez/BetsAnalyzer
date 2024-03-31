import pandas as pd


def transform_season_data(transformed_data: pd.DataFrame, seasons: pd.DataFrame):
    """
    Method to transform season data

    Parameters
    ----------
    transformed_data: pd.DataFrame
        clean data
    seasons: pd.DataFrame
        seasons data
    """
    # we create an aux index to be able to get the teams by seasons
    # so if we have 2 seasons, we will have 2 rows for each team
    transformed_data.loc[:, "aux_index"] = 1
    seasons_ = seasons.copy(deep=True)
    seasons_.loc[:, "aux_index"] = 1

    transformed_data = transformed_data.merge(
        seasons_[["aux_index", "season", "season_id"]], on="aux_index"
    )
    transformed_data.drop(columns="aux_index", inplace=True)

    return transformed_data
