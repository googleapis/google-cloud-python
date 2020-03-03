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
import pyarrow
import mock
import pandas
import pandas.testing
import pytest
import pytz
import six

import google.api_core.exceptions
from google.cloud import bigquery_storage_v1


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
# This dictionary is duplicated in bigquery/google/cloud/bigquery/_pandas_helpers.py
# When modifying it be sure to update it there as well.
BQ_TO_ARROW_TYPES = {
    "int64": pyarrow.int64(),
    "float64": pyarrow.float64(),
    "bool": pyarrow.bool_(),
    "numeric": pyarrow.decimal128(38, 9),
    "string": pyarrow.utf8(),
    "bytes": pyarrow.binary(),
    "date": pyarrow.date32(),  # int32 days since epoch
    "datetime": pyarrow.timestamp("us"),
    "time": pyarrow.time64("us"),
    "timestamp": pyarrow.timestamp("us", tz="UTC"),
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
    from google.cloud.bigquery_storage_v1 import reader

    return reader


@pytest.fixture()
def class_under_test(mut):
    return mut.ReadRowsStream


@pytest.fixture()
def mock_client():
    from google.cloud.bigquery_storage_v1.gapic import big_query_read_client

    return mock.create_autospec(big_query_read_client.BigQueryReadClient)


def _bq_to_avro_blocks(bq_blocks, avro_schema_json):
    avro_schema = fastavro.parse_schema(avro_schema_json)
    avro_blocks = []
    for block in bq_blocks:
        blockio = six.BytesIO()
        for row in block:
            fastavro.schemaless_writer(blockio, avro_schema, row)
        response = bigquery_storage_v1.types.ReadRowsResponse()
        response.row_count = len(block)
        response.avro_rows.serialized_binary_rows = blockio.getvalue()
        avro_blocks.append(response)
    return avro_blocks


def _bq_to_arrow_batch_objects(bq_blocks, arrow_schema):
    arrow_batches = []
    for block in bq_blocks:
        arrays = []
        for name in arrow_schema.names:
            arrays.append(
                pyarrow.array(
                    (row[name] for row in block),
                    type=arrow_schema.field(name).type,
                    size=len(block),
                )
            )
        arrow_batches.append(
            pyarrow.RecordBatch.from_arrays(arrays, schema=arrow_schema)
        )
    return arrow_batches


def _bq_to_arrow_batches(bq_blocks, arrow_schema):
    arrow_batches = []
    for record_batch in _bq_to_arrow_batch_objects(bq_blocks, arrow_schema):
        response = bigquery_storage_v1.types.ReadRowsResponse()
        response.arrow_record_batch.serialized_record_batch = (
            record_batch.serialize().to_pybytes()
        )
        arrow_batches.append(response)
    return arrow_batches


def _pages_w_nonresumable_internal_error(avro_blocks):
    for block in avro_blocks:
        yield block
    raise google.api_core.exceptions.InternalServerError(
        "INTERNAL: Got a nonresumable error."
    )


def _pages_w_resumable_internal_error(avro_blocks):
    for block in avro_blocks:
        yield block
    raise google.api_core.exceptions.InternalServerError(
        "INTERNAL: Received RST_STREAM with error code 2."
    )


def _pages_w_unavailable(pages):
    for page in pages:
        yield page
    raise google.api_core.exceptions.ServiceUnavailable("test: please reconnect")


def _avro_blocks_w_deadline(avro_blocks):
    for block in avro_blocks:
        yield block
    raise google.api_core.exceptions.DeadlineExceeded("test: timeout, don't reconnect")


def _generate_avro_read_session(avro_schema_json):
    schema = json.dumps(avro_schema_json)
    return bigquery_storage_v1.types.ReadSession(avro_schema={"schema": schema})


def _generate_arrow_read_session(arrow_schema):
    return bigquery_storage_v1.types.ReadSession(
        arrow_schema={"serialized_schema": arrow_schema.serialize().to_pybytes()}
    )


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


def _bq_to_arrow_schema(bq_columns):
    def bq_col_as_field(column):
        doc = column.get("description")
        name = column["name"]
        type_ = BQ_TO_ARROW_TYPES[column["type"]]
        mode = column.get("mode", "nullable").lower()

        return pyarrow.field(name, type_, mode == "nullable", {"description": doc})

    return pyarrow.schema(bq_col_as_field(c) for c in bq_columns)


def _get_avro_bytes(rows, avro_schema):
    avro_file = six.BytesIO()
    for row in rows:
        fastavro.schemaless_writer(avro_file, avro_schema, row)
    return avro_file.getvalue()


def test_avro_rows_raises_import_error(mut, class_under_test, mock_client, monkeypatch):
    monkeypatch.setattr(mut, "fastavro", None)
    reader = class_under_test([], mock_client, "", 0, {})

    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    read_session = _generate_avro_read_session(avro_schema)

    with pytest.raises(ImportError):
        reader.rows(read_session)


def test_pyarrow_rows_raises_import_error(
    mut, class_under_test, mock_client, monkeypatch
):
    monkeypatch.setattr(mut, "pyarrow", None)
    reader = class_under_test([], mock_client, "", 0, {})

    bq_columns = [{"name": "int_col", "type": "int64"}]
    arrow_schema = _bq_to_arrow_schema(bq_columns)
    read_session = _generate_arrow_read_session(arrow_schema)

    with pytest.raises(ImportError):
        reader.rows(read_session)


def test_rows_no_schema_set_raises_type_error(
    mut, class_under_test, mock_client, monkeypatch
):
    reader = class_under_test([], mock_client, "", 0, {})
    read_session = bigquery_storage_v1.types.ReadSession()

    with pytest.raises(TypeError):
        reader.rows(read_session)


def test_rows_w_empty_stream(class_under_test, mock_client):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    read_session = _generate_avro_read_session(avro_schema)
    reader = class_under_test([], mock_client, "", 0, {})

    got = reader.rows(read_session)
    assert tuple(got) == ()


def test_rows_w_empty_stream_arrow(class_under_test, mock_client):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    arrow_schema = _bq_to_arrow_schema(bq_columns)
    read_session = _generate_arrow_read_session(arrow_schema)
    reader = class_under_test([], mock_client, "", 0, {})

    got = reader.rows(read_session)
    assert tuple(got) == ()


def test_rows_w_scalars(class_under_test, mock_client):
    avro_schema = _bq_to_avro_schema(SCALAR_COLUMNS)
    read_session = _generate_avro_read_session(avro_schema)
    avro_blocks = _bq_to_avro_blocks(SCALAR_BLOCKS, avro_schema)

    reader = class_under_test(avro_blocks, mock_client, "", 0, {})
    got = tuple(reader.rows(read_session))

    expected = tuple(itertools.chain.from_iterable(SCALAR_BLOCKS))
    assert got == expected


def test_rows_w_scalars_arrow(class_under_test, mock_client):
    arrow_schema = _bq_to_arrow_schema(SCALAR_COLUMNS)
    read_session = _generate_arrow_read_session(arrow_schema)
    arrow_batches = _bq_to_arrow_batches(SCALAR_BLOCKS, arrow_schema)

    reader = class_under_test(arrow_batches, mock_client, "", 0, {})
    got = tuple(reader.rows(read_session))

    expected = tuple(itertools.chain.from_iterable(SCALAR_BLOCKS))
    assert got == expected


def test_rows_w_timeout(class_under_test, mock_client):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    read_session = _generate_avro_read_session(avro_schema)
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

    reader = class_under_test(
        avro_blocks_1,
        mock_client,
        "teststream",
        0,
        {"metadata": {"test-key": "test-value"}},
    )

    with pytest.raises(google.api_core.exceptions.DeadlineExceeded):
        list(reader.rows(read_session))

    # Don't reconnect on DeadlineException. This allows user-specified timeouts
    # to be respected.
    mock_client.read_rows.assert_not_called()


def test_rows_w_nonresumable_internal_error(class_under_test, mock_client):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    read_session = _generate_avro_read_session(avro_schema)
    bq_blocks = [[{"int_col": 1024}, {"int_col": 512}], [{"int_col": 256}]]
    avro_blocks = _pages_w_nonresumable_internal_error(
        _bq_to_avro_blocks(bq_blocks, avro_schema)
    )

    reader = class_under_test(avro_blocks, mock_client, "teststream", 0, {})

    with pytest.raises(
        google.api_core.exceptions.InternalServerError, match="nonresumable error"
    ):
        list(reader.rows(read_session))

    mock_client.read_rows.assert_not_called()


def test_rows_w_reconnect(class_under_test, mock_client):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    read_session = _generate_avro_read_session(avro_schema)
    bq_blocks_1 = [
        [{"int_col": 123}, {"int_col": 234}],
        [{"int_col": 345}, {"int_col": 456}],
    ]
    avro_blocks_1 = _pages_w_unavailable(_bq_to_avro_blocks(bq_blocks_1, avro_schema))
    bq_blocks_2 = [[{"int_col": 1024}, {"int_col": 512}], [{"int_col": 256}]]
    avro_blocks_2 = _bq_to_avro_blocks(bq_blocks_2, avro_schema)
    avro_blocks_2 = _pages_w_resumable_internal_error(
        _bq_to_avro_blocks(bq_blocks_2, avro_schema)
    )
    bq_blocks_3 = [[{"int_col": 567}, {"int_col": 789}], [{"int_col": 890}]]
    avro_blocks_3 = _bq_to_avro_blocks(bq_blocks_3, avro_schema)

    mock_client.read_rows.side_effect = (avro_blocks_2, avro_blocks_3)

    reader = class_under_test(
        avro_blocks_1,
        mock_client,
        "teststream",
        0,
        {"metadata": {"test-key": "test-value"}},
    )
    got = reader.rows(read_session)

    expected = tuple(
        itertools.chain(
            itertools.chain.from_iterable(bq_blocks_1),
            itertools.chain.from_iterable(bq_blocks_2),
            itertools.chain.from_iterable(bq_blocks_3),
        )
    )

    assert tuple(got) == expected
    mock_client.read_rows.assert_any_call(
        "teststream", 4, metadata={"test-key": "test-value"}
    )
    mock_client.read_rows.assert_called_with(
        "teststream", 7, metadata={"test-key": "test-value"}
    )


def test_rows_w_reconnect_by_page(class_under_test, mock_client):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    read_session = _generate_avro_read_session(avro_schema)
    bq_blocks_1 = [
        [{"int_col": 123}, {"int_col": 234}],
        [{"int_col": 345}, {"int_col": 456}],
    ]
    avro_blocks_1 = _bq_to_avro_blocks(bq_blocks_1, avro_schema)
    bq_blocks_2 = [[{"int_col": 567}, {"int_col": 789}], [{"int_col": 890}]]
    avro_blocks_2 = _bq_to_avro_blocks(bq_blocks_2, avro_schema)

    mock_client.read_rows.return_value = avro_blocks_2

    reader = class_under_test(
        _pages_w_unavailable(avro_blocks_1),
        mock_client,
        "teststream",
        0,
        {"metadata": {"test-key": "test-value"}},
    )
    got = reader.rows(read_session)
    pages = iter(got.pages)

    page_1 = next(pages)
    assert page_1.num_items == 2
    assert page_1.remaining == 2
    assert tuple(page_1) == tuple(bq_blocks_1[0])
    assert page_1.num_items == 2
    assert page_1.remaining == 0

    page_2 = next(pages)
    assert next(page_2) == bq_blocks_1[1][0]
    assert page_2.num_items == 2
    assert page_2.remaining == 1
    assert next(page_2) == bq_blocks_1[1][1]

    page_3 = next(pages)
    assert tuple(page_3) == tuple(bq_blocks_2[0])
    assert page_3.num_items == 2
    assert page_3.remaining == 0

    page_4 = next(pages)
    assert tuple(page_4) == tuple(bq_blocks_2[1])
    assert page_4.num_items == 1
    assert page_4.remaining == 0


def test_to_arrow_no_pyarrow_raises_import_error(
    mut, class_under_test, mock_client, monkeypatch
):
    monkeypatch.setattr(mut, "pyarrow", None)
    arrow_schema = _bq_to_arrow_schema(SCALAR_COLUMNS)
    read_session = _generate_arrow_read_session(arrow_schema)
    arrow_batches = _bq_to_arrow_batches(SCALAR_BLOCKS, arrow_schema)
    reader = class_under_test(arrow_batches, mock_client, "", 0, {})

    with pytest.raises(ImportError):
        reader.to_arrow(read_session)

    with pytest.raises(ImportError):
        reader.rows(read_session).to_arrow()

    with pytest.raises(ImportError):
        next(reader.rows(read_session).pages).to_arrow()


def test_to_arrow_w_scalars_arrow(class_under_test):
    arrow_schema = _bq_to_arrow_schema(SCALAR_COLUMNS)
    read_session = _generate_arrow_read_session(arrow_schema)
    arrow_batches = _bq_to_arrow_batches(SCALAR_BLOCKS, arrow_schema)
    reader = class_under_test(arrow_batches, mock_client, "", 0, {})
    actual_table = reader.to_arrow(read_session)
    expected_table = pyarrow.Table.from_batches(
        _bq_to_arrow_batch_objects(SCALAR_BLOCKS, arrow_schema)
    )
    assert actual_table == expected_table


def test_to_dataframe_no_pandas_raises_import_error(
    mut, class_under_test, mock_client, monkeypatch
):
    monkeypatch.setattr(mut, "pandas", None)
    avro_schema = _bq_to_avro_schema(SCALAR_COLUMNS)
    read_session = _generate_avro_read_session(avro_schema)
    avro_blocks = _bq_to_avro_blocks(SCALAR_BLOCKS, avro_schema)

    reader = class_under_test(avro_blocks, mock_client, "", 0, {})

    with pytest.raises(ImportError):
        reader.to_dataframe(read_session)

    with pytest.raises(ImportError):
        reader.rows(read_session).to_dataframe()

    with pytest.raises(ImportError):
        next(reader.rows(read_session).pages).to_dataframe()


def test_to_dataframe_no_schema_set_raises_type_error(
    mut, class_under_test, mock_client, monkeypatch
):
    reader = class_under_test([], mock_client, "", 0, {})
    read_session = bigquery_storage_v1.types.ReadSession()

    with pytest.raises(TypeError):
        reader.to_dataframe(read_session)


def test_to_dataframe_w_scalars(class_under_test):
    avro_schema = _bq_to_avro_schema(SCALAR_COLUMNS)
    read_session = _generate_avro_read_session(avro_schema)
    avro_blocks = _bq_to_avro_blocks(SCALAR_BLOCKS, avro_schema)

    reader = class_under_test(avro_blocks, mock_client, "", 0, {})
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


def test_to_dataframe_w_scalars_arrow(class_under_test):
    arrow_schema = _bq_to_arrow_schema(SCALAR_COLUMNS)
    read_session = _generate_arrow_read_session(arrow_schema)
    arrow_batches = _bq_to_arrow_batches(SCALAR_BLOCKS, arrow_schema)

    reader = class_under_test(arrow_batches, mock_client, "", 0, {})
    got = reader.to_dataframe(read_session)

    expected = pandas.DataFrame(
        list(itertools.chain.from_iterable(SCALAR_BLOCKS)), columns=SCALAR_COLUMN_NAMES
    )

    pandas.testing.assert_frame_equal(
        got.reset_index(drop=True),  # reset_index to ignore row labels
        expected.reset_index(drop=True),
    )


def test_to_dataframe_w_dtypes(class_under_test):
    avro_schema = _bq_to_avro_schema(
        [
            {"name": "bigfloat", "type": "float64"},
            {"name": "lilfloat", "type": "float64"},
        ]
    )
    read_session = _generate_avro_read_session(avro_schema)
    blocks = [
        [{"bigfloat": 1.25, "lilfloat": 30.5}, {"bigfloat": 2.5, "lilfloat": 21.125}],
        [{"bigfloat": 3.75, "lilfloat": 11.0}],
    ]
    avro_blocks = _bq_to_avro_blocks(blocks, avro_schema)

    reader = class_under_test(avro_blocks, mock_client, "", 0, {})
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


def test_to_dataframe_w_dtypes_arrow(class_under_test):
    arrow_schema = _bq_to_arrow_schema(
        [
            {"name": "bigfloat", "type": "float64"},
            {"name": "lilfloat", "type": "float64"},
        ]
    )
    read_session = _generate_arrow_read_session(arrow_schema)
    blocks = [
        [{"bigfloat": 1.25, "lilfloat": 30.5}, {"bigfloat": 2.5, "lilfloat": 21.125}],
        [{"bigfloat": 3.75, "lilfloat": 11.0}],
    ]
    arrow_batches = _bq_to_arrow_batches(blocks, arrow_schema)

    reader = class_under_test(arrow_batches, mock_client, "", 0, {})
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


def test_to_dataframe_by_page(class_under_test, mock_client):
    bq_columns = [
        {"name": "int_col", "type": "int64"},
        {"name": "bool_col", "type": "bool"},
    ]
    avro_schema = _bq_to_avro_schema(bq_columns)
    read_session = _generate_avro_read_session(avro_schema)
    block_1 = [{"int_col": 123, "bool_col": True}, {"int_col": 234, "bool_col": False}]
    block_2 = [{"int_col": 345, "bool_col": True}, {"int_col": 456, "bool_col": False}]
    block_3 = [{"int_col": 567, "bool_col": True}, {"int_col": 789, "bool_col": False}]
    block_4 = [{"int_col": 890, "bool_col": True}]
    # Break blocks into two groups to test that iteration continues across
    # reconnection.
    bq_blocks_1 = [block_1, block_2]
    bq_blocks_2 = [block_3, block_4]
    avro_blocks_1 = _bq_to_avro_blocks(bq_blocks_1, avro_schema)
    avro_blocks_2 = _bq_to_avro_blocks(bq_blocks_2, avro_schema)

    mock_client.read_rows.return_value = avro_blocks_2

    reader = class_under_test(
        _pages_w_unavailable(avro_blocks_1),
        mock_client,
        "teststream",
        0,
        {"metadata": {"test-key": "test-value"}},
    )
    got = reader.rows(read_session)
    pages = iter(got.pages)

    page_1 = next(pages)
    pandas.testing.assert_frame_equal(
        page_1.to_dataframe().reset_index(drop=True),
        pandas.DataFrame(block_1, columns=["int_col", "bool_col"]).reset_index(
            drop=True
        ),
    )

    page_2 = next(pages)
    pandas.testing.assert_frame_equal(
        page_2.to_dataframe().reset_index(drop=True),
        pandas.DataFrame(block_2, columns=["int_col", "bool_col"]).reset_index(
            drop=True
        ),
    )

    page_3 = next(pages)
    pandas.testing.assert_frame_equal(
        page_3.to_dataframe().reset_index(drop=True),
        pandas.DataFrame(block_3, columns=["int_col", "bool_col"]).reset_index(
            drop=True
        ),
    )

    page_4 = next(pages)
    pandas.testing.assert_frame_equal(
        page_4.to_dataframe().reset_index(drop=True),
        pandas.DataFrame(block_4, columns=["int_col", "bool_col"]).reset_index(
            drop=True
        ),
    )


def test_to_dataframe_by_page_arrow(class_under_test, mock_client):
    bq_columns = [
        {"name": "int_col", "type": "int64"},
        {"name": "bool_col", "type": "bool"},
    ]
    arrow_schema = _bq_to_arrow_schema(bq_columns)
    read_session = _generate_arrow_read_session(arrow_schema)

    bq_block_1 = [
        {"int_col": 123, "bool_col": True},
        {"int_col": 234, "bool_col": False},
    ]
    bq_block_2 = [
        {"int_col": 345, "bool_col": True},
        {"int_col": 456, "bool_col": False},
    ]
    bq_block_3 = [
        {"int_col": 567, "bool_col": True},
        {"int_col": 789, "bool_col": False},
    ]
    bq_block_4 = [{"int_col": 890, "bool_col": True}]
    # Break blocks into two groups to test that iteration continues across
    # reconnection.
    bq_blocks_1 = [bq_block_1, bq_block_2]
    bq_blocks_2 = [bq_block_3, bq_block_4]
    batch_1 = _bq_to_arrow_batches(bq_blocks_1, arrow_schema)
    batch_2 = _bq_to_arrow_batches(bq_blocks_2, arrow_schema)

    mock_client.read_rows.return_value = batch_2

    reader = class_under_test(_pages_w_unavailable(batch_1), mock_client, "", 0, {})
    got = reader.rows(read_session)
    pages = iter(got.pages)

    page_1 = next(pages)
    pandas.testing.assert_frame_equal(
        page_1.to_dataframe(
            dtypes={"int_col": "int64", "bool_col": "bool"}
        ).reset_index(drop=True),
        pandas.DataFrame(bq_block_1, columns=["int_col", "bool_col"]).reset_index(
            drop=True
        ),
    )

    page_2 = next(pages)
    pandas.testing.assert_frame_equal(
        page_2.to_dataframe().reset_index(drop=True),
        pandas.DataFrame(bq_block_2, columns=["int_col", "bool_col"]).reset_index(
            drop=True
        ),
    )

    page_3 = next(pages)
    pandas.testing.assert_frame_equal(
        page_3.to_dataframe().reset_index(drop=True),
        pandas.DataFrame(bq_block_3, columns=["int_col", "bool_col"]).reset_index(
            drop=True
        ),
    )

    page_4 = next(pages)
    pandas.testing.assert_frame_equal(
        page_4.to_dataframe().reset_index(drop=True),
        pandas.DataFrame(bq_block_4, columns=["int_col", "bool_col"]).reset_index(
            drop=True
        ),
    )
