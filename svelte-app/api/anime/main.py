from api.anime.insights import general_insights, genre_insights, table_insights
from api.anime.processing import check_nulls, get_anime_info, get_id, get_user_data
from api.plots import plot_genres, plot_main


def fetch_anime(username: str):

    # Local testing
    # username = "BlessedBaka"

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
    plt_div_genres = plot_genres(genre_insights=genre_info, username=username)

    (
        avg_score_diff,
        true_score_diff,
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
    plt_div_main = plot_main(merged_dfs=merged_dfs, username=username)

    score_table_html = table_insights(merged_dfs=merged_dfs)

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
        "absScoreDiff": true_score_diff,
        # "plotMain": plt_div_main,
        # "plot_genres": plt_div_genres,
        "genreMax": genre_max,
        "genreMaxTitle": genre_max_name,
        "genreDiffTitle": genre_fav_title,
        "genreDiffUser": genre_fav_u_score,
        "genreDiffAvg": genre_fav_avg_score,
        # "scoreTable": score_table_html,
    }

    return dfs, anilist_id, insights