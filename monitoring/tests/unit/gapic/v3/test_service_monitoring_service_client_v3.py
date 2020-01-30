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

from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.proto import service_pb2
from google.cloud.monitoring_v3.proto import service_service_pb2
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


class TestServiceMonitoringServiceClient(object):
    def test_create_service(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        expected_response = {"name": name, "display_name": display_name}
        expected_response = service_pb2.Service(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        service = {}

        response = client.create_service(parent, service)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_service_pb2.CreateServiceRequest(
            parent=parent, service=service
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_service_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        service = {}

        with pytest.raises(CustomException):
            client.create_service(parent, service)

    def test_get_service(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        expected_response = {"name": name_2, "display_name": display_name}
        expected_response = service_pb2.Service(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup Request
        name = client.service_path("[PROJECT]", "[SERVICE]")

        response = client.get_service(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_service_pb2.GetServiceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_service_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup request
        name = client.service_path("[PROJECT]", "[SERVICE]")

        with pytest.raises(CustomException):
            client.get_service(name)

    def test_list_services(self):
        # Setup Expected Response
        next_page_token = ""
        services_element = {}
        services = [services_element]
        expected_response = {"next_page_token": next_page_token, "services": services}
        expected_response = service_service_pb2.ListServicesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_services(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.services[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = service_service_pb2.ListServicesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_services_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_services(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_update_service(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        expected_response = {"name": name, "display_name": display_name}
        expected_response = service_pb2.Service(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup Request
        service = {}

        response = client.update_service(service)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_service_pb2.UpdateServiceRequest(service=service)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_service_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup request
        service = {}

        with pytest.raises(CustomException):
            client.update_service(service)

    def test_delete_service(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup Request
        name = client.service_path("[PROJECT]", "[SERVICE]")

        client.delete_service(name)

        assert len(channel.requests) == 1
        expected_request = service_service_pb2.DeleteServiceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_service_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup request
        name = client.service_path("[PROJECT]", "[SERVICE]")

        with pytest.raises(CustomException):
            client.delete_service(name)

    def test_create_service_level_objective(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        goal = 317825.0
        expected_response = {"name": name, "display_name": display_name, "goal": goal}
        expected_response = service_pb2.ServiceLevelObjective(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup Request
        parent = client.service_path("[PROJECT]", "[SERVICE]")
        service_level_objective = {}

        response = client.create_service_level_objective(
            parent, service_level_objective
        )
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_service_pb2.CreateServiceLevelObjectiveRequest(
            parent=parent, service_level_objective=service_level_objective
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_service_level_objective_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup request
        parent = client.service_path("[PROJECT]", "[SERVICE]")
        service_level_objective = {}

        with pytest.raises(CustomException):
            client.create_service_level_objective(parent, service_level_objective)

    def test_get_service_level_objective(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        goal = 317825.0
        expected_response = {"name": name_2, "display_name": display_name, "goal": goal}
        expected_response = service_pb2.ServiceLevelObjective(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup Request
        name = client.service_level_objective_path(
            "[PROJECT]", "[SERVICE]", "[SERVICE_LEVEL_OBJECTIVE]"
        )

        response = client.get_service_level_objective(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_service_pb2.GetServiceLevelObjectiveRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_service_level_objective_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup request
        name = client.service_level_objective_path(
            "[PROJECT]", "[SERVICE]", "[SERVICE_LEVEL_OBJECTIVE]"
        )

        with pytest.raises(CustomException):
            client.get_service_level_objective(name)

    def test_list_service_level_objectives(self):
        # Setup Expected Response
        next_page_token = ""
        service_level_objectives_element = {}
        service_level_objectives = [service_level_objectives_element]
        expected_response = {
            "next_page_token": next_page_token,
            "service_level_objectives": service_level_objectives,
        }
        expected_response = service_service_pb2.ListServiceLevelObjectivesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup Request
        parent = client.service_path("[PROJECT]", "[SERVICE]")

        paged_list_response = client.list_service_level_objectives(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.service_level_objectives[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = service_service_pb2.ListServiceLevelObjectivesRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_service_level_objectives_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup request
        parent = client.service_path("[PROJECT]", "[SERVICE]")

        paged_list_response = client.list_service_level_objectives(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_update_service_level_objective(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        goal = 317825.0
        expected_response = {"name": name, "display_name": display_name, "goal": goal}
        expected_response = service_pb2.ServiceLevelObjective(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup Request
        service_level_objective = {}

        response = client.update_service_level_objective(service_level_objective)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = service_service_pb2.UpdateServiceLevelObjectiveRequest(
            service_level_objective=service_level_objective
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_service_level_objective_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup request
        service_level_objective = {}

        with pytest.raises(CustomException):
            client.update_service_level_objective(service_level_objective)

    def test_delete_service_level_objective(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup Request
        name = client.service_level_objective_path(
            "[PROJECT]", "[SERVICE]", "[SERVICE_LEVEL_OBJECTIVE]"
        )

        client.delete_service_level_objective(name)

        assert len(channel.requests) == 1
        expected_request = service_service_pb2.DeleteServiceLevelObjectiveRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_service_level_objective_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.ServiceMonitoringServiceClient()

        # Setup request
        name = client.service_level_objective_path(
            "[PROJECT]", "[SERVICE]", "[SERVICE_LEVEL_OBJECTIVE]"
        )

        with pytest.raises(CustomException):
            client.delete_service_level_objective(name)
