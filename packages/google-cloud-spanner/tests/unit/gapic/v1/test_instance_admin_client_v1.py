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

from google.cloud import spanner_admin_instance_v1
from google.cloud.spanner_admin_instance_v1.proto import spanner_instance_admin_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


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


class TestInstanceAdminClient(object):
    def test_list_instance_configs(self):
        # Setup Expected Response
        next_page_token = ""
        instance_configs_element = {}
        instance_configs = [instance_configs_element]
        expected_response = {
            "next_page_token": next_page_token,
            "instance_configs": instance_configs,
        }
        expected_response = spanner_instance_admin_pb2.ListInstanceConfigsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_instance_configs(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.instance_configs[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = spanner_instance_admin_pb2.ListInstanceConfigsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_instance_configs_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_instance_configs(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_instance_config(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        expected_response = {"name": name_2, "display_name": display_name}
        expected_response = spanner_instance_admin_pb2.InstanceConfig(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup Request
        name = client.instance_config_path("[PROJECT]", "[INSTANCE_CONFIG]")

        response = client.get_instance_config(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_instance_admin_pb2.GetInstanceConfigRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_instance_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup request
        name = client.instance_config_path("[PROJECT]", "[INSTANCE_CONFIG]")

        with pytest.raises(CustomException):
            client.get_instance_config(name)

    def test_list_instances(self):
        # Setup Expected Response
        next_page_token = ""
        instances_element = {}
        instances = [instances_element]
        expected_response = {"next_page_token": next_page_token, "instances": instances}
        expected_response = spanner_instance_admin_pb2.ListInstancesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_instances(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.instances[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = spanner_instance_admin_pb2.ListInstancesRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_instances_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_instances(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_instance(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        config = "config-1354792126"
        display_name = "displayName1615086568"
        node_count = 1539922066
        expected_response = {
            "name": name_2,
            "config": config,
            "display_name": display_name,
            "node_count": node_count,
        }
        expected_response = spanner_instance_admin_pb2.Instance(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup Request
        name = client.instance_path("[PROJECT]", "[INSTANCE]")

        response = client.get_instance(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = spanner_instance_admin_pb2.GetInstanceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_instance_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup request
        name = client.instance_path("[PROJECT]", "[INSTANCE]")

        with pytest.raises(CustomException):
            client.get_instance(name)

    def test_create_instance(self):
        # Setup Expected Response
        name = "name3373707"
        config = "config-1354792126"
        display_name = "displayName1615086568"
        node_count = 1539922066
        expected_response = {
            "name": name,
            "config": config,
            "display_name": display_name,
            "node_count": node_count,
        }
        expected_response = spanner_instance_admin_pb2.Instance(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_create_instance", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        instance_id = "instanceId-2101995259"
        instance = {}

        response = client.create_instance(parent, instance_id, instance)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = spanner_instance_admin_pb2.CreateInstanceRequest(
            parent=parent, instance_id=instance_id, instance=instance
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_instance_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_create_instance_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        instance_id = "instanceId-2101995259"
        instance = {}

        response = client.create_instance(parent, instance_id, instance)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_update_instance(self):
        # Setup Expected Response
        name = "name3373707"
        config = "config-1354792126"
        display_name = "displayName1615086568"
        node_count = 1539922066
        expected_response = {
            "name": name,
            "config": config,
            "display_name": display_name,
            "node_count": node_count,
        }
        expected_response = spanner_instance_admin_pb2.Instance(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_update_instance", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup Request
        instance = {}
        field_mask = {}

        response = client.update_instance(instance, field_mask)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = spanner_instance_admin_pb2.UpdateInstanceRequest(
            instance=instance, field_mask=field_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_instance_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_update_instance_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup Request
        instance = {}
        field_mask = {}

        response = client.update_instance(instance, field_mask)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_delete_instance(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup Request
        name = client.instance_path("[PROJECT]", "[INSTANCE]")

        client.delete_instance(name)

        assert len(channel.requests) == 1
        expected_request = spanner_instance_admin_pb2.DeleteInstanceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_instance_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup request
        name = client.instance_path("[PROJECT]", "[INSTANCE]")

        with pytest.raises(CustomException):
            client.delete_instance(name)

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
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup Request
        resource = client.instance_path("[PROJECT]", "[INSTANCE]")
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
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup request
        resource = client.instance_path("[PROJECT]", "[INSTANCE]")
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
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup Request
        resource = client.instance_path("[PROJECT]", "[INSTANCE]")

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
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup request
        resource = client.instance_path("[PROJECT]", "[INSTANCE]")

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
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup Request
        resource = client.instance_path("[PROJECT]", "[INSTANCE]")
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
            client = spanner_admin_instance_v1.InstanceAdminClient()

        # Setup request
        resource = client.instance_path("[PROJECT]", "[INSTANCE]")
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)
