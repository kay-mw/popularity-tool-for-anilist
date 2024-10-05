import os
from datetime import datetime as dt
from typing import List

import pandas as pd
from azure.storage.blob import BlobServiceClient


def blob_upload(dfs: List[pd.DataFrame], names: List[str], anilist_id: int) -> None:
    storage_connection_string = os.environ["STORAGE_CONNECTION_STRING"]
    blob_service_client = BlobServiceClient.from_connection_string(
        storage_connection_string
    )
    container_id = "projectanilist"

    date = dt.today().strftime("%Y-%m-%d")
    for i, df in enumerate(dfs):
        name = names[i]
        file_path = os.path.join("./api/", f"{name}.csv")
        df.to_csv(path_or_buf=file_path)

        blob_path = f"data/{date}/{anilist_id}/{name}.csv"
        blob_object = blob_service_client.get_blob_client(
            container=container_id, blob=blob_path
        )

        with open(file_path, mode="rb") as csv:
            blob_object.upload_blob(csv, overwrite=True)
            os.remove(file_path)
