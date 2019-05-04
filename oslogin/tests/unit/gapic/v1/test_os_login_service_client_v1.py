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

from google.cloud import oslogin_v1
from google.cloud.oslogin_v1.proto import common_pb2
from google.cloud.oslogin_v1.proto import oslogin_pb2
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


class TestOsLoginServiceClient(object):
    def test_delete_posix_account(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = oslogin_v1.OsLoginServiceClient()

        # Setup Request
        name = client.project_path("[USER]", "[PROJECT]")

        client.delete_posix_account(name)

        assert len(channel.requests) == 1
        expected_request = oslogin_pb2.DeletePosixAccountRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_posix_account_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = oslogin_v1.OsLoginServiceClient()

        # Setup request
        name = client.project_path("[USER]", "[PROJECT]")

        with pytest.raises(CustomException):
            client.delete_posix_account(name)

    def test_delete_ssh_public_key(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = oslogin_v1.OsLoginServiceClient()

        # Setup Request
        name = client.fingerprint_path("[USER]", "[FINGERPRINT]")

        client.delete_ssh_public_key(name)

        assert len(channel.requests) == 1
        expected_request = oslogin_pb2.DeleteSshPublicKeyRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_ssh_public_key_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = oslogin_v1.OsLoginServiceClient()

        # Setup request
        name = client.fingerprint_path("[USER]", "[FINGERPRINT]")

        with pytest.raises(CustomException):
            client.delete_ssh_public_key(name)

    def test_get_login_profile(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        suspended = False
        expected_response = {"name": name_2, "suspended": suspended}
        expected_response = oslogin_pb2.LoginProfile(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = oslogin_v1.OsLoginServiceClient()

        # Setup Request
        name = client.user_path("[USER]")

        response = client.get_login_profile(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = oslogin_pb2.GetLoginProfileRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_login_profile_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = oslogin_v1.OsLoginServiceClient()

        # Setup request
        name = client.user_path("[USER]")

        with pytest.raises(CustomException):
            client.get_login_profile(name)

    def test_get_ssh_public_key(self):
        # Setup Expected Response
        key = "key106079"
        expiration_time_usec = 2058878882
        fingerprint = "fingerprint-1375934236"
        expected_response = {
            "key": key,
            "expiration_time_usec": expiration_time_usec,
            "fingerprint": fingerprint,
        }
        expected_response = common_pb2.SshPublicKey(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = oslogin_v1.OsLoginServiceClient()

        # Setup Request
        name = client.fingerprint_path("[USER]", "[FINGERPRINT]")

        response = client.get_ssh_public_key(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = oslogin_pb2.GetSshPublicKeyRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_ssh_public_key_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = oslogin_v1.OsLoginServiceClient()

        # Setup request
        name = client.fingerprint_path("[USER]", "[FINGERPRINT]")

        with pytest.raises(CustomException):
            client.get_ssh_public_key(name)

    def test_import_ssh_public_key(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = oslogin_pb2.ImportSshPublicKeyResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = oslogin_v1.OsLoginServiceClient()

        # Setup Request
        parent = client.user_path("[USER]")
        ssh_public_key = {}

        response = client.import_ssh_public_key(parent, ssh_public_key)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = oslogin_pb2.ImportSshPublicKeyRequest(
            parent=parent, ssh_public_key=ssh_public_key
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_import_ssh_public_key_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = oslogin_v1.OsLoginServiceClient()

        # Setup request
        parent = client.user_path("[USER]")
        ssh_public_key = {}

        with pytest.raises(CustomException):
            client.import_ssh_public_key(parent, ssh_public_key)

    def test_update_ssh_public_key(self):
        # Setup Expected Response
        key = "key106079"
        expiration_time_usec = 2058878882
        fingerprint = "fingerprint-1375934236"
        expected_response = {
            "key": key,
            "expiration_time_usec": expiration_time_usec,
            "fingerprint": fingerprint,
        }
        expected_response = common_pb2.SshPublicKey(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = oslogin_v1.OsLoginServiceClient()

        # Setup Request
        name = client.fingerprint_path("[USER]", "[FINGERPRINT]")
        ssh_public_key = {}

        response = client.update_ssh_public_key(name, ssh_public_key)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = oslogin_pb2.UpdateSshPublicKeyRequest(
            name=name, ssh_public_key=ssh_public_key
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_ssh_public_key_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = oslogin_v1.OsLoginServiceClient()

        # Setup request
        name = client.fingerprint_path("[USER]", "[FINGERPRINT]")
        ssh_public_key = {}

        with pytest.raises(CustomException):
            client.update_ssh_public_key(name, ssh_public_key)
