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

from google.cloud import redis_v1
from google.cloud.redis_v1 import enums
from google.cloud.redis_v1.proto import cloud_redis_pb2
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


class TestCloudRedisClient(object):
    def test_list_instances(self):
        # Setup Expected Response
        next_page_token = ""
        instances_element = {}
        instances = [instances_element]
        expected_response = {"next_page_token": next_page_token, "instances": instances}
        expected_response = cloud_redis_pb2.ListInstancesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = redis_v1.CloudRedisClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_instances(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.instances[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = cloud_redis_pb2.ListInstancesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_instances_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = redis_v1.CloudRedisClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_instances(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_instance(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        location_id = "locationId552319461"
        alternative_location_id = "alternativeLocationId-718920621"
        redis_version = "redisVersion-685310444"
        reserved_ip_range = "reservedIpRange-1082940580"
        host = "host3208616"
        port = 3446913
        current_location_id = "currentLocationId1312712735"
        status_message = "statusMessage-239442758"
        memory_size_gb = 34199707
        authorized_network = "authorizedNetwork-1733809270"
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "location_id": location_id,
            "alternative_location_id": alternative_location_id,
            "redis_version": redis_version,
            "reserved_ip_range": reserved_ip_range,
            "host": host,
            "port": port,
            "current_location_id": current_location_id,
            "status_message": status_message,
            "memory_size_gb": memory_size_gb,
            "authorized_network": authorized_network,
        }
        expected_response = cloud_redis_pb2.Instance(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = redis_v1.CloudRedisClient()

        # Setup Request
        name = client.instance_path("[PROJECT]", "[LOCATION]", "[INSTANCE]")

        response = client.get_instance(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = cloud_redis_pb2.GetInstanceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_instance_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = redis_v1.CloudRedisClient()

        # Setup request
        name = client.instance_path("[PROJECT]", "[LOCATION]", "[INSTANCE]")

        with pytest.raises(CustomException):
            client.get_instance(name)

    def test_create_instance(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        location_id = "locationId552319461"
        alternative_location_id = "alternativeLocationId-718920621"
        redis_version = "redisVersion-685310444"
        reserved_ip_range = "reservedIpRange-1082940580"
        host = "host3208616"
        port = 3446913
        current_location_id = "currentLocationId1312712735"
        status_message = "statusMessage-239442758"
        memory_size_gb_2 = 1493816946
        authorized_network = "authorizedNetwork-1733809270"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "location_id": location_id,
            "alternative_location_id": alternative_location_id,
            "redis_version": redis_version,
            "reserved_ip_range": reserved_ip_range,
            "host": host,
            "port": port,
            "current_location_id": current_location_id,
            "status_message": status_message,
            "memory_size_gb": memory_size_gb_2,
            "authorized_network": authorized_network,
        }
        expected_response = cloud_redis_pb2.Instance(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_create_instance", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = redis_v1.CloudRedisClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        instance_id = "test_instance"
        tier = enums.Instance.Tier.BASIC
        memory_size_gb = 1
        instance = {"tier": tier, "memory_size_gb": memory_size_gb}

        response = client.create_instance(parent, instance_id, instance)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = cloud_redis_pb2.CreateInstanceRequest(
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
            client = redis_v1.CloudRedisClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        instance_id = "test_instance"
        tier = enums.Instance.Tier.BASIC
        memory_size_gb = 1
        instance = {"tier": tier, "memory_size_gb": memory_size_gb}

        response = client.create_instance(parent, instance_id, instance)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_update_instance(self):
        # Setup Expected Response
        name = "name3373707"
        display_name_2 = "displayName21615000987"
        location_id = "locationId552319461"
        alternative_location_id = "alternativeLocationId-718920621"
        redis_version = "redisVersion-685310444"
        reserved_ip_range = "reservedIpRange-1082940580"
        host = "host3208616"
        port = 3446913
        current_location_id = "currentLocationId1312712735"
        status_message = "statusMessage-239442758"
        memory_size_gb_2 = 1493816946
        authorized_network = "authorizedNetwork-1733809270"
        expected_response = {
            "name": name,
            "display_name": display_name_2,
            "location_id": location_id,
            "alternative_location_id": alternative_location_id,
            "redis_version": redis_version,
            "reserved_ip_range": reserved_ip_range,
            "host": host,
            "port": port,
            "current_location_id": current_location_id,
            "status_message": status_message,
            "memory_size_gb": memory_size_gb_2,
            "authorized_network": authorized_network,
        }
        expected_response = cloud_redis_pb2.Instance(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_update_instance", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = redis_v1.CloudRedisClient()

        # Setup Request
        paths_element = "display_name"
        paths_element_2 = "memory_size_gb"
        paths = [paths_element, paths_element_2]
        update_mask = {"paths": paths}
        display_name = "UpdatedDisplayName"
        memory_size_gb = 4
        instance = {"display_name": display_name, "memory_size_gb": memory_size_gb}

        response = client.update_instance(update_mask, instance)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = cloud_redis_pb2.UpdateInstanceRequest(
            update_mask=update_mask, instance=instance
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
            client = redis_v1.CloudRedisClient()

        # Setup Request
        paths_element = "display_name"
        paths_element_2 = "memory_size_gb"
        paths = [paths_element, paths_element_2]
        update_mask = {"paths": paths}
        display_name = "UpdatedDisplayName"
        memory_size_gb = 4
        instance = {"display_name": display_name, "memory_size_gb": memory_size_gb}

        response = client.update_instance(update_mask, instance)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_delete_instance(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = empty_pb2.Empty(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_delete_instance", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = redis_v1.CloudRedisClient()

        # Setup Request
        name = client.instance_path("[PROJECT]", "[LOCATION]", "[INSTANCE]")

        response = client.delete_instance(name)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = cloud_redis_pb2.DeleteInstanceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_instance_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_delete_instance_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = redis_v1.CloudRedisClient()

        # Setup Request
        name = client.instance_path("[PROJECT]", "[LOCATION]", "[INSTANCE]")

        response = client.delete_instance(name)
        exception = response.exception()
        assert exception.errors[0] == error
