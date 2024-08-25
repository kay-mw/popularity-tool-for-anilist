import datetime as dt
from typing import List

import pandas as pd


def test_dataframes(
    dfs: List[pd.DataFrame],
    anime_info: pd.DataFrame,
    user_info: pd.DataFrame,
    user_score: pd.DataFrame,
) -> None | AssertionError:
    anime_info.name = "anime_info"
    user_info.name = "user_info"
    user_score.name = "user_score"
    for df in dfs:
        assert not df.empty, f"{df.name} is empty."

    assert len(anime_info.index) == len(
        user_score.index
    ), "Row counts between anime_info and user_score are not equal."

    def check_range(df: pd.DataFrame, column: str) -> None:
        assert (
            df[column].max() <= 100
        ), f"{df.name}[{column}] contains values greater than 100."
        assert (
            df[column].max() >= 0
        ), f"{df.name}[{column}] contains values less than 0."

    check_range(df=anime_info, column="average_score")
    check_range(df=user_score, column="user_score")

    def check_key(df: pd.DataFrame, column: str) -> None:
        assert len(df[column].unique()) == len(
            df[column]
        ), f"Primary key column {column} in {df.name} contains non-unique values."

    check_key(df=anime_info, column="anime_id")
    check_key(df=user_info, column="user_id")
    check_key(df=user_score, column="anime_id")

    assert user_info.loc[
        user_info["request_date"] >= dt.datetime.now()
    ].empty, "user_info['request_date'] contains invalid dates from the future."

    for df in dfs:
        for col in df:
            assert bool(
                df[f"{col}"].notna().any()
            ), f"Column {col} in {df.name} contains NA values."
