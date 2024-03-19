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

import uuid

from google.api_core import exceptions
import pytest

from google.cloud.bigquery_storage_v1 import types as gapic_types
from google.cloud.bigquery_storage_v1.writer import AppendRowsStream


@pytest.fixture
def table(project_id, dataset, bq_client):
    from google.cloud import bigquery

    schema = [
        bigquery.SchemaField("first_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("last_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("age", "INTEGER", mode="NULLABLE"),
    ]

    unique_suffix = str(uuid.uuid4()).replace("-", "_")
    table_id = "users_" + unique_suffix
    table_id_full = f"{project_id}.{dataset.dataset_id}.{table_id}"
    bq_table = bigquery.Table(table_id_full, schema=schema)
    created_table = bq_client.create_table(bq_table)

    yield created_table

    bq_client.delete_table(created_table)


@pytest.fixture(scope="session")
def bqstorage_write_client(credentials):
    from google.cloud import bigquery_storage_v1

    return bigquery_storage_v1.BigQueryWriteClient(credentials=credentials)


def test_append_rows_with_invalid_stream_name_fails_fast(bqstorage_write_client):
    bad_request = gapic_types.AppendRowsRequest()
    bad_request.write_stream = "this-is-an-invalid-stream-resource-path"

    with pytest.raises(exceptions.GoogleAPICallError):
        bqstorage_write_client.append_rows(bad_request)


def test_append_rows_with_proto3(bqstorage_write_client, table):
    from google.protobuf import descriptor_pb2
    import proto

    # Using Proto Plus to build proto3
    # Declare proto3 field `optional` for presence
    class PersonProto(proto.Message):
        first_name = proto.Field(
            proto.STRING,
            number=1,
            optional=True,
        )
        last_name = proto.Field(
            proto.STRING,
            number=2,
            optional=True,
        )
        age = proto.Field(
            proto.INT64,
            number=3,
            optional=True,
        )

    person_pb = PersonProto.pb()

    stream_name = f"projects/{table.project}/datasets/{table.dataset_id}/tables/{table.table_id}/_default"
    request_template = gapic_types.AppendRowsRequest()
    request_template.write_stream = stream_name

    proto_schema = gapic_types.ProtoSchema()
    proto_descriptor = descriptor_pb2.DescriptorProto()
    person_pb.DESCRIPTOR.CopyToProto(
        proto_descriptor,
    )
    proto_schema.proto_descriptor = proto_descriptor
    proto_data = gapic_types.AppendRowsRequest.ProtoData()
    proto_data.writer_schema = proto_schema
    request_template.proto_rows = proto_data

    append_rows_stream = AppendRowsStream(
        bqstorage_write_client,
        request_template,
    )

    request = gapic_types.AppendRowsRequest()
    proto_data = gapic_types.AppendRowsRequest.ProtoData()
    proto_rows = gapic_types.ProtoRows()
    row = person_pb()
    row.first_name = "fn"
    row.last_name = "ln"
    row.age = 20
    proto_rows.serialized_rows.append(row.SerializeToString())
    proto_data.rows = proto_rows
    request.proto_rows = proto_data
    response_future = append_rows_stream.send(request)

    assert response_future.result()
    # The request should success
