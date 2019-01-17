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

from google.cloud import spanner_admin_database_v1
from google.cloud.spanner_admin_database_v1.proto import spanner_database_admin_pb2
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


class TestDatabaseAdminClient(object):
    def test_list_databases(self):
        # Setup Expected Response
        next_page_token = ""
        databases_element = {}
        databases = [databases_element]
        expected_response = {"next_page_token": next_page_token, "databases": databases}
        expected_response = spanner_database_admin_pb2.ListDatabasesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup Request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")

        paged_list_response = client.list_databases(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.databases[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = spanner_database_admin_pb2.ListDatabasesRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_databases_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")

        paged_list_response = client.list_databases(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_database(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = spanner_database_admin_pb2.Database(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_create_database", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup Request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")
        create_statement = "createStatement552974828"

        response = client.create_database(parent, create_statement)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = spanner_database_admin_pb2.CreateDatabaseRequest(
            parent=parent, create_statement=create_statement
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_database_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_create_database_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup Request
        parent = client.instance_path("[PROJECT]", "[INSTANCE]")
        create_statement = "createStatement552974828"

        response = client.create_database(parent, create_statement)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_get_database(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = spanner_database_admin_pb2.Database(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup Request
        name = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        response = client.get_database(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_database_admin_pb2.GetDatabaseRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_database_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup request
        name = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        with pytest.raises(CustomException):
            client.get_database(name)

    def test_update_database_ddl(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_update_database_ddl", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup Request
        database = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")
        statements = []

        response = client.update_database_ddl(database, statements)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = spanner_database_admin_pb2.UpdateDatabaseDdlRequest(
            database=database, statements=statements
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_database_ddl_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_update_database_ddl_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup Request
        database = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")
        statements = []

        response = client.update_database_ddl(database, statements)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_drop_database(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup Request
        database = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        client.drop_database(database)

        assert len(channel.requests) == 1
        expected_request = spanner_database_admin_pb2.DropDatabaseRequest(
            database=database
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_drop_database_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup request
        database = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        with pytest.raises(CustomException):
            client.drop_database(database)

    def test_get_database_ddl(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = spanner_database_admin_pb2.GetDatabaseDdlResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup Request
        database = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        response = client.get_database_ddl(database)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_database_admin_pb2.GetDatabaseDdlRequest(
            database=database
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_database_ddl_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup request
        database = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        with pytest.raises(CustomException):
            client.get_database_ddl(database)

    def test_set_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b"21"
        expected_response = {"version": version, "etag": etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup Request
        resource = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")
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
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup request
        resource = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")
        policy = {}

        with pytest.raises(CustomException):
            client.set_iam_policy(resource, policy)

    def test_get_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b"21"
        expected_response = {"version": version, "etag": etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup Request
        resource = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

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
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup request
        resource = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")

        with pytest.raises(CustomException):
            client.get_iam_policy(resource)

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
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup Request
        resource = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")
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
            client = spanner_admin_database_v1.DatabaseAdminClient()

        # Setup request
        resource = client.database_path("[PROJECT]", "[INSTANCE]", "[DATABASE]")
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)
