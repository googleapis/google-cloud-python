# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import decimal
from unittest import mock

import pyarrow
import pytest

from google.cloud import bigquery

pandas = pytest.importorskip("pandas")


TEST_PATH = "/v1/project/test-proj/dataset/test-dset/table/test-tbl/data"


@pytest.fixture
def class_under_test():
    from google.cloud.bigquery.table import RowIterator

    return RowIterator


def test_to_dataframe_nullable_scalars(monkeypatch, class_under_test):
    # See tests/system/test_arrow.py for the actual types we get from the API.
    arrow_schema = pyarrow.schema(
        [
            pyarrow.field("bignumeric_col", pyarrow.decimal256(76, scale=38)),
            pyarrow.field("bool_col", pyarrow.bool_()),
            pyarrow.field("bytes_col", pyarrow.binary()),
            pyarrow.field("date_col", pyarrow.date32()),
            pyarrow.field("datetime_col", pyarrow.timestamp("us", tz=None)),
            pyarrow.field("float64_col", pyarrow.float64()),
            pyarrow.field("int64_col", pyarrow.int64()),
            pyarrow.field("numeric_col", pyarrow.decimal128(38, scale=9)),
            pyarrow.field("string_col", pyarrow.string()),
            pyarrow.field("time_col", pyarrow.time64("us")),
            pyarrow.field(
                "timestamp_col", pyarrow.timestamp("us", tz=datetime.timezone.utc)
            ),
        ]
    )
    arrow_table = pyarrow.Table.from_pydict(
        {
            "bignumeric_col": [decimal.Decimal("123.456789101112131415")],
            "bool_col": [True],
            "bytes_col": [b"Hello,\x00World!"],
            "date_col": [datetime.date(2021, 8, 9)],
            "datetime_col": [datetime.datetime(2021, 8, 9, 13, 30, 44, 123456)],
            "float64_col": [1.25],
            "int64_col": [-7],
            "numeric_col": [decimal.Decimal("-123.456789")],
            "string_col": ["abcdefg"],
            "time_col": [datetime.time(14, 21, 17, 123456)],
            "timestamp_col": [
                datetime.datetime(
                    2021, 8, 9, 13, 30, 44, 123456, tzinfo=datetime.timezone.utc
                )
            ],
        },
        schema=arrow_schema,
    )

    nullable_schema = [
        bigquery.SchemaField("bignumeric_col", "BIGNUMERIC"),
        bigquery.SchemaField("bool_col", "BOOLEAN"),
        bigquery.SchemaField("bytes_col", "BYTES"),
        bigquery.SchemaField("date_col", "DATE"),
        bigquery.SchemaField("datetime_col", "DATETIME"),
        bigquery.SchemaField("float64_col", "FLOAT"),
        bigquery.SchemaField("int64_col", "INT64"),
        bigquery.SchemaField("numeric_col", "NUMERIC"),
        bigquery.SchemaField("string_col", "STRING"),
        bigquery.SchemaField("time_col", "TIME"),
        bigquery.SchemaField("timestamp_col", "TIMESTAMP"),
    ]
    mock_client = mock.create_autospec(bigquery.Client)
    mock_client.project = "test-proj"
    mock_api_request = mock.Mock()
    mock_to_arrow = mock.Mock()
    mock_to_arrow.return_value = arrow_table
    rows = class_under_test(mock_client, mock_api_request, TEST_PATH, nullable_schema)
    monkeypatch.setattr(rows, "to_arrow", mock_to_arrow)
    df = rows.to_dataframe()

    # Check for expected dtypes.
    # Keep these in sync with tests/system/test_pandas.py
    assert df.dtypes["bignumeric_col"].name == "object"
    assert df.dtypes["bool_col"].name == "boolean"
    assert df.dtypes["bytes_col"].name == "object"
    assert df.dtypes["date_col"].name == "dbdate"
    assert df.dtypes["datetime_col"].name == "datetime64[ns]"
    assert df.dtypes["float64_col"].name == "float64"
    assert df.dtypes["int64_col"].name == "Int64"
    assert df.dtypes["numeric_col"].name == "object"
    assert df.dtypes["string_col"].name == "object"
    assert df.dtypes["time_col"].name == "dbtime"
    assert df.dtypes["timestamp_col"].name == "datetime64[ns, UTC]"

    # Check for expected values.
    assert df["bignumeric_col"][0] == decimal.Decimal("123.456789101112131415")
    assert df["bool_col"][0]  # True
    assert df["bytes_col"][0] == b"Hello,\x00World!"

    # object is used by default, but we can use "datetime64[ns]" automatically
    # when data is within the supported range.
    # https://github.com/googleapis/python-bigquery/issues/861
    assert df["date_col"][0] == datetime.date(2021, 8, 9)

    assert df["datetime_col"][0] == pandas.to_datetime("2021-08-09 13:30:44.123456")
    assert df["float64_col"][0] == 1.25
    assert df["int64_col"][0] == -7
    assert df["numeric_col"][0] == decimal.Decimal("-123.456789")
    assert df["string_col"][0] == "abcdefg"

    # Pandas timedelta64 might be a better choice for pandas time columns. Then
    # they can more easily be combined with date columns to form datetimes.
    # https://github.com/googleapis/python-bigquery/issues/862
    assert df["time_col"][0] == datetime.time(14, 21, 17, 123456)

    assert df["timestamp_col"][0] == pandas.to_datetime("2021-08-09 13:30:44.123456Z")


def test_to_dataframe_nullable_scalars_with_custom_dtypes(
    monkeypatch, class_under_test
):
    """Passing in explicit dtypes is merged with default behavior."""
    arrow_schema = pyarrow.schema(
        [
            pyarrow.field("int64_col", pyarrow.int64()),
            pyarrow.field("other_int_col", pyarrow.int64()),
        ]
    )
    arrow_table = pyarrow.Table.from_pydict(
        {"int64_col": [1000], "other_int_col": [-7]},
        schema=arrow_schema,
    )

    nullable_schema = [
        bigquery.SchemaField("int64_col", "INT64"),
        bigquery.SchemaField("other_int_col", "INT64"),
    ]
    mock_client = mock.create_autospec(bigquery.Client)
    mock_client.project = "test-proj"
    mock_api_request = mock.Mock()
    mock_to_arrow = mock.Mock()
    mock_to_arrow.return_value = arrow_table
    rows = class_under_test(mock_client, mock_api_request, TEST_PATH, nullable_schema)
    monkeypatch.setattr(rows, "to_arrow", mock_to_arrow)
    df = rows.to_dataframe(dtypes={"other_int_col": "int8"})

    assert df.dtypes["int64_col"].name == "Int64"
    assert df["int64_col"][0] == 1000

    assert df.dtypes["other_int_col"].name == "int8"
    assert df["other_int_col"][0] == -7


def test_to_dataframe_arrays(monkeypatch, class_under_test):
    arrow_schema = pyarrow.schema(
        [pyarrow.field("int64_repeated", pyarrow.list_(pyarrow.int64()))]
    )
    arrow_table = pyarrow.Table.from_pydict(
        {"int64_repeated": [[-1, 0, 2]]},
        schema=arrow_schema,
    )

    nullable_schema = [
        bigquery.SchemaField("int64_repeated", "INT64", mode="REPEATED"),
    ]
    mock_client = mock.create_autospec(bigquery.Client)
    mock_client.project = "test-proj"
    mock_api_request = mock.Mock()
    mock_to_arrow = mock.Mock()
    mock_to_arrow.return_value = arrow_table
    rows = class_under_test(mock_client, mock_api_request, TEST_PATH, nullable_schema)
    monkeypatch.setattr(rows, "to_arrow", mock_to_arrow)
    df = rows.to_dataframe()

    assert df.dtypes["int64_repeated"].name == "object"
    assert tuple(df["int64_repeated"][0]) == (-1, 0, 2)
