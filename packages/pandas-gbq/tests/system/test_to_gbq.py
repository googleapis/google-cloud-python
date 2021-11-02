# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import functools
import random

import pandas
import pandas.testing
import pytest


pytest.importorskip("google.cloud.bigquery", minversion="1.24.0")


@pytest.fixture
def method_under_test(credentials, project_id):
    import pandas_gbq

    return functools.partial(
        pandas_gbq.to_gbq, project_id=project_id, credentials=credentials
    )


@pytest.mark.parametrize(
    ["input_series"],
    [
        # Ensure that 64-bit floating point numbers are unchanged.
        # See: https://github.com/pydata/pandas-gbq/issues/326
        (
            pandas.Series(
                [
                    0.14285714285714285,
                    0.4406779661016949,
                    1.05148,
                    1.05153,
                    1.8571428571428572,
                    2.718281828459045,
                    3.141592653589793,
                    2.0988936657440586e43,
                ],
                name="test_col",
            ),
        ),
        (
            pandas.Series(
                [
                    "abc",
                    "defg",
                    # Ensure that empty strings are written as empty string,
                    # not NULL. See:
                    # https://github.com/googleapis/python-bigquery-pandas/issues/366
                    "",
                    None,
                    # Ensure that unicode characters are encoded. See:
                    # https://github.com/googleapis/python-bigquery-pandas/issues/106
                    "信用卡",
                    "Skywalker™",
                    "hülle",
                ],
                name="test_col",
            ),
        ),
    ],
)
def test_series_round_trip(
    method_under_test, random_dataset_id, bigquery_client, input_series
):
    table_id = f"{random_dataset_id}.round_trip_{random.randrange(1_000_000)}"
    input_series = input_series.sort_values().reset_index(drop=True)
    df = pandas.DataFrame(
        # Some errors only occur in multi-column dataframes. See:
        # https://github.com/googleapis/python-bigquery-pandas/issues/366
        {"test_col": input_series, "test_col2": input_series}
    )
    method_under_test(df, table_id)

    round_trip = bigquery_client.list_rows(table_id).to_dataframe()
    round_trip_series = round_trip["test_col"].sort_values().reset_index(drop=True)
    pandas.testing.assert_series_equal(
        round_trip_series, input_series, check_exact=True,
    )
