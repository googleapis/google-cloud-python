# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""System tests for pandas connector."""

import collections
import datetime
import decimal
import json
import io
import operator

import google.api_core.retry
import pkg_resources
import pytest

from google.cloud import bigquery
from . import helpers


bigquery_storage = pytest.importorskip(
    "google.cloud.bigquery_storage", minversion="2.0.0"
)
pandas = pytest.importorskip("pandas", minversion="0.23.0")
pyarrow = pytest.importorskip("pyarrow", minversion="1.0.0")


PANDAS_INSTALLED_VERSION = pkg_resources.get_distribution("pandas").parsed_version
PANDAS_INT64_VERSION = pkg_resources.parse_version("1.0.0")


class MissingDataError(Exception):
    pass


def test_load_table_from_dataframe_w_automatic_schema(bigquery_client, dataset_id):
    """Test that a DataFrame with dtypes that map well to BigQuery types
    can be uploaded without specifying a schema.

    https://github.com/googleapis/google-cloud-python/issues/9044
    """
    df_data = collections.OrderedDict(
        [
            ("bool_col", pandas.Series([True, False, True], dtype="bool")),
            (
                "ts_col",
                pandas.Series(
                    [
                        datetime.datetime(2010, 1, 2, 3, 44, 50),
                        datetime.datetime(2011, 2, 3, 14, 50, 59),
                        datetime.datetime(2012, 3, 14, 15, 16),
                    ],
                    dtype="datetime64[ns]",
                ).dt.tz_localize(datetime.timezone.utc),
            ),
            (
                "dt_col",
                pandas.Series(
                    [
                        datetime.datetime(2010, 1, 2, 3, 44, 50),
                        datetime.datetime(2011, 2, 3, 14, 50, 59),
                        datetime.datetime(2012, 3, 14, 15, 16),
                    ],
                    dtype="datetime64[ns]",
                ),
            ),
            ("float32_col", pandas.Series([1.0, 2.0, 3.0], dtype="float32")),
            ("float64_col", pandas.Series([4.0, 5.0, 6.0], dtype="float64")),
            ("int8_col", pandas.Series([-12, -11, -10], dtype="int8")),
            ("int16_col", pandas.Series([-9, -8, -7], dtype="int16")),
            ("int32_col", pandas.Series([-6, -5, -4], dtype="int32")),
            ("int64_col", pandas.Series([-3, -2, -1], dtype="int64")),
            ("uint8_col", pandas.Series([0, 1, 2], dtype="uint8")),
            ("uint16_col", pandas.Series([3, 4, 5], dtype="uint16")),
            ("uint32_col", pandas.Series([6, 7, 8], dtype="uint32")),
        ]
    )
    dataframe = pandas.DataFrame(df_data, columns=df_data.keys())

    table_id = "{}.{}.load_table_from_dataframe_w_automatic_schema".format(
        bigquery_client.project, dataset_id
    )

    load_job = bigquery_client.load_table_from_dataframe(dataframe, table_id)
    load_job.result()

    table = bigquery_client.get_table(table_id)
    assert tuple(table.schema) == (
        bigquery.SchemaField("bool_col", "BOOLEAN"),
        bigquery.SchemaField("ts_col", "TIMESTAMP"),
        # BigQuery does not support uploading DATETIME values from
        # Parquet files. See:
        # https://github.com/googleapis/google-cloud-python/issues/9996
        bigquery.SchemaField("dt_col", "TIMESTAMP"),
        bigquery.SchemaField("float32_col", "FLOAT"),
        bigquery.SchemaField("float64_col", "FLOAT"),
        bigquery.SchemaField("int8_col", "INTEGER"),
        bigquery.SchemaField("int16_col", "INTEGER"),
        bigquery.SchemaField("int32_col", "INTEGER"),
        bigquery.SchemaField("int64_col", "INTEGER"),
        bigquery.SchemaField("uint8_col", "INTEGER"),
        bigquery.SchemaField("uint16_col", "INTEGER"),
        bigquery.SchemaField("uint32_col", "INTEGER"),
    )
    assert table.num_rows == 3


@pytest.mark.skipif(
    PANDAS_INSTALLED_VERSION < PANDAS_INT64_VERSION,
    reason="Only `pandas version >=1.0.0` is supported",
)
def test_load_table_from_dataframe_w_nullable_int64_datatype(
    bigquery_client, dataset_id
):
    """Test that a DataFrame containing column with None-type values and int64 datatype
    can be uploaded if a BigQuery schema is specified.

    https://github.com/googleapis/python-bigquery/issues/22
    """
    table_id = "{}.{}.load_table_from_dataframe_w_nullable_int64_datatype".format(
        bigquery_client.project, dataset_id
    )
    table_schema = (bigquery.SchemaField("x", "INTEGER", mode="NULLABLE"),)
    table = helpers.retry_403(bigquery_client.create_table)(
        bigquery.Table(table_id, schema=table_schema)
    )

    df_data = collections.OrderedDict(
        [("x", pandas.Series([1, 2, None, 4], dtype="Int64"))]
    )
    dataframe = pandas.DataFrame(df_data, columns=df_data.keys())
    load_job = bigquery_client.load_table_from_dataframe(dataframe, table_id)
    load_job.result()
    table = bigquery_client.get_table(table_id)
    assert tuple(table.schema) == (bigquery.SchemaField("x", "INTEGER"),)
    assert table.num_rows == 4


@pytest.mark.skipif(
    PANDAS_INSTALLED_VERSION < PANDAS_INT64_VERSION,
    reason="Only `pandas version >=1.0.0` is supported",
)
def test_load_table_from_dataframe_w_nullable_int64_datatype_automatic_schema(
    bigquery_client, dataset_id, table_id
):
    """Test that a DataFrame containing column with None-type values and int64 datatype
    can be uploaded without specifying a schema.

    https://github.com/googleapis/python-bigquery/issues/22
    """

    df_data = collections.OrderedDict(
        [("x", pandas.Series([1, 2, None, 4], dtype="Int64"))]
    )
    dataframe = pandas.DataFrame(df_data, columns=df_data.keys())
    load_job = bigquery_client.load_table_from_dataframe(dataframe, table_id)
    load_job.result()
    table = bigquery_client.get_table(table_id)
    assert tuple(table.schema) == (bigquery.SchemaField("x", "INTEGER"),)
    assert table.num_rows == 4


def test_load_table_from_dataframe_w_nulls(bigquery_client, dataset_id):
    """Test that a DataFrame with null columns can be uploaded if a
    BigQuery schema is specified.

    See: https://github.com/googleapis/google-cloud-python/issues/7370
    """
    # Schema with all scalar types.
    scalars_schema = (
        bigquery.SchemaField("bool_col", "BOOLEAN"),
        bigquery.SchemaField("bytes_col", "BYTES"),
        bigquery.SchemaField("date_col", "DATE"),
        bigquery.SchemaField("dt_col", "DATETIME"),
        bigquery.SchemaField("float_col", "FLOAT"),
        bigquery.SchemaField("geo_col", "GEOGRAPHY"),
        bigquery.SchemaField("int_col", "INTEGER"),
        bigquery.SchemaField("num_col", "NUMERIC"),
        bigquery.SchemaField("bignum_col", "BIGNUMERIC"),
        bigquery.SchemaField("str_col", "STRING"),
        bigquery.SchemaField("time_col", "TIME"),
        bigquery.SchemaField("ts_col", "TIMESTAMP"),
    )

    table_schema = scalars_schema + (
        # TODO: Array columns can't be read due to NULLABLE versus REPEATED
        #       mode mismatch. See:
        #       https://issuetracker.google.com/133415569#comment3
        # bigquery.SchemaField("array_col", "INTEGER", mode="REPEATED"),
        # TODO: Support writing StructArrays to Parquet. See:
        #       https://jira.apache.org/jira/browse/ARROW-2587
        # bigquery.SchemaField("struct_col", "RECORD", fields=scalars_schema),
    )
    num_rows = 100
    nulls = [None] * num_rows
    df_data = [
        ("bool_col", nulls),
        ("bytes_col", nulls),
        ("date_col", nulls),
        ("dt_col", nulls),
        ("float_col", nulls),
        ("geo_col", nulls),
        ("int_col", nulls),
        ("num_col", nulls),
        ("bignum_col", nulls),
        ("str_col", nulls),
        ("time_col", nulls),
        ("ts_col", nulls),
    ]
    df_data = collections.OrderedDict(df_data)
    dataframe = pandas.DataFrame(df_data, columns=df_data.keys())

    table_id = "{}.{}.load_table_from_dataframe_w_nulls".format(
        bigquery_client.project, dataset_id
    )

    # Create the table before loading so that schema mismatch errors are
    # identified.
    table = helpers.retry_403(bigquery_client.create_table)(
        bigquery.Table(table_id, schema=table_schema)
    )

    job_config = bigquery.LoadJobConfig(schema=table_schema)
    load_job = bigquery_client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )
    load_job.result()

    table = bigquery_client.get_table(table)
    assert tuple(table.schema) == table_schema
    assert table.num_rows == num_rows


def test_load_table_from_dataframe_w_required(bigquery_client, dataset_id):
    """Test that a DataFrame with required columns can be uploaded if a
    BigQuery schema is specified.

    See: https://github.com/googleapis/google-cloud-python/issues/8093
    """
    table_schema = (
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    )

    records = [{"name": "Chip", "age": 2}, {"name": "Dale", "age": 3}]
    dataframe = pandas.DataFrame(records, columns=["name", "age"])
    job_config = bigquery.LoadJobConfig(schema=table_schema)
    table_id = "{}.{}.load_table_from_dataframe_w_required".format(
        bigquery_client.project, dataset_id
    )

    # Create the table before loading so that schema mismatch errors are
    # identified.
    table = helpers.retry_403(bigquery_client.create_table)(
        bigquery.Table(table_id, schema=table_schema)
    )

    job_config = bigquery.LoadJobConfig(schema=table_schema)
    load_job = bigquery_client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )
    load_job.result()

    table = bigquery_client.get_table(table)
    assert tuple(table.schema) == table_schema
    assert table.num_rows == 2


def test_load_table_from_dataframe_w_explicit_schema(bigquery_client, dataset_id):
    # Schema with all scalar types.
    # See:
    #       https://github.com/googleapis/python-bigquery/issues/61
    #       https://issuetracker.google.com/issues/151765076
    scalars_schema = (
        bigquery.SchemaField("bool_col", "BOOLEAN"),
        bigquery.SchemaField("bytes_col", "BYTES"),
        bigquery.SchemaField("date_col", "DATE"),
        bigquery.SchemaField("dt_col", "DATETIME"),
        bigquery.SchemaField("float_col", "FLOAT"),
        bigquery.SchemaField("geo_col", "GEOGRAPHY"),
        bigquery.SchemaField("int_col", "INTEGER"),
        bigquery.SchemaField("num_col", "NUMERIC"),
        bigquery.SchemaField("bignum_col", "BIGNUMERIC"),
        bigquery.SchemaField("str_col", "STRING"),
        bigquery.SchemaField("time_col", "TIME"),
        bigquery.SchemaField("ts_col", "TIMESTAMP"),
    )

    table_schema = scalars_schema + (
        # TODO: Array columns can't be read due to NULLABLE versus REPEATED
        #       mode mismatch. See:
        #       https://issuetracker.google.com/133415569#comment3
        # bigquery.SchemaField("array_col", "INTEGER", mode="REPEATED"),
        # TODO: Support writing StructArrays to Parquet. See:
        #       https://jira.apache.org/jira/browse/ARROW-2587
        # bigquery.SchemaField("struct_col", "RECORD", fields=scalars_schema),
    )

    df_data = [
        ("bool_col", [True, None, False]),
        ("bytes_col", [b"abc", None, b"def"]),
        ("date_col", [datetime.date(1, 1, 1), None, datetime.date(9999, 12, 31)]),
        (
            "dt_col",
            [
                datetime.datetime(1, 1, 1, 0, 0, 0),
                None,
                datetime.datetime(9999, 12, 31, 23, 59, 59, 999999),
            ],
        ),
        ("float_col", [float("-inf"), float("nan"), float("inf")]),
        (
            "geo_col",
            ["POINT(30 10)", None, "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"],
        ),
        ("int_col", [-9223372036854775808, None, 9223372036854775807]),
        (
            "num_col",
            [
                decimal.Decimal("-99999999999999999999999999999.999999999"),
                None,
                decimal.Decimal("99999999999999999999999999999.999999999"),
            ],
        ),
        (
            "bignum_col",
            [
                decimal.Decimal("-{d38}.{d38}".format(d38="9" * 38)),
                None,
                decimal.Decimal("{d38}.{d38}".format(d38="9" * 38)),
            ],
        ),
        ("str_col", ["abc", None, "def"]),
        (
            "time_col",
            [datetime.time(0, 0, 0), None, datetime.time(23, 59, 59, 999999)],
        ),
        (
            "ts_col",
            [
                datetime.datetime(1, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
                None,
                datetime.datetime(
                    9999, 12, 31, 23, 59, 59, 999999, tzinfo=datetime.timezone.utc
                ),
            ],
        ),
    ]
    df_data = collections.OrderedDict(df_data)
    dataframe = pandas.DataFrame(df_data, dtype="object", columns=df_data.keys())

    table_id = "{}.{}.load_table_from_dataframe_w_explicit_schema".format(
        bigquery_client.project, dataset_id
    )

    job_config = bigquery.LoadJobConfig(schema=table_schema)
    load_job = bigquery_client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )
    load_job.result()

    table = bigquery_client.get_table(table_id)
    assert tuple(table.schema) == table_schema
    assert table.num_rows == 3


def test_load_table_from_dataframe_w_struct_datatype(bigquery_client, dataset_id):
    """Test that a DataFrame with struct datatype can be uploaded if a
    BigQuery schema is specified.

    https://github.com/googleapis/python-bigquery/issues/21
    """
    table_id = "{}.{}.load_table_from_dataframe_w_struct_datatype".format(
        bigquery_client.project, dataset_id
    )
    table_schema = [
        bigquery.SchemaField(
            "bar",
            "RECORD",
            fields=[
                bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
            ],
            mode="REQUIRED",
        ),
    ]
    table = helpers.retry_403(bigquery_client.create_table)(
        bigquery.Table(table_id, schema=table_schema)
    )

    df_data = [{"id": 1, "age": 21}, {"id": 2, "age": 22}, {"id": 2, "age": 23}]
    dataframe = pandas.DataFrame(data={"bar": df_data}, columns=["bar"])

    load_job = bigquery_client.load_table_from_dataframe(dataframe, table_id)
    load_job.result()

    table = bigquery_client.get_table(table_id)
    assert table.schema == table_schema
    assert table.num_rows == 3


def test_load_table_from_dataframe_w_explicit_schema_source_format_csv(
    bigquery_client, dataset_id
):
    from google.cloud.bigquery.job import SourceFormat

    table_schema = (
        bigquery.SchemaField("bool_col", "BOOLEAN"),
        bigquery.SchemaField("bytes_col", "BYTES"),
        bigquery.SchemaField("date_col", "DATE"),
        bigquery.SchemaField("dt_col", "DATETIME"),
        bigquery.SchemaField("float_col", "FLOAT"),
        bigquery.SchemaField("geo_col", "GEOGRAPHY"),
        bigquery.SchemaField("int_col", "INTEGER"),
        bigquery.SchemaField("num_col", "NUMERIC"),
        bigquery.SchemaField("bignum_col", "BIGNUMERIC"),
        bigquery.SchemaField("str_col", "STRING"),
        bigquery.SchemaField("time_col", "TIME"),
        bigquery.SchemaField("ts_col", "TIMESTAMP"),
    )
    df_data = collections.OrderedDict(
        [
            ("bool_col", [True, None, False]),
            ("bytes_col", ["abc", None, "def"]),
            ("date_col", [datetime.date(1, 1, 1), None, datetime.date(9999, 12, 31)],),
            (
                "dt_col",
                [
                    datetime.datetime(1, 1, 1, 0, 0, 0),
                    None,
                    datetime.datetime(9999, 12, 31, 23, 59, 59, 999999),
                ],
            ),
            ("float_col", [float("-inf"), float("nan"), float("inf")]),
            (
                "geo_col",
                [
                    "POINT(30 10)",
                    None,
                    "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
                ],
            ),
            ("int_col", [-9223372036854775808, None, 9223372036854775807]),
            (
                "num_col",
                [
                    decimal.Decimal("-99999999999999999999999999999.999999999"),
                    None,
                    decimal.Decimal("99999999999999999999999999999.999999999"),
                ],
            ),
            (
                "bignum_col",
                [
                    decimal.Decimal("-{d38}.{d38}".format(d38="9" * 38)),
                    None,
                    decimal.Decimal("{d38}.{d38}".format(d38="9" * 38)),
                ],
            ),
            ("str_col", ["abc", None, "def"]),
            (
                "time_col",
                [datetime.time(0, 0, 0), None, datetime.time(23, 59, 59, 999999)],
            ),
            (
                "ts_col",
                [
                    datetime.datetime(1, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
                    None,
                    datetime.datetime(
                        9999, 12, 31, 23, 59, 59, 999999, tzinfo=datetime.timezone.utc
                    ),
                ],
            ),
        ]
    )
    dataframe = pandas.DataFrame(df_data, dtype="object", columns=df_data.keys())

    table_id = "{}.{}.load_table_from_dataframe_w_explicit_schema_csv".format(
        bigquery_client.project, dataset_id
    )

    job_config = bigquery.LoadJobConfig(
        schema=table_schema, source_format=SourceFormat.CSV
    )
    load_job = bigquery_client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )
    load_job.result()

    table = bigquery_client.get_table(table_id)
    assert tuple(table.schema) == table_schema
    assert table.num_rows == 3


def test_load_table_from_dataframe_w_explicit_schema_source_format_csv_floats(
    bigquery_client, dataset_id, table_id
):
    from google.cloud.bigquery.job import SourceFormat

    table_schema = (bigquery.SchemaField("float_col", "FLOAT"),)
    df_data = collections.OrderedDict(
        [
            (
                "float_col",
                [
                    0.14285714285714285,
                    0.51428571485748,
                    0.87128748,
                    1.807960649,
                    2.0679610649,
                    2.4406779661016949,
                    3.7148514257,
                    3.8571428571428572,
                    1.51251252e40,
                ],
            ),
        ]
    )
    dataframe = pandas.DataFrame(df_data, dtype="object", columns=df_data.keys())

    job_config = bigquery.LoadJobConfig(
        schema=table_schema, source_format=SourceFormat.CSV
    )
    load_job = bigquery_client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )
    load_job.result()

    table = bigquery_client.get_table(table_id)
    rows = bigquery_client.list_rows(table_id)
    floats = [r.values()[0] for r in rows]
    assert tuple(table.schema) == table_schema
    assert table.num_rows == 9
    assert floats == df_data["float_col"]


def test_query_results_to_dataframe(bigquery_client):
    QUERY = """
    SELECT id, author, time_ts, dead
    FROM `bigquery-public-data.hacker_news.comments`
    LIMIT 10
    """

    df = bigquery_client.query(QUERY).result().to_dataframe()

    assert isinstance(df, pandas.DataFrame)
    assert len(df) == 10  # verify the number of rows
    column_names = ["id", "author", "time_ts", "dead"]
    assert list(df) == column_names  # verify the column names
    exp_datatypes = {
        "id": int,
        "author": str,
        "time_ts": pandas.Timestamp,
        "dead": bool,
    }
    for _, row in df.iterrows():
        for col in column_names:
            # all the schema fields are nullable, so None is acceptable
            if not row[col] is None:
                assert isinstance(row[col], exp_datatypes[col])


def test_query_results_to_dataframe_w_bqstorage(bigquery_client):
    query = """
    SELECT id, author, time_ts, dead
    FROM `bigquery-public-data.hacker_news.comments`
    LIMIT 10
    """

    bqstorage_client = bigquery_storage.BigQueryReadClient(
        credentials=bigquery_client._credentials
    )

    df = bigquery_client.query(query).result().to_dataframe(bqstorage_client)

    assert isinstance(df, pandas.DataFrame)
    assert len(df) == 10  # verify the number of rows
    column_names = ["id", "author", "time_ts", "dead"]
    assert list(df) == column_names
    exp_datatypes = {
        "id": int,
        "author": str,
        "time_ts": pandas.Timestamp,
        "dead": bool,
    }
    for index, row in df.iterrows():
        for col in column_names:
            # all the schema fields are nullable, so None is acceptable
            if not row[col] is None:
                assert isinstance(row[col], exp_datatypes[col])


def test_insert_rows_from_dataframe(bigquery_client, dataset_id):
    SF = bigquery.SchemaField
    schema = [
        SF("float_col", "FLOAT", mode="REQUIRED"),
        SF("int_col", "INTEGER", mode="REQUIRED"),
        SF("bool_col", "BOOLEAN", mode="REQUIRED"),
        SF("string_col", "STRING", mode="NULLABLE"),
    ]

    dataframe = pandas.DataFrame(
        [
            {
                "float_col": 1.11,
                "bool_col": True,
                "string_col": "my string",
                "int_col": 10,
            },
            {
                "float_col": 2.22,
                "bool_col": False,
                "string_col": "another string",
                "int_col": 20,
            },
            {
                "float_col": 3.33,
                "bool_col": False,
                "string_col": "another string",
                "int_col": 30,
            },
            {
                "float_col": 4.44,
                "bool_col": True,
                "string_col": "another string",
                "int_col": 40,
            },
            {
                "float_col": 5.55,
                "bool_col": False,
                "string_col": "another string",
                "int_col": 50,
            },
            {
                "float_col": 6.66,
                "bool_col": True,
                # Include a NaN value, because pandas often uses NaN as a
                # NULL value indicator.
                "string_col": float("NaN"),
                "int_col": 60,
            },
        ]
    )

    table_id = f"{bigquery_client.project}.{dataset_id}.test_insert_rows_from_dataframe"
    table_arg = bigquery.Table(table_id, schema=schema)
    table = helpers.retry_403(bigquery_client.create_table)(table_arg)

    chunk_errors = bigquery_client.insert_rows_from_dataframe(
        table, dataframe, chunk_size=3
    )
    for errors in chunk_errors:
        assert not errors
    expected = [
        # Pandas often represents NULL values as NaN. Convert to None for
        # easier comparison.
        tuple(None if col != col else col for col in data_row)
        for data_row in dataframe.itertuples(index=False)
    ]

    # Use query to fetch rows instead of listing directly from the table so
    # that we get values from the streaming buffer "within a few seconds".
    # https://cloud.google.com/bigquery/streaming-data-into-bigquery#dataavailability
    @google.api_core.retry.Retry(
        predicate=google.api_core.retry.if_exception_type(MissingDataError)
    )
    def get_rows():
        rows = list(
            bigquery_client.query(
                "SELECT * FROM `{}.{}.{}`".format(
                    table.project, table.dataset_id, table.table_id
                )
            )
        )
        if len(rows) != len(expected):
            raise MissingDataError()
        return rows

    rows = get_rows()
    sorted_rows = sorted(rows, key=operator.attrgetter("int_col"))
    row_tuples = [r.values() for r in sorted_rows]

    for row, expected_row in zip(row_tuples, expected):
        assert (
            # Use Counter to verify the same number of values in each, because
            # column order does not matter.
            collections.Counter(row)
            == collections.Counter(expected_row)
        )


def test_nested_table_to_dataframe(bigquery_client, dataset_id):
    from google.cloud.bigquery.job import SourceFormat
    from google.cloud.bigquery.job import WriteDisposition

    SF = bigquery.SchemaField
    schema = [
        SF("string_col", "STRING", mode="NULLABLE"),
        SF(
            "record_col",
            "RECORD",
            mode="NULLABLE",
            fields=[
                SF("nested_string", "STRING", mode="NULLABLE"),
                SF("nested_repeated", "INTEGER", mode="REPEATED"),
                SF(
                    "nested_record",
                    "RECORD",
                    mode="NULLABLE",
                    fields=[SF("nested_nested_string", "STRING", mode="NULLABLE")],
                ),
            ],
        ),
        SF("bigfloat_col", "FLOAT", mode="NULLABLE"),
        SF("smallfloat_col", "FLOAT", mode="NULLABLE"),
    ]
    record = {
        "nested_string": "another string value",
        "nested_repeated": [0, 1, 2],
        "nested_record": {"nested_nested_string": "some deep insight"},
    }
    to_insert = [
        {
            "string_col": "Some value",
            "record_col": record,
            "bigfloat_col": 3.14,
            "smallfloat_col": 2.72,
        }
    ]
    rows = [json.dumps(row) for row in to_insert]
    body = io.BytesIO("{}\n".format("\n".join(rows)).encode("ascii"))
    table_id = f"{bigquery_client.project}.{dataset_id}.test_nested_table_to_dataframe"
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = WriteDisposition.WRITE_TRUNCATE
    job_config.source_format = SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.schema = schema
    # Load a table using a local JSON file from memory.
    bigquery_client.load_table_from_file(body, table_id, job_config=job_config).result()

    df = bigquery_client.list_rows(table_id, selected_fields=schema).to_dataframe(
        dtypes={"smallfloat_col": "float16"}
    )

    assert isinstance(df, pandas.DataFrame)
    assert len(df) == 1  # verify the number of rows
    exp_columns = ["string_col", "record_col", "bigfloat_col", "smallfloat_col"]
    assert list(df) == exp_columns  # verify the column names
    row = df.iloc[0]
    # verify the row content
    assert row["string_col"] == "Some value"
    expected_keys = tuple(sorted(record.keys()))
    row_keys = tuple(sorted(row["record_col"].keys()))
    assert row_keys == expected_keys
    # Can't compare numpy arrays, which pyarrow encodes the embedded
    # repeated column to, so convert to list.
    assert list(row["record_col"]["nested_repeated"]) == [0, 1, 2]
    # verify that nested data can be accessed with indices/keys
    assert row["record_col"]["nested_repeated"][0] == 0
    assert (
        row["record_col"]["nested_record"]["nested_nested_string"]
        == "some deep insight"
    )
    # verify dtypes
    assert df.dtypes["bigfloat_col"].name == "float64"
    assert df.dtypes["smallfloat_col"].name == "float16"


def test_list_rows_max_results_w_bqstorage(bigquery_client):
    table_ref = bigquery.DatasetReference("bigquery-public-data", "utility_us").table(
        "country_code_iso"
    )
    bqstorage_client = bigquery_storage.BigQueryReadClient(
        credentials=bigquery_client._credentials
    )

    row_iterator = bigquery_client.list_rows(
        table_ref,
        selected_fields=[bigquery.SchemaField("country_name", "STRING")],
        max_results=100,
    )
    with pytest.warns(
        UserWarning, match="Cannot use bqstorage_client if max_results is set"
    ):
        dataframe = row_iterator.to_dataframe(bqstorage_client=bqstorage_client)

    assert len(dataframe.index) == 100


def test_upload_time_and_datetime_56(bigquery_client, dataset_id):
    df = pandas.DataFrame(
        dict(
            dt=[
                datetime.datetime(2020, 1, 8, 8, 0, 0),
                datetime.datetime(
                    2020,
                    1,
                    8,
                    8,
                    0,
                    0,
                    tzinfo=datetime.timezone(datetime.timedelta(hours=-7)),
                ),
            ],
            t=[datetime.time(0, 0, 10, 100001), None],
        )
    )
    table = f"{dataset_id}.test_upload_time_and_datetime"
    bigquery_client.load_table_from_dataframe(df, table).result()
    data = list(map(list, bigquery_client.list_rows(table)))
    assert data == [
        [
            datetime.datetime(2020, 1, 8, 8, 0, tzinfo=datetime.timezone.utc),
            datetime.time(0, 0, 10, 100001),
        ],
        [datetime.datetime(2020, 1, 8, 15, 0, tzinfo=datetime.timezone.utc), None],
    ]

    from google.cloud.bigquery import job, schema

    table = f"{dataset_id}.test_upload_time_and_datetime_dt"
    config = job.LoadJobConfig(
        schema=[schema.SchemaField("dt", "DATETIME"), schema.SchemaField("t", "TIME")]
    )

    bigquery_client.load_table_from_dataframe(df, table, job_config=config).result()
    data = list(map(list, bigquery_client.list_rows(table)))
    assert data == [
        [datetime.datetime(2020, 1, 8, 8, 0), datetime.time(0, 0, 10, 100001)],
        [datetime.datetime(2020, 1, 8, 15, 0), None],
    ]


def test_to_dataframe_geography_as_objects(bigquery_client, dataset_id):
    wkt = pytest.importorskip("shapely.wkt")
    bigquery_client.query(
        f"create table {dataset_id}.lake (name string, geog geography)"
    ).result()
    bigquery_client.query(
        f"""
        insert into {dataset_id}.lake (name, geog) values
        ('foo', st_geogfromtext('point(0 0)')),
        ('bar', st_geogfromtext('point(0 1)')),
        ('baz', null)
        """
    ).result()
    df = bigquery_client.query(
        f"select * from {dataset_id}.lake order by name"
    ).to_dataframe(geography_as_object=True)
    assert list(df["name"]) == ["bar", "baz", "foo"]
    assert df["geog"][0] == wkt.loads("point(0 1)")
    assert pandas.isna(df["geog"][1])
    assert df["geog"][2] == wkt.loads("point(0 0)")


def test_to_geodataframe(bigquery_client, dataset_id):
    geopandas = pytest.importorskip("geopandas")
    from shapely import wkt

    bigquery_client.query(
        f"create table {dataset_id}.geolake (name string, geog geography)"
    ).result()
    bigquery_client.query(
        f"""
        insert into {dataset_id}.geolake (name, geog) values
        ('foo', st_geogfromtext('point(0 0)')),
        ('bar', st_geogfromtext('polygon((0 0, 1 0, 1 1, 0 0))')),
        ('baz', null)
        """
    ).result()
    df = bigquery_client.query(
        f"select * from {dataset_id}.geolake order by name"
    ).to_geodataframe()
    assert df["geog"][0] == wkt.loads("polygon((0 0, 1 0, 1 1, 0 0))")
    assert pandas.isna(df["geog"][1])
    assert df["geog"][2] == wkt.loads("point(0 0)")
    assert isinstance(df, geopandas.GeoDataFrame)
    assert isinstance(df["geog"], geopandas.GeoSeries)
    assert df.area[0] == 0.5
    assert pandas.isna(df.area[1])
    assert df.area[2] == 0.0
    assert df.crs.srs == "EPSG:4326"
    assert df.crs.name == "WGS 84"
    assert df.geog.crs.srs == "EPSG:4326"
    assert df.geog.crs.name == "WGS 84"


def test_load_geodataframe(bigquery_client, dataset_id):
    geopandas = pytest.importorskip("geopandas")
    import pandas
    from shapely import wkt
    from google.cloud.bigquery.schema import SchemaField

    df = geopandas.GeoDataFrame(
        pandas.DataFrame(
            dict(
                name=["foo", "bar"],
                geo1=[None, None],
                geo2=[None, wkt.loads("Point(1 1)")],
            )
        ),
        geometry="geo1",
    )

    table_id = f"{dataset_id}.lake_from_gp"
    bigquery_client.load_table_from_dataframe(df, table_id).result()

    table = bigquery_client.get_table(table_id)
    assert table.schema == [
        SchemaField("name", "STRING", "NULLABLE"),
        SchemaField("geo1", "GEOGRAPHY", "NULLABLE"),
        SchemaField("geo2", "GEOGRAPHY", "NULLABLE"),
    ]
    assert sorted(map(list, bigquery_client.list_rows(table_id))) == [
        ["bar", None, "POINT(1 1)"],
        ["foo", None, None],
    ]


def test_load_dataframe_w_shapely(bigquery_client, dataset_id):
    wkt = pytest.importorskip("shapely.wkt")
    from google.cloud.bigquery.schema import SchemaField

    df = pandas.DataFrame(
        dict(name=["foo", "bar"], geo=[None, wkt.loads("Point(1 1)")])
    )

    table_id = f"{dataset_id}.lake_from_shapes"
    bigquery_client.load_table_from_dataframe(df, table_id).result()

    table = bigquery_client.get_table(table_id)
    assert table.schema == [
        SchemaField("name", "STRING", "NULLABLE"),
        SchemaField("geo", "GEOGRAPHY", "NULLABLE"),
    ]
    assert sorted(map(list, bigquery_client.list_rows(table_id))) == [
        ["bar", "POINT(1 1)"],
        ["foo", None],
    ]

    bigquery_client.load_table_from_dataframe(df, table_id).result()
    assert sorted(map(list, bigquery_client.list_rows(table_id))) == [
        ["bar", "POINT(1 1)"],
        ["bar", "POINT(1 1)"],
        ["foo", None],
        ["foo", None],
    ]


def test_load_dataframe_w_wkb(bigquery_client, dataset_id):
    wkt = pytest.importorskip("shapely.wkt")
    from shapely import wkb
    from google.cloud.bigquery.schema import SchemaField

    df = pandas.DataFrame(
        dict(name=["foo", "bar"], geo=[None, wkb.dumps(wkt.loads("Point(1 1)"))])
    )

    table_id = f"{dataset_id}.lake_from_wkb"
    # We create the table first, to inform the interpretation of the wkb data
    bigquery_client.query(
        f"create table {table_id} (name string, geo GEOGRAPHY)"
    ).result()
    bigquery_client.load_table_from_dataframe(df, table_id).result()

    table = bigquery_client.get_table(table_id)
    assert table.schema == [
        SchemaField("name", "STRING", "NULLABLE"),
        SchemaField("geo", "GEOGRAPHY", "NULLABLE"),
    ]
    assert sorted(map(list, bigquery_client.list_rows(table_id))) == [
        ["bar", "POINT(1 1)"],
        ["foo", None],
    ]
