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

from google.cloud import iam_credentials_v1
from google.cloud.iam_credentials_v1.proto import common_pb2


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


class TestIAMCredentialsClient(object):
    def test_generate_access_token(self):
        # Setup Expected Response
        access_token = "accessToken-1938933922"
        expected_response = {"access_token": access_token}
        expected_response = common_pb2.GenerateAccessTokenResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iam_credentials_v1.IAMCredentialsClient()

        # Setup Request
        name = client.service_account_path("[PROJECT]", "[SERVICE_ACCOUNT]")
        scope = []

        response = client.generate_access_token(name, scope)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = common_pb2.GenerateAccessTokenRequest(name=name, scope=scope)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_generate_access_token_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iam_credentials_v1.IAMCredentialsClient()

        # Setup request
        name = client.service_account_path("[PROJECT]", "[SERVICE_ACCOUNT]")
        scope = []

        with pytest.raises(CustomException):
            client.generate_access_token(name, scope)

    def test_generate_id_token(self):
        # Setup Expected Response
        token = "token110541305"
        expected_response = {"token": token}
        expected_response = common_pb2.GenerateIdTokenResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iam_credentials_v1.IAMCredentialsClient()

        # Setup Request
        name = client.service_account_path("[PROJECT]", "[SERVICE_ACCOUNT]")
        audience = "audience975628804"

        response = client.generate_id_token(name, audience)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = common_pb2.GenerateIdTokenRequest(
            name=name, audience=audience
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_generate_id_token_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iam_credentials_v1.IAMCredentialsClient()

        # Setup request
        name = client.service_account_path("[PROJECT]", "[SERVICE_ACCOUNT]")
        audience = "audience975628804"

        with pytest.raises(CustomException):
            client.generate_id_token(name, audience)

    def test_sign_blob(self):
        # Setup Expected Response
        key_id = "keyId-1134673157"
        signed_blob = b"-32"
        expected_response = {"key_id": key_id, "signed_blob": signed_blob}
        expected_response = common_pb2.SignBlobResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iam_credentials_v1.IAMCredentialsClient()

        # Setup Request
        name = client.service_account_path("[PROJECT]", "[SERVICE_ACCOUNT]")
        payload = b"-114"

        response = client.sign_blob(name, payload)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = common_pb2.SignBlobRequest(name=name, payload=payload)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_sign_blob_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iam_credentials_v1.IAMCredentialsClient()

        # Setup request
        name = client.service_account_path("[PROJECT]", "[SERVICE_ACCOUNT]")
        payload = b"-114"

        with pytest.raises(CustomException):
            client.sign_blob(name, payload)

    def test_sign_jwt(self):
        # Setup Expected Response
        key_id = "keyId-1134673157"
        signed_jwt = "signedJwt-979546844"
        expected_response = {"key_id": key_id, "signed_jwt": signed_jwt}
        expected_response = common_pb2.SignJwtResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iam_credentials_v1.IAMCredentialsClient()

        # Setup Request
        name = client.service_account_path("[PROJECT]", "[SERVICE_ACCOUNT]")
        payload = "-114"

        response = client.sign_jwt(name, payload)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = common_pb2.SignJwtRequest(name=name, payload=payload)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_sign_jwt_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iam_credentials_v1.IAMCredentialsClient()

        # Setup request
        name = client.service_account_path("[PROJECT]", "[SERVICE_ACCOUNT]")
        payload = "-114"

        with pytest.raises(CustomException):
            client.sign_jwt(name, payload)

    def test_generate_identity_binding_access_token(self):
        # Setup Expected Response
        access_token = "accessToken-1938933922"
        expected_response = {"access_token": access_token}
        expected_response = common_pb2.GenerateIdentityBindingAccessTokenResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iam_credentials_v1.IAMCredentialsClient()

        # Setup Request
        name = client.service_account_path("[PROJECT]", "[SERVICE_ACCOUNT]")
        scope = []
        jwt = "jwt105671"

        response = client.generate_identity_binding_access_token(name, scope, jwt)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = common_pb2.GenerateIdentityBindingAccessTokenRequest(
            name=name, scope=scope, jwt=jwt
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_generate_identity_binding_access_token_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = iam_credentials_v1.IAMCredentialsClient()

        # Setup request
        name = client.service_account_path("[PROJECT]", "[SERVICE_ACCOUNT]")
        scope = []
        jwt = "jwt105671"

        with pytest.raises(CustomException):
            client.generate_identity_binding_access_token(name, scope, jwt)
