import asyncio
import os
from datetime import datetime as dt

import aiohttp
import pandas as pd
import requests
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv


def fetch_data(username: str):
    # NOTE: Define functions

    def load_query(file_name: str) -> str:
        file_path = os.path.join("./app/api_request/gql/", file_name)
        with open(file_path, "r") as file:
            return file.read()

    url = "https://graphql.anilist.co"

    def fetch_anilist_data(query: str, variables: dict) -> tuple[dict, pd.Series]:
        response = requests.post(
            url, json={"query": query, "variables": variables}, timeout=10
        )
        response.raise_for_status()
        response_header = pd.Series(response.headers["Date"])
        return response.json(), response_header

    async def fetch_anilist_data_async(query: str, variables: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json={"query": query, "variables": variables}, timeout=10
            ) as response:
                response.raise_for_status()
                return await response.json()

    # NOTE: Fetch user ID

    query_get_id = load_query("get_id.gql")
    variables_get_id = {"name": username}
    json_response, response_header = fetch_anilist_data(query_get_id, variables_get_id)
    anilist_id = json_response["data"]["User"]["id"]

    # NOTE: Fetch user scores

    query_user = load_query("user_query.gql")
    variables_user = {"page": 1, "id": anilist_id}
    json_response, response_header = fetch_anilist_data(query_user, variables_user)

    user_score = pd.json_normalize(
        json_response,
        record_path=["data", "Page", "users", "statistics", "anime", "scores"],
        meta=[["data", "Page", "users", "id"]],
    )
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

    # NOTE: Get anime info

    async def main():
        anime_info = pd.DataFrame()

        id_list = user_score["anime_id"].values.tolist()
        variables_anime = {"page": 1, "id_in": id_list}
        query_anime = load_query("anime_query.gql")

        while True:
            response_ids = await fetch_anilist_data_async(query_anime, variables_anime)
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

    # NOTE: Get user insights

    merged_dfs = user_score.merge(anime_info, on="anime_id", how="left")
    merged_dfs["score_diff"] = merged_dfs["user_score"] - merged_dfs["average_score"]

    float_avg_score_diff = abs(merged_dfs.loc[:, "score_diff"]).mean()
    avg_score_diff = round(float_avg_score_diff, 2)
    float_true_score_diff = merged_dfs.loc[:, "score_diff"].mean()
    true_score_diff = round(float_true_score_diff, 2)

    max_diff = merged_dfs.loc[
        merged_dfs["score_diff"].abs() == max(merged_dfs["score_diff"].abs())
    ]
    min_diff = merged_dfs.loc[
        merged_dfs["score_diff"].abs() == min(merged_dfs["score_diff"].abs())
    ]

    score_max = int(max_diff["user_score"].iloc[0])
    score_min = int(min_diff["user_score"].iloc[0])
    avg_max = int(max_diff["average_score"].iloc[0])
    avg_min = int(min_diff["average_score"].iloc[0])
    title_max = max_diff["title_romaji"].iloc[0]
    title_min = min_diff["title_romaji"].iloc[0]

    image_id_1 = int(max_diff["anime_id"].iloc[0])
    image_id_2 = int(min_diff["anime_id"].iloc[0])
    query_image = load_query("image_query.gql")
    variables_image_1 = {"id": image_id_1}
    variables_image_2 = {"id": image_id_2}
    cover_image_1, response_header = fetch_anilist_data(query_image, variables_image_1)
    cover_image_2, response_header = fetch_anilist_data(query_image, variables_image_2)
    cover_image_1 = cover_image_1["data"]["Media"]["coverImage"]["extraLarge"]
    cover_image_2 = cover_image_2["data"]["Media"]["coverImage"]["extraLarge"]

    # NOTE: Upload data

    load_dotenv()
    storage_connection_string = os.environ["STORAGE_CONNECTION_STRING"]
    blob_service_client = BlobServiceClient.from_connection_string(
        storage_connection_string
    )
    container_id = "projectanilist"

    dfs = [anime_info, user_info, user_score]
    names = ["anime_info", "user_info", "user_score"]
    for i, df in enumerate(dfs):
        name = names[i]
        file_path = os.path.join("./app/api_request/temp/", f"{name}.csv")
        df.to_csv(path_or_buf=file_path)

        date = dt.today().strftime("%Y-%m-%d")
        blob_path = f"data/{date}/{anilist_id}/{name}.csv"
        blob_object = blob_service_client.get_blob_client(
            container=container_id, blob=blob_path
        )

        with open(file_path, mode="rb") as csv:
            blob_object.upload_blob(csv, overwrite=True)
            os.remove(file_path)

    # NOTE: Return

    insights = (
        avg_score_diff,
        true_score_diff,
        score_max,
        score_min,
        avg_max,
        avg_min,
        title_max,
        title_min,
    )

    return dfs, insights
