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

from google.cloud import talent_v4beta1
from google.cloud.talent_v4beta1.proto import tenant_pb2
from google.cloud.talent_v4beta1.proto import tenant_service_pb2
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


class TestTenantServiceClient(object):
    def test_create_tenant(self):
        # Setup Expected Response
        name = "name3373707"
        external_id = "externalId-1153075697"
        expected_response = {"name": name, "external_id": external_id}
        expected_response = tenant_pb2.Tenant(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.TenantServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        tenant = {}

        response = client.create_tenant(parent, tenant)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = tenant_service_pb2.CreateTenantRequest(
            parent=parent, tenant=tenant
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_tenant_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.TenantServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        tenant = {}

        with pytest.raises(CustomException):
            client.create_tenant(parent, tenant)

    def test_get_tenant(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        external_id = "externalId-1153075697"
        expected_response = {"name": name_2, "external_id": external_id}
        expected_response = tenant_pb2.Tenant(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.TenantServiceClient()

        # Setup Request
        name = client.tenant_path("[PROJECT]", "[TENANT]")

        response = client.get_tenant(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = tenant_service_pb2.GetTenantRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_tenant_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.TenantServiceClient()

        # Setup request
        name = client.tenant_path("[PROJECT]", "[TENANT]")

        with pytest.raises(CustomException):
            client.get_tenant(name)

    def test_update_tenant(self):
        # Setup Expected Response
        name = "name3373707"
        external_id = "externalId-1153075697"
        expected_response = {"name": name, "external_id": external_id}
        expected_response = tenant_pb2.Tenant(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.TenantServiceClient()

        # Setup Request
        tenant = {}

        response = client.update_tenant(tenant)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = tenant_service_pb2.UpdateTenantRequest(tenant=tenant)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_tenant_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.TenantServiceClient()

        # Setup request
        tenant = {}

        with pytest.raises(CustomException):
            client.update_tenant(tenant)

    def test_delete_tenant(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.TenantServiceClient()

        # Setup Request
        name = client.tenant_path("[PROJECT]", "[TENANT]")

        client.delete_tenant(name)

        assert len(channel.requests) == 1
        expected_request = tenant_service_pb2.DeleteTenantRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_tenant_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.TenantServiceClient()

        # Setup request
        name = client.tenant_path("[PROJECT]", "[TENANT]")

        with pytest.raises(CustomException):
            client.delete_tenant(name)

    def test_list_tenants(self):
        # Setup Expected Response
        next_page_token = ""
        tenants_element = {}
        tenants = [tenants_element]
        expected_response = {"next_page_token": next_page_token, "tenants": tenants}
        expected_response = tenant_service_pb2.ListTenantsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.TenantServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_tenants(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.tenants[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = tenant_service_pb2.ListTenantsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_tenants_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.TenantServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_tenants(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)
