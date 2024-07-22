class FetchAnimeDataByUser:
    def __init__(self, username):
        self.username = username
        self.cover_image_1 = None
        self.cover_image_2 = None
        self.score_max = None
        self.score_min = None
        self.avg_max = None
        self.avg_min = None
        self.title_max = None
        self.title_min = None
        self.avg_score_diff = None
        self.true_score_diff = None

    def fetch_data(self):
        import asyncio
        import os
        from urllib.parse import quote_plus

        import aiohttp
        import great_expectations as ge
        import pandas as pd
        import requests
        from dotenv import load_dotenv
        from sqlalchemy import create_engine, text

        def load_query(file_name):
            file_path = os.path.join("./app/api_request/", file_name)
            with open(file_path, "r") as file:
                return file.read()

        def fetch_anilist_data(query, variables):
            try:
                response = requests.post(
                    url, json={"query": query, "variables": variables}, timeout=10
                )
                response.raise_for_status()
                global response_header
                response_header = response.headers["Date"]
                response_header = pd.Series(response_header)
                return response.json()
            except requests.exceptions.Timeout:
                print("Request timed out.")
                return None
            except requests.exceptions.RequestException as e:
                print(f"Error in request: {e}")
                return None

        async def fetch_anilist_data_async(query, variables):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url, json={"query": query, "variables": variables}, timeout=10
                    ) as response:
                        response.raise_for_status()
                        global response_header
                        response_header = response.headers["Date"]
                        response_header = pd.Series(response_header)
                        return await response.json()
            except asyncio.TimeoutError:
                print("Request timed out.")
                return None
            except aiohttp.ClientResponseError as e:
                print(f"Error in request: {e}")
                return None

        query_get_id = load_query("get_id.gql")

        variables_get_id = {"name": self.username}

        url = "https://graphql.anilist.co"

        json_response = fetch_anilist_data(query_get_id, variables_get_id)
        anilist_id = json_response["data"]["User"]["id"]

        # # # # # # # # # # # # # # # # # # # # #

        query_user = load_query("user_query.gql")

        variables_user = {"page": 1, "id": anilist_id}

        json_response = fetch_anilist_data(query_user, variables_user)

        user_score = pd.json_normalize(
            json_response,
            record_path=["data", "Page", "users", "statistics", "anime", "scores"],
            meta=[["data", "Page", "users", "id"]],
        )

        user_score = user_score.explode("mediaIds", ignore_index=True)
        user_score["mediaIds"] = user_score["mediaIds"].astype(int)

        user_score.rename(
            columns={
                "mediaIds": "anime_id",
                "data.Page.users.id": "user_id",
                "id": "anime_id",
                "score": "user_score",
            },
            inplace=True,
        )

        if max(user_score["user_score"]) <= 10:
            user_score["user_score"] = user_score["user_score"].apply(lambda x: x * 10)
        else:
            pass

        # # # # # # # # # # # # # # # # # # # # # # # # Make user info table # # # # # # # # # # # # # # # # # # # # #

        user_info = pd.json_normalize(
            json_response, record_path=["data", "Page", "users"]
        )
        user_info.drop("statistics.anime.scores", axis=1, inplace=True)

        user_info = pd.concat([user_info, response_header], axis=1)
        user_info.rename(
            columns={0: "request_date", "id": "user_id", "name": "user_name"},
            inplace=True,
        )

        user_info["request_date"] = pd.to_datetime(
            user_info["request_date"], format="%a, %d %b %Y %H:%M:%S %Z"
        ).dt.tz_localize(None)

        # # # # # # # # # # # # # # # # # # # # # # # # # Get anime info # # # # # # # # # # # # # # # # # # # # # # #

        async def main():
            anime_info = pd.DataFrame()

            id_list = user_score["anime_id"].values.tolist()

            variables_anime = {"page": 1, "id_in": id_list}

            query_anime = load_query("anime_query.gql")

            while True:
                response_ids = await fetch_anilist_data_async(
                    query_anime, variables_anime
                )

                page_df = pd.json_normalize(
                    response_ids, record_path=["data", "Page", "media"]
                )
                anime_info = pd.concat([anime_info, page_df], ignore_index=True)

                if not response_ids["data"]["Page"]["pageInfo"]["hasNextPage"]:
                    break

                variables_anime["page"] += 1

            return anime_info

        anime_info = asyncio.run(main())

        anime_info.rename(
            columns={
                "averageScore": "average_score",
                "title.romaji": "title_romaji",
                "id": "anime_id",
            },
            inplace=True,
        )

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        merged_dfs = user_score.merge(anime_info, on="anime_id", how="left")

        merged_dfs["score_diff"] = (
            merged_dfs["user_score"] - merged_dfs["average_score"]
        )

        float_avg_score_diff = abs(merged_dfs.loc[:, "score_diff"]).mean()
        self.avg_score_diff = round(float_avg_score_diff, 2)

        float_true_score_diff = merged_dfs.loc[:, "score_diff"].mean()
        self.true_score_diff = round(float_true_score_diff, 2)

        max_diff = merged_dfs.loc[
            merged_dfs["score_diff"].abs() == max(merged_dfs["score_diff"].abs())
        ]
        min_diff = merged_dfs.loc[
            merged_dfs["score_diff"].abs() == min(merged_dfs["score_diff"].abs())
        ]

        self.score_max = int(max_diff["user_score"].iloc[0])
        self.score_min = int(min_diff["user_score"].iloc[0])

        self.avg_max = int(max_diff["average_score"].iloc[0])
        self.avg_min = int(min_diff["average_score"].iloc[0])

        self.title_max = max_diff["title_romaji"].iloc[0]
        self.title_min = min_diff["title_romaji"].iloc[0]

        image_id_1 = int(max_diff["anime_id"].iloc[0])
        image_id_2 = int(min_diff["anime_id"].iloc[0])

        query_image = load_query("image_query.gql")

        variables_image_1 = {"id": image_id_1}
        variables_image_2 = {"id": image_id_2}

        cover_image_1 = fetch_anilist_data(query_image, variables_image_1)
        cover_image_2 = fetch_anilist_data(query_image, variables_image_2)

        self.cover_image_1 = cover_image_1["data"]["Media"]["coverImage"]["extraLarge"]
        self.cover_image_2 = cover_image_2["data"]["Media"]["coverImage"]["extraLarge"]

        # # # # # # # # # # # # # # # # # # # # # # # Data Quality Checks # # # # # # # # # # # # # # # # # # # # # # #

        ge_anime_info = ge.from_pandas(anime_info)
        ge_user_info = ge.from_pandas(user_info)
        ge_user_score = ge.from_pandas(user_score)

        ge_anime_info.expect_column_values_to_be_unique("anime_id")
        ge_anime_info.expect_column_values_to_not_be_null("anime_id")
        ge_anime_info.expect_column_max_to_be_between("average_score", 0, 100)
        anime_info_suite = ge_anime_info.get_expectation_suite()

        ge_user_score.expect_column_values_to_be_unique("anime_id")
        ge_user_score.expect_column_values_to_not_be_null("anime_id")
        ge_user_score.expect_column_max_to_be_between("user_score", 0, 100)
        user_score_suite = ge_user_score.get_expectation_suite()

        ge_user_info.expect_column_values_to_be_unique("user_id")
        ge_user_info.expect_column_values_to_not_be_null("user_id")
        user_info_suite = ge_user_info.get_expectation_suite()

        anime_info_results = ge_anime_info.validate(expectation_suite=anime_info_suite)
        user_score_results = ge_user_score.validate(expectation_suite=user_score_suite)
        user_info_results = ge_user_info.validate(expectation_suite=user_info_suite)

        all_ge_results = anime_info_results, user_score_results, user_info_results

        for results in all_ge_results:
            assert results["success"], "Failure: Some Data Quality Check(s) Failed"

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        load_dotenv()
        connection_string = os.environ["AZURE_ODBC"]

        params = quote_plus(connection_string)
        connection_url = f"mssql+pyodbc:///?odbc_connect={params}"
        engine = create_engine(connection_url)

        def upload_table(primary_key, table_name, df, column_1, column_2):
            with engine.connect() as connection:
                df.to_sql("temp_table", con=connection, if_exists="replace")

                query = (
                    f"MERGE {table_name} AS target USING temp_table AS source "
                    f"ON source.{primary_key} = target.{primary_key} "
                    f"WHEN NOT MATCHED BY target THEN INSERT ({primary_key}, {column_1}, {column_2}) "
                    f"VALUES (source.{primary_key}, source.{column_1}, source.{column_2}) "
                    f"WHEN MATCHED THEN UPDATE "
                    f"SET target.{column_1} = source.{column_1}, "
                    f"target.{column_2} = source.{column_2};"
                )
                connection.execute(text(query))
                connection.commit()

        upload_table(
            "anime_id", "anime_info", anime_info, "average_score", "title_romaji"
        )
        upload_table("user_id", "user_info", user_info, "user_name", "request_date")

        def upload_user_score(df, table_name, foreign_key_1, foreign_key_2, column_1):
            check_query = f"SELECT {foreign_key_1}, {foreign_key_2}, {column_1} FROM {table_name} WHERE {foreign_key_1} = {anilist_id};"

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
                query = f"DELETE FROM {table_name} WHERE {foreign_key_1} = {anilist_id}"
                with engine.connect() as connection:
                    connection.execute(text(query))
                    connection.commit()

                with engine.connect() as connection:
                    df.to_sql(
                        name=f"{table_name}",
                        con=connection,
                        if_exists="append",
                        index=False,
                    )

        upload_user_score(
            user_score, "user_anime_score", "user_id", "anime_id", "user_score"
        )
