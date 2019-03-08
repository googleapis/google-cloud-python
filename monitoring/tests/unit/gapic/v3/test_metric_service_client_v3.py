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

from google.api import metric_pb2 as api_metric_pb2
from google.api import monitored_resource_pb2
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import enums
from google.cloud.monitoring_v3.proto import common_pb2
from google.cloud.monitoring_v3.proto import metric_pb2 as proto_metric_pb2
from google.cloud.monitoring_v3.proto import metric_service_pb2
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


class TestMetricServiceClient(object):
    def test_list_monitored_resource_descriptors(self):
        # Setup Expected Response
        next_page_token = ""
        resource_descriptors_element = {}
        resource_descriptors = [resource_descriptors_element]
        expected_response = {
            "next_page_token": next_page_token,
            "resource_descriptors": resource_descriptors,
        }
        expected_response = metric_service_pb2.ListMonitoredResourceDescriptorsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")

        paged_list_response = client.list_monitored_resource_descriptors(name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.resource_descriptors[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = metric_service_pb2.ListMonitoredResourceDescriptorsRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_monitored_resource_descriptors_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")

        paged_list_response = client.list_monitored_resource_descriptors(name)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_monitored_resource_descriptor(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        type_ = "type3575610"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name_2,
            "type": type_,
            "display_name": display_name,
            "description": description,
        }
        expected_response = monitored_resource_pb2.MonitoredResourceDescriptor(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup Request
        name = client.monitored_resource_descriptor_path(
            "[PROJECT]", "[MONITORED_RESOURCE_DESCRIPTOR]"
        )

        response = client.get_monitored_resource_descriptor(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = metric_service_pb2.GetMonitoredResourceDescriptorRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_monitored_resource_descriptor_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup request
        name = client.monitored_resource_descriptor_path(
            "[PROJECT]", "[MONITORED_RESOURCE_DESCRIPTOR]"
        )

        with pytest.raises(CustomException):
            client.get_monitored_resource_descriptor(name)

    def test_list_metric_descriptors(self):
        # Setup Expected Response
        next_page_token = ""
        metric_descriptors_element = {}
        metric_descriptors = [metric_descriptors_element]
        expected_response = {
            "next_page_token": next_page_token,
            "metric_descriptors": metric_descriptors,
        }
        expected_response = metric_service_pb2.ListMetricDescriptorsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")

        paged_list_response = client.list_metric_descriptors(name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.metric_descriptors[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = metric_service_pb2.ListMetricDescriptorsRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_metric_descriptors_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")

        paged_list_response = client.list_metric_descriptors(name)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_metric_descriptor(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        type_ = "type3575610"
        unit = "unit3594628"
        description = "description-1724546052"
        display_name = "displayName1615086568"
        expected_response = {
            "name": name_2,
            "type": type_,
            "unit": unit,
            "description": description,
            "display_name": display_name,
        }
        expected_response = api_metric_pb2.MetricDescriptor(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup Request
        name = client.metric_descriptor_path("[PROJECT]", "[METRIC_DESCRIPTOR]")

        response = client.get_metric_descriptor(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = metric_service_pb2.GetMetricDescriptorRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_metric_descriptor_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup request
        name = client.metric_descriptor_path("[PROJECT]", "[METRIC_DESCRIPTOR]")

        with pytest.raises(CustomException):
            client.get_metric_descriptor(name)

    def test_create_metric_descriptor(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        type_ = "type3575610"
        unit = "unit3594628"
        description = "description-1724546052"
        display_name = "displayName1615086568"
        expected_response = {
            "name": name_2,
            "type": type_,
            "unit": unit,
            "description": description,
            "display_name": display_name,
        }
        expected_response = api_metric_pb2.MetricDescriptor(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")
        metric_descriptor = {}

        response = client.create_metric_descriptor(name, metric_descriptor)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = metric_service_pb2.CreateMetricDescriptorRequest(
            name=name, metric_descriptor=metric_descriptor
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_metric_descriptor_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")
        metric_descriptor = {}

        with pytest.raises(CustomException):
            client.create_metric_descriptor(name, metric_descriptor)

    def test_delete_metric_descriptor(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup Request
        name = client.metric_descriptor_path("[PROJECT]", "[METRIC_DESCRIPTOR]")

        client.delete_metric_descriptor(name)

        assert len(channel.requests) == 1
        expected_request = metric_service_pb2.DeleteMetricDescriptorRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_metric_descriptor_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup request
        name = client.metric_descriptor_path("[PROJECT]", "[METRIC_DESCRIPTOR]")

        with pytest.raises(CustomException):
            client.delete_metric_descriptor(name)

    def test_list_time_series(self):
        # Setup Expected Response
        next_page_token = ""
        time_series_element = {}
        time_series = [time_series_element]
        expected_response = {
            "next_page_token": next_page_token,
            "time_series": time_series,
        }
        expected_response = metric_service_pb2.ListTimeSeriesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")
        filter_ = "filter-1274492040"
        interval = {}
        view = enums.ListTimeSeriesRequest.TimeSeriesView.FULL

        paged_list_response = client.list_time_series(name, filter_, interval, view)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.time_series[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = metric_service_pb2.ListTimeSeriesRequest(
            name=name, filter=filter_, interval=interval, view=view
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_time_series_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")
        filter_ = "filter-1274492040"
        interval = {}
        view = enums.ListTimeSeriesRequest.TimeSeriesView.FULL

        paged_list_response = client.list_time_series(name, filter_, interval, view)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_time_series(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup Request
        name = client.project_path("[PROJECT]")
        time_series = []

        client.create_time_series(name, time_series)

        assert len(channel.requests) == 1
        expected_request = metric_service_pb2.CreateTimeSeriesRequest(
            name=name, time_series=time_series
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_time_series_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = monitoring_v3.MetricServiceClient()

        # Setup request
        name = client.project_path("[PROJECT]")
        time_series = []

        with pytest.raises(CustomException):
            client.create_time_series(name, time_series)
