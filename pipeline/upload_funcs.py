import pandas as pd
from sqlalchemy import engine, text


def upload_one_to_one(
    df: pd.DataFrame,
    table_name: str,
    primary_key: str,
    column_1: str,
    column_2: str,
    engine: engine.base.Engine,
) -> None:
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

def upload_many_to_many(
    df: pd.DataFrame,
    table_name: str,
    foreign_key_1: str,
    foreign_key_2: str,
    column_1: str,
    anilist_id: int,
    engine: engine.base.Engine,
) -> None:
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
