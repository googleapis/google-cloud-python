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

from google.api import monitored_resource_pb2
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.proto import group_pb2
from google.cloud.monitoring_v3.proto import group_service_pb2
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


class TestGroupServiceClient(object):
    def test_list_groups(self):
        # Setup Expected Response
        next_page_token = ""
        group_element = {}
        group = [group_element]
        expected_response = {"next_page_token": next_page_token, "group": group}
        expected_response = group_service_pb2.ListGroupsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.GroupServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")

        paged_list_response = client.list_groups(name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.group[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = group_service_pb2.ListGroupsRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_groups_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.GroupServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")

        paged_list_response = client.list_groups(name)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_group(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        parent_name = "parentName1015022848"
        filter_ = "filter-1274492040"
        is_cluster = False
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "parent_name": parent_name,
            "filter": filter_,
            "is_cluster": is_cluster,
        }
        expected_response = group_pb2.Group(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.GroupServiceClient()

        # Setup Request
        name = client.group_path("[PROJECT]", "[GROUP]")

        response = client.get_group(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = group_service_pb2.GetGroupRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_group_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.GroupServiceClient()

        # Setup request
        name = client.group_path("[PROJECT]", "[GROUP]")

        with pytest.raises(CustomException):
            client.get_group(name)

    def test_create_group(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        parent_name = "parentName1015022848"
        filter_ = "filter-1274492040"
        is_cluster = False
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "parent_name": parent_name,
            "filter": filter_,
            "is_cluster": is_cluster,
        }
        expected_response = group_pb2.Group(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.GroupServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")
        group = {}

        response = client.create_group(name, group)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = group_service_pb2.CreateGroupRequest(name=name, group=group)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_group_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.GroupServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")
        group = {}

        with pytest.raises(CustomException):
            client.create_group(name, group)

    def test_update_group(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        parent_name = "parentName1015022848"
        filter_ = "filter-1274492040"
        is_cluster = False
        expected_response = {
            "name": name,
            "display_name": display_name,
            "parent_name": parent_name,
            "filter": filter_,
            "is_cluster": is_cluster,
        }
        expected_response = group_pb2.Group(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.GroupServiceClient()

        # Setup Request
        group = {}

        response = client.update_group(group)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = group_service_pb2.UpdateGroupRequest(group=group)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_group_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.GroupServiceClient()

        # Setup request
        group = {}

        with pytest.raises(CustomException):
            client.update_group(group)

    def test_delete_group(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.GroupServiceClient()

        # Setup Request
        name = client.group_path("[PROJECT]", "[GROUP]")

        client.delete_group(name)

        assert len(channel.requests) == 1
        expected_request = group_service_pb2.DeleteGroupRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_group_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.GroupServiceClient()

        # Setup request
        name = client.group_path("[PROJECT]", "[GROUP]")

        with pytest.raises(CustomException):
            client.delete_group(name)

    def test_list_group_members(self):
        # Setup Expected Response
        next_page_token = ""
        total_size = 705419236
        members_element = {}
        members = [members_element]
        expected_response = {
            "next_page_token": next_page_token,
            "total_size": total_size,
            "members": members,
        }
        expected_response = group_service_pb2.ListGroupMembersResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.GroupServiceClient()

        # Setup Request
        name = client.group_path("[PROJECT]", "[GROUP]")

        paged_list_response = client.list_group_members(name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.members[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = group_service_pb2.ListGroupMembersRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_group_members_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.GroupServiceClient()

        # Setup request
        name = client.group_path("[PROJECT]", "[GROUP]")

        paged_list_response = client.list_group_members(name)
        with pytest.raises(CustomException):
            list(paged_list_response)
