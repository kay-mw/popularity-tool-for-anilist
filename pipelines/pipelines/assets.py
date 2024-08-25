import datetime as dt
from io import StringIO

import pandas as pd
from dagster import asset

from pipelines.funcs import blob_init, sql_init, upload, upload_many_to_many
from pipelines.tests import test_dataframes


@asset()
def upload_data() -> None:
    engine = sql_init()
    blob_service_client = blob_init()

    container_id = "projectanilist"
    container_client = blob_service_client.get_container_client(container_id)
    yesterday = dt.date.today() - dt.timedelta(days=1)

    blobs = container_client.list_blobs(name_starts_with=f"data/{yesterday}")
    blob_names = [blob["name"] for blob in blobs]

    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    blobs_by_user = list(chunks(blob_names, 3))
    for user in blobs_by_user:
        assert len(user) == 3, "Some CSVs are missing!"

    def get_blob(blob_name):
        blob_client = blob_service_client.get_blob_client(
            container=container_id, blob=blob_name
        )
        downloader = blob_client.download_blob(max_concurrency=1, encoding="UTF-8")
        blob_text = downloader.readall()
        csv = StringIO(f"""{blob_text}""")
        return csv

    for user in blobs_by_user:
        anime_info = get_blob(user[0])
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

        user_info = get_blob(user[1])
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

        user_score = get_blob(user[2])
        user_score = pd.read_csv(
            user_score,
            sep=",",
            dtype={
                "Unnamed: 0": int,
                "user_id": int,
                "anime_id": int,
                "user_score": int,
            },
        )
        user_score.drop(labels="Unnamed: 0", axis=1, inplace=True)

        test_dataframes(
            dfs=[anime_info, user_info, user_score],
            anime_info=anime_info,
            user_info=user_info,
            user_score=user_score,
        )

        upload(
            df=anime_info,
            table_name="anime_info",
            primary_key="anime_id",
            column_1="average_score",
            column_2="title_romaji",
            engine=engine,
        )
        upload(
            df=user_info,
            table_name="user_info",
            primary_key="user_id",
            column_1="user_name",
            column_2="request_date",
            engine=engine,
        )
        anilist_id = user_score.iloc[0]["user_id"]
        upload_many_to_many(
            df=user_score,
            table_name="user_anime_score",
            foreign_key_1="user_id",
            foreign_key_2="anime_id",
            column_1="user_score",
            anilist_id=anilist_id,
            engine=engine,
        )
