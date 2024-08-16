import asyncio
import os
from datetime import datetime as dt

import pandas as pd
import plotly.graph_objects as go
import requests
from api.funcs import fetch_anilist_data, fetch_anilist_data_async, load_query
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from plotly.offline import plot

# from app.api.funcs import (  # Local testing
#     fetch_anilist_data,
#     fetch_anilist_data_async,
#     load_query,
# )


def fetch_data(username: str):

    # NOTE: Fetch user ID
    query_get_id = load_query("get_id.gql")
    # variables_get_id = {"name": username}
    variables_get_id = {"name": "keejan"}  # Local testing
    json_response = None
    try:
        json_response, response_header = fetch_anilist_data(
            query_get_id, variables_get_id
        )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Username {username} not found.")

    if json_response is None:
        raise ValueError(f"Failed to fetch data for {username}.")

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

    merged_dfs = user_score.merge(anime_info, on="anime_id", how="left")

    # NOTE: Plots (main/scores)
    def generate_plot_data(column: str, color: str, name: str):
        plot_df = merged_dfs.value_counts(column).reset_index().sort_values(by=column)
        return go.Scatter(
            x=plot_df[column],
            y=plot_df["count"],
            mode="lines+markers",
            name=name,
            line=dict(color=color),
            marker=dict(color=color),
        )

    user_score_trace = generate_plot_data("user_score", "#00bbbc", "Your Scores")
    average_score_trace = generate_plot_data(
        "average_score", "#00c79c", "AniList Average"
    )
    fig = go.Figure(data=[user_score_trace, average_score_trace])
    fig.update_layout(
        template="plotly_dark",
        title="",
        xaxis_title="Score",
        yaxis_title="Count",
        legend_title="",
        legend=dict(yanchor="top", y=1.03, xanchor="left", x=0.01),
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    plt_div_main = plot(
        fig,
        output_type="div",
        include_plotlyjs=False,
        show_link=False,
        link_text="",
    )

    # NOTE: Genre insights
    # TODO: Make legend part of plot so that it doesn't take up a bunch of width on website.
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
        genre_insights["weighted_diff"].abs() == max(genre_insights["weighted_diff"].abs())
    ]
    genre_max = round(float(max_genre_df["weighted_diff"].iloc[0]), 2)
    genre_max_name = str(max_genre_df["genres"].iloc[0])

    fig = go.Figure(
        data=[
            go.Bar(
                x=genre_insights["genres"],
                y=genre_insights["weighted_user"],
                marker=dict(color="#00bbbc"),
                name="Your Scores",
            ),
            go.Bar(
                x=genre_insights["genres"],
                y=genre_insights["weighted_average"],
                marker=dict(color="#00c79c"),
                name="AniList Average",
            ),
        ],
    )
    ymin = min(
        genre_insights["weighted_user"].min(), genre_insights["weighted_average"].min()
    )
    ymax = max(
        genre_insights["weighted_user"].max(), genre_insights["weighted_average"].max()
    )
    fig.update_yaxes(range=[ymin - 10, ymax + 5])
    fig.update_layout(
        template="plotly_dark",
        title="",
        xaxis_title="Genre",
        yaxis_title="Score",
        legend_title="",
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    plt_div_genres = plot(
        fig,
        output_type="div",
        include_plotlyjs=False,
        show_link=False,
        link_text="",
    )

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

    image_id_1 = int(max_diff["anime_id"].iloc[0])
    image_id_2 = int(min_diff["anime_id"].iloc[0])
    query_image = load_query("image_query.gql")
    variables_image_1 = {"id": image_id_1}
    variables_image_2 = {"id": image_id_2}
    cover_image_1, response_header = fetch_anilist_data(query_image, variables_image_1)
    cover_image_2, response_header = fetch_anilist_data(query_image, variables_image_2)
    cover_image_1 = cover_image_1["data"]["Media"]["coverImage"]["extraLarge"]
    cover_image_2 = cover_image_2["data"]["Media"]["coverImage"]["extraLarge"]

    # NOTE: Return
    insights = {
        "image1": cover_image_1,
        "image2": cover_image_2,
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
    }

    dfs = [anime_info, user_info, user_score]

    # NOTE: Data upload
    load_dotenv()
    storage_connection_string = os.environ["STORAGE_CONNECTION_STRING"]
    blob_service_client = BlobServiceClient.from_connection_string(
        storage_connection_string
    )
    container_id = "projectanilist"

    names = ["anime_info", "user_info", "user_score"]
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
