import os
import time
import requests
import pandas as pd
import great_expectations as ge
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

def load_query(file_name):
    file_path = os.path.join("./app/api_request/", file_name)
    with open(file_path, "r") as file:
        return file.read()

def fetch_anilist_data(query, variables):
    try:
        response = requests.post(url, json={'query': query, 'variables': variables}, timeout=10)
        response.raise_for_status()
        global response_header
        response_header = response.headers['Date']
        response_header = pd.Series(response_header)
        return response.json()
    except requests.exceptions.Timeout:
        print("Request timed out.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error in request: {e}")
        return None

query_get_id = load_query("get_id.gql")

username = 'keejan'

variables_get_id = {
    "name": username
}

url = 'https://graphql.anilist.co'

json_response = fetch_anilist_data(query_get_id, variables_get_id)
anilist_id = json_response['data']['User']['id']

# # # # # # # # # # # # # # # # # # # # # 

query_user = load_query("user_query.gql")

variables_user = {
    "page": 1,
    "id": anilist_id
}

url = 'https://graphql.anilist.co'

json_response = fetch_anilist_data(query_user, variables_user)

user_score = pd.json_normalize(json_response,
                            record_path=['data', 'Page', 'users', 'statistics', 'anime', 'scores'],
                            meta=[['data', 'Page', 'users', 'id']])

user_score = user_score.explode('mediaIds', ignore_index=True)
user_score['mediaIds'] = user_score['mediaIds'].astype(int)

user_score.rename(columns={
    'mediaIds': 'anime_id',
    'data.Page.users.id': 'user_id',
    'id': 'anime_id',
    'score': 'user_score'
}, inplace=True)

print(user_score.to_string())

# # # # # # # # # # # # # # # # # # # # # # # # Make user info table # # # # # # # # # # # # # # # # # # # # #

user_info = pd.json_normalize(json_response, record_path=['data', 'Page', 'users'])
user_info.drop('statistics.anime.scores', axis=1, inplace=True)

user_info = pd.concat([user_info, response_header], axis=1)
user_info.rename(columns={0: 'request_date',
                        'id': 'user_id',
                        'name': 'user_name'}, inplace=True)

user_info['request_date'] = pd.to_datetime(
    user_info['request_date'], 
    format='%a, %d %b %Y %H:%M:%S %Z'
    ).dt.tz_localize(None)

print(user_info.to_string())

# # # # # # # # # # # # # # # # # # # # # # # # # Get anime info # # # # # # # # # # # # # # # # # # # # # # #

query_anime = load_query('anime_query.gql')

id_list = user_score['anime_id'].values.tolist()

variables_anime = {
    "page": 1,
    "id_in": id_list
}

url = 'https://graphql.anilist.co'

anime_info = pd.DataFrame()

while True:
    response_ids = fetch_anilist_data(query_anime, variables_anime)
    print("Fetching anime info...")
    time.sleep(2)

    page_df = pd.json_normalize(response_ids, record_path=['data', 'Page', 'media'])
    anime_info = pd.concat([anime_info, page_df], ignore_index=True)

    if not response_ids['data']['Page']['pageInfo']['hasNextPage']:
        break

    variables_anime['page'] += 1

anime_info.rename(columns={'averageScore': 'average_score',
                        'title.romaji': 'title_romaji',
                        'id': 'anime_id'}, inplace=True)

print(anime_info.to_string())

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

merged_dfs = user_score.merge(anime_info, on='anime_id', how='left')

merged_dfs['score_diff'] = merged_dfs['user_score'] - merged_dfs['average_score']

max_diff = merged_dfs.loc[merged_dfs['score_diff'].abs() == max(merged_dfs['score_diff'].abs())]
min_diff = merged_dfs.loc[merged_dfs['score_diff'].abs() == min(merged_dfs['score_diff'].abs())]

score_max = int(max_diff['user_score'].iloc[0])
score_min = int(min_diff['user_score'].iloc[0])

avg_max = int(max_diff['average_score'].iloc[0])
avg_min = int(min_diff['average_score'].iloc[0])

title_max = max_diff['title_romaji'].iloc[0]
title_min = min_diff['title_romaji'].iloc[0]

image_id_1 = int(max_diff['anime_id'].iloc[0])
image_id_2 = int(min_diff['anime_id'].iloc[0])

query_image = load_query('image_query.gql')

variables_image_1 = {
    "id": image_id_1
}
variables_image_2 = {
    "id": image_id_2
}

cover_image_1 = fetch_anilist_data(query_image, variables_image_1)
cover_image_2 = fetch_anilist_data(query_image, variables_image_2)

cover_image_1 = cover_image_1['data']['Media']['coverImage']['extraLarge']
cover_image_2 = cover_image_2['data']['Media']['coverImage']['extraLarge']

# # # # # # # # # # # # # # # # # # # # # # # Data Quality Checks # # # # # # # # # # # # # # # # # # # # # # #

ge_anime_info = ge.from_pandas(anime_info)
ge_user_info = ge.from_pandas(user_info)
ge_user_score = ge.from_pandas(user_score)

ge_anime_info.expect_column_values_to_be_unique('anime_id')
ge_anime_info.expect_column_values_to_not_be_null('anime_id')
ge_anime_info.expect_column_max_to_be_between('average_score', 0, 100)
anime_info_suite = ge_anime_info.get_expectation_suite()

ge_user_score.expect_column_values_to_be_unique('anime_id')
ge_user_score.expect_column_values_to_not_be_null('anime_id')
ge_user_score.expect_column_max_to_be_between('user_score', 0, 100)
user_score_suite = ge_user_score.get_expectation_suite()

ge_user_info.expect_column_values_to_be_unique('user_id')
ge_user_info.expect_column_values_to_not_be_null('user_id')
user_info_suite = ge_user_info.get_expectation_suite()

anime_info_results = ge_anime_info.validate(expectation_suite=anime_info_suite)
user_score_results = ge_user_score.validate(expectation_suite=user_score_suite)
user_info_results = ge_user_info.validate(expectation_suite=user_info_suite)

all_ge_results = anime_info_results, user_score_results, user_info_results

for results in all_ge_results:
    if results["success"]:
        print("Success: Data Quality Checks All Passed!")
    else:
        raise Exception("Failure: Some Data Quality Check(s) Failed")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

server = "anilist-sqlserver.database.windows.net"
database = "anilist-db"

load_dotenv()
AZURE_ODBC = os.environ['AZURE_ODBC']
connection_string = AZURE_ODBC

params = quote_plus(connection_string)
connection_url = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(connection_url)

session = sessionmaker(bind=engine)

def upload_table(primary_key, table_name, df, column_1, column_2):
    with engine.connect() as connection:
        print(f"Uploading {table_name} to Azure SQL Database...")

        df.to_sql("temp_table", con=connection, if_exists="replace")

        query = (f"MERGE {table_name} AS target USING temp_table AS source "
                f"ON source.{primary_key} = target.{primary_key} "
                f"WHEN NOT MATCHED BY target THEN INSERT ({primary_key}, {column_1}, {column_2}) "
                f"VALUES (source.{primary_key}, source.{column_1}, source.{column_2}) "
                f"WHEN MATCHED THEN UPDATE "
                f"SET target.{primary_key} = source.{primary_key}, "
                f"target.{column_1} = source.{column_1}, "
                f"target.{column_2} = source.{column_2};")
        print(query)
        connection.execute(text(query))
        connection.commit()

upload_table("anime_id", "anime_info", anime_info, "average_score", "title_romaji")
upload_table("anime_id", "user_score", user_score, "user_id", "user_score")
upload_table("user_id", "user_info", user_info, "user_name", "request_date")
