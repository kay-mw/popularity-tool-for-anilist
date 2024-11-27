import pandas as pd
from api.funcs import create_genre_data, create_plot_data, create_table, round_scores
from api.manga.insights import general_insights, genre_insights
from api.manga.processing import check_nulls, get_id, get_manga_info, get_user_data
from api.upload import blob_upload


def fetch_manga(username: str):
    # Local testing
    # username = "ZNote"

    # NOTE: Processing
    anilist_id = get_id(username=username)
    user_score, user_info, id_list = get_user_data(
        username=username, anilist_id=anilist_id
    )
    manga_info = get_manga_info(username=username, id_list=id_list)
    manga_info, user_score = check_nulls(manga_info=manga_info, user_score=user_score)

    # NOTE: Insights
    merged_dfs = user_score.merge(manga_info, on="manga_id", how="left")

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
    ) = general_insights(merged_dfs=merged_dfs, genre_fav=genre_fav)

    merged_dfs, new_rows = round_scores(df=merged_dfs)
    plot_json = create_plot_data(df=merged_dfs, fill_df=new_rows)
    table_dict = create_table(df=merged_dfs)
    genre_dict = create_genre_data(genre_df=genre_info)

    # NOTE: Upload
    dfs = [manga_info, user_info, user_score]
    names = ["manga_info", "user_info", "user_manga_score"]
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
    }

    return dfs, anilist_id, insights
