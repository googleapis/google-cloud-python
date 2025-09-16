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

import io
import itertools
import json
from unittest import mock

import fastavro
import google.api_core.exceptions
import google.rpc.error_details_pb2
import pandas
import pandas.testing
import pytest

from google.cloud.bigquery_storage import types

from .helpers import SCALAR_BLOCKS, SCALAR_COLUMN_NAMES, SCALAR_COLUMNS

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


@pytest.fixture()
def mut():
    from google.cloud.bigquery_storage_v1 import reader

    return reader


@pytest.fixture()
def class_under_test(mut):
    return mut.ReadRowsStream


@pytest.fixture()
def mock_gapic_client():
    from google.cloud.bigquery_storage_v1.services import big_query_read

    return mock.create_autospec(big_query_read.BigQueryReadClient)


def _bq_to_avro_blocks(bq_blocks, avro_schema_json):
    avro_schema = fastavro.parse_schema(avro_schema_json)
    avro_blocks = []
    first_message = True
    for block in bq_blocks:
        blockio = io.BytesIO()
        for row in block:
            fastavro.schemaless_writer(blockio, avro_schema, row)
        response = types.ReadRowsResponse()
        response.row_count = len(block)
        response.avro_rows.serialized_binary_rows = blockio.getvalue()
        if first_message:
            response.avro_schema = {"schema": json.dumps(avro_schema_json)}
            first_message = False
        avro_blocks.append(response)
    return avro_blocks


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


def _pages_w_nonresumable_resource_exhausted_error(avro_blocks):
    for block in avro_blocks:
        yield block
    raise google.api_core.exceptions.ResourceExhausted(
        "RESOURCE_EXHAUSTED: do not retry"
    )


def _pages_w_resumable_resource_exhausted_error(
    avro_blocks, delay_seconds, delay_nanos
):
    for block in avro_blocks:
        yield block
    retry_info = google.rpc.error_details_pb2.RetryInfo()
    retry_info.retry_delay.seconds = delay_seconds
    retry_info.retry_delay.nanos = delay_nanos
    error = google.api_core.exceptions.ResourceExhausted(
        "RESOURCE_EXHAUSTED: retry later"
    )
    error._details = (retry_info,)
    raise error


def _pages_w_unavailable(pages):
    for page in pages:
        yield page
    raise google.api_core.exceptions.ServiceUnavailable("test: please reconnect")


def _pages_w_unknown(pages):
    for page in pages:
        yield page
    raise google.api_core.exceptions.Unknown("No status received")


def _avro_blocks_w_deadline(avro_blocks):
    for block in avro_blocks:
        yield block
    raise google.api_core.exceptions.DeadlineExceeded("test: timeout, don't reconnect")


def _generate_avro_read_session(avro_schema_json):
    schema = json.dumps(avro_schema_json)
    return types.ReadSession(avro_schema={"schema": schema})


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


def test_avro_rows_raises_import_error(
    mut, class_under_test, mock_gapic_client, monkeypatch
):
    monkeypatch.setattr(mut, "fastavro", None)
    avro_schema = _bq_to_avro_schema(SCALAR_COLUMNS)
    avro_blocks = _bq_to_avro_blocks(SCALAR_BLOCKS, avro_schema)
    mock_gapic_client.read_rows.return_value = avro_blocks
    reader = class_under_test(mock_gapic_client, "", 0, {})
    rows = iter(reader.rows())

    # Since session isn't passed in, reader doesn't know serialization type
    # until you start iterating.
    with pytest.raises(ImportError):
        next(rows)


def test_rows_no_schema_set_raises_type_error(
    mut, class_under_test, mock_gapic_client, monkeypatch
):
    avro_schema = _bq_to_avro_schema(SCALAR_COLUMNS)
    avro_blocks = _bq_to_avro_blocks(SCALAR_BLOCKS, avro_schema)
    avro_blocks[0].avro_schema = None
    mock_gapic_client.read_rows.return_value = avro_blocks
    reader = class_under_test(mock_gapic_client, "", 0, {})
    rows = iter(reader.rows())

    # Since session isn't passed in, reader doesn't know serialization type
    # until you start iterating.
    with pytest.raises(TypeError):
        next(rows)


def test_rows_w_empty_stream(class_under_test, mock_gapic_client):
    mock_gapic_client.read_rows.return_value = []
    reader = class_under_test(mock_gapic_client, "", 0, {})
    got = reader.rows()
    assert tuple(got) == ()


def test_rows_w_scalars(class_under_test, mock_gapic_client):
    avro_schema = _bq_to_avro_schema(SCALAR_COLUMNS)
    avro_blocks = _bq_to_avro_blocks(SCALAR_BLOCKS, avro_schema)
    mock_gapic_client.read_rows.return_value = avro_blocks
    reader = class_under_test(mock_gapic_client, "", 0, {})
    got = tuple(reader.rows())

    expected = tuple(itertools.chain.from_iterable(SCALAR_BLOCKS))
    assert got == expected


def test_rows_w_timeout(class_under_test, mock_gapic_client):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    bq_blocks_1 = [
        [{"int_col": 123}, {"int_col": 234}],
        [{"int_col": 345}, {"int_col": 456}],
    ]
    avro_blocks_1 = _avro_blocks_w_deadline(
        _bq_to_avro_blocks(bq_blocks_1, avro_schema)
    )
    bq_blocks_2 = [[{"int_col": 567}, {"int_col": 789}], [{"int_col": 890}]]
    avro_blocks_2 = _bq_to_avro_blocks(bq_blocks_2, avro_schema)

    mock_gapic_client.read_rows.side_effect = (
        avro_blocks_1,
        avro_blocks_2,
    )

    reader = class_under_test(
        mock_gapic_client,
        "teststream",
        0,
        {"metadata": {"test-key": "test-value"}},
    )

    with pytest.raises(google.api_core.exceptions.DeadlineExceeded):
        list(reader.rows())

    # Don't reconnect on DeadlineException so user-specified timeouts
    # are respected. This requires client.read_rows to be called
    # exactly once which fails with DeadlineException.
    mock_gapic_client.read_rows.assert_called_once()


def test_rows_w_nonresumable_internal_error(class_under_test, mock_gapic_client):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    bq_blocks = [[{"int_col": 1024}, {"int_col": 512}], [{"int_col": 256}]]
    avro_blocks = _pages_w_nonresumable_internal_error(
        _bq_to_avro_blocks(bq_blocks, avro_schema)
    )
    mock_gapic_client.read_rows.return_value = avro_blocks
    reader = class_under_test(mock_gapic_client, "teststream", 0, {})

    with pytest.raises(
        google.api_core.exceptions.InternalServerError, match="nonresumable error"
    ):
        list(reader.rows())

    mock_gapic_client.read_rows.assert_called_once()


def test_rows_w_nonresumable_resource_exhausted_error(
    class_under_test, mock_gapic_client
):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    bq_blocks = [[{"int_col": 1024}, {"int_col": 512}], [{"int_col": 256}]]
    avro_blocks = _pages_w_nonresumable_resource_exhausted_error(
        _bq_to_avro_blocks(bq_blocks, avro_schema)
    )

    retry_delay_num_calls = 0

    def retry_delay_callback(delay):
        nonlocal retry_delay_num_calls
        retry_delay_num_calls += 1

    mock_gapic_client.read_rows.return_value = avro_blocks
    reader = class_under_test(mock_gapic_client, "teststream", 0, {})

    with pytest.raises(
        google.api_core.exceptions.ResourceExhausted, match="do not retry"
    ):
        list(reader.rows())

    mock_gapic_client.read_rows.assert_called_once()
    assert retry_delay_num_calls == 0


def test_rows_w_reconnect(class_under_test, mock_gapic_client):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    bq_blocks_1 = [
        [{"int_col": 123}, {"int_col": 234}],
        [{"int_col": 345}, {"int_col": 456}],
    ]
    avro_blocks_1 = _pages_w_unavailable(_bq_to_avro_blocks(bq_blocks_1, avro_schema))
    bq_blocks_2 = [[{"int_col": 1024}, {"int_col": 512}], [{"int_col": 256}]]
    avro_blocks_2 = _pages_w_resumable_internal_error(
        _bq_to_avro_blocks(bq_blocks_2, avro_schema)
    )
    bq_blocks_3 = [[{"int_col": -1}, {"int_col": -2}], [{"int_col": -4}]]
    avro_blocks_3 = _pages_w_unknown(_bq_to_avro_blocks(bq_blocks_3, avro_schema))
    bq_blocks_4 = [[{"int_col": 567}, {"int_col": 789}], [{"int_col": 890}]]
    delay_seconds = 1
    delay_nanos = 234
    avro_blocks_4 = _pages_w_resumable_resource_exhausted_error(
        _bq_to_avro_blocks(bq_blocks_4, avro_schema), delay_seconds, delay_nanos
    )
    bq_blocks_5 = [[{"int_col": 859}, {"int_col": 231}], [{"int_col": 777}]]
    avro_blocks_5 = _bq_to_avro_blocks(bq_blocks_5, avro_schema)

    mock_gapic_client.read_rows.side_effect = (
        avro_blocks_1,
        avro_blocks_2,
        avro_blocks_3,
        avro_blocks_4,
        avro_blocks_5,
    )

    retry_delay_num_calls = 0
    retry_delay = 0

    def retry_delay_callback(delay):
        nonlocal retry_delay_num_calls
        nonlocal retry_delay
        retry_delay_num_calls += 1
        retry_delay = delay

    reader = class_under_test(
        mock_gapic_client,
        "teststream",
        0,
        {"metadata": {"test-key": "test-value"}},
        retry_delay_callback=retry_delay_callback,
    )
    got = reader.rows()

    expected = tuple(
        itertools.chain(
            itertools.chain.from_iterable(bq_blocks_1),
            itertools.chain.from_iterable(bq_blocks_2),
            itertools.chain.from_iterable(bq_blocks_3),
            itertools.chain.from_iterable(bq_blocks_4),
            itertools.chain.from_iterable(bq_blocks_5),
        )
    )

    assert tuple(got) == expected
    mock_gapic_client.read_rows.assert_any_call(
        read_stream="teststream", offset=4, metadata={"test-key": "test-value"}
    )
    mock_gapic_client.read_rows.assert_any_call(
        read_stream="teststream", offset=7, metadata={"test-key": "test-value"}
    )
    mock_gapic_client.read_rows.assert_any_call(
        read_stream="teststream", offset=10, metadata={"test-key": "test-value"}
    )
    mock_gapic_client.read_rows.assert_called_with(
        read_stream="teststream", offset=13, metadata={"test-key": "test-value"}
    )
    assert retry_delay_num_calls == 1
    assert retry_delay == delay_seconds + (delay_nanos / 1e9)


def test_rows_w_reconnect_by_page(class_under_test, mock_gapic_client):
    bq_columns = [{"name": "int_col", "type": "int64"}]
    avro_schema = _bq_to_avro_schema(bq_columns)
    bq_blocks_1 = [
        [{"int_col": 123}, {"int_col": 234}],
        [{"int_col": 345}, {"int_col": 456}],
    ]
    avro_blocks_1 = _bq_to_avro_blocks(bq_blocks_1, avro_schema)
    bq_blocks_2 = [[{"int_col": 567}, {"int_col": 789}], [{"int_col": 890}]]
    avro_blocks_2 = _bq_to_avro_blocks(bq_blocks_2, avro_schema)

    mock_gapic_client.read_rows.side_effect = (
        _pages_w_unavailable(avro_blocks_1),
        avro_blocks_2,
    )

    reader = class_under_test(
        mock_gapic_client,
        "teststream",
        0,
        {"metadata": {"test-key": "test-value"}},
    )
    got = reader.rows()
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


def test_to_dataframe_no_pandas_raises_import_error(
    mut, class_under_test, mock_gapic_client, monkeypatch
):
    monkeypatch.setattr(mut, "pandas", None)
    avro_schema = _bq_to_avro_schema(SCALAR_COLUMNS)
    avro_blocks = _bq_to_avro_blocks(SCALAR_BLOCKS, avro_schema)

    mock_gapic_client.read_rows.return_value = avro_blocks
    reader = class_under_test(mock_gapic_client, "", 0, {})

    with pytest.raises(ImportError):
        reader.to_dataframe()

    with pytest.raises(ImportError):
        reader.rows().to_dataframe()

    with pytest.raises(ImportError):
        next(reader.rows().pages).to_dataframe()


def test_to_dataframe_no_schema_set_raises_type_error(
    mut, class_under_test, mock_gapic_client, monkeypatch
):
    avro_schema = _bq_to_avro_schema(SCALAR_COLUMNS)
    avro_blocks = _bq_to_avro_blocks(SCALAR_BLOCKS, avro_schema)
    avro_blocks[0].avro_schema = None
    mock_gapic_client.read_rows.return_value = avro_blocks
    reader = class_under_test(mock_gapic_client, "", 0, {})
    rows = reader.rows()

    # Since session isn't passed in, reader doesn't know serialization type
    # until you start iterating.
    with pytest.raises(TypeError):
        rows.to_dataframe()


def test_to_dataframe_w_scalars(class_under_test, mock_gapic_client):
    avro_schema = _bq_to_avro_schema(SCALAR_COLUMNS)
    avro_blocks = _bq_to_avro_blocks(SCALAR_BLOCKS, avro_schema)

    mock_gapic_client.read_rows.return_value = avro_blocks
    reader = class_under_test(mock_gapic_client, "", 0, {})
    got = reader.to_dataframe()

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
        expected_ts.reset_index(drop=True).astype(got_ts.dtype),
    )


def test_to_dataframe_w_dtypes(class_under_test, mock_gapic_client):
    avro_schema = _bq_to_avro_schema(
        [
            {"name": "bigfloat", "type": "float64"},
            {"name": "lilfloat", "type": "float64"},
        ]
    )
    blocks = [
        [{"bigfloat": 1.25, "lilfloat": 30.5}, {"bigfloat": 2.5, "lilfloat": 21.125}],
        [{"bigfloat": 3.75, "lilfloat": 11.0}],
    ]
    avro_blocks = _bq_to_avro_blocks(blocks, avro_schema)

    mock_gapic_client.read_rows.return_value = avro_blocks
    reader = class_under_test(mock_gapic_client, "", 0, {})
    got = reader.to_dataframe(dtypes={"lilfloat": "float16"})

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


def test_to_dataframe_empty_w_scalars_avro(class_under_test, mock_gapic_client):
    avro_schema = _bq_to_avro_schema(SCALAR_COLUMNS)
    read_session = _generate_avro_read_session(avro_schema)
    avro_blocks = _bq_to_avro_blocks([], avro_schema)
    mock_gapic_client.read_rows.return_value = avro_blocks
    reader = class_under_test(mock_gapic_client, "", 0, {})

    # Read session is needed to get a schema for empty streams.
    got = reader.to_dataframe(read_session)

    expected = pandas.DataFrame(columns=SCALAR_COLUMN_NAMES)
    expected["int_col"] = expected["int_col"].astype("int64")
    expected["float_col"] = expected["float_col"].astype("float64")
    expected["bool_col"] = expected["bool_col"].astype("bool")
    expected["ts_col"] = (
        expected["ts_col"].astype("datetime64[ns]").dt.tz_localize("UTC")
    )

    pandas.testing.assert_frame_equal(
        got.reset_index(drop=True),  # reset_index to ignore row labels
        expected.reset_index(drop=True),
    )


def test_to_dataframe_empty_w_dtypes_avro(class_under_test, mock_gapic_client):
    avro_schema = _bq_to_avro_schema(
        [
            {"name": "bigfloat", "type": "float64"},
            {"name": "lilfloat", "type": "float64"},
        ]
    )
    read_session = _generate_avro_read_session(avro_schema)
    avro_blocks = _bq_to_avro_blocks([], avro_schema)
    mock_gapic_client.read_rows.return_value = avro_blocks
    reader = class_under_test(mock_gapic_client, "", 0, {})

    # Read session is needed to get a schema for empty streams.
    got = reader.to_dataframe(read_session, dtypes={"lilfloat": "float16"})

    expected = pandas.DataFrame([], columns=["bigfloat", "lilfloat"])
    expected["bigfloat"] = expected["bigfloat"].astype("float64")
    expected["lilfloat"] = expected["lilfloat"].astype("float16")

    pandas.testing.assert_frame_equal(
        got.reset_index(drop=True),  # reset_index to ignore row labels
        expected.reset_index(drop=True),
    )


def test_to_dataframe_by_page(class_under_test, mock_gapic_client):
    bq_columns = [
        {"name": "int_col", "type": "int64"},
        {"name": "bool_col", "type": "bool"},
    ]
    avro_schema = _bq_to_avro_schema(bq_columns)
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

    mock_gapic_client.read_rows.side_effect = (
        _pages_w_unavailable(avro_blocks_1),
        avro_blocks_2,
    )

    reader = class_under_test(
        mock_gapic_client,
        "teststream",
        0,
        {"metadata": {"test-key": "test-value"}},
    )
    got = reader.rows()
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
