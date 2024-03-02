def fetch_data(anilist_id):
    import os
    import time
    from urllib.parse import quote_plus

    import pandas as pd
    import requests
    from dotenv import load_dotenv
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker

    def load_query(file_name):
        file_path = os.path.join("./", file_name)
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

    # # # # # # # # # # # # # # # # # # # # # # # # Make user info table # # # # # # # # # # # # # # # # # # # # # # #

    user_info = pd.json_normalize(json_response, record_path=['data', 'Page', 'users'])
    user_info.drop('statistics.anime.scores', axis=1, inplace=True)

    user_info = pd.concat([user_info, response_header], axis=1)
    user_info.rename(columns={0: 'request_date',
                              'id': 'user_id',
                              'name': 'user_name'}, inplace=True)

    user_info['request_date'] = pd.to_datetime(user_info['request_date'])

    print(user_info.to_string())

    # # # # # # # # # # # # # # # # # # # # # # # # # Get anime info # # # # # # # # # # # # # # # # # # # # # # # # #

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
        time.sleep(5)

        page_df = pd.json_normalize(response_ids, record_path=['data', 'Page', 'media'])
        anime_info = pd.concat([anime_info, page_df], ignore_index=True)

        if not response_ids['data']['Page']['pageInfo']['hasNextPage']:
            break

        variables_anime['page'] += 1

    anime_info.rename(columns={'averageScore': 'average_score',
                               'title.romaji': 'title_romaji',
                               'id': 'anime_id'}, inplace=True)

    print(anime_info.to_string())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Merge dataframes to calculate avg. score diff, least popular take, most popular take
    # GraphQL query to fetch the anime cover images for least and most popular takes
    # Use Jinja to insert these into HTML, e.g. {{ image1 }} in HTML, in flask image1=image_variable or something

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    load_dotenv(dotenv_path="F:/PyCharm Projects/project/.env")

    server = "anilist-sqlserver.database.windows.net"
    database = "anilist-db"
    connection_string = os.getenv('AZURE_ODBC')

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

