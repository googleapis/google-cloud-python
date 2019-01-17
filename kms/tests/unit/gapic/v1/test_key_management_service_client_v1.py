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

from google.cloud import kms_v1
from google.cloud.kms_v1 import enums
from google.cloud.kms_v1.proto import resources_pb2
from google.cloud.kms_v1.proto import service_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import duration_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2


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


class TestKeyManagementServiceClient(object):
    def test_list_key_rings(self):
        # Setup Expected Response
        next_page_token = ""
        total_size = 705419236
        key_rings_element = {}
        key_rings = [key_rings_element]
        expected_response = {
            "next_page_token": next_page_token,
            "total_size": total_size,
            "key_rings": key_rings,
        }
        expected_response = service_pb2.ListKeyRingsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_key_rings(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.key_rings[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = service_pb2.ListKeyRingsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_key_rings_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_key_rings(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_list_crypto_keys(self):
        # Setup Expected Response
        next_page_token = ""
        total_size = 705419236
        crypto_keys_element = {}
        crypto_keys = [crypto_keys_element]
        expected_response = {
            "next_page_token": next_page_token,
            "total_size": total_size,
            "crypto_keys": crypto_keys,
        }
        expected_response = service_pb2.ListCryptoKeysResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        parent = client.key_ring_path("[PROJECT]", "[LOCATION]", "[KEY_RING]")

        paged_list_response = client.list_crypto_keys(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.crypto_keys[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = service_pb2.ListCryptoKeysRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_crypto_keys_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        parent = client.key_ring_path("[PROJECT]", "[LOCATION]", "[KEY_RING]")

        paged_list_response = client.list_crypto_keys(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_list_crypto_key_versions(self):
        # Setup Expected Response
        next_page_token = ""
        total_size = 705419236
        crypto_key_versions_element = {}
        crypto_key_versions = [crypto_key_versions_element]
        expected_response = {
            "next_page_token": next_page_token,
            "total_size": total_size,
            "crypto_key_versions": crypto_key_versions,
        }
        expected_response = service_pb2.ListCryptoKeyVersionsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        parent = client.crypto_key_path(
            "[PROJECT]", "[LOCATION]", "[KEY_RING]", "[CRYPTO_KEY]"
        )

        paged_list_response = client.list_crypto_key_versions(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.crypto_key_versions[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = service_pb2.ListCryptoKeyVersionsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_crypto_key_versions_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        parent = client.crypto_key_path(
            "[PROJECT]", "[LOCATION]", "[KEY_RING]", "[CRYPTO_KEY]"
        )

        paged_list_response = client.list_crypto_key_versions(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_key_ring(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = resources_pb2.KeyRing(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        name = client.key_ring_path("[PROJECT]", "[LOCATION]", "[KEY_RING]")

        response = client.get_key_ring(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.GetKeyRingRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_key_ring_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        name = client.key_ring_path("[PROJECT]", "[LOCATION]", "[KEY_RING]")

        with pytest.raises(CustomException):
            client.get_key_ring(name)

    def test_get_crypto_key(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = resources_pb2.CryptoKey(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        name = client.crypto_key_path(
            "[PROJECT]", "[LOCATION]", "[KEY_RING]", "[CRYPTO_KEY]"
        )

        response = client.get_crypto_key(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.GetCryptoKeyRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_crypto_key_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        name = client.crypto_key_path(
            "[PROJECT]", "[LOCATION]", "[KEY_RING]", "[CRYPTO_KEY]"
        )

        with pytest.raises(CustomException):
            client.get_crypto_key(name)

    def test_get_crypto_key_version(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = resources_pb2.CryptoKeyVersion(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        name = client.crypto_key_version_path(
            "[PROJECT]",
            "[LOCATION]",
            "[KEY_RING]",
            "[CRYPTO_KEY]",
            "[CRYPTO_KEY_VERSION]",
        )

        response = client.get_crypto_key_version(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.GetCryptoKeyVersionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_crypto_key_version_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        name = client.crypto_key_version_path(
            "[PROJECT]",
            "[LOCATION]",
            "[KEY_RING]",
            "[CRYPTO_KEY]",
            "[CRYPTO_KEY_VERSION]",
        )

        with pytest.raises(CustomException):
            client.get_crypto_key_version(name)

    def test_create_key_ring(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = resources_pb2.KeyRing(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        key_ring_id = "keyRingId-2056646742"
        key_ring = {}

        response = client.create_key_ring(parent, key_ring_id, key_ring)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.CreateKeyRingRequest(
            parent=parent, key_ring_id=key_ring_id, key_ring=key_ring
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_key_ring_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        key_ring_id = "keyRingId-2056646742"
        key_ring = {}

        with pytest.raises(CustomException):
            client.create_key_ring(parent, key_ring_id, key_ring)

    def test_create_crypto_key(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = resources_pb2.CryptoKey(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        parent = client.key_ring_path("[PROJECT]", "[LOCATION]", "[KEY_RING]")
        crypto_key_id = "my-app-key"
        purpose = enums.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
        seconds = 2147483647
        next_rotation_time = {"seconds": seconds}
        seconds_2 = 604800
        rotation_period = {"seconds": seconds_2}
        crypto_key = {
            "purpose": purpose,
            "next_rotation_time": next_rotation_time,
            "rotation_period": rotation_period,
        }

        response = client.create_crypto_key(parent, crypto_key_id, crypto_key)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.CreateCryptoKeyRequest(
            parent=parent, crypto_key_id=crypto_key_id, crypto_key=crypto_key
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_crypto_key_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        parent = client.key_ring_path("[PROJECT]", "[LOCATION]", "[KEY_RING]")
        crypto_key_id = "my-app-key"
        purpose = enums.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
        seconds = 2147483647
        next_rotation_time = {"seconds": seconds}
        seconds_2 = 604800
        rotation_period = {"seconds": seconds_2}
        crypto_key = {
            "purpose": purpose,
            "next_rotation_time": next_rotation_time,
            "rotation_period": rotation_period,
        }

        with pytest.raises(CustomException):
            client.create_crypto_key(parent, crypto_key_id, crypto_key)

    def test_create_crypto_key_version(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = resources_pb2.CryptoKeyVersion(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        parent = client.crypto_key_path(
            "[PROJECT]", "[LOCATION]", "[KEY_RING]", "[CRYPTO_KEY]"
        )
        crypto_key_version = {}

        response = client.create_crypto_key_version(parent, crypto_key_version)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.CreateCryptoKeyVersionRequest(
            parent=parent, crypto_key_version=crypto_key_version
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_crypto_key_version_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        parent = client.crypto_key_path(
            "[PROJECT]", "[LOCATION]", "[KEY_RING]", "[CRYPTO_KEY]"
        )
        crypto_key_version = {}

        with pytest.raises(CustomException):
            client.create_crypto_key_version(parent, crypto_key_version)

    def test_update_crypto_key(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = resources_pb2.CryptoKey(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        crypto_key = {}
        update_mask = {}

        response = client.update_crypto_key(crypto_key, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.UpdateCryptoKeyRequest(
            crypto_key=crypto_key, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_crypto_key_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        crypto_key = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_crypto_key(crypto_key, update_mask)

    def test_update_crypto_key_version(self):
        # Setup Expected Response
        name = "name3373707"
        expected_response = {"name": name}
        expected_response = resources_pb2.CryptoKeyVersion(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        crypto_key_version = {}
        update_mask = {}

        response = client.update_crypto_key_version(crypto_key_version, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.UpdateCryptoKeyVersionRequest(
            crypto_key_version=crypto_key_version, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_crypto_key_version_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        crypto_key_version = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_crypto_key_version(crypto_key_version, update_mask)

    def test_encrypt(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        ciphertext = b"-72"
        expected_response = {"name": name_2, "ciphertext": ciphertext}
        expected_response = service_pb2.EncryptResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        name = client.crypto_key_path_path(
            "[PROJECT]", "[LOCATION]", "[KEY_RING]", "[CRYPTO_KEY_PATH]"
        )
        plaintext = b"-9"

        response = client.encrypt(name, plaintext)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.EncryptRequest(name=name, plaintext=plaintext)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_encrypt_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        name = client.crypto_key_path_path(
            "[PROJECT]", "[LOCATION]", "[KEY_RING]", "[CRYPTO_KEY_PATH]"
        )
        plaintext = b"-9"

        with pytest.raises(CustomException):
            client.encrypt(name, plaintext)

    def test_decrypt(self):
        # Setup Expected Response
        plaintext = b"-9"
        expected_response = {"plaintext": plaintext}
        expected_response = service_pb2.DecryptResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        name = client.crypto_key_path(
            "[PROJECT]", "[LOCATION]", "[KEY_RING]", "[CRYPTO_KEY]"
        )
        ciphertext = b"-72"

        response = client.decrypt(name, ciphertext)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.DecryptRequest(name=name, ciphertext=ciphertext)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_decrypt_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        name = client.crypto_key_path(
            "[PROJECT]", "[LOCATION]", "[KEY_RING]", "[CRYPTO_KEY]"
        )
        ciphertext = b"-72"

        with pytest.raises(CustomException):
            client.decrypt(name, ciphertext)

    def test_update_crypto_key_primary_version(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = resources_pb2.CryptoKey(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        name = client.crypto_key_path(
            "[PROJECT]", "[LOCATION]", "[KEY_RING]", "[CRYPTO_KEY]"
        )
        crypto_key_version_id = "cryptoKeyVersionId729489152"

        response = client.update_crypto_key_primary_version(name, crypto_key_version_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.UpdateCryptoKeyPrimaryVersionRequest(
            name=name, crypto_key_version_id=crypto_key_version_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_crypto_key_primary_version_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        name = client.crypto_key_path(
            "[PROJECT]", "[LOCATION]", "[KEY_RING]", "[CRYPTO_KEY]"
        )
        crypto_key_version_id = "cryptoKeyVersionId729489152"

        with pytest.raises(CustomException):
            client.update_crypto_key_primary_version(name, crypto_key_version_id)

    def test_destroy_crypto_key_version(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = resources_pb2.CryptoKeyVersion(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        name = client.crypto_key_version_path(
            "[PROJECT]",
            "[LOCATION]",
            "[KEY_RING]",
            "[CRYPTO_KEY]",
            "[CRYPTO_KEY_VERSION]",
        )

        response = client.destroy_crypto_key_version(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.DestroyCryptoKeyVersionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_destroy_crypto_key_version_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        name = client.crypto_key_version_path(
            "[PROJECT]",
            "[LOCATION]",
            "[KEY_RING]",
            "[CRYPTO_KEY]",
            "[CRYPTO_KEY_VERSION]",
        )

        with pytest.raises(CustomException):
            client.destroy_crypto_key_version(name)

    def test_restore_crypto_key_version(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = resources_pb2.CryptoKeyVersion(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        name = client.crypto_key_version_path(
            "[PROJECT]",
            "[LOCATION]",
            "[KEY_RING]",
            "[CRYPTO_KEY]",
            "[CRYPTO_KEY_VERSION]",
        )

        response = client.restore_crypto_key_version(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.RestoreCryptoKeyVersionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_restore_crypto_key_version_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        name = client.crypto_key_version_path(
            "[PROJECT]",
            "[LOCATION]",
            "[KEY_RING]",
            "[CRYPTO_KEY]",
            "[CRYPTO_KEY_VERSION]",
        )

        with pytest.raises(CustomException):
            client.restore_crypto_key_version(name)

    def test_get_public_key(self):
        # Setup Expected Response
        pem = "pem110872"
        expected_response = {"pem": pem}
        expected_response = resources_pb2.PublicKey(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        name = client.crypto_key_version_path(
            "[PROJECT]",
            "[LOCATION]",
            "[KEY_RING]",
            "[CRYPTO_KEY]",
            "[CRYPTO_KEY_VERSION]",
        )

        response = client.get_public_key(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.GetPublicKeyRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_public_key_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        name = client.crypto_key_version_path(
            "[PROJECT]",
            "[LOCATION]",
            "[KEY_RING]",
            "[CRYPTO_KEY]",
            "[CRYPTO_KEY_VERSION]",
        )

        with pytest.raises(CustomException):
            client.get_public_key(name)

    def test_asymmetric_decrypt(self):
        # Setup Expected Response
        plaintext = b"-9"
        expected_response = {"plaintext": plaintext}
        expected_response = service_pb2.AsymmetricDecryptResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        name = client.crypto_key_version_path(
            "[PROJECT]",
            "[LOCATION]",
            "[KEY_RING]",
            "[CRYPTO_KEY]",
            "[CRYPTO_KEY_VERSION]",
        )
        ciphertext = b"-72"

        response = client.asymmetric_decrypt(name, ciphertext)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.AsymmetricDecryptRequest(
            name=name, ciphertext=ciphertext
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_asymmetric_decrypt_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        name = client.crypto_key_version_path(
            "[PROJECT]",
            "[LOCATION]",
            "[KEY_RING]",
            "[CRYPTO_KEY]",
            "[CRYPTO_KEY_VERSION]",
        )
        ciphertext = b"-72"

        with pytest.raises(CustomException):
            client.asymmetric_decrypt(name, ciphertext)

    def test_asymmetric_sign(self):
        # Setup Expected Response
        signature = b"-100"
        expected_response = {"signature": signature}
        expected_response = service_pb2.AsymmetricSignResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        name = client.crypto_key_version_path(
            "[PROJECT]",
            "[LOCATION]",
            "[KEY_RING]",
            "[CRYPTO_KEY]",
            "[CRYPTO_KEY_VERSION]",
        )
        digest = {}

        response = client.asymmetric_sign(name, digest)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_pb2.AsymmetricSignRequest(name=name, digest=digest)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_asymmetric_sign_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        name = client.crypto_key_version_path(
            "[PROJECT]",
            "[LOCATION]",
            "[KEY_RING]",
            "[CRYPTO_KEY]",
            "[CRYPTO_KEY_VERSION]",
        )
        digest = {}

        with pytest.raises(CustomException):
            client.asymmetric_sign(name, digest)

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
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        resource = client.key_ring_path("[PROJECT]", "[LOCATION]", "[KEY_RING]")
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
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        resource = client.key_ring_path("[PROJECT]", "[LOCATION]", "[KEY_RING]")
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
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        resource = client.key_ring_path("[PROJECT]", "[LOCATION]", "[KEY_RING]")

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
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        resource = client.key_ring_path("[PROJECT]", "[LOCATION]", "[KEY_RING]")

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
            client = kms_v1.KeyManagementServiceClient()

        # Setup Request
        resource = client.key_ring_path("[PROJECT]", "[LOCATION]", "[KEY_RING]")
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
            client = kms_v1.KeyManagementServiceClient()

        # Setup request
        resource = client.key_ring_path("[PROJECT]", "[LOCATION]", "[KEY_RING]")
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)
