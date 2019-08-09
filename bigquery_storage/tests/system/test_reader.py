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

import datetime as dt
import json
import io

import pytest

from google.cloud import bigquery
from google.cloud import bigquery_storage_v1beta1
from google.protobuf import timestamp_pb2


def _add_rows(table_ref, new_data):
    """Insert additional rows into an existing table.

    Args:
        table_ref (bigquery_storage_v1beta1.types.TableReference):
            A reference to the target table.
        new_data (Iterable[Dict[str, Any]]):
            New data to insert with each row represented as a dictionary.
            The keys must match the table column names, and the values
            must be JSON serializable.
    """
    bq_client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    )

    new_data_str = u"\n".join(json.dumps(item) for item in new_data)
    new_data_file = io.BytesIO(new_data_str.encode())

    destination_ref = bigquery.table.TableReference.from_api_repr(
        {
            "projectId": table_ref.project_id,
            "datasetId": table_ref.dataset_id,
            "tableId": table_ref.table_id,
        }
    )
    job = bq_client.load_table_from_file(
        new_data_file, destination=destination_ref, job_config=job_config
    )
    job.result()  # wait for the load to complete


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


def test_snapshot(client, project_id, table_with_data_ref):
    before_new_data = timestamp_pb2.Timestamp()
    before_new_data.GetCurrentTime()

    # load additional data into the table
    new_data = [
        {u"first_name": u"NewGuyFoo", u"last_name": u"Smith", u"age": 46},
        {u"first_name": u"NewGuyBar", u"last_name": u"Jones", u"age": 30},
    ]
    _add_rows(table_with_data_ref, new_data)

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


def test_column_partitioned_table(client, project_id, col_partition_table_ref):
    data = [
        {"description": "Tracking established.", "occurred": "2017-02-15"},
        {"description": "Look, a solar eclipse!", "occurred": "2018-02-15"},
        {"description": "Fake solar eclipse reported.", "occurred": "2018-02-15"},
        {"description": "1 day after false eclipse report.", "occurred": "2018-02-16"},
        {"description": "1 year after false eclipse report.", "occurred": "2019-02-15"},
    ]

    _add_rows(col_partition_table_ref, data)

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
