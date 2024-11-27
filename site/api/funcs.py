import os

import aiohttp
import pandas as pd
import requests


def load_query(file_name: str) -> str:
    file_path = os.path.join("./api/gql/", file_name)
    with open(file_path, "r") as file:
        return file.read()


def fetch_anilist_data(query: str, variables: dict) -> tuple[dict, pd.Series]:
    url = "https://graphql.anilist.co"
    response = requests.post(
        url, json={"query": query, "variables": variables}, timeout=10
    )
    response.raise_for_status()
    response_header = pd.Series(response.headers["Date"])
    return response.json(), response_header


async def fetch_anilist_data_async(query: str, variables: dict) -> dict:
    url = "https://graphql.anilist.co"
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        async with session.post(
            url,
            json={"query": query, "variables": variables},
        ) as response:
            return await response.json()


def round_scores(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if (df["user_score"] % 10 == 0).all():
        df["average_score"] = 10 * round(df["average_score"] / 10)
        all_scores = list(range(10, 101, 10))
        new_rows = pd.DataFrame(
            {
                "score": all_scores,
                "user_count": 0,
                "average_count": 0,
            }
        )
    else:
        df["average_score"] = 5 * round(df["average_score"] / 5)
        all_scores = list(range(10, 101, 5))
        new_rows = pd.DataFrame(
            {
                "score": all_scores,
                "user_count": 0,
                "average_count": 0,
            }
        )

    return df, new_rows


def create_plot_data(df: pd.DataFrame, fill_df: pd.DataFrame) -> list[dict]:
    user_count = df.value_counts("user_score").reset_index()
    average_count = df.value_counts("average_score").reset_index()

    user_count = user_count.rename(columns={"count": "user_count"})
    average_count = average_count.rename(columns={"count": "average_count"})

    average_count["average_score"] = average_count["average_score"].astype(int)

    plot_data = user_count.merge(
        right=average_count,
        how="outer",
        left_on="user_score",
        right_on="average_score",
    )

    plot_data["user_score"] = plot_data["user_score"].fillna(plot_data["average_score"])
    plot_data = plot_data.fillna(0.0).astype({"average_count": int})

    plot_data = plot_data.drop("average_score", axis=1).rename(
        columns={"user_score": "score"}
    )

    plot_data = pd.concat([plot_data, fill_df], ignore_index=True)
    plot_data = plot_data.drop_duplicates(subset=["score"], keep="first")

    plot_data = plot_data.sort_values(by="score", ascending=True).reset_index(drop=True)
    plot_json = plot_data.to_dict(orient="records")

    return plot_json


def create_table(df: pd.DataFrame) -> list[dict]:
    score_table = df[
        ["title_romaji", "score_diff", "user_score", "average_score"]
    ].copy()
    score_table["abs_score_diff"] = abs(score_table.loc[:, "score_diff"])
    score_table["average_score"] = score_table["average_score"].astype(int)
    score_table = score_table.sort_values(by="abs_score_diff", ascending=False)
    score_table = score_table.reset_index(drop=True)
    score_table = score_table.drop(labels="abs_score_diff", axis=1)
    table_dict = score_table.to_dict(orient="records")

    return table_dict


def create_genre_data(genre_df: pd.DataFrame) -> list[dict]:
    genre_df = (
        genre_df.round({"weighted_average": 1, "weighted_user": 1, "weighted_diff": 2})
        .reset_index(drop=True)
        .drop(
            labels=["average_score", "user_score", "count"],
            axis=1,
        )
        .sort_values("weighted_diff", ascending=False, key=abs)
    )
    genre_dict = genre_df.to_dict(orient="records")

    return genre_dict
