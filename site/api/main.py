import os
from typing import Literal
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from scipy.stats import percentileofscore
from sqlalchemy import create_engine

from api.insights import general_insights, genre_insights
from api.processing import (
    check_nulls,
    create_genre_data,
    create_plot_data,
    create_table,
    get_format_info,
    get_id,
    get_user_data,
    round_scores,
)
from api.upload import blob_upload


def fetch_data(username: str, format: Literal["anime", "manga"]):
    # Local testing
    # username = "keejan"
    # format = "anime"

    # NOTE: Processing
    anilist_id = get_id(username=username)
    user_score, user_info, id_list = get_user_data(
        username=username,
        anilist_id=anilist_id,
        format=format,
    )
    format_info = get_format_info(username=username, id_list=id_list, format=format)
    format_info, user_score = check_nulls(
        format_info=format_info, user_score=user_score, format=format
    )

    # NOTE: Insights
    merged_dfs = user_score.merge(format_info, on=f"{format}_id", how="left")

    (
        genre_max,
        genre_max_name,
        genre_info,
        genre_fav,
        genre_fav_title,
        genre_fav_u_score,
        genre_fav_avg_score,
    ) = genre_insights(merged_dfs=merged_dfs)

    (
        abs_score_diff,
        avg_score_diff,
        score_max,
        score_min,
        avg_max,
        avg_min,
        title_max,
        title_min,
        cover_image_1,
        cover_image_2,
        cover_image_3,
    ) = general_insights(merged_dfs=merged_dfs, genre_fav=genre_fav, format=format)

    merged_dfs, new_rows = round_scores(df=merged_dfs)
    plot_json = create_plot_data(df=merged_dfs, fill_df=new_rows)
    table_dict = create_table(df=merged_dfs)
    genre_dict = create_genre_data(genre_df=genre_info)

    load_dotenv()
    connection_string = os.environ["AZURE_ODBC"]
    connection_url = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
    engine = create_engine(connection_url)

    with engine.connect() as connection:
        query = f"""SELECT *
        FROM user_{format}_score;"""
        existing_user_score = pd.read_sql(sql=query, con=connection)
        query = f"""SELECT *
        FROM {format}_info;"""
        existing_format_info = pd.read_sql(sql=query, con=connection)

    existing_merged_dfs = existing_user_score.merge(
        existing_format_info, on=f"{format}_id", how="left"
    )
    existing_merged_dfs["score_diff"] = (
        existing_merged_dfs["user_score"] - existing_merged_dfs["average_score"]
    )
    existing_merged_dfs["abs_score_diff"] = (
        existing_merged_dfs["user_score"] - existing_merged_dfs["average_score"]
    ).abs()

    abs_data = existing_merged_dfs.groupby(by="user_id", as_index=False).agg(
        {"abs_score_diff": "mean"}
    )
    abs_data["abs_score_diff"] = 2 * round(abs_data["abs_score_diff"] / 2)
    abs_data["abs_score_diff"] = abs_data["abs_score_diff"].astype(int)
    abs_data = (
        pd.DataFrame(abs_data.value_counts("abs_score_diff", sort=False))
        .reset_index()
        .to_dict(orient="records")
    )

    avg_data = existing_merged_dfs.groupby(by="user_id", as_index=False).agg(
        {"score_diff": "mean"}
    )
    avg_data = avg_data.to_dict(orient="records")

    # NOTE: Upload
    dfs = [format_info, user_info, user_score]
    names = [f"{format}_info", "user_info", f"user_{format}_score"]
    blob_upload(dfs=dfs, names=names, anilist_id=anilist_id)

    # NOTE: Return
    insights = {
        "imageMax": cover_image_1,
        "imageMin": cover_image_2,
        "imageGenre": cover_image_3,
        "userMaxScore": score_max,
        "userMinScore": score_min,
        "avgMaxScore": avg_max,
        "avgMinScore": avg_min,
        "titleMax": title_max,
        "titleMin": title_min,
        "avgScoreDiff": avg_score_diff,
        "absScoreDiff": abs_score_diff,
        "userData": plot_json,
        "genreMax": genre_max,
        "genreMaxTitle": genre_max_name,
        "genreDiffTitle": genre_fav_title,
        "genreDiffUser": genre_fav_u_score,
        "genreDiffAvg": genre_fav_avg_score,
        "tableData": table_dict,
        "genreData": genre_dict,
        "absData": abs_data,
        "existingAbsScoreDiff": abs_data,
    }

    return dfs, anilist_id, insights
