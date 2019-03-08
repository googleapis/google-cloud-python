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

from google.cloud import iot_v1
from google.cloud.iot_v1.proto import device_manager_pb2
from google.cloud.iot_v1.proto import resources_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
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


class TestDeviceManagerClient(object):
    def test_create_device_registry(self):
        # Setup Expected Response
        id_ = "id3355"
        name = "name3373707"
        expected_response = {"id": id_, "name": name}
        expected_response = resources_pb2.DeviceRegistry(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        device_registry = {}

        response = client.create_device_registry(parent, device_registry)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.CreateDeviceRegistryRequest(
            parent=parent, device_registry=device_registry
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_device_registry_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        device_registry = {}

        with pytest.raises(CustomException):
            client.create_device_registry(parent, device_registry)

    def test_get_device_registry(self):
        # Setup Expected Response
        id_ = "id3355"
        name_2 = "name2-1052831874"
        expected_response = {"id": id_, "name": name_2}
        expected_response = resources_pb2.DeviceRegistry(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        name = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")

        response = client.get_device_registry(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.GetDeviceRegistryRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_device_registry_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        name = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")

        with pytest.raises(CustomException):
            client.get_device_registry(name)

    def test_update_device_registry(self):
        # Setup Expected Response
        id_ = "id3355"
        name = "name3373707"
        expected_response = {"id": id_, "name": name}
        expected_response = resources_pb2.DeviceRegistry(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        device_registry = {}
        update_mask = {}

        response = client.update_device_registry(device_registry, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.UpdateDeviceRegistryRequest(
            device_registry=device_registry, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_device_registry_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        device_registry = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_device_registry(device_registry, update_mask)

    def test_delete_device_registry(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        name = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")

        client.delete_device_registry(name)

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.DeleteDeviceRegistryRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_device_registry_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        name = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")

        with pytest.raises(CustomException):
            client.delete_device_registry(name)

    def test_list_device_registries(self):
        # Setup Expected Response
        next_page_token = ""
        device_registries_element = {}
        device_registries = [device_registries_element]
        expected_response = {
            "next_page_token": next_page_token,
            "device_registries": device_registries,
        }
        expected_response = device_manager_pb2.ListDeviceRegistriesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_device_registries(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.device_registries[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.ListDeviceRegistriesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_device_registries_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_device_registries(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_device(self):
        # Setup Expected Response
        id_ = "id3355"
        name = "name3373707"
        num_id = 1034366860
        blocked = True
        expected_response = {
            "id": id_,
            "name": name,
            "num_id": num_id,
            "blocked": blocked,
        }
        expected_response = resources_pb2.Device(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        parent = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")
        device = {}

        response = client.create_device(parent, device)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.CreateDeviceRequest(
            parent=parent, device=device
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_device_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        parent = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")
        device = {}

        with pytest.raises(CustomException):
            client.create_device(parent, device)

    def test_get_device(self):
        # Setup Expected Response
        id_ = "id3355"
        name_2 = "name2-1052831874"
        num_id = 1034366860
        blocked = True
        expected_response = {
            "id": id_,
            "name": name_2,
            "num_id": num_id,
            "blocked": blocked,
        }
        expected_response = resources_pb2.Device(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        name = client.device_path("[PROJECT]", "[LOCATION]", "[REGISTRY]", "[DEVICE]")

        response = client.get_device(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.GetDeviceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_device_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        name = client.device_path("[PROJECT]", "[LOCATION]", "[REGISTRY]", "[DEVICE]")

        with pytest.raises(CustomException):
            client.get_device(name)

    def test_update_device(self):
        # Setup Expected Response
        id_ = "id3355"
        name = "name3373707"
        num_id = 1034366860
        blocked = True
        expected_response = {
            "id": id_,
            "name": name,
            "num_id": num_id,
            "blocked": blocked,
        }
        expected_response = resources_pb2.Device(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        device = {}
        update_mask = {}

        response = client.update_device(device, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.UpdateDeviceRequest(
            device=device, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_device_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        device = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_device(device, update_mask)

    def test_delete_device(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        name = client.device_path("[PROJECT]", "[LOCATION]", "[REGISTRY]", "[DEVICE]")

        client.delete_device(name)

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.DeleteDeviceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_device_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        name = client.device_path("[PROJECT]", "[LOCATION]", "[REGISTRY]", "[DEVICE]")

        with pytest.raises(CustomException):
            client.delete_device(name)

    def test_list_devices(self):
        # Setup Expected Response
        next_page_token = ""
        devices_element = {}
        devices = [devices_element]
        expected_response = {"next_page_token": next_page_token, "devices": devices}
        expected_response = device_manager_pb2.ListDevicesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        parent = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")

        paged_list_response = client.list_devices(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.devices[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.ListDevicesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_devices_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        parent = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")

        paged_list_response = client.list_devices(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_modify_cloud_to_device_config(self):
        # Setup Expected Response
        version = 351608024
        binary_data_2 = b"-37"
        expected_response = {"version": version, "binary_data": binary_data_2}
        expected_response = resources_pb2.DeviceConfig(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        name = client.device_path("[PROJECT]", "[LOCATION]", "[REGISTRY]", "[DEVICE]")
        binary_data = b"40"

        response = client.modify_cloud_to_device_config(name, binary_data)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.ModifyCloudToDeviceConfigRequest(
            name=name, binary_data=binary_data
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_modify_cloud_to_device_config_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        name = client.device_path("[PROJECT]", "[LOCATION]", "[REGISTRY]", "[DEVICE]")
        binary_data = b"40"

        with pytest.raises(CustomException):
            client.modify_cloud_to_device_config(name, binary_data)

    def test_list_device_config_versions(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = device_manager_pb2.ListDeviceConfigVersionsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        name = client.device_path("[PROJECT]", "[LOCATION]", "[REGISTRY]", "[DEVICE]")

        response = client.list_device_config_versions(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.ListDeviceConfigVersionsRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_device_config_versions_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        name = client.device_path("[PROJECT]", "[LOCATION]", "[REGISTRY]", "[DEVICE]")

        with pytest.raises(CustomException):
            client.list_device_config_versions(name)

    def test_list_device_states(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = device_manager_pb2.ListDeviceStatesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        name = client.device_path("[PROJECT]", "[LOCATION]", "[REGISTRY]", "[DEVICE]")

        response = client.list_device_states(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.ListDeviceStatesRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_device_states_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        name = client.device_path("[PROJECT]", "[LOCATION]", "[REGISTRY]", "[DEVICE]")

        with pytest.raises(CustomException):
            client.list_device_states(name)

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
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        resource = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")
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
            client = iot_v1.DeviceManagerClient()

        # Setup request
        resource = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")
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
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        resource = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")

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
            client = iot_v1.DeviceManagerClient()

        # Setup request
        resource = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")

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
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        resource = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")
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
            client = iot_v1.DeviceManagerClient()

        # Setup request
        resource = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)

    def test_send_command_to_device(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = device_manager_pb2.SendCommandToDeviceResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        name = client.device_path("[PROJECT]", "[LOCATION]", "[REGISTRY]", "[DEVICE]")
        binary_data = b"40"

        response = client.send_command_to_device(name, binary_data)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.SendCommandToDeviceRequest(
            name=name, binary_data=binary_data
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_send_command_to_device_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        name = client.device_path("[PROJECT]", "[LOCATION]", "[REGISTRY]", "[DEVICE]")
        binary_data = b"40"

        with pytest.raises(CustomException):
            client.send_command_to_device(name, binary_data)

    def test_bind_device_to_gateway(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = device_manager_pb2.BindDeviceToGatewayResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        parent = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")
        gateway_id = "gatewayId955798774"
        device_id = "deviceId25209764"

        response = client.bind_device_to_gateway(parent, gateway_id, device_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.BindDeviceToGatewayRequest(
            parent=parent, gateway_id=gateway_id, device_id=device_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_bind_device_to_gateway_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        parent = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")
        gateway_id = "gatewayId955798774"
        device_id = "deviceId25209764"

        with pytest.raises(CustomException):
            client.bind_device_to_gateway(parent, gateway_id, device_id)

    def test_unbind_device_from_gateway(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = device_manager_pb2.UnbindDeviceFromGatewayResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup Request
        parent = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")
        gateway_id = "gatewayId955798774"
        device_id = "deviceId25209764"

        response = client.unbind_device_from_gateway(parent, gateway_id, device_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = device_manager_pb2.UnbindDeviceFromGatewayRequest(
            parent=parent, gateway_id=gateway_id, device_id=device_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_unbind_device_from_gateway_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iot_v1.DeviceManagerClient()

        # Setup request
        parent = client.registry_path("[PROJECT]", "[LOCATION]", "[REGISTRY]")
        gateway_id = "gatewayId955798774"
        device_id = "deviceId25209764"

        with pytest.raises(CustomException):
            client.unbind_device_from_gateway(parent, gateway_id, device_id)
