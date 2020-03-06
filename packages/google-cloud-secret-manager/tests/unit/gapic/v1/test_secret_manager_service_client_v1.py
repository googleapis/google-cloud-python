# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

from google.cloud import secretmanager_v1
from google.cloud.secretmanager_v1.proto import resources_pb2
from google.cloud.secretmanager_v1.proto import service_pb2
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


class TestSecretManagerServiceClient(object):
    def test_list_secrets(self):
        # Setup Expected Response
        next_page_token = ""
        total_size = 705419236
        secrets_element = {}
        secrets = [secrets_element]
        expected_response = {
            "next_page_token": next_page_token,
            "total_size": total_size,
            "secrets": secrets,
        }
        expected_response = service_pb2.ListSecretsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_secrets(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.secrets[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = service_pb2.ListSecretsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_secrets_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_secrets(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_secret(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = resources_pb2.Secret(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        secret_id = "secretId-739547894"
        secret = {}

        response = client.create_secret(parent, secret_id, secret)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.CreateSecretRequest(
            parent=parent, secret_id=secret_id, secret=secret
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_secret_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        secret_id = "secretId-739547894"
        secret = {}

        with pytest.raises(CustomException):
            client.create_secret(parent, secret_id, secret)

    def test_add_secret_version(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = resources_pb2.SecretVersion(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        parent = client.secret_path("[PROJECT]", "[SECRET]")
        payload = {}

        response = client.add_secret_version(parent, payload)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.AddSecretVersionRequest(
            parent=parent, payload=payload
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_add_secret_version_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        parent = client.secret_path("[PROJECT]", "[SECRET]")
        payload = {}

        with pytest.raises(CustomException):
            client.add_secret_version(parent, payload)

    def test_get_secret(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = resources_pb2.Secret(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        name = client.secret_path("[PROJECT]", "[SECRET]")

        response = client.get_secret(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.GetSecretRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_secret_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        name = client.secret_path("[PROJECT]", "[SECRET]")

        with pytest.raises(CustomException):
            client.get_secret(name)

    def test_update_secret(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = resources_pb2.Secret(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        secret = {}
        update_mask = {}

        response = client.update_secret(secret, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.UpdateSecretRequest(
            secret=secret, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_secret_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        secret = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_secret(secret, update_mask)

    def test_delete_secret(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        name = client.secret_path("[PROJECT]", "[SECRET]")

        client.delete_secret(name)

        assert len(channel.requests) == 1
        expected_request = service_pb2.DeleteSecretRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_secret_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        name = client.secret_path("[PROJECT]", "[SECRET]")

        with pytest.raises(CustomException):
            client.delete_secret(name)

    def test_list_secret_versions(self):
        # Setup Expected Response
        next_page_token = ""
        total_size = 705419236
        versions_element = {}
        versions = [versions_element]
        expected_response = {
            "next_page_token": next_page_token,
            "total_size": total_size,
            "versions": versions,
        }
        expected_response = service_pb2.ListSecretVersionsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        parent = client.secret_path("[PROJECT]", "[SECRET]")

        paged_list_response = client.list_secret_versions(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.versions[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = service_pb2.ListSecretVersionsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_secret_versions_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        parent = client.secret_path("[PROJECT]", "[SECRET]")

        paged_list_response = client.list_secret_versions(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_secret_version(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = resources_pb2.SecretVersion(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        name = client.secret_version_path("[PROJECT]", "[SECRET]", "[SECRET_VERSION]")

        response = client.get_secret_version(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.GetSecretVersionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_secret_version_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        name = client.secret_version_path("[PROJECT]", "[SECRET]", "[SECRET_VERSION]")

        with pytest.raises(CustomException):
            client.get_secret_version(name)

    def test_access_secret_version(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = service_pb2.AccessSecretVersionResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        name = client.secret_version_path("[PROJECT]", "[SECRET]", "[SECRET_VERSION]")

        response = client.access_secret_version(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.AccessSecretVersionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_access_secret_version_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        name = client.secret_version_path("[PROJECT]", "[SECRET]", "[SECRET_VERSION]")

        with pytest.raises(CustomException):
            client.access_secret_version(name)

    def test_disable_secret_version(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = resources_pb2.SecretVersion(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        name = client.secret_version_path("[PROJECT]", "[SECRET]", "[SECRET_VERSION]")

        response = client.disable_secret_version(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.DisableSecretVersionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_disable_secret_version_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        name = client.secret_version_path("[PROJECT]", "[SECRET]", "[SECRET_VERSION]")

        with pytest.raises(CustomException):
            client.disable_secret_version(name)

    def test_enable_secret_version(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = resources_pb2.SecretVersion(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        name = client.secret_version_path("[PROJECT]", "[SECRET]", "[SECRET_VERSION]")

        response = client.enable_secret_version(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.EnableSecretVersionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_enable_secret_version_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        name = client.secret_version_path("[PROJECT]", "[SECRET]", "[SECRET_VERSION]")

        with pytest.raises(CustomException):
            client.enable_secret_version(name)

    def test_destroy_secret_version(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = resources_pb2.SecretVersion(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        name = client.secret_version_path("[PROJECT]", "[SECRET]", "[SECRET_VERSION]")

        response = client.destroy_secret_version(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.DestroySecretVersionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_destroy_secret_version_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        name = client.secret_version_path("[PROJECT]", "[SECRET]", "[SECRET_VERSION]")

        with pytest.raises(CustomException):
            client.destroy_secret_version(name)

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
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        resource = "resource-341064690"
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
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        resource = "resource-341064690"
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
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        resource = "resource-341064690"

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
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        resource = "resource-341064690"

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
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup Request
        resource = "resource-341064690"
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
            client = secretmanager_v1.SecretManagerServiceClient()

        # Setup request
        resource = "resource-341064690"
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)
