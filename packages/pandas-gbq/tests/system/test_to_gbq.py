# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import datetime
import decimal
import collections
import random

import db_dtypes
import pandas
import pandas.testing
import pytest


pytest.importorskip("google.cloud.bigquery", minversion="1.24.0")


@pytest.fixture(params=["load_parquet", "load_csv"])
def api_method(request):
    return request.param


@pytest.fixture
def method_under_test(to_gbq):
    return to_gbq


SeriesRoundTripTestCase = collections.namedtuple(
    "SeriesRoundTripTestCase",
    ["input_series", "api_methods"],
    defaults=[None, {"load_csv", "load_parquet"}],
)


@pytest.mark.parametrize(
    ["input_series", "api_methods"],
    [
        # Ensure that 64-bit floating point numbers are unchanged.
        # See: https://github.com/pydata/pandas-gbq/issues/326
        SeriesRoundTripTestCase(
            input_series=pandas.Series(
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
        SeriesRoundTripTestCase(
            input_series=pandas.Series(
                [
                    "abc",
                    "defg",
                    # Ensure that unicode characters are encoded. See:
                    # https://github.com/googleapis/python-bigquery-pandas/issues/106
                    "信用卡",
                    "Skywalker™",
                    "hülle",
                ],
                name="test_col",
            ),
        ),
        SeriesRoundTripTestCase(
            input_series=pandas.Series(
                [
                    "abc",
                    "defg",
                    # Ensure that empty strings are written as empty string,
                    # not NULL. See:
                    # https://github.com/googleapis/python-bigquery-pandas/issues/366
                    "",
                    None,
                ],
                name="empty_strings",
            ),
            # BigQuery CSV loader uses empty string as the "null marker" by
            # default. Potentially one could choose a rarely used character or
            # string as the null marker to disambiguate null from empty string,
            # but then that string couldn't be loaded.
            # TODO: Revist when custom load job configuration is supported.
            #       https://github.com/googleapis/python-bigquery-pandas/issues/425
            api_methods={"load_parquet"},
        ),
    ],
)
def test_series_round_trip(
    method_under_test,
    random_dataset_id,
    read_gbq,
    input_series,
    api_method,
    api_methods,
):
    if api_method not in api_methods:
        pytest.skip(f"{api_method} not supported.")
    table_id = f"{random_dataset_id}.round_trip_{random.randrange(1_000_000)}"
    input_series = input_series.sort_values().reset_index(drop=True)
    df = pandas.DataFrame(
        # Some errors only occur in multi-column dataframes. See:
        # https://github.com/googleapis/python-bigquery-pandas/issues/366
        {"test_col": input_series, "test_col2": input_series}
    )
    method_under_test(df, table_id, api_method=api_method)

    round_trip = read_gbq(table_id)
    round_trip_series = round_trip["test_col"].sort_values().reset_index(drop=True)
    pandas.testing.assert_series_equal(
        round_trip_series, input_series, check_exact=True, check_names=False,
    )


DataFrameRoundTripTestCase = collections.namedtuple(
    "DataFrameRoundTripTestCase",
    ["input_df", "expected_df", "table_schema", "api_methods"],
    defaults=[None, None, [], {"load_csv", "load_parquet"}],
)

DATAFRAME_ROUND_TRIPS = [
    # Ensure that a DATE column can be written with datetime64[ns] dtype
    # data. See:
    # https://github.com/googleapis/python-bigquery-pandas/issues/362
    DataFrameRoundTripTestCase(
        input_df=pandas.DataFrame(
            {
                "row_num": [0, 1, 2],
                "date_col": pandas.Series(
                    ["2021-04-17", "1999-12-31", "2038-01-19"], dtype="datetime64[ns]",
                ),
            }
        ),
        table_schema=[{"name": "date_col", "type": "DATE"}],
        # Skip CSV because the pandas CSV writer includes time when writing
        # datetime64 values.
        api_methods={"load_parquet"},
    ),
    DataFrameRoundTripTestCase(
        input_df=pandas.DataFrame(
            {
                "row_num": [0, 1, 2],
                "date_col": pandas.Series(
                    ["2021-04-17", "1999-12-31", "2038-01-19"],
                    dtype=db_dtypes.DateDtype(),
                ),
            }
        ),
        table_schema=[{"name": "date_col", "type": "DATE"}],
    ),
    # Loading a DATE column should work for string objects. See:
    # https://github.com/googleapis/python-bigquery-pandas/issues/421
    DataFrameRoundTripTestCase(
        input_df=pandas.DataFrame(
            {"row_num": [123], "date_col": ["2021-12-12"]},
            columns=["row_num", "date_col"],
        ),
        expected_df=pandas.DataFrame(
            {
                "row_num": [123],
                "date_col": pandas.Series(
                    [datetime.date(2021, 12, 12)], dtype=db_dtypes.DateDtype()
                ),
            },
            columns=["row_num", "date_col"],
        ),
        table_schema=[
            {"name": "row_num", "type": "INTEGER"},
            {"name": "date_col", "type": "DATE"},
        ],
    ),
    # Loading a NUMERIC column should work for floating point objects. See:
    # https://github.com/googleapis/python-bigquery-pandas/issues/421
    DataFrameRoundTripTestCase(
        input_df=pandas.DataFrame(
            {"row_num": [123], "num_col": [1.25]}, columns=["row_num", "num_col"],
        ),
        expected_df=pandas.DataFrame(
            {"row_num": [123], "num_col": [decimal.Decimal("1.25")]},
            columns=["row_num", "num_col"],
        ),
        table_schema=[
            {"name": "row_num", "type": "INTEGER"},
            {"name": "num_col", "type": "NUMERIC"},
        ],
    ),
    pytest.param(
        *DataFrameRoundTripTestCase(
            input_df=pandas.DataFrame(
                {
                    "row_num": [1, 2, 3],
                    # DATE valuess outside the pandas range for timestamp
                    # aren't supported by the db-dtypes package.
                    # https://github.com/googleapis/python-bigquery-pandas/issues/441
                    "date_col": [
                        datetime.date(1, 1, 1),
                        datetime.date(1970, 1, 1),
                        datetime.date(9999, 12, 31),
                    ],
                    # DATETIME values outside of the range for pandas timestamp
                    # require `date_as_object` parameter in
                    # google-cloud-bigquery versions 1.x and 2.x, but not 3.x.
                    # https://github.com/googleapis/python-bigquery-pandas/issues/365
                    "datetime_col": [
                        datetime.datetime(1, 1, 1),
                        datetime.datetime(1970, 1, 1),
                        datetime.datetime(9999, 12, 31, 23, 59, 59, 999999),
                    ],
                    "timestamp_col": [
                        datetime.datetime(1, 1, 1, tzinfo=datetime.timezone.utc),
                        datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc),
                        datetime.datetime(
                            9999,
                            12,
                            31,
                            23,
                            59,
                            59,
                            999999,
                            tzinfo=datetime.timezone.utc,
                        ),
                    ],
                },
                columns=["row_num", "date_col", "datetime_col", "timestamp_col"],
            ),
            table_schema=[
                {"name": "row_num", "type": "INTEGER"},
                {"name": "date_col", "type": "DATE"},
                {"name": "datetime_col", "type": "DATETIME"},
                {"name": "timestamp_col", "type": "TIMESTAMP"},
            ],
        ),
        id="issue365-extreme-datetimes",
    ),
]


@pytest.mark.parametrize(
    ["input_df", "expected_df", "table_schema", "api_methods"], DATAFRAME_ROUND_TRIPS
)
def test_dataframe_round_trip_with_table_schema(
    method_under_test,
    read_gbq,
    random_dataset_id,
    input_df,
    expected_df,
    table_schema,
    api_method,
    api_methods,
):
    if api_method not in api_methods:
        pytest.skip(f"{api_method} not supported.")
    if expected_df is None:
        expected_df = input_df
    table_id = f"{random_dataset_id}.round_trip_w_schema_{random.randrange(1_000_000)}"
    method_under_test(
        input_df, table_id, table_schema=table_schema, api_method=api_method
    )
    round_trip = read_gbq(
        table_id,
        dtypes=dict(zip(expected_df.columns, expected_df.dtypes)),
        # BigQuery Storage API is required to avoid out-of-bound due to extra
        # day from rounding error which was fixed in google-cloud-bigquery
        # 2.6.0. https://github.com/googleapis/python-bigquery/pull/402
        use_bqstorage_api=True,
    )
    round_trip.sort_values("row_num", inplace=True)
    pandas.testing.assert_frame_equal(expected_df, round_trip)
