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

import pytest

from google.cloud import bigquery_storage_v1beta1


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
