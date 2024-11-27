import datetime as dt
from typing import List

import pandas as pd


def check_range(df: pd.DataFrame, column: str) -> AssertionError | None:
    assert (
        df[column].max() <= 100
    ), f"Column {column} in DataFrame {df.name} contains values greater than 100."
    assert (
        df[column].max() >= 0
    ), f"Column {column} in DataFrame {df.name} contains values less than 0."


def check_key(df: pd.DataFrame, column: str) -> AssertionError | None:
    assert len(df[column].unique()) == len(
        df[column]
    ), f"Primary key column {column} in {df.name} contains duplicate values."


def test_anime(
    dfs: List[pd.DataFrame],
    anime_info: pd.DataFrame,
    user_anime_score: pd.DataFrame,
    user_info: pd.DataFrame,
) -> None | AssertionError:
    anime_info.name = "anime_info"
    user_anime_score.name = "user_anime_score"
    user_info.name = "user_info"

    for df in dfs:
        assert not df.empty, f"{df.name} is empty."

    assert (
        len(anime_info.index) == len(user_anime_score.index)
    ), f"Row counts between anime_info and user_anime_score are not equal. anime_info: {len(anime_info.index)}, user_anime_score: {len(user_anime_score.index)}"

    check_range(df=anime_info, column="average_score")
    check_range(df=user_anime_score, column="user_score")

    check_key(df=anime_info, column="anime_id")
    check_key(df=user_info, column="user_id")
    check_key(df=user_anime_score, column="anime_id")

    assert user_info.loc[
        user_info["request_date"] >= dt.datetime.now()
    ].empty, "user_info['request_date'] contains dates from the future."

    for df in dfs:
        for col in df:
            assert bool(
                df[f"{col}"].notna().any()
            ), f"Column {col} in {df.name} contains NA values."


def test_manga(
    dfs: List[pd.DataFrame],
    manga_info: pd.DataFrame,
    user_info: pd.DataFrame,
    user_manga_score: pd.DataFrame,
) -> None | AssertionError:
    manga_info.name = "manga_info"
    user_manga_score.name = "user_manga_score"
    user_info.name = "user_info"

    for df in dfs:
        assert not df.empty, f"{df.name} is empty."

    assert len(manga_info.index) == len(
        user_manga_score.index
    ), "Row counts between manga_info and user_manga_score are not equal."

    check_range(df=manga_info, column="average_score")
    check_range(df=user_manga_score, column="user_score")

    check_key(df=manga_info, column="manga_id")
    check_key(df=user_info, column="user_id")
    check_key(df=user_manga_score, column="manga_id")

    assert user_info.loc[
        user_info["request_date"] >= dt.datetime.now()
    ].empty, "user_info['request_date'] contains dates from the future."

    for df in dfs:
        for col in df:
            assert bool(
                df[f"{col}"].notna().any()
            ), f"Column {col} in {df.name} contains NA values."


def test_anime_and_manga(
    dfs: List[pd.DataFrame],
    anime_info: pd.DataFrame,
    manga_info: pd.DataFrame,
    user_anime_score: pd.DataFrame,
    user_info: pd.DataFrame,
    user_manga_score: pd.DataFrame,
) -> None | AssertionError:
    anime_info.name = "anime_info"
    manga_info.name = "manga_info"
    user_anime_score.name = "user_anime_score"
    user_info.name = "user_info"
    user_manga_score.name = "user_manga_score"

    for df in dfs:
        assert not df.empty, f"{df.name} is empty."

    assert len(anime_info.index) == len(
        user_anime_score.index
    ), "Row counts between anime_info and user_anime_score are not equal."
    assert len(manga_info.index) == len(
        user_manga_score.index
    ), "Row counts between manga_info and user_manga_score are not equal."

    check_range(df=anime_info, column="average_score")
    check_range(df=user_anime_score, column="user_score")
    check_range(df=manga_info, column="average_score")
    check_range(df=user_manga_score, column="user_score")

    check_key(df=anime_info, column="anime_id")
    check_key(df=user_info, column="user_id")
    check_key(df=user_anime_score, column="anime_id")
    check_key(df=manga_info, column="manga_id")
    check_key(df=user_manga_score, column="manga_id")

    assert user_info.loc[
        user_info["request_date"] >= dt.datetime.now()
    ].empty, "user_info['request_date'] contains dates from the future."

    for df in dfs:
        for col in df:
            assert bool(
                df[f"{col}"].notna().any()
            ), f"Column {col} in {df.name} contains NA values."
