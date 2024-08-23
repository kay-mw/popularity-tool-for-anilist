import os
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine


def get_user_count():
    def sql_init() -> Engine:
        load_dotenv()
        connection_string = os.environ["AZURE_ODBC"]
        connection_url = (
            f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
        )
        engine = create_engine(connection_url)
        return engine

    engine = sql_init()
    with engine.connect() as connection:
        query_user = """
            SELECT
                COUNT(user_id) as user_count
            FROM
                user_info;
        """
        result = pd.read_sql(query_user, connection)

    user_count = result["user_count"][0]
    return user_count
