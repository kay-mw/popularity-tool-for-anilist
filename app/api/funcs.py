import os

import aiohttp
import pandas as pd
import requests


def load_query(file_name: str) -> str:
    file_path = os.path.join("./app/api/gql/", file_name)
    with open(file_path, "r") as file:
        return file.read()


def fetch_anilist_data(query: str, variables: dict) -> tuple[dict, pd.Series]:
    url = "https://graphql.anilist.co"
    response = requests.post(
        url, json={"query": query, "variables": variables}, timeout=10
    )
    response.raise_for_status()
    response_header = pd.Series(response.headers["Date"])
    return response.json(), response_header


async def fetch_anilist_data_async(query: str, variables: dict) -> dict:
    url = "https://graphql.anilist.co"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, json={"query": query, "variables": variables}, timeout=10
        ) as response:
            response.raise_for_status()
            return await response.json()
