# NOTE: Maybe add try: except: for error handling?

import datetime as dt
import os
from io import StringIO
from urllib.parse import quote_plus

import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from sqlalchemy import create_engine

from pipeline.upload_funcs import upload_many_to_many, upload_one_to_one

load_dotenv()

# NOTE: Azure Blob Storage
storage_connection_string = os.environ["STORAGE_CONNECTION_STRING"]
blob_service_client = BlobServiceClient.from_connection_string(
    storage_connection_string
)
container_id = "projectanilist"
container_client = blob_service_client.get_container_client(container_id)

# NOTE: SQLAlchemy
connection_string = os.environ["AZURE_ODBC"]
connection_url = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
engine = create_engine(connection_url)

today = dt.date.today()
blobs = container_client.list_blobs(name_starts_with=f"data/{today}")

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

        upload_one_to_one(
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

        upload_one_to_one(
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
