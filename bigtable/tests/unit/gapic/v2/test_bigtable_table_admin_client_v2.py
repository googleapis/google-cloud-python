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

"""Unit tests."""

import mock
import pytest

from google.rpc import status_pb2

from google.cloud import bigtable_admin_v2
from google.cloud.bigtable_admin_v2.proto import bigtable_table_admin_pb2
from google.cloud.bigtable_admin_v2.proto import table_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2


class MultiCallableStub(object):
    """Stub for the grpc.UnaryUnaryMultiCallable interface."""

    def __init__(self, method, channel_stub):
        self.method = method
        self.channel_stub = channel_stub

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        self.channel_stub.requests.append((self.method, request))

        response = None
        if self.channel_stub.responses:
            response = self.channel_stub.responses.pop()

        if isinstance(response, Exception):
            raise response

        if response:
            return response


class ChannelStub(object):
    """Stub for the grpc.Channel interface."""

    def __init__(self, responses=[]):
        self.responses = responses
        self.requests = []

    def unary_unary(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestBigtableTableAdminClient(object):
    def test_create_table(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = table_pb2.Table(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")
        table_id = "tableId-895419604"
        table = {}

        response = client.create_table(parent, table_id, table)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.CreateTableRequest(
            parent=parent, table_id=table_id, table=table
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_table_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")
        table_id = "tableId-895419604"
        table = {}

        with pytest.raises(CustomException):
            client.create_table(parent, table_id, table)

    def test_create_table_from_snapshot(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = table_pb2.Table(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_create_table_from_snapshot", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")
        table_id = "tableId-895419604"
        source_snapshot = "sourceSnapshot-947679896"

        response = client.create_table_from_snapshot(parent, table_id, source_snapshot)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.CreateTableFromSnapshotRequest(
            parent=parent, table_id=table_id, source_snapshot=source_snapshot
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_table_from_snapshot_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_create_table_from_snapshot_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")
        table_id = "tableId-895419604"
        source_snapshot = "sourceSnapshot-947679896"

        response = client.create_table_from_snapshot(parent, table_id, source_snapshot)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_list_tables(self):
        # Setup Expected Response
        next_page_token = ""
        tables_element = {}
        tables = [tables_element]
        expected_response = {"next_page_token": next_page_token, "tables": tables}
        expected_response = bigtable_table_admin_pb2.ListTablesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")

        paged_list_response = client.list_tables(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.tables[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.ListTablesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_tables_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")

        paged_list_response = client.list_tables(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_table(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = table_pb2.Table(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        response = client.get_table(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.GetTableRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_table_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        with pytest.raises(CustomException):
            client.get_table(name)

    def test_delete_table(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        client.delete_table(name)

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.DeleteTableRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_table_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        with pytest.raises(CustomException):
            client.delete_table(name)

    def test_modify_column_families(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = table_pb2.Table(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        modifications = []

        response = client.modify_column_families(name, modifications)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.ModifyColumnFamiliesRequest(
            name=name, modifications=modifications
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_modify_column_families_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        modifications = []

        with pytest.raises(CustomException):
            client.modify_column_families(name, modifications)

    def test_drop_row_range(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        client.drop_row_range(name)

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.DropRowRangeRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_drop_row_range_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        with pytest.raises(CustomException):
            client.drop_row_range(name)

    def test_generate_consistency_token(self):
        # Setup Expected Response
        consistency_token = "consistencyToken-1090516718"
        expected_response = {"consistency_token": consistency_token}
        expected_response = bigtable_table_admin_pb2.GenerateConsistencyTokenResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        response = client.generate_consistency_token(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.GenerateConsistencyTokenRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_generate_consistency_token_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        with pytest.raises(CustomException):
            client.generate_consistency_token(name)

    def test_check_consistency(self):
        # Setup Expected Response
        consistent = True
        expected_response = {"consistent": consistent}
        expected_response = bigtable_table_admin_pb2.CheckConsistencyResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        consistency_token = "consistencyToken-1090516718"

        response = client.check_consistency(name, consistency_token)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.CheckConsistencyRequest(
            name=name, consistency_token=consistency_token
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_check_consistency_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        consistency_token = "consistencyToken-1090516718"

        with pytest.raises(CustomException):
            client.check_consistency(name, consistency_token)

    def test_get_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b"etag3123477"
        expected_response = {"version": version, "etag": etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        resource = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        response = client.get_iam_policy(resource)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_iam_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        resource = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")

        with pytest.raises(CustomException):
            client.get_iam_policy(resource)

    def test_set_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b"etag3123477"
        expected_response = {"version": version, "etag": etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        resource = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        policy = {}

        response = client.set_iam_policy(resource, policy)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource, policy=policy
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_iam_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        resource = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        policy = {}

        with pytest.raises(CustomException):
            client.set_iam_policy(resource, policy)

    def test_test_iam_permissions(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = iam_policy_pb2.TestIamPermissionsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        resource = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        permissions = []

        response = client.test_iam_permissions(resource, permissions)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_test_iam_permissions_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        resource = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)

    def test_snapshot_table(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        data_size_bytes = 2110122398
        description_2 = "description2568623279"
        expected_response = {
            "name": name_2,
            "data_size_bytes": data_size_bytes,
            "description": description_2,
        }
        expected_response = table_pb2.Snapshot(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_snapshot_table", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        cluster = "cluster872092154"
        snapshot_id = "snapshotId-168585866"
        description = "description-1724546052"

        response = client.snapshot_table(name, cluster, snapshot_id, description)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.SnapshotTableRequest(
            name=name, cluster=cluster, snapshot_id=snapshot_id, description=description
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_snapshot_table_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_snapshot_table_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        name = client.table_path("[PROJECT]", "[INSTANCE]", "[TABLE]")
        cluster = "cluster872092154"
        snapshot_id = "snapshotId-168585866"
        description = "description-1724546052"

        response = client.snapshot_table(name, cluster, snapshot_id, description)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_get_snapshot(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        data_size_bytes = 2110122398
        description = "description-1724546052"
        expected_response = {
            "name": name_2,
            "data_size_bytes": data_size_bytes,
            "description": description,
        }
        expected_response = table_pb2.Snapshot(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        name = client.snapshot_path(
            "[PROJECT]", "[INSTANCE]", "[CLUSTER]", "[SNAPSHOT]"
        )

        response = client.get_snapshot(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.GetSnapshotRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_snapshot_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        name = client.snapshot_path(
            "[PROJECT]", "[INSTANCE]", "[CLUSTER]", "[SNAPSHOT]"
        )

        with pytest.raises(CustomException):
            client.get_snapshot(name)

    def test_list_snapshots(self):
        # Setup Expected Response
        next_page_token = ""
        snapshots_element = {}
        snapshots = [snapshots_element]
        expected_response = {"next_page_token": next_page_token, "snapshots": snapshots}
        expected_response = bigtable_table_admin_pb2.ListSnapshotsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        parent = client.cluster_path("[PROJECT]", "[INSTANCE]", "[CLUSTER]")

        paged_list_response = client.list_snapshots(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.snapshots[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.ListSnapshotsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_snapshots_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        parent = client.cluster_path("[PROJECT]", "[INSTANCE]", "[CLUSTER]")

        paged_list_response = client.list_snapshots(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_snapshot(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup Request
        name = client.snapshot_path(
            "[PROJECT]", "[INSTANCE]", "[CLUSTER]", "[SNAPSHOT]"
        )

        client.delete_snapshot(name)

        assert len(channel.requests) == 1
        expected_request = bigtable_table_admin_pb2.DeleteSnapshotRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_snapshot_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = bigtable_admin_v2.BigtableTableAdminClient()

        # Setup request
        name = client.snapshot_path(
            "[PROJECT]", "[INSTANCE]", "[CLUSTER]", "[SNAPSHOT]"
        )

        with pytest.raises(CustomException):
            client.delete_snapshot(name)
