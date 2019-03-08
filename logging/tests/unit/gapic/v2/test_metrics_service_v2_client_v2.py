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

from google.cloud import logging_v2
from google.cloud.logging_v2.proto import logging_metrics_pb2
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


class TestMetricsServiceV2Client(object):
    def test_list_log_metrics(self):
        # Setup Expected Response
        next_page_token = ""
        metrics_element = {}
        metrics = [metrics_element]
        expected_response = {"next_page_token": next_page_token, "metrics": metrics}
        expected_response = logging_metrics_pb2.ListLogMetricsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.MetricsServiceV2Client()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_log_metrics(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.metrics[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = logging_metrics_pb2.ListLogMetricsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_log_metrics_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.MetricsServiceV2Client()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_log_metrics(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_log_metric(self):
        # Setup Expected Response
        name = "name3373707"
        description = "description-1724546052"
        filter_ = "filter-1274492040"
        value_extractor = "valueExtractor2047672534"
        expected_response = {
            "name": name,
            "description": description,
            "filter": filter_,
            "value_extractor": value_extractor,
        }
        expected_response = logging_metrics_pb2.LogMetric(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.MetricsServiceV2Client()

        # Setup Request
        metric_name = client.metric_path("[PROJECT]", "[METRIC]")

        response = client.get_log_metric(metric_name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = logging_metrics_pb2.GetLogMetricRequest(
            metric_name=metric_name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_log_metric_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.MetricsServiceV2Client()

        # Setup request
        metric_name = client.metric_path("[PROJECT]", "[METRIC]")

        with pytest.raises(CustomException):
            client.get_log_metric(metric_name)

    def test_create_log_metric(self):
        # Setup Expected Response
        name = "name3373707"
        description = "description-1724546052"
        filter_ = "filter-1274492040"
        value_extractor = "valueExtractor2047672534"
        expected_response = {
            "name": name,
            "description": description,
            "filter": filter_,
            "value_extractor": value_extractor,
        }
        expected_response = logging_metrics_pb2.LogMetric(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.MetricsServiceV2Client()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        metric = {}

        response = client.create_log_metric(parent, metric)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = logging_metrics_pb2.CreateLogMetricRequest(
            parent=parent, metric=metric
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_log_metric_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.MetricsServiceV2Client()

        # Setup request
        parent = client.project_path("[PROJECT]")
        metric = {}

        with pytest.raises(CustomException):
            client.create_log_metric(parent, metric)

    def test_update_log_metric(self):
        # Setup Expected Response
        name = "name3373707"
        description = "description-1724546052"
        filter_ = "filter-1274492040"
        value_extractor = "valueExtractor2047672534"
        expected_response = {
            "name": name,
            "description": description,
            "filter": filter_,
            "value_extractor": value_extractor,
        }
        expected_response = logging_metrics_pb2.LogMetric(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.MetricsServiceV2Client()

        # Setup Request
        metric_name = client.metric_path("[PROJECT]", "[METRIC]")
        metric = {}

        response = client.update_log_metric(metric_name, metric)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = logging_metrics_pb2.UpdateLogMetricRequest(
            metric_name=metric_name, metric=metric
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_log_metric_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.MetricsServiceV2Client()

        # Setup request
        metric_name = client.metric_path("[PROJECT]", "[METRIC]")
        metric = {}

        with pytest.raises(CustomException):
            client.update_log_metric(metric_name, metric)

    def test_delete_log_metric(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.MetricsServiceV2Client()

        # Setup Request
        metric_name = client.metric_path("[PROJECT]", "[METRIC]")

        client.delete_log_metric(metric_name)

        assert len(channel.requests) == 1
        expected_request = logging_metrics_pb2.DeleteLogMetricRequest(
            metric_name=metric_name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_log_metric_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = logging_v2.MetricsServiceV2Client()

        # Setup request
        metric_name = client.metric_path("[PROJECT]", "[METRIC]")

        with pytest.raises(CustomException):
            client.delete_log_metric(metric_name)
