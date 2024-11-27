import great_expectations as ge
import pandas
import pytest
from api.main import fetch_data


@pytest.fixture
def dfs():
    dfs, _, _ = fetch_data(username="keejan", format="anime")
    return dfs


def test_exists(dfs):
    for df in dfs:
        assert df.empty == False, "DataFrame is empty."


def test_data(dfs):
    ge_anime_info, ge_user_info, ge_user_anime_score = [
        ge.from_pandas(df) for df in dfs
    ]

    ge_anime_info.expect_column_values_to_not_be_null("anime_id")
    ge_anime_info.expect_column_max_to_be_between("average_score", 0, 100)

    ge_user_anime_score.expect_column_values_to_be_unique("anime_id")
    ge_user_anime_score.expect_column_values_to_not_be_null("anime_id")
    ge_user_anime_score.expect_column_max_to_be_between("user_score", 0, 100)

    ge_user_info.expect_column_values_to_be_unique("user_id")
    ge_user_info.expect_column_values_to_not_be_null("user_id")

    ge_dfs = [ge_anime_info, ge_user_info, ge_user_anime_score]
    for ge_df in ge_dfs:
        suite = ge_df.get_expectation_suite(discard_failed_expectations=False)
        result = ge_df.validate(expectation_suite=suite)
        assert result[
            "success"
        ], f"Failure: Some Data Quality Check(s) Failed, {result}"
