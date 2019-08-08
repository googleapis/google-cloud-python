# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
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
"""System tests for reading rows with pandas connector."""

import numpy
import pyarrow.types
import pytest

from google.cloud import bigquery_storage_v1beta1


def test_read_rows_to_arrow(client, project_id):
    table_ref = bigquery_storage_v1beta1.types.TableReference()
    table_ref.project_id = "bigquery-public-data"
    table_ref.dataset_id = "new_york_citibike"
    table_ref.table_id = "citibike_stations"

    read_options = bigquery_storage_v1beta1.types.TableReadOptions()
    read_options.selected_fields.append("station_id")
    read_options.selected_fields.append("latitude")
    read_options.selected_fields.append("longitude")
    read_options.selected_fields.append("name")
    session = client.create_read_session(
        table_ref,
        "projects/{}".format(project_id),
        format_=bigquery_storage_v1beta1.enums.DataFormat.ARROW,
        read_options=read_options,
        requested_streams=1,
    )
    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=session.streams[0]
    )

    tbl = client.read_rows(stream_pos).to_arrow(session)

    assert tbl.num_columns == 4
    schema = tbl.schema
    # Use field_by_name because the order doesn't currently match that of
    # selected_fields.
    assert pyarrow.types.is_int64(schema.field_by_name("station_id").type)
    assert pyarrow.types.is_float64(schema.field_by_name("latitude").type)
    assert pyarrow.types.is_float64(schema.field_by_name("longitude").type)
    assert pyarrow.types.is_string(schema.field_by_name("name").type)


@pytest.mark.parametrize(
    "data_format,expected_schema_type",
    (
        (bigquery_storage_v1beta1.enums.DataFormat.AVRO, "avro_schema"),
        (bigquery_storage_v1beta1.enums.DataFormat.ARROW, "arrow_schema"),
    ),
)
def test_read_rows_to_dataframe(client, project_id, data_format, expected_schema_type):
    table_ref = bigquery_storage_v1beta1.types.TableReference()
    table_ref.project_id = "bigquery-public-data"
    table_ref.dataset_id = "new_york_citibike"
    table_ref.table_id = "citibike_stations"
    session = client.create_read_session(
        table_ref,
        "projects/{}".format(project_id),
        format_=data_format,
        requested_streams=1,
    )
    schema_type = session.WhichOneof("schema")
    assert schema_type == expected_schema_type

    stream_pos = bigquery_storage_v1beta1.types.StreamPosition(
        stream=session.streams[0]
    )

    frame = client.read_rows(stream_pos).to_dataframe(
        session, dtypes={"latitude": numpy.float16}
    )

    # Station ID is a required field (no nulls), so the datatype should always
    # be integer.
    assert frame.station_id.dtype.name == "int64"
    assert frame.latitude.dtype.name == "float16"
    assert frame.longitude.dtype.name == "float64"
    assert frame["name"].str.startswith("Central Park").any()
