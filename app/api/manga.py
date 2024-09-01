import asyncio
import os
from datetime import datetime as dt

import pandas as pd
import requests
from api.funcs import fetch_anilist_data, fetch_anilist_data_async, load_query
from api.plots import plot_genres, plot_main
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# from app.api.funcs import (  # Local testing
#     fetch_anilist_data,
#     fetch_anilist_data_async,
#     load_query,
# )
# from app.api.plots import plot_genres, plot_main  # Local testing


def fetch_manga(username: str):

    # Local testing
    # username = "ZNote"

    # NOTE: Fetch user ID
    query_get_id = load_query("get_id.gql")
    variables_get_id = {"name": username}
    json_response = None
    response_header = None
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

    # NOTE: Fetch user scores
    query_user = load_query("manga_user.gql")

    variables_user = {"page": 1, "id": anilist_id}
    try:
        json_response, response_header = fetch_anilist_data(query_user, variables_user)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            raise ValueError(
                "Oops! AniList is a bit overloaded at the moment, please try again later."
            )

    if response_header is None:
        raise ValueError(f"Failed to fetch data for {username}.")

    user_score = pd.json_normalize(
        json_response,
        record_path=["data", "Page", "users", "statistics", "manga", "scores"],
        meta=[["data", "Page", "users", "id"]],
    )
    user_score = user_score.explode("mediaIds", ignore_index=True)
    user_score["mediaIds"] = user_score["mediaIds"].astype(int)
    user_score.rename(
        columns={
            "mediaIds": "manga_id",
            "data.Page.users.id": "user_id",
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
    user_info.drop("statistics.manga.scores", axis=1, inplace=True)

    user_info = pd.concat([user_info, response_header], axis=1)
    user_info.rename(
        columns={0: "request_date", "id": "user_id", "name": "user_name"},
        inplace=True,
    )
    user_info["request_date"] = pd.to_datetime(
        user_info["request_date"], format="%a, %d %b %Y %H:%M:%S %Z"
    ).dt.tz_localize(None)

    # NOTE: Get manga info
    async def main():
        manga_info = pd.DataFrame()

        id_list = user_score["manga_id"].values.tolist()
        variables_manga = {"page": 1, "id_in": id_list}
        query_manga = load_query("media.gql")
        response_ids = None

        while True:
            try:
                response_ids = await fetch_anilist_data_async(
                    query_manga, variables_manga
                )
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    raise ValueError(
                        "Oops! AniList is a bit overloaded at the moment, please try again later."
                    )

            if response_ids == None:
                raise ValueError("Failed to fetch data for {username}.")

            page_df = pd.json_normalize(
                response_ids, record_path=["data", "Page", "media"]
            )
            manga_info = pd.concat([manga_info, page_df], ignore_index=True)

            if not response_ids["data"]["Page"]["pageInfo"]["hasNextPage"]:
                break

            variables_manga["page"] += 1

        return manga_info

    manga_info = asyncio.run(main())

    manga_info.rename(
        columns={
            "averageScore": "average_score",
            "title.romaji": "title_romaji",
            "id": "manga_id",
        },
        inplace=True,
    )

    null_ids = list(manga_info.loc[manga_info.isna().any(axis=1)]["manga_id"])
    if len(null_ids) > 0:
        manga_info.dropna(axis=0, inplace=True)
        user_score = user_score[~user_score["manga_id"].isin(null_ids)]
    manga_info = manga_info.astype({"average_score": int})

    merged_dfs = user_score.merge(manga_info, on="manga_id", how="left")

    # NOTE: Plots (main/scores)
    plt_div_main = plot_main(merged_dfs=merged_dfs, username=username)

    # NOTE: Genre insights
    genres = merged_dfs.explode(column="genres", ignore_index=False)
    averages = genres.groupby(by="genres", as_index=False).agg(
        {
            "average_score": "mean",
            "user_score": "mean",
        }
    )
    count = genres["genres"].value_counts(sort=False)
    genre_insights = averages.merge(count, on="genres", how="left")

    def bayesian_average(
        weight: pd.Series | float | int,
        default: pd.Series | float | int,
        count: pd.Series | pd.DataFrame,
        score: pd.Series | pd.DataFrame,
    ) -> pd.Series | float:
        weighted_rating = (weight * default + count * score) / (weight + count)
        return weighted_rating

    genre_insights["weighted_average"] = bayesian_average(
        weight=genre_insights["count"].mean(),
        default=genre_insights["average_score"].mean(),
        count=genre_insights["count"],
        score=genre_insights["average_score"],
    )

    genre_insights["weighted_user"] = bayesian_average(
        weight=genre_insights["count"].mean(),
        default=genre_insights["user_score"].mean(),
        count=genre_insights["count"],
        score=genre_insights["user_score"],
    )

    genre_insights["weighted_diff"] = (
        genre_insights["weighted_user"] - genre_insights["weighted_average"]
    )
    genre_insights = genre_insights.sort_values(by="weighted_diff", ascending=False)

    max_genre_df = genre_insights.loc[
        genre_insights["weighted_diff"].abs()
        == max(genre_insights["weighted_diff"].abs())
    ]
    genre_max = round(float(max_genre_df["weighted_diff"].iloc[0]), 2)
    genre_max_name = str(max_genre_df["genres"].iloc[0])

    if genre_max > 0:
        genre_fav = genres.loc[genres["genres"] == genre_max_name]
        genre_fav = genre_fav.loc[
            genre_fav["user_score"] == genre_fav["user_score"].max()
        ]
        genre_fav["score_diff"] = genre_fav["user_score"] - genre_fav["average_score"]
        genre_fav = genre_fav.sort_values(by="score_diff", ascending=False)
        genre_fav_title = genre_fav["title_romaji"].iloc[0]
        genre_fav_u_score = int(genre_fav["user_score"].iloc[0])
        genre_fav_avg_score = int(genre_fav["average_score"].iloc[0])
    else:
        genre_fav = genres.loc[genres["genres"] == genre_max_name]
        genre_fav = genre_fav.loc[
            genre_fav["user_score"] == genre_fav["user_score"].min()
        ]
        genre_fav["score_diff"] = genre_fav["user_score"] - genre_fav["average_score"]
        genre_fav = genre_fav.sort_values(by="score_diff", ascending=True)
        genre_fav_title = genre_fav["title_romaji"].iloc[0]
        genre_fav_u_score = int(genre_fav["user_score"].iloc[0])
        genre_fav_avg_score = int(genre_fav["average_score"].iloc[0])

    plt_div_genres = plot_genres(genre_insights=genre_insights, username=username)

    # NOTE: Scores
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

    image_id_1 = int(max_diff["manga_id"].iloc[0])
    image_id_2 = int(min_diff["manga_id"].iloc[0])
    image_id_3 = int(genre_fav["manga_id"].iloc[0])
    query_image = load_query("image.gql")
    variables_image_1 = {"id": image_id_1}
    variables_image_2 = {"id": image_id_2}
    variables_image_3 = {"id": image_id_3}
    cover_image_1, response_header = fetch_anilist_data(query_image, variables_image_1)
    cover_image_2, response_header = fetch_anilist_data(query_image, variables_image_2)
    cover_image_3, response_header = fetch_anilist_data(query_image, variables_image_3)
    cover_image_1 = cover_image_1["data"]["Media"]["coverImage"]["extraLarge"]
    cover_image_2 = cover_image_2["data"]["Media"]["coverImage"]["extraLarge"]
    cover_image_3 = cover_image_3["data"]["Media"]["coverImage"]["extraLarge"]

    score_table = merged_dfs.loc[:, "title_romaji":"score_diff"]
    score_table["abs_score_diff"] = abs(score_table.loc[:, "score_diff"])
    score_table = score_table.sort_values(by="abs_score_diff", ascending=False)
    score_table = score_table.reset_index(drop=True)
    score_table = score_table.drop(labels="abs_score_diff", axis=1)

    score_table_html = """
    <thead>
        <tr>
            <th>Title</th>
            <th>Score Difference</th>
        </tr>
    </thead>
    <tbody>"""

    for index, row in score_table.iterrows():
        score_table_html += f"""<tr>
            <td class="text-primary">{row['title_romaji']}</td>
            <td class="text-secondary">{row['score_diff']}</td>
        </tr>"""

    score_table_html += """</tbody>"""

    # NOTE: Return
    insights = {
        "image1": cover_image_1,
        "image2": cover_image_2,
        "image3": cover_image_3,
        "u_score_max": score_max,
        "u_score_min": score_min,
        "avg_score_max": avg_max,
        "avg_score_min": avg_min,
        "title_max": title_max,
        "title_min": title_min,
        "avg_score_diff": avg_score_diff,
        "true_score_diff": true_score_diff,
        "plot_main": plt_div_main,
        "plot_genres": plt_div_genres,
        "genre_max": genre_max,
        "genre_max_name": genre_max_name,
        "genre_fav_title": genre_fav_title,
        "genre_fav_u_score": genre_fav_u_score,
        "genre_fav_avg_score": genre_fav_avg_score,
        "score_table": score_table_html,
    }

    dfs = [manga_info, user_info, user_score]

    # NOTE: Data upload
    load_dotenv()
    storage_connection_string = os.environ["STORAGE_CONNECTION_STRING"]
    blob_service_client = BlobServiceClient.from_connection_string(
        storage_connection_string
    )
    container_id = "projectanilist"

    names = ["manga_info", "user_info", "user_manga_score"]
    date = dt.today().strftime("%Y-%m-%d")
    for i, df in enumerate(dfs):
        name = names[i]
        file_path = os.path.join("./app/api/", f"{name}.csv")
        df.to_csv(path_or_buf=file_path)

        blob_path = f"data/{date}/{anilist_id}/{name}.csv"
        blob_object = blob_service_client.get_blob_client(
            container=container_id, blob=blob_path
        )

        with open(file_path, mode="rb") as csv:
            blob_object.upload_blob(csv, overwrite=True)
            os.remove(file_path)

    return dfs, anilist_id, insights
