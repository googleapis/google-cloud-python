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

from google.cloud import datacatalog_v1beta1
from google.cloud.datacatalog_v1beta1.proto import policytagmanager_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
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


class TestPolicyTagManagerClient(object):
    def test_create_taxonomy(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
        }
        expected_response = policytagmanager_pb2.Taxonomy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        response = client.create_taxonomy()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.CreateTaxonomyRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_taxonomy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.create_taxonomy()

    def test_delete_taxonomy(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        client.delete_taxonomy()

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.DeleteTaxonomyRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_taxonomy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.delete_taxonomy()

    def test_update_taxonomy(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
        }
        expected_response = policytagmanager_pb2.Taxonomy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        response = client.update_taxonomy()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.UpdateTaxonomyRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_taxonomy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.update_taxonomy()

    def test_list_taxonomies(self):
        # Setup Expected Response
        next_page_token = "nextPageToken-1530815211"
        expected_response = {"next_page_token": next_page_token}
        expected_response = policytagmanager_pb2.ListTaxonomiesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        response = client.list_taxonomies()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.ListTaxonomiesRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_taxonomies_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.list_taxonomies()

    def test_get_taxonomy(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
        }
        expected_response = policytagmanager_pb2.Taxonomy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        response = client.get_taxonomy()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.GetTaxonomyRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_taxonomy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.get_taxonomy()

    def test_create_policy_tag(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        parent_policy_tag = "parentPolicyTag2071382466"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
            "parent_policy_tag": parent_policy_tag,
        }
        expected_response = policytagmanager_pb2.PolicyTag(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        response = client.create_policy_tag()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.CreatePolicyTagRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_policy_tag_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.create_policy_tag()

    def test_delete_policy_tag(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        client.delete_policy_tag()

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.DeletePolicyTagRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_policy_tag_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.delete_policy_tag()

    def test_update_policy_tag(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        parent_policy_tag = "parentPolicyTag2071382466"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
            "parent_policy_tag": parent_policy_tag,
        }
        expected_response = policytagmanager_pb2.PolicyTag(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        response = client.update_policy_tag()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.UpdatePolicyTagRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_policy_tag_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.update_policy_tag()

    def test_list_policy_tags(self):
        # Setup Expected Response
        next_page_token = "nextPageToken-1530815211"
        expected_response = {"next_page_token": next_page_token}
        expected_response = policytagmanager_pb2.ListPolicyTagsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        response = client.list_policy_tags()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.ListPolicyTagsRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_policy_tags_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.list_policy_tags()

    def test_get_policy_tag(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        parent_policy_tag = "parentPolicyTag2071382466"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
            "parent_policy_tag": parent_policy_tag,
        }
        expected_response = policytagmanager_pb2.PolicyTag(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        response = client.get_policy_tag()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.GetPolicyTagRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_policy_tag_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.get_policy_tag()

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
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        response = client.get_iam_policy()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.GetIamPolicyRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_iam_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.get_iam_policy()

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
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        response = client.set_iam_policy()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.SetIamPolicyRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_iam_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.set_iam_policy()

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
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        response = client.test_iam_permissions()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.TestIamPermissionsRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_test_iam_permissions_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        with pytest.raises(CustomException):
            client.test_iam_permissions()
