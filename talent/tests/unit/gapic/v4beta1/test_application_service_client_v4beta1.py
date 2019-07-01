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
from google.cloud.talent_v4beta1.proto import application_pb2
from google.cloud.talent_v4beta1.proto import application_service_pb2
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


class TestApplicationServiceClient(object):
    def test_create_application(self):
        # Setup Expected Response
        name = "name3373707"
        external_id = "externalId-1153075697"
        profile = "profile-309425751"
        job = "job105405"
        company = "company950484093"
        outcome_notes = "outcomeNotes-355961964"
        job_title_snippet = "jobTitleSnippet-1100512972"
        expected_response = {
            "name": name,
            "external_id": external_id,
            "profile": profile,
            "job": job,
            "company": company,
            "outcome_notes": outcome_notes,
            "job_title_snippet": job_title_snippet,
        }
        expected_response = application_pb2.Application(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ApplicationServiceClient()

        # Setup Request
        parent = client.profile_path("[PROJECT]", "[TENANT]", "[PROFILE]")
        application = {}

        response = client.create_application(parent, application)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = application_service_pb2.CreateApplicationRequest(
            parent=parent, application=application
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_application_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ApplicationServiceClient()

        # Setup request
        parent = client.profile_path("[PROJECT]", "[TENANT]", "[PROFILE]")
        application = {}

        with pytest.raises(CustomException):
            client.create_application(parent, application)

    def test_get_application(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        external_id = "externalId-1153075697"
        profile = "profile-309425751"
        job = "job105405"
        company = "company950484093"
        outcome_notes = "outcomeNotes-355961964"
        job_title_snippet = "jobTitleSnippet-1100512972"
        expected_response = {
            "name": name_2,
            "external_id": external_id,
            "profile": profile,
            "job": job,
            "company": company,
            "outcome_notes": outcome_notes,
            "job_title_snippet": job_title_snippet,
        }
        expected_response = application_pb2.Application(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ApplicationServiceClient()

        # Setup Request
        name = client.application_path(
            "[PROJECT]", "[TENANT]", "[PROFILE]", "[APPLICATION]"
        )

        response = client.get_application(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = application_service_pb2.GetApplicationRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_application_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ApplicationServiceClient()

        # Setup request
        name = client.application_path(
            "[PROJECT]", "[TENANT]", "[PROFILE]", "[APPLICATION]"
        )

        with pytest.raises(CustomException):
            client.get_application(name)

    def test_update_application(self):
        # Setup Expected Response
        name = "name3373707"
        external_id = "externalId-1153075697"
        profile = "profile-309425751"
        job = "job105405"
        company = "company950484093"
        outcome_notes = "outcomeNotes-355961964"
        job_title_snippet = "jobTitleSnippet-1100512972"
        expected_response = {
            "name": name,
            "external_id": external_id,
            "profile": profile,
            "job": job,
            "company": company,
            "outcome_notes": outcome_notes,
            "job_title_snippet": job_title_snippet,
        }
        expected_response = application_pb2.Application(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ApplicationServiceClient()

        # Setup Request
        application = {}

        response = client.update_application(application)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = application_service_pb2.UpdateApplicationRequest(
            application=application
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_application_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ApplicationServiceClient()

        # Setup request
        application = {}

        with pytest.raises(CustomException):
            client.update_application(application)

    def test_delete_application(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ApplicationServiceClient()

        # Setup Request
        name = client.application_path(
            "[PROJECT]", "[TENANT]", "[PROFILE]", "[APPLICATION]"
        )

        client.delete_application(name)

        assert len(channel.requests) == 1
        expected_request = application_service_pb2.DeleteApplicationRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_application_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ApplicationServiceClient()

        # Setup request
        name = client.application_path(
            "[PROJECT]", "[TENANT]", "[PROFILE]", "[APPLICATION]"
        )

        with pytest.raises(CustomException):
            client.delete_application(name)

    def test_list_applications(self):
        # Setup Expected Response
        next_page_token = ""
        applications_element = {}
        applications = [applications_element]
        expected_response = {
            "next_page_token": next_page_token,
            "applications": applications,
        }
        expected_response = application_service_pb2.ListApplicationsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ApplicationServiceClient()

        # Setup Request
        parent = client.profile_path("[PROJECT]", "[TENANT]", "[PROFILE]")

        paged_list_response = client.list_applications(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.applications[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = application_service_pb2.ListApplicationsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_applications_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.ApplicationServiceClient()

        # Setup request
        parent = client.profile_path("[PROJECT]", "[TENANT]", "[PROFILE]")

        paged_list_response = client.list_applications(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)
