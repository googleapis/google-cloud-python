# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import decimal
import itertools
import json

import fastavro
import mock
import pandas
import pandas.testing
import pytest
import pytz
import six

import google.api_core.exceptions
from google.cloud import bigquery_storage_v1beta1


PROJECT = "my-project"
BQ_TO_AVRO_TYPES = {
    "int64": "long",
    "float64": "double",
    "bool": "boolean",
    "numeric": {"type": "bytes", "logicalType": "decimal", "precision": 38, "scale": 9},
    "string": "string",
    "bytes": "bytes",
    "date": {"type": "int", "logicalType": "date"},
    "datetime": {"type": "string", "sqlType": "DATETIME"},
    "time": {"type": "long", "logicalType": "time-micros"},
    "timestamp": {"type": "long", "logicalType": "timestamp-micros"},
}
SCALAR_COLUMNS = [
    {"name": "int_col", "type": "int64"},
    {"name": "float_col", "type": "float64"},
    {"name": "num_col", "type": "numeric"},
    {"name": "bool_col", "type": "bool"},
    {"name": "str_col", "type": "string"},
    {"name": "bytes_col", "type": "bytes"},
    {"name": "date_col", "type": "date"},
    {"name": "time_col", "type": "time"},
    {"name": "ts_col", "type": "timestamp"},
]
SCALAR_COLUMN_NAMES = [field["name"] for field in SCALAR_COLUMNS]
SCALAR_BLOCKS = [
    [
        {
            "int_col": 123,
            "float_col": 3.14,
            "num_col": decimal.Decimal("9.99"),
            "bool_col": True,
            "str_col": "hello world",
            "bytes_col": b"ascii bytes",
            "date_col": datetime.date(1998, 9, 4),
            "time_col": datetime.time(12, 0),
            "ts_col": datetime.datetime(2000, 1, 1, 5, 0, tzinfo=pytz.utc),
        },
        {
            "int_col": 456,
            "float_col": 2.72,
            "num_col": decimal.Decimal("0.99"),
            "bool_col": False,
            "str_col": "hallo welt",
            "bytes_col": b"\xbb\xee\xff",
            "date_col": datetime.date(1995, 3, 2),
            "time_col": datetime.time(13, 37),
            "ts_col": datetime.datetime(1965, 4, 3, 2, 1, tzinfo=pytz.utc),
        },
    ],
    [
        {
            "int_col": 789,
            "float_col": 1.23,
            "num_col": decimal.Decimal("5.67"),
            "bool_col": True,
            "str_col": u"こんにちは世界",
            "bytes_col": b"\x54\x69\x6d",
            "date_col": datetime.date(1970, 1, 1),
            "time_col": datetime.time(16, 20),
            "ts_col": datetime.datetime(1991, 8, 25, 20, 57, 8, tzinfo=pytz.utc),
        }
    ],
]


@pytest.fixture()
def mut():
    from google.cloud.bigquery_storage_v1beta1 import reader

    return reader


@pytest.fixture()
def class_under_test(mut):
    return mut.ReadRowsStream


@pytest.fixture()
def mock_client():
    from google.cloud.bigquery_storage_v1beta1.gapic import big_query_storage_client

    return mock.create_autospec(big_query_storage_client.BigQueryStorageClient)


def _bq_to_avro_blocks(bq_blocks, avro_schema_json):
    avro_schema = fastavro.parse_schema(avro_schema_json)
    avro_blocks = []
    for block in bq_blocks:
        blockio = six.BytesIO()
        for row in block:
            fastavro.schemaless_writer(blockio, avro_schema, row)

        response = bigquery_storage_v1beta1.types.ReadRowsResponse()
        response.avro_rows.row_count = len(block)
        response.avro_rows.serialized_binary_rows = blockio.getvalue()
        avro_blocks.append(response)
    return avro_blocks


def _avro_blocks_w_deadline(avro_blocks):
    for block in avro_blocks:
        yield block
    raise google.api_core.exceptions.DeadlineExceeded("test: please reconnect")


def _generate_read_session(avro_schema_json):
    schema = json.dumps(avro_schema_json)
    return bigquery_storage_v1beta1.types.ReadSession(avro_schema={"schema": schema})


def _bq_to_avro_schema(bq_columns):
    fields = []
    avro_schema = {"type": "record", "name": "__root__", "fields": fields}

    for column in bq_columns:
        doc = column.get("description")
        name = column["name"]
        type_ = BQ_TO_AVRO_TYPES[column["type"]]
        mode = column.get("mode", "nullable").lower()

        if mode == "nullable":
            type_ = ["null", type_]

        fields.append({"name": name, "type": type_, "doc": doc})

    return avro_schema


def _get_avro_bytes(rows, avro_schema):
    avro_file = six.BytesIO()
    for row in rows:
        fastavro.schemaless_writer(avro_file, avro_schema, row)
    return avro_file.getvalue()


def test_rows_raises_import_error(mut, class_under_test, mock_client, monkeypatch):
    monkeypatch.setattr(mut, "fastavro", None)
    reader = class_under_test(
        [], mock_client, bigquery_storage_v1beta1.types.StreamPosition(), {}
    )
    read_session = bigquery_storage_v1beta1.types.ReadSession()

    with pytest.raises(ImportError):
        reader.rows(read_session)


def test_rows_w_empty_stream(class_under_test, mock_client):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    read_session = _generate_read_session(avro_schema)
    reader = class_under_test(
        [], mock_client, bigquery_storage_v1beta1.types.StreamPosition(), {}
    )

    got = tuple(reader.rows(read_session))
    assert got == ()


def test_rows_w_scalars(class_under_test, mock_client):
    avro_schema = _bq_to_avro_schema(SCALAR_COLUMNS)
    read_session = _generate_read_session(avro_schema)
    avro_blocks = _bq_to_avro_blocks(SCALAR_BLOCKS, avro_schema)

    reader = class_under_test(
        avro_blocks, mock_client, bigquery_storage_v1beta1.types.StreamPosition(), {}
    )
    got = tuple(reader.rows(read_session))

    expected = tuple(itertools.chain.from_iterable(SCALAR_BLOCKS))
    assert got == expected


def test_rows_w_reconnect(class_under_test, mock_client):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    read_session = _generate_read_session(avro_schema)
    bq_blocks_1 = [
        [{"int_col": 123}, {"int_col": 234}],
        [{"int_col": 345}, {"int_col": 456}],
    ]
    avro_blocks_1 = _avro_blocks_w_deadline(
        _bq_to_avro_blocks(bq_blocks_1, avro_schema)
    )
    bq_blocks_2 = [[{"int_col": 567}, {"int_col": 789}], [{"int_col": 890}]]
    avro_blocks_2 = _bq_to_avro_blocks(bq_blocks_2, avro_schema)
    mock_client.read_rows.return_value = avro_blocks_2
    stream_position = bigquery_storage_v1beta1.types.StreamPosition(
        stream={"name": "test"}
    )

    reader = class_under_test(
        avro_blocks_1,
        mock_client,
        stream_position,
        {"metadata": {"test-key": "test-value"}},
    )
    got = tuple(reader.rows(read_session))

    expected = tuple(
        itertools.chain(
            itertools.chain.from_iterable(bq_blocks_1),
            itertools.chain.from_iterable(bq_blocks_2),
        )
    )

    assert got == expected
    mock_client.read_rows.assert_called_once_with(
        bigquery_storage_v1beta1.types.StreamPosition(
            stream={"name": "test"}, offset=4
        ),
        metadata={"test-key": "test-value"},
    )


def test_to_dataframe_no_pandas_raises_import_error(
    mut, class_under_test, mock_client, monkeypatch
):
    monkeypatch.setattr(mut, "pandas", None)
    reader = class_under_test(
        [], mock_client, bigquery_storage_v1beta1.types.StreamPosition(), {}
    )
    read_session = bigquery_storage_v1beta1.types.ReadSession()

    with pytest.raises(ImportError):
        reader.to_dataframe(read_session)


def test_to_dataframe_no_fastavro_raises_import_error(
    mut, class_under_test, mock_client, monkeypatch
):
    monkeypatch.setattr(mut, "fastavro", None)
    reader = class_under_test(
        [], mock_client, bigquery_storage_v1beta1.types.StreamPosition(), {}
    )
    read_session = bigquery_storage_v1beta1.types.ReadSession()

    with pytest.raises(ImportError):
        reader.to_dataframe(read_session)


def test_to_dataframe_w_scalars(class_under_test):
    avro_schema = _bq_to_avro_schema(SCALAR_COLUMNS)
    read_session = _generate_read_session(avro_schema)
    avro_blocks = _bq_to_avro_blocks(SCALAR_BLOCKS, avro_schema)

    reader = class_under_test(
        avro_blocks, mock_client, bigquery_storage_v1beta1.types.StreamPosition(), {}
    )
    got = reader.to_dataframe(read_session)

    expected = pandas.DataFrame(
        list(itertools.chain.from_iterable(SCALAR_BLOCKS)), columns=SCALAR_COLUMN_NAMES
    )
    # fastavro provides its own UTC definition, so
    # compare the timestamp columns separately.
    got_ts = got["ts_col"]
    got = got.drop(columns=["ts_col"])
    expected_ts = expected["ts_col"]
    expected = expected.drop(columns=["ts_col"])

    pandas.testing.assert_frame_equal(
        got.reset_index(drop=True),  # reset_index to ignore row labels
        expected.reset_index(drop=True),
    )
    pandas.testing.assert_series_equal(
        got_ts.reset_index(drop=True),
        expected_ts.reset_index(drop=True),
        check_dtype=False,  # fastavro's UTC means different dtype
        check_datetimelike_compat=True,
    )


def test_to_dataframe_w_dtypes(class_under_test):
    # TODOTODOTODOTODO
    avro_schema = _bq_to_avro_schema(
        [
            {"name": "bigfloat", "type": "float64"},
            {"name": "lilfloat", "type": "float64"},
        ]
    )
    read_session = _generate_read_session(avro_schema)
    blocks = [
        [{"bigfloat": 1.25, "lilfloat": 30.5}, {"bigfloat": 2.5, "lilfloat": 21.125}],
        [{"bigfloat": 3.75, "lilfloat": 11.0}],
    ]
    avro_blocks = _bq_to_avro_blocks(blocks, avro_schema)

    reader = class_under_test(
        avro_blocks, mock_client, bigquery_storage_v1beta1.types.StreamPosition(), {}
    )
    got = reader.to_dataframe(read_session, dtypes={"lilfloat": "float16"})

    expected = pandas.DataFrame(
        {
            "bigfloat": [1.25, 2.5, 3.75],
            "lilfloat": pandas.Series([30.5, 21.125, 11.0], dtype="float16"),
        },
        columns=["bigfloat", "lilfloat"],
    )
    pandas.testing.assert_frame_equal(
        got.reset_index(drop=True),  # reset_index to ignore row labels
        expected.reset_index(drop=True),
    )


def test_copy_stream_position(mut):
    read_position = bigquery_storage_v1beta1.types.StreamPosition(
        stream={"name": "test"}, offset=41
    )
    got = mut._copy_stream_position(read_position)
    assert got == read_position
    got.offset = 42
    assert read_position.offset == 41


def test_copy_stream_position_w_dict(mut):
    read_position = {"stream": {"name": "test"}, "offset": 42}
    got = mut._copy_stream_position(read_position)
    assert got.stream.name == "test"
    assert got.offset == 42
