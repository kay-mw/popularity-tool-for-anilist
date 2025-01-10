import datetime as dt

import pandas as pd
from dagster import asset

from pipelines.funcs import blob_init, sql_init, upload, upload_many_to_many
from pipelines.read_blobs import read_anime, read_anime_and_manga, read_manga
from pipelines.tests import test_anime, test_anime_and_manga, test_manga


@asset()
def upload_data() -> None:
    engine = sql_init()
    blob_service_client = blob_init()

    container_id = "projectanilist"
    container_client = blob_service_client.get_container_client(container_id)
    yesterday = dt.date.today() - dt.timedelta(days=1)

    blobs = container_client.list_blobs(name_starts_with=f"data/{str(yesterday)}")
    blob_names = [blob["name"] for blob in blobs]

    split_names = [name.split("/") for name in blob_names]
    ids = []
    for name in split_names:
        ids.append(int(name[2]))

    unique_ids = set(ids)
    blobs_by_user = dict.fromkeys(unique_ids)

    insert_date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    for key in unique_ids:
        blobs = [name for name in blob_names if str(key) in name]
        blobs = sorted(blobs)
        assert (
            len(blobs) == 3 or len(blobs) == 5
        ), f"Unexpected number of blobs ({len(blobs)}) for user {key}: {blobs}"
        blobs_by_user[key] = blobs

    for blobs in blobs_by_user.values():
        if blobs == None:
            print("No blobs found.")
            break
        else:
            manga = False
            for blob in blobs:
                if "user_manga_score.csv" and "manga_info.csv" in blob:
                    manga = True
            if len(blobs) == 5:
                (
                    dfs,
                    anime_info,
                    manga_info,
                    user_anime_score,
                    user_info,
                    user_manga_score,
                ) = read_anime_and_manga(
                    blob_service_client=blob_service_client,
                    container_id=container_id,
                    blobs=blobs,
                    insert_date=insert_date,
                )
                test_anime_and_manga(
                    dfs=dfs,
                    anime_info=anime_info,
                    manga_info=manga_info,
                    user_anime_score=user_anime_score,
                    user_info=user_info,
                    user_manga_score=user_manga_score,
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
                    df=manga_info,
                    table_name="manga_info",
                    primary_key="manga_id",
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

                anilist_id = user_manga_score.iloc[0]["user_id"]
                upload_many_to_many(
                    df=user_anime_score,
                    table_name="user_anime_score",
                    foreign_key_1="user_id",
                    foreign_key_2="anime_id",
                    column_1="user_score",
                    anilist_id=anilist_id,
                    insert_date=insert_date,
                    engine=engine,
                )
                upload_many_to_many(
                    df=user_manga_score,
                    table_name="user_manga_score",
                    foreign_key_1="user_id",
                    foreign_key_2="manga_id",
                    column_1="user_score",
                    anilist_id=anilist_id,
                    insert_date=insert_date,
                    engine=engine,
                )
            elif len(blobs) == 3 and manga == False:
                dfs, anime_info, user_anime_score, user_info = read_anime(
                    blob_service_client=blob_service_client,
                    container_id=container_id,
                    blobs=blobs,
                    insert_date=insert_date,
                )
                test_anime(
                    dfs=dfs,
                    anime_info=anime_info,
                    user_anime_score=user_anime_score,
                    user_info=user_info,
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

                anilist_id = user_anime_score.iloc[0]["user_id"]
                upload_many_to_many(
                    df=user_anime_score,
                    table_name="user_anime_score",
                    foreign_key_1="user_id",
                    foreign_key_2="anime_id",
                    column_1="user_score",
                    anilist_id=anilist_id,
                    insert_date=insert_date,
                    engine=engine,
                )
            elif len(blobs) == 3 and manga == True:
                dfs, manga_info, user_info, user_manga_score = read_manga(
                    blob_service_client=blob_service_client,
                    container_id=container_id,
                    blobs=blobs,
                    insert_date=insert_date,
                )
                test_manga(
                    dfs=dfs,
                    manga_info=manga_info,
                    user_info=user_info,
                    user_manga_score=user_manga_score,
                )
                upload(
                    df=manga_info,
                    table_name="manga_info",
                    primary_key="manga_id",
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

                anilist_id = user_manga_score.iloc[0]["user_id"]
                upload_many_to_many(
                    df=user_manga_score,
                    table_name="user_manga_score",
                    foreign_key_1="user_id",
                    foreign_key_2="manga_id",
                    column_1="user_score",
                    anilist_id=anilist_id,
                    insert_date=insert_date,
                    engine=engine,
                )
