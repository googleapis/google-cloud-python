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
from google.cloud.talent_v4beta1.proto import common_pb2
from google.cloud.talent_v4beta1.proto import profile_pb2
from google.cloud.talent_v4beta1.proto import profile_service_pb2
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


class TestProfileServiceClient(object):
    def test_list_profiles(self):
        # Setup Expected Response
        next_page_token = ""
        profiles_element = {}
        profiles = [profiles_element]
        expected_response = {"next_page_token": next_page_token, "profiles": profiles}
        expected_response = profile_service_pb2.ListProfilesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ProfileServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")

        paged_list_response = client.list_profiles(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.profiles[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = profile_service_pb2.ListProfilesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_profiles_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ProfileServiceClient()

        # Setup request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")

        paged_list_response = client.list_profiles(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_profile(self):
        # Setup Expected Response
        name = "name3373707"
        external_id = "externalId-1153075697"
        source = "source-896505829"
        uri = "uri116076"
        group_id = "groupId506361563"
        processed = True
        keyword_snippet = "keywordSnippet1325317319"
        expected_response = {
            "name": name,
            "external_id": external_id,
            "source": source,
            "uri": uri,
            "group_id": group_id,
            "processed": processed,
            "keyword_snippet": keyword_snippet,
        }
        expected_response = profile_pb2.Profile(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ProfileServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        profile = {}

        response = client.create_profile(parent, profile)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = profile_service_pb2.CreateProfileRequest(
            parent=parent, profile=profile
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_profile_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ProfileServiceClient()

        # Setup request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        profile = {}

        with pytest.raises(CustomException):
            client.create_profile(parent, profile)

    def test_get_profile(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        external_id = "externalId-1153075697"
        source = "source-896505829"
        uri = "uri116076"
        group_id = "groupId506361563"
        processed = True
        keyword_snippet = "keywordSnippet1325317319"
        expected_response = {
            "name": name_2,
            "external_id": external_id,
            "source": source,
            "uri": uri,
            "group_id": group_id,
            "processed": processed,
            "keyword_snippet": keyword_snippet,
        }
        expected_response = profile_pb2.Profile(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ProfileServiceClient()

        # Setup Request
        name = client.profile_path("[PROJECT]", "[TENANT]", "[PROFILE]")

        response = client.get_profile(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = profile_service_pb2.GetProfileRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_profile_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ProfileServiceClient()

        # Setup request
        name = client.profile_path("[PROJECT]", "[TENANT]", "[PROFILE]")

        with pytest.raises(CustomException):
            client.get_profile(name)

    def test_update_profile(self):
        # Setup Expected Response
        name = "name3373707"
        external_id = "externalId-1153075697"
        source = "source-896505829"
        uri = "uri116076"
        group_id = "groupId506361563"
        processed = True
        keyword_snippet = "keywordSnippet1325317319"
        expected_response = {
            "name": name,
            "external_id": external_id,
            "source": source,
            "uri": uri,
            "group_id": group_id,
            "processed": processed,
            "keyword_snippet": keyword_snippet,
        }
        expected_response = profile_pb2.Profile(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ProfileServiceClient()

        # Setup Request
        profile = {}

        response = client.update_profile(profile)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = profile_service_pb2.UpdateProfileRequest(profile=profile)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_profile_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ProfileServiceClient()

        # Setup request
        profile = {}

        with pytest.raises(CustomException):
            client.update_profile(profile)

    def test_delete_profile(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ProfileServiceClient()

        # Setup Request
        name = client.profile_path("[PROJECT]", "[TENANT]", "[PROFILE]")

        client.delete_profile(name)

        assert len(channel.requests) == 1
        expected_request = profile_service_pb2.DeleteProfileRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_profile_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ProfileServiceClient()

        # Setup request
        name = client.profile_path("[PROJECT]", "[TENANT]", "[PROFILE]")

        with pytest.raises(CustomException):
            client.delete_profile(name)

    def test_search_profiles(self):
        # Setup Expected Response
        estimated_total_size = 1882144769
        next_page_token = ""
        result_set_id = "resultSetId-770306950"
        summarized_profiles_element = {}
        summarized_profiles = [summarized_profiles_element]
        expected_response = {
            "estimated_total_size": estimated_total_size,
            "next_page_token": next_page_token,
            "result_set_id": result_set_id,
            "summarized_profiles": summarized_profiles,
        }
        expected_response = profile_service_pb2.SearchProfilesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ProfileServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        request_metadata = {}

        paged_list_response = client.search_profiles(parent, request_metadata)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.summarized_profiles[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = profile_service_pb2.SearchProfilesRequest(
            parent=parent, request_metadata=request_metadata
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_profiles_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ProfileServiceClient()

        # Setup request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        request_metadata = {}

        paged_list_response = client.search_profiles(parent, request_metadata)
        with pytest.raises(CustomException):
            list(paged_list_response)
