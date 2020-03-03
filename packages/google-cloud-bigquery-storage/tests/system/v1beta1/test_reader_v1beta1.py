# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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
"""System tests for reading rows from tables."""

import copy
import datetime as dt
import decimal
import re

import pytest
import pytz

from google.cloud import bigquery
from google.cloud import bigquery_storage_v1beta1
from google.protobuf import timestamp_pb2


def _to_bq_table_ref(proto_table_ref, partition_suffix=""):
    """Converts protobuf table reference to bigquery table reference.

    Args:
        proto_table_ref (bigquery_storage_v1beta1.types.TableReference):
            A protobuf reference to a table.
        partition_suffix (str):
            An optional suffix to append to the table_id, useful for selecting
            partitions of ingestion-time partitioned tables.

    Returns:
        google.cloud.bigquery.table.TableReference
    """
    return bigquery.table.TableReference.from_api_repr(
        {
            "projectId": proto_table_ref.project_id,
            "datasetId": proto_table_ref.dataset_id,
            "tableId": proto_table_ref.table_id + partition_suffix,
        }
    )


@pytest.mark.parametrize(
    "data_format,expected_schema_type",
    (
        (None, "avro_schema"),  # Default format (Avro).
        (bigquery_storage_v1beta1.enums.DataFormat.AVRO, "avro_schema"),
        (bigquery_storage_v1beta1.enums.DataFormat.ARROW, "arrow_schema"),
    ),
)
def test_read_rows_as_blocks_full_table(
    client, project_id, small_table_reference, data_format, expected_schema_type
):
    session = client.create_read_session(
        small_table_reference,
        "projects/{}".format(project_id),
        format_=data_format,
        requested_streams=1,
    )
    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=session.streams[0]
    )
    schema_type = session.WhichOneof("schema")
    assert schema_type == expected_schema_type

    blocks = list(client.read_rows(stream_pos))

    assert len(blocks) > 0
    block = blocks[0]
    assert block.status.estimated_row_count > 0


@pytest.mark.parametrize(
    "data_format,expected_schema_type",
    (
        (bigquery_storage_v1beta1.enums.DataFormat.AVRO, "avro_schema"),
        (bigquery_storage_v1beta1.enums.DataFormat.ARROW, "arrow_schema"),
    ),
)
def test_read_rows_as_rows_full_table(
    client, project_id, small_table_reference, data_format, expected_schema_type
):
    session = client.create_read_session(
        small_table_reference,
        "projects/{}".format(project_id),
        format_=data_format,
        requested_streams=1,
    )
    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=session.streams[0]
    )

    rows = list(client.read_rows(stream_pos).rows(session))

    assert len(rows) > 0


@pytest.mark.parametrize(
    "data_format",
    (
        (bigquery_storage_v1beta1.enums.DataFormat.AVRO),
        (bigquery_storage_v1beta1.enums.DataFormat.ARROW),
    ),
)
def test_basic_nonfiltered_read(client, project_id, table_with_data_ref, data_format):
    session = client.create_read_session(
        table_with_data_ref,
        "projects/{}".format(project_id),
        format_=data_format,
        requested_streams=1,
    )
    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=session.streams[0]
    )

    rows = list(client.read_rows(stream_pos).rows(session))

    assert len(rows) == 5  # all table rows


def test_filtered_rows_read(client, project_id, table_with_data_ref):
    read_options = bigquery_storage_v1beta1.types.TableReadOptions()
    read_options.row_restriction = "age >= 50"

    session = client.create_read_session(
        table_with_data_ref,
        "projects/{}".format(project_id),
        format_=bigquery_storage_v1beta1.enums.DataFormat.AVRO,
        requested_streams=1,
        read_options=read_options,
    )
    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=session.streams[0]
    )

    rows = list(client.read_rows(stream_pos).rows(session))

    assert len(rows) == 2


@pytest.mark.parametrize(
    "data_format",
    (
        (bigquery_storage_v1beta1.enums.DataFormat.AVRO),
        (bigquery_storage_v1beta1.enums.DataFormat.ARROW),
    ),
)
def test_column_selection_read(client, project_id, table_with_data_ref, data_format):
    read_options = bigquery_storage_v1beta1.types.TableReadOptions()
    read_options.selected_fields.append("first_name")
    read_options.selected_fields.append("age")

    session = client.create_read_session(
        table_with_data_ref,
        "projects/{}".format(project_id),
        format_=data_format,
        requested_streams=1,
        read_options=read_options,
    )
    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=session.streams[0]
    )

    rows = list(client.read_rows(stream_pos).rows(session))

    for row in rows:
        assert sorted(row.keys()) == ["age", "first_name"]


def test_snapshot(client, project_id, table_with_data_ref, bq_client):
    before_new_data = timestamp_pb2.Timestamp()
    before_new_data.GetCurrentTime()

    # load additional data into the table
    new_data = [
        {u"first_name": u"NewGuyFoo", u"last_name": u"Smith", u"age": 46},
        {u"first_name": u"NewGuyBar", u"last_name": u"Jones", u"age": 30},
    ]

    destination = _to_bq_table_ref(table_with_data_ref)
    bq_client.load_table_from_json(new_data, destination).result()

    # read data using the timestamp before the additional data load
    session = client.create_read_session(
        table_with_data_ref,
        "projects/{}".format(project_id),
        format_=bigquery_storage_v1beta1.enums.DataFormat.AVRO,
        requested_streams=1,
        table_modifiers={"snapshot_time": before_new_data},
    )
    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=session.streams[0]
    )

    rows = list(client.read_rows(stream_pos).rows(session))

    # verify that only the data before the timestamp was returned
    assert len(rows) == 5  # all initial records

    for row in rows:
        assert "NewGuy" not in row["first_name"]  # no new records


def test_column_partitioned_table(
    client, project_id, col_partition_table_ref, bq_client
):
    data = [
        {"description": "Tracking established.", "occurred": "2017-02-15"},
        {"description": "Look, a solar eclipse!", "occurred": "2018-02-15"},
        {"description": "Fake solar eclipse reported.", "occurred": "2018-02-15"},
        {"description": "1 day after false eclipse report.", "occurred": "2018-02-16"},
        {"description": "1 year after false eclipse report.", "occurred": "2019-02-15"},
    ]

    destination = _to_bq_table_ref(col_partition_table_ref)
    bq_client.load_table_from_json(data, destination).result()

    # Read from the table with a partition filter specified, and verify that
    # only the expected data is returned.
    read_options = bigquery_storage_v1beta1.types.TableReadOptions()
    read_options.row_restriction = "occurred = '2018-02-15'"

    session = client.create_read_session(
        col_partition_table_ref,
        "projects/{}".format(project_id),
        format_=bigquery_storage_v1beta1.enums.DataFormat.AVRO,
        requested_streams=1,
        read_options=read_options,
    )

    assert session.streams  # there should be some data to fetch

    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=session.streams[0]
    )
    rows = list(client.read_rows(stream_pos).rows(session))

    assert len(rows) == 2

    expected_descriptions = ("Look, a solar eclipse!", "Fake solar eclipse reported.")
    for row in rows:
        assert row["occurred"] == dt.date(2018, 2, 15)
        assert row["description"] in expected_descriptions


@pytest.mark.parametrize(
    "data_format",
    (
        (bigquery_storage_v1beta1.enums.DataFormat.AVRO),
        (bigquery_storage_v1beta1.enums.DataFormat.ARROW),
    ),
)
def test_ingestion_time_partitioned_table(
    client, project_id, ingest_partition_table_ref, bq_client, data_format
):
    data = [{"shape": "cigar", "altitude": 1200}, {"shape": "disc", "altitude": 750}]
    destination = _to_bq_table_ref(
        ingest_partition_table_ref, partition_suffix="$20190809"
    )
    bq_client.load_table_from_json(data, destination).result()

    data = [
        {"shape": "sphere", "altitude": 3500},
        {"shape": "doughnut", "altitude": 100},
    ]
    destination = _to_bq_table_ref(
        ingest_partition_table_ref, partition_suffix="$20190810"
    )
    bq_client.load_table_from_json(data, destination).result()

    data = [
        {"shape": "elephant", "altitude": 1},
        {"shape": "rocket", "altitude": 12700},
    ]
    destination = _to_bq_table_ref(
        ingest_partition_table_ref, partition_suffix="$20190811"
    )
    bq_client.load_table_from_json(data, destination).result()

    read_options = bigquery_storage_v1beta1.types.TableReadOptions()
    read_options.row_restriction = "DATE(_PARTITIONTIME) = '2019-08-10'"

    session = client.create_read_session(
        ingest_partition_table_ref,
        "projects/{}".format(project_id),
        format_=data_format,
        requested_streams=1,
        read_options=read_options,
    )

    assert session.streams  # there should be some data to fetch

    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=session.streams[0]
    )
    rows = list(client.read_rows(stream_pos).rows(session))
    assert len(rows) == 2

    actual_items = {(row["shape"], row["altitude"]) for row in rows}
    expected_items = {("sphere", 3500), ("doughnut", 100)}
    assert actual_items == expected_items


@pytest.mark.parametrize(
    "data_format",
    (
        (bigquery_storage_v1beta1.enums.DataFormat.AVRO),
        (bigquery_storage_v1beta1.enums.DataFormat.ARROW),
    ),
)
def test_decoding_data_types(
    client, project_id, all_types_table_ref, bq_client, data_format
):
    data = [
        {
            u"string_field": u"Price: € 9.95.",
            u"bytes_field": bigquery._helpers._bytes_to_json(b"byteees"),
            u"int64_field": -1085,
            u"float64_field": -42.195,
            u"numeric_field": "1.4142",
            u"bool_field": True,
            u"geography_field": '{"type": "Point", "coordinates": [-49.3028, 69.0622]}',
            u"person_struct_field": {u"name": u"John", u"age": 42},
            u"timestamp_field": 1565357902.017896,  # 2019-08-09T13:38:22.017896
            u"date_field": u"1995-03-17",
            u"time_field": u"16:24:51",
            u"datetime_field": u"2005-10-26T19:49:41",
            u"string_array_field": [u"foo", u"bar", u"baz"],
        }
    ]

    # Explicit schema is needed to recognize bytes_field as BYTES, and not STRING.
    # Since partial schemas are not supported in load_table_from_json(), a full
    # schema needs to be specified.
    schema = [
        bigquery.SchemaField("string_field", "STRING"),
        bigquery.SchemaField("bytes_field", "BYTES"),
        bigquery.SchemaField("int64_field", "INT64"),
        bigquery.SchemaField("float64_field", "FLOAT64"),
        bigquery.SchemaField("numeric_field", "NUMERIC"),
        bigquery.SchemaField("bool_field", "BOOL"),
        bigquery.SchemaField("geography_field", "GEOGRAPHY"),
        bigquery.SchemaField(
            "person_struct_field",
            "STRUCT",
            fields=(
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("age", "INT64"),
            ),
        ),
        bigquery.SchemaField("timestamp_field", "TIMESTAMP"),
        bigquery.SchemaField("date_field", "DATE"),
        bigquery.SchemaField("time_field", "TIME"),
        bigquery.SchemaField("datetime_field", "DATETIME"),
        bigquery.SchemaField("string_array_field", "STRING", mode="REPEATED"),
    ]

    job_config = bigquery.LoadJobConfig(schema=schema)
    destination = _to_bq_table_ref(all_types_table_ref)
    bq_client.load_table_from_json(data, destination, job_config=job_config).result()

    session = client.create_read_session(
        all_types_table_ref,
        "projects/{}".format(project_id),
        format_=data_format,
        requested_streams=1,
    )

    assert session.streams  # there should be data available

    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=session.streams[0]
    )

    rows = list(client.read_rows(stream_pos).rows(session))

    expected_result = {
        u"string_field": u"Price: € 9.95.",
        u"bytes_field": b"byteees",
        u"int64_field": -1085,
        u"float64_field": -42.195,
        u"numeric_field": decimal.Decimal("1.4142"),
        u"bool_field": True,
        u"geography_field": "POINT(-49.3028 69.0622)",
        u"person_struct_field": {u"name": u"John", u"age": 42},
        u"timestamp_field": dt.datetime(2019, 8, 9, 13, 38, 22, 17896, tzinfo=pytz.UTC),
        u"date_field": dt.date(1995, 3, 17),
        u"time_field": dt.time(16, 24, 51),
        u"string_array_field": [u"foo", u"bar", u"baz"],
    }

    result_copy = copy.copy(rows[0])
    del result_copy["datetime_field"]
    assert result_copy == expected_result

    # Compare datetime separately, AVRO and PYARROW return different object types,
    # although they should both represent the same value.
    # TODO: when fixed, change assertion to assert a datetime instance!
    expected_pattern = re.compile(r"2005-10-26( |T)19:49:41")
    assert expected_pattern.match(str(rows[0]["datetime_field"]))


@pytest.mark.parametrize(
    "data_format",
    (
        (bigquery_storage_v1beta1.enums.DataFormat.AVRO),
        (bigquery_storage_v1beta1.enums.DataFormat.ARROW),
    ),
)
def test_resuming_read_from_offset(client, project_id, data_format):
    shakespeare_ref = bigquery_storage_v1beta1.types.TableReference()
    shakespeare_ref.project_id = project_id
    shakespeare_ref.dataset_id = "public_samples_copy"
    shakespeare_ref.table_id = "shakespeare"

    read_session = client.create_read_session(
        shakespeare_ref,
        "projects/{}".format(project_id),
        format_=data_format,
        requested_streams=1,
    )

    assert read_session.streams  # there should be data available

    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=read_session.streams[0], offset=0
    )
    read_rows_stream = client.read_rows(stream_pos)

    # fetch the first two batches of rows
    rows_iter = iter(read_rows_stream)
    some_rows = next(rows_iter)
    more_rows = next(rows_iter)

    # fetch the rest of the rows using the stream offset
    new_stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=read_session.streams[0], offset=some_rows.row_count + more_rows.row_count
    )
    remaining_rows_count = sum(
        1 for _ in client.read_rows(new_stream_pos).rows(read_session)
    )

    # verify that the counts match
    expected_len = 164656  # total rows in shakespeare table
    actual_len = remaining_rows_count + some_rows.row_count + more_rows.row_count
    assert actual_len == expected_len
