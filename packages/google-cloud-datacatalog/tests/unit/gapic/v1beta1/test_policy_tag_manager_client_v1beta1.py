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

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        response = client.create_taxonomy(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.CreateTaxonomyRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_taxonomy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        with pytest.raises(CustomException):
            client.create_taxonomy(parent)

    def test_delete_taxonomy(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup Request
        name = client.taxonomy_path("[PROJECT]", "[LOCATION]", "[TAXONOMY]")

        client.delete_taxonomy(name)

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.DeleteTaxonomyRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_taxonomy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup request
        name = client.taxonomy_path("[PROJECT]", "[LOCATION]", "[TAXONOMY]")

        with pytest.raises(CustomException):
            client.delete_taxonomy(name)

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
        next_page_token = ""
        taxonomies_element = {}
        taxonomies = [taxonomies_element]
        expected_response = {
            "next_page_token": next_page_token,
            "taxonomies": taxonomies,
        }
        expected_response = policytagmanager_pb2.ListTaxonomiesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_taxonomies(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.taxonomies[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.ListTaxonomiesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_taxonomies_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_taxonomies(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_taxonomy(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name_2,
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

        # Setup Request
        name = client.taxonomy_path("[PROJECT]", "[LOCATION]", "[TAXONOMY]")

        response = client.get_taxonomy(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.GetTaxonomyRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_taxonomy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup request
        name = client.taxonomy_path("[PROJECT]", "[LOCATION]", "[TAXONOMY]")

        with pytest.raises(CustomException):
            client.get_taxonomy(name)

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

        # Setup Request
        parent = client.taxonomy_path("[PROJECT]", "[LOCATION]", "[TAXONOMY]")

        response = client.create_policy_tag(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.CreatePolicyTagRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_policy_tag_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup request
        parent = client.taxonomy_path("[PROJECT]", "[LOCATION]", "[TAXONOMY]")

        with pytest.raises(CustomException):
            client.create_policy_tag(parent)

    def test_delete_policy_tag(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup Request
        name = client.policy_tag_path(
            "[PROJECT]", "[LOCATION]", "[TAXONOMY]", "[POLICY_TAG]"
        )

        client.delete_policy_tag(name)

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.DeletePolicyTagRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_policy_tag_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup request
        name = client.policy_tag_path(
            "[PROJECT]", "[LOCATION]", "[TAXONOMY]", "[POLICY_TAG]"
        )

        with pytest.raises(CustomException):
            client.delete_policy_tag(name)

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
        next_page_token = ""
        policy_tags_element = {}
        policy_tags = [policy_tags_element]
        expected_response = {
            "next_page_token": next_page_token,
            "policy_tags": policy_tags,
        }
        expected_response = policytagmanager_pb2.ListPolicyTagsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup Request
        parent = client.taxonomy_path("[PROJECT]", "[LOCATION]", "[TAXONOMY]")

        paged_list_response = client.list_policy_tags(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.policy_tags[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.ListPolicyTagsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_policy_tags_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup request
        parent = client.taxonomy_path("[PROJECT]", "[LOCATION]", "[TAXONOMY]")

        paged_list_response = client.list_policy_tags(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_policy_tag(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        parent_policy_tag = "parentPolicyTag2071382466"
        expected_response = {
            "name": name_2,
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

        # Setup Request
        name = client.policy_tag_path(
            "[PROJECT]", "[LOCATION]", "[TAXONOMY]", "[POLICY_TAG]"
        )

        response = client.get_policy_tag(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = policytagmanager_pb2.GetPolicyTagRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_policy_tag_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup request
        name = client.policy_tag_path(
            "[PROJECT]", "[LOCATION]", "[TAXONOMY]", "[POLICY_TAG]"
        )

        with pytest.raises(CustomException):
            client.get_policy_tag(name)

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
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup request
        resource = "resource-341064690"

        with pytest.raises(CustomException):
            client.get_iam_policy(resource)

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
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup request
        resource = "resource-341064690"
        policy = {}

        with pytest.raises(CustomException):
            client.set_iam_policy(resource, policy)

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
            client = datacatalog_v1beta1.PolicyTagManagerClient()

        # Setup request
        resource = "resource-341064690"
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)
