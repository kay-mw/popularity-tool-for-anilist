import datetime as dt
from io import StringIO
from typing import List

import numpy as np
import pandas as pd
from azure.storage.blob import BlobServiceClient


def get_blob(
    blob_service_client: BlobServiceClient, container_id: str, blob_name: str
) -> StringIO:
    blob_client = blob_service_client.get_blob_client(
        container=container_id, blob=blob_name
    )
    downloader = blob_client.download_blob(max_concurrency=1, encoding="UTF-8")
    blob_text = downloader.readall()
    csv = StringIO(f"""{blob_text}""")
    return csv


def read_anime_and_manga(
    blob_service_client: BlobServiceClient,
    container_id: str,
    blobs: List[str],
    insert_date: str,
) -> tuple[
    List[pd.DataFrame],
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    anime_info = get_blob(blob_service_client, container_id, blobs[0])
    anime_info = pd.read_csv(
        anime_info,
        sep=",",
        dtype={
            "Unnamed: 0": int,
            "anime_id": int,
            "average_score": int,
            "title_romaji": str,
        },
    )
    anime_info.drop(labels="Unnamed: 0", axis=1, inplace=True)

    manga_info = get_blob(blob_service_client, container_id, blobs[1])
    manga_info = pd.read_csv(
        manga_info,
        sep=",",
        dtype={
            "Unnamed: 0": int,
            "manga_id": int,
            "average_score": int,
            "title_romaji": str,
        },
    )
    manga_info.drop(labels="Unnamed: 0", axis=1, inplace=True)

    user_anime_score = get_blob(blob_service_client, container_id, blobs[2])
    user_anime_score = pd.read_csv(
        user_anime_score,
        sep=",",
        dtype={
            "Unnamed: 0": int,
            "user_id": int,
            "anime_id": int,
            "user_score": int,
        },
    )
    user_anime_score.drop(labels="Unnamed: 0", axis=1, inplace=True)
    user_anime_score["start_date"] = insert_date
    user_anime_score["end_date"] = np.nan
    print(user_anime_score)

    user_info = get_blob(blob_service_client, container_id, blobs[3])
    user_info = pd.read_csv(
        user_info,
        sep=",",
        dtype={
            "Unnamed: 0": int,
            "user_id": int,
            "user_name": str,
        },
        parse_dates=["request_date"],
        date_format="%Y-%m-%d %H:%M:%S",
    )
    user_info.drop(labels="Unnamed: 0", axis=1, inplace=True)

    user_manga_score = get_blob(blob_service_client, container_id, blobs[4])
    user_manga_score = pd.read_csv(
        user_manga_score,
        sep=",",
        dtype={
            "Unnamed: 0": int,
            "user_id": int,
            "manga_id": int,
            "user_score": int,
        },
    )
    user_manga_score.drop(labels="Unnamed: 0", axis=1, inplace=True)
    user_manga_score["start_date"] = insert_date
    user_manga_score["end_date"] = np.nan
    print(user_manga_score)

    dfs = [anime_info, manga_info, user_anime_score, user_info, user_manga_score]
    return dfs, anime_info, manga_info, user_anime_score, user_info, user_manga_score


def read_anime(
    blob_service_client: BlobServiceClient,
    container_id: str,
    blobs: List[str],
    insert_date: str,
) -> tuple[List[pd.DataFrame], pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    anime_info = get_blob(blob_service_client, container_id, blobs[0])
    anime_info = pd.read_csv(
        anime_info,
        sep=",",
        dtype={
            "Unnamed: 0": int,
            "anime_id": int,
            "average_score": int,
            "title_romaji": str,
        },
    )
    anime_info.drop(labels="Unnamed: 0", axis=1, inplace=True)

    user_anime_score = get_blob(blob_service_client, container_id, blobs[1])
    user_anime_score = pd.read_csv(
        user_anime_score,
        sep=",",
        dtype={
            "Unnamed: 0": int,
            "user_id": int,
            "anime_id": int,
            "user_score": int,
        },
    )
    user_anime_score.drop(labels="Unnamed: 0", axis=1, inplace=True)
    user_anime_score["start_date"] = insert_date
    user_anime_score["end_date"] = np.nan

    user_info = get_blob(blob_service_client, container_id, blobs[2])
    user_info = pd.read_csv(
        user_info,
        sep=",",
        dtype={
            "Unnamed: 0": int,
            "user_id": int,
            "user_name": str,
        },
        parse_dates=["request_date"],
        date_format="%Y-%m-%d %H:%M:%S",
    )
    user_info.drop(labels="Unnamed: 0", axis=1, inplace=True)

    dfs = [anime_info, user_anime_score, user_info]
    return dfs, anime_info, user_anime_score, user_info


def read_manga(
    blob_service_client: BlobServiceClient,
    container_id: str,
    blobs: List[str],
    insert_date: str,
) -> tuple[List[pd.DataFrame], pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    manga_info = get_blob(blob_service_client, container_id, blobs[0])
    manga_info = pd.read_csv(
        manga_info,
        sep=",",
        dtype={
            "Unnamed: 0": int,
            "manga_id": int,
            "average_score": float,
            "title_romaji": str,
        },
    )
    manga_info.drop(labels="Unnamed: 0", axis=1, inplace=True)

    user_info = get_blob(blob_service_client, container_id, blobs[1])
    user_info = pd.read_csv(
        user_info,
        sep=",",
        dtype={
            "Unnamed: 0": int,
            "user_id": int,
            "user_name": str,
        },
        parse_dates=["request_date"],
        date_format="%Y-%m-%d %H:%M:%S",
    )
    user_info.drop(labels="Unnamed: 0", axis=1, inplace=True)

    user_manga_score = get_blob(blob_service_client, container_id, blobs[2])
    user_manga_score = pd.read_csv(
        user_manga_score,
        sep=",",
        dtype={
            "Unnamed: 0": int,
            "user_id": int,
            "manga_id": int,
            "user_score": int,
        },
    )
    user_manga_score.drop(labels="Unnamed: 0", axis=1, inplace=True)
    user_manga_score["start_date"] = insert_date
    user_manga_score["end_date"] = np.nan

    dfs = [manga_info, user_info, user_manga_score]
    return dfs, manga_info, user_info, user_manga_score
