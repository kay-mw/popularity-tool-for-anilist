import os
from urllib.parse import quote_plus

import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import DataError


def sql_init() -> Engine:
    load_dotenv()
    connection_string = os.environ["AZURE_ODBC"]
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": quote_plus(connection_string)}
    )
    engine = create_engine(connection_url)
    return engine


def blob_init() -> BlobServiceClient:
    load_dotenv()
    storage_connection_string = os.environ["STORAGE_CONNECTION_STRING"]
    blob_service_client = BlobServiceClient.from_connection_string(
        storage_connection_string
    )
    return blob_service_client


def upload(
    df: pd.DataFrame,
    table_name: str,
    primary_key: str,
    column_1: str,
    column_2: str,
    engine,
    column_3="genres",
    column_4="popularity",
) -> None:
    with engine.connect() as connection:
        df.to_sql("temp_table", con=connection, if_exists="replace")

        if table_name in ["anime_info", "manga_info"]:
            query = f"""
                    MERGE {table_name} AS target USING temp_table AS source
                    ON source.{primary_key} = target.{primary_key}
                    WHEN NOT MATCHED BY target
                    THEN INSERT ({primary_key}, {column_1}, {column_2}, {column_3}, {column_4})
                    VALUES (source.{primary_key}, source.{column_1}, source.{column_2}, source.{column_3}, source.{column_4})
                    WHEN MATCHED THEN UPDATE 
                    SET target.{column_1} = source.{column_1}, 
                    target.{column_2} = source.{column_2},
                    target.{column_3} = source.{column_3},
                    target.{column_4} = source.{column_4};
                """
        else:
            query = f"""
                MERGE {table_name} AS target USING temp_table AS source
                ON source.{primary_key} = target.{primary_key}
                WHEN NOT MATCHED BY target
                THEN INSERT ({primary_key}, {column_1}, {column_2})
                VALUES (source.{primary_key}, source.{column_1}, source.{column_2})
                WHEN MATCHED THEN UPDATE 
                SET target.{column_1} = source.{column_1}, 
                target.{column_2} = source.{column_2};
            """

        connection.execute(
            text(query),
        )
        connection.commit()


def upload_many_to_many(
    df: pd.DataFrame,
    table_name: str,
    foreign_key_1: str,
    foreign_key_2: str,
    column_1: str,
    anilist_id: int,
    insert_date: str,
    engine,
) -> None:
    check_query = f"""
        SELECT {foreign_key_1}, {foreign_key_2}, {column_1}, start_date, end_date 
        FROM (
            SELECT 
                {foreign_key_1}, {foreign_key_2}, {column_1}, start_date, end_date,
                ROW_NUMBER() OVER(ORDER BY start_date DESC) AS rn
            FROM {table_name} 
            WHERE {foreign_key_1} = {anilist_id}
        ) AS t
        WHERE t.rn = 1;
    """

    with engine.connect() as connection:
        check_exists = pd.read_sql(check_query, con=connection)

    if check_exists.empty:
        with engine.connect() as connection:
            df.to_sql(
                name=f"{table_name}",
                con=connection,
                if_exists="append",
                index=False,
            )
    else:
        old_start_date = check_exists.loc[0, "start_date"]

        if old_start_date != None:
            query = f"""
                UPDATE user_anime_score 
                SET end_date = '{insert_date}'
                WHERE user_id = {anilist_id}
                AND start_date = '{old_start_date}';
            """
        else:
            query = f"""
                UPDATE user_anime_score
                SET end_date = '{insert_date}'
                WHERE user_id = {anilist_id}
                AND start_date IS NULL;
            """

        with engine.connect() as connection:
            try:
                connection.execute(text(query))
                connection.commit()
            except DataError:
                old_start_date = check_exists.loc[0, "start_date"].strftime(
                    "%Y-%m-%d %H:%M:%S.%f"
                )[:-3]
                query = f"""
                    UPDATE user_anime_score 
                    SET end_date = '{insert_date}'
                    WHERE user_id = {anilist_id}
                    AND start_date = '{old_start_date}';
                """
                connection.execute(text(query))
                connection.commit()

        with engine.connect() as connection:
            df.to_sql(
                name=f"{table_name}",
                con=connection,
                if_exists="append",
                index=False,
            )
