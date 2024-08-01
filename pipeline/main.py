# NOTE: Define explicit schemas when importing to ensure data quality and correct typing.

import os
from io import StringIO
from urllib.parse import quote_plus

import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
storage_connection_string = os.environ["STORAGE_CONNECTION_STRING"]
blob_service_client = BlobServiceClient.from_connection_string(
    storage_connection_string
)
container_id = "projectanilist"
container_client = blob_service_client.get_container_client(container_id)

blobs = container_client.list_blobs()
for blob in blobs:
    blob_name = blob["name"]
    blob_client = blob_service_client.get_blob_client(
        container=container_id, blob=blob_name
    )
    downloader = blob_client.download_blob(max_concurrency=1, encoding="UTF-8")
    blob_text = downloader.readall()
    csv = StringIO(f"""{blob_text}""")

    df = pd.read_csv(csv, sep=",", index_col=False)
    df.drop(labels="Unnamed: 0", axis=1, inplace=True)

    connection_string = os.environ['AZURE_ODBC']
    connection_url = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
    engine = create_engine(connection_url)

    def upload_one_to_one(primary_key: str, table_name: str, df: pd.DataFrame, column_1: str, column_2: str) -> None:
        with engine.connect() as connection:
            df.to_sql("temp_table", con=connection, if_exists="replace")

            query = (f"MERGE {table_name} AS target USING temp_table AS source "
                    f"ON source.{primary_key} = target.{primary_key} "
                    f"WHEN NOT MATCHED BY target THEN INSERT ({primary_key}, {column_1}, {column_2}) "
                    f"VALUES (source.{primary_key}, source.{column_1}, source.{column_2}) "
                    f"WHEN MATCHED THEN UPDATE "
                    f"SET target.{column_1} = source.{column_1}, "
                    f"target.{column_2} = source.{column_2};")
            connection.execute(text(query))
            connection.commit()

    def upload_many_to_many(df: pd.DataFrame, table_name: str, foreign_key_1: str, foreign_key_2: str, column_1: str, anilist_id: int) -> None:
        check_query = f'SELECT {foreign_key_1}, {foreign_key_2}, {column_1} FROM {table_name} WHERE {foreign_key_1} = {anilist_id};' 

        with engine.connect() as connection:
            check_exists = pd.read_sql(check_query, con=connection) 

        if check_exists.empty:
            with engine.connect() as connection:
                df.to_sql(name=f"{table_name}", con=connection, if_exists="append", index=False)
        else:
            query = (f'DELETE FROM {table_name} WHERE {foreign_key_1} = {anilist_id}')
            with engine.connect() as connection:
                connection.execute(text(query))
                connection.commit()

            with engine.connect() as connection:
                df.to_sql(name=f'{table_name}', con=connection, if_exists="append", index=False)

    file_name = blob_name.split("/")
    file_name = file_name[3]

    if file_name == "anime_info.csv":
        pass
        upload_one_to_one("anime_id", "anime_info", df, "average_score", "title_romaji")
    elif file_name == "user_info.csv":
        pass
        upload_one_to_one("user_id", "user_info", df, "user_name", "request_date")
    else:
        anilist_id = df.iloc[0]["user_id"]
        upload_many_to_many(df, "user_anime_score", "user_id", "anime_id", "user_score", anilist_id)
