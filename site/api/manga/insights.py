import pandas as pd
from api.funcs import fetch_anilist_data, load_query


def genre_insights(
    merged_dfs: pd.DataFrame,
) -> tuple[float, str, pd.DataFrame, pd.DataFrame, str, float, float]:
    genres = merged_dfs.explode(column="genres", ignore_index=False)
    averages = genres.groupby(by="genres", as_index=False).agg(
        {
            "average_score": "mean",
            "user_score": "mean",
        }
    )
    count = genres["genres"].value_counts(sort=False)
    genre_info = averages.merge(count, on="genres", how="left")

    def bayesian_average(
        weight: pd.Series | float | int,
        default: pd.Series | float | int,
        count: pd.Series | pd.DataFrame,
        score: pd.Series | pd.DataFrame,
    ) -> pd.Series | float:
        weighted_rating = (weight * default + count * score) / (weight + count)
        return weighted_rating

    genre_info["weighted_average"] = bayesian_average(
        weight=genre_info["count"].mean(),
        default=genre_info["average_score"].mean(),
        count=genre_info["count"],
        score=genre_info["average_score"],
    )

    genre_info["weighted_user"] = bayesian_average(
        weight=genre_info["count"].mean(),
        default=genre_info["user_score"].mean(),
        count=genre_info["count"],
        score=genre_info["user_score"],
    )

    genre_info["weighted_diff"] = (
        genre_info["weighted_user"] - genre_info["weighted_average"]
    )
    genre_info = genre_info.sort_values(by="weighted_diff", ascending=False)

    max_genre_df = genre_info.loc[
        genre_info["weighted_diff"].abs() == max(genre_info["weighted_diff"].abs())
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

    return (
        genre_max,
        genre_max_name,
        genre_info,
        genre_fav,
        genre_fav_title,
        genre_fav_u_score,
        genre_fav_avg_score,
    )


def general_insights(
    merged_dfs: pd.DataFrame, genre_fav: pd.DataFrame
) -> tuple[float, float, int, int, int, int, str, str, str, str, str]:
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
    cover_image_1, _ = fetch_anilist_data(query_image, variables_image_1)
    cover_image_2, _ = fetch_anilist_data(query_image, variables_image_2)
    cover_image_3, _ = fetch_anilist_data(query_image, variables_image_3)
    cover_image_1 = cover_image_1["data"]["Media"]["coverImage"]["extraLarge"]
    cover_image_2 = cover_image_2["data"]["Media"]["coverImage"]["extraLarge"]
    cover_image_3 = cover_image_3["data"]["Media"]["coverImage"]["extraLarge"]

    return (
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
    )
