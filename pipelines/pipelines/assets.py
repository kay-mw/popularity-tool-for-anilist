import datetime as dt
from io import StringIO

import pandas as pd
from dagster import asset

from pipelines.funcs import blob_init, sql_init, upload, upload_many_to_many


@asset()
def upload_data() -> None:
    engine = sql_init()
    blob_service_client = blob_init()

    container_id = "projectanilist"
    container_client = blob_service_client.get_container_client(container_id)
    yesterday = dt.date.today() - dt.timedelta(days = 1)
    blobs = container_client.list_blobs(name_starts_with=f"data/{yesterday}")
    for blob in blobs:
        blob_name = blob["name"]
        blob_client = blob_service_client.get_blob_client(
            container=container_id, blob=blob_name
        )
        downloader = blob_client.download_blob(max_concurrency=1, encoding="UTF-8")
        blob_text = downloader.readall()
        csv = StringIO(f"""{blob_text}""")

        file_name = blob_name.split("/")
        file_name = file_name[3]

        df = pd.DataFrame
        if file_name == "anime_info.csv":
            df = pd.read_csv(
                csv,
                sep=",",
                dtype={
                    "Unnamed: 0": int,
                    "anime_id": int,
                    "average_score": int,
                    "title_romaji": str,
                },
            )
            df.drop(labels="Unnamed: 0", axis=1, inplace=True)

            upload(
                df=df,
                table_name="anime_info",
                primary_key="anime_id",
                column_1="average_score",
                column_2="title_romaji",
                engine=engine,
            )
        elif file_name == "user_info.csv":
            df = pd.read_csv(
                csv,
                sep=",",
                dtype={
                    "Unnamed: 0": int,
                    "user_id": int,
                    "user_name": str,
                },
                parse_dates=True,
                date_format="%Y-%m-%d %H:%M:%S",
            )
            df.drop(labels="Unnamed: 0", axis=1, inplace=True)

            upload(
                df=df,
                table_name="user_info",
                primary_key="user_id",
                column_1="user_name",
                column_2="request_date",
                engine=engine,
            )
        else:
            df = pd.read_csv(
                csv,
                sep=",",
                dtype={
                    "Unnamed: 0": int,
                    "user_id": int,
                    "anime_id": int,
                    "user_score": int,
                },
            )
            df.drop(labels="Unnamed: 0", axis=1, inplace=True)

            anilist_id = df.iloc[0]["user_id"]
            upload_many_to_many(
                df=df,
                table_name="user_anime_score",
                foreign_key_1="user_id",
                foreign_key_2="anime_id",
                column_1="user_score",
                anilist_id=anilist_id,
                engine=engine,
            )
