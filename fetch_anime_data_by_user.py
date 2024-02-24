def fetch_data(anilist_id):
    import os
    import time
    from urllib.parse import quote_plus

    import pandas as pd
    import requests
    from dotenv import load_dotenv
    from sqlalchemy import create_engine, inspect, exc
    from sqlalchemy.orm import sessionmaker

    def load_query(file_name):
        file_path = os.path.join("./", file_name)
        with open(file_path, "r") as file:
            return file.read()

    def fetch_anilist_data(query, variables):
        try:
            response = requests.post(URL, json={'query': query, 'variables': variables}, timeout=10)
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

    QUERY_USER = load_query("user_query.gql")

    variables_user = {
        "page": 1,
        "id": anilist_id
    }

    URL = 'https://graphql.anilist.co'

    json_response = fetch_anilist_data(QUERY_USER, variables_user)

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

    QUERY_ANIME = load_query('anime_query.gql')

    id_list = user_score['anime_id'].values.tolist()

    variables_anime = {
        "page": 1,
        "id_in": id_list
    }

    URL = 'https://graphql.anilist.co'

    anime_info = pd.DataFrame()

    while True:
        response_ids = fetch_anilist_data(QUERY_ANIME, variables_anime)
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
    load_dotenv(dotenv_path="F:/PyCharm Projects/project/.env")

    server = "anilist-sqlserver.database.windows.net"
    database = "anilist-db"
    connection_string = os.getenv('AZURE_ODBC')

    params = quote_plus(connection_string)
    connection_url = f"mssql+pyodbc:///?odbc_connect={params}"
    engine = create_engine(connection_url)

    Session = sessionmaker(bind=engine)
    session = Session()

    df_list = [anime_info, user_info, user_score]
    table_names = ['anime_info', 'user_info', 'user_score']

    with engine.connect() as connection:
        for df, table_name in zip(df_list, table_names):
            try:
                print(f'Loading dataframe into table {table_name}')

                inspector = inspect(engine)
                table_exists = table_name in inspector.get_table_names(schema="dbo")

                if table_name == 'anime_info':
                    primary_key_column = 'anime_id'
                elif table_name == 'user_info' or table_name == 'user_score':
                    primary_key_column = 'user_id'
                else:
                    primary_key_column = None

                if table_exists:
                    existing_columns = inspector.get_columns(table_name, schema="dbo")
                    existing_column_names = [col['name'] for col in existing_columns]

                    if primary_key_column in existing_column_names:
                        existing_values = pd.read_sql(
                            f"SELECT {primary_key_column} FROM {table_name}", engine
                        )[primary_key_column].tolist()

                        new_rows = df[~df[primary_key_column].isin(existing_values)]

                        new_rows.to_sql(table_name, engine, if_exists='append', index=False)

                        df[df[primary_key_column].isin(existing_values)].to_sql(
                            table_name, engine, if_exists='replace', index=False
                        )
                    else:
                        df.to_sql(table_name, engine, if_exists='append', index=False)
                else:
                    df.to_sql(table_name, engine, if_exists='append', index=False)
            except (exc.IntegrityError, exc.DataError) as e:
                print(f'Error loading dataframe into table {table_name}: {str(e)}')
