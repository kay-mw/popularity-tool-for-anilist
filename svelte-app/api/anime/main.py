from api.anime.insights import general_insights, genre_insights
from api.anime.processing import check_nulls, get_anime_info, get_id, get_user_data


def fetch_anime(username: str):

    # Local testing
    # username = "keejan"

    # NOTE: Processing
    anilist_id = get_id(username=username)
    user_score, user_info, id_list = get_user_data(
        username=username, anilist_id=anilist_id
    )
    anime_info = get_anime_info(username=username, id_list=id_list)
    anime_info, user_score = check_nulls(anime_info=anime_info, user_score=user_score)

    # NOTE: Insights
    merged_dfs = user_score.merge(anime_info, on="anime_id", how="left")

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

    if (merged_dfs["user_score"] % 10 == 0).all():
        merged_dfs["average_score"] = 10 * round(merged_dfs["average_score"] / 10)
    else:
        merged_dfs["average_score"] = 5 * round(merged_dfs["average_score"] / 5)

    user_count = merged_dfs.value_counts("user_score").reset_index()
    average_count = merged_dfs.value_counts("average_score").reset_index()
    user_count = user_count.rename(columns={"count": "user_count"})
    average_count = average_count.rename(columns={"count": "average_count"})
    average_count["average_score"] = average_count["average_score"].astype(int)
    plot_data = user_count.merge(
        right=average_count, how="outer", left_on="user_score", right_on="average_score"
    )
    plot_data = plot_data.fillna(0.0).astype(
        {"average_score": int, "average_count": int}
    )
    assert plot_data["average_count"].sum() == plot_data["user_count"].sum()
    plot_json = plot_data.to_dict(orient="records")

    score_table = merged_dfs[
        ["title_romaji", "score_diff", "user_score", "average_score"]
    ].copy()
    score_table["abs_score_diff"] = abs(score_table.loc[:, "score_diff"])
    score_table["average_score"] = score_table["average_score"].astype(int)
    score_table = score_table.sort_values(by="abs_score_diff", ascending=False)
    score_table = score_table.reset_index(drop=True)
    score_table = score_table.drop(labels="abs_score_diff", axis=1)
    table_dict = score_table.to_dict(orient="records")

    genre_info = (
        genre_info.round(
            {"weighted_average": 1, "weighted_user": 1, "weighted_diff": 2}
        )
        .reset_index(drop=True)
        .drop(
            labels=["average_score", "user_score", "count"],
            axis=1,
        )
        .sort_values("weighted_diff", ascending=False, key=abs)
    )
    genre_dict = genre_info.to_dict(orient="records")

    # NOTE: Upload
    dfs = [anime_info, user_info, user_score]
    # names = ["anime_info", "user_info", "user_anime_score"]
    # blob_upload(dfs=dfs, names=names, anilist_id=anilist_id)

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
