import asyncio
from typing import List

import pandas as pd
import requests
from api.funcs import fetch_anilist_data, fetch_anilist_data_async, load_query


def get_id(username: str) -> int:
    query_get_id = load_query("get_id.gql")
    variables_get_id = {"name": username}
    json_response = None
    try:
        json_response, response_header = fetch_anilist_data(
            query_get_id, variables_get_id
        )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Username {username} not found.")
        if e.response.status_code == 429:
            raise ValueError(
                "Oops! AniList is a bit overloaded at the moment, please try again later."
            )

    if json_response is None:
        raise ValueError(f"Failed to fetch data for {username}.")

    anilist_id = json_response["data"]["User"]["id"]

    return anilist_id


def get_user_data(
    username: str, anilist_id: int
) -> tuple[pd.DataFrame, pd.DataFrame, List[int]]:
    json_response = None
    response_header = None
    query_user = load_query("anime_user.gql")

    variables_user = {"page": 1, "id": anilist_id}
    try:
        json_response, response_header = fetch_anilist_data(query_user, variables_user)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            raise ValueError(
                "Oops! AniList is a bit overloaded at the moment, please try again later."
            )

    if json_response is None or response_header is None:
        raise ValueError(f"Failed to fetch data for {username}.")

    user_score = pd.json_normalize(
        json_response,
        record_path=["data", "Page", "users", "statistics", "anime", "scores"],
        meta=[["data", "Page", "users", "id"]],
    )

    if user_score.empty:
        raise ValueError(f"AniList returned no anime for {username}.")

    user_score = user_score.explode("mediaIds", ignore_index=True)
    user_score["mediaIds"] = user_score["mediaIds"].astype(int)
    user_score.rename(
        columns={
            "mediaIds": "anime_id",
            "data.Page.users.id": "user_id",
            "id": "anime_id",
            "score": "user_score",
        },
        inplace=True,
    )

    if max(user_score["user_score"]) <= 10:
        user_score["user_score"] = user_score["user_score"].apply(lambda x: x * 10)
    else:
        pass

    # NOTE: Make user info table
    user_info = pd.json_normalize(json_response, record_path=["data", "Page", "users"])
    user_info.drop("statistics.anime.scores", axis=1, inplace=True)

    user_info = pd.concat([user_info, response_header], axis=1)
    user_info.rename(
        columns={0: "request_date", "id": "user_id", "name": "user_name"},
        inplace=True,
    )
    user_info["request_date"] = pd.to_datetime(
        user_info["request_date"], format="%a, %d %b %Y %H:%M:%S %Z"
    ).dt.tz_localize(None)

    id_list = user_score["anime_id"].values.tolist()
    return user_score, user_info, id_list


def get_anime_info(username: str, id_list: List[int]) -> pd.DataFrame:
    async def main():
        response_ids = None
        anime_info = pd.DataFrame()

        variables_anime = {"page": 1, "id_in": id_list}
        query_anime = load_query("media.gql")

        while True:
            try:
                response_ids = await fetch_anilist_data_async(
                    query_anime, variables_anime
                )
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    raise ValueError(
                        "Oops! AniList is a bit overloaded at the moment, please try again later."
                    )

            if response_ids == None:
                raise ValueError(f"Failed to fetch data for {username}.")

            page_df = pd.json_normalize(
                response_ids, record_path=["data", "Page", "media"]
            )
            anime_info = pd.concat([anime_info, page_df], ignore_index=True)

            if not response_ids["data"]["Page"]["pageInfo"]["hasNextPage"]:
                break

            variables_anime["page"] += 1

        return anime_info

    anime_info = asyncio.run(main())

    anime_info.rename(
        columns={
            "averageScore": "average_score",
            "title.romaji": "title_romaji",
            "id": "anime_id",
        },
        inplace=True,
    )

    return anime_info


def check_nulls(
    anime_info: pd.DataFrame, user_score: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    null_ids = list(anime_info.loc[anime_info.isna().any(axis=1)]["anime_id"])
    if len(null_ids) > 0:
        anime_info.dropna(axis=0, inplace=True)
        user_score = user_score[~user_score["anime_id"].isin(null_ids)]
    anime_info = anime_info.astype({"average_score": int})

    return anime_info, user_score
