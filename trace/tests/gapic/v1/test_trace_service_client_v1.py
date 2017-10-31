# Copyright 2017, Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests."""

import mock
import unittest

from google.gax import errors

from google.cloud.gapic.trace.v1 import trace_service_client
from google.cloud.proto.devtools.cloudtrace.v1 import trace_pb2
from google.protobuf import empty_pb2


class CustomException(Exception):
    pass


class TestTraceServiceClient(unittest.TestCase):
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_patch_traces(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = trace_service_client.TraceServiceClient()

        # Mock request
        project_id = 'projectId-1969970175'
        traces = trace_pb2.Traces()

        client.patch_traces(project_id, traces)

        grpc_stub.PatchTraces.assert_called_once()
        args, kwargs = grpc_stub.PatchTraces.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = trace_pb2.PatchTracesRequest(
            project_id=project_id, traces=traces)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_patch_traces_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = trace_service_client.TraceServiceClient()

        # Mock request
        project_id = 'projectId-1969970175'
        traces = trace_pb2.Traces()

        # Mock exception response
        grpc_stub.PatchTraces.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.patch_traces, project_id,
                          traces)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_trace(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = trace_service_client.TraceServiceClient()

        # Mock request
        project_id = 'projectId-1969970175'
        trace_id = 'traceId1270300245'

        # Mock response
        project_id_2 = 'projectId2939242356'
        trace_id_2 = 'traceId2987826376'
        expected_response = trace_pb2.Trace(
            project_id=project_id_2, trace_id=trace_id_2)
        grpc_stub.GetTrace.return_value = expected_response

        response = client.get_trace(project_id, trace_id)
        self.assertEqual(expected_response, response)

        grpc_stub.GetTrace.assert_called_once()
        args, kwargs = grpc_stub.GetTrace.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = trace_pb2.GetTraceRequest(
            project_id=project_id, trace_id=trace_id)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_get_trace_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = trace_service_client.TraceServiceClient()

        # Mock request
        project_id = 'projectId-1969970175'
        trace_id = 'traceId1270300245'

        # Mock exception response
        grpc_stub.GetTrace.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.get_trace, project_id,
                          trace_id)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_traces(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = trace_service_client.TraceServiceClient()

        # Mock request
        project_id = 'projectId-1969970175'

        # Mock response
        next_page_token = ''
        traces_element = trace_pb2.Trace()
        traces = [traces_element]
        expected_response = trace_pb2.ListTracesResponse(
            next_page_token=next_page_token, traces=traces)
        grpc_stub.ListTraces.return_value = expected_response

        paged_list_response = client.list_traces(project_id)
        resources = list(paged_list_response)
        self.assertEqual(1, len(resources))
        self.assertEqual(expected_response.traces[0], resources[0])

        grpc_stub.ListTraces.assert_called_once()
        args, kwargs = grpc_stub.ListTraces.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = trace_pb2.ListTracesRequest(project_id=project_id)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_list_traces_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = trace_service_client.TraceServiceClient()

        # Mock request
        project_id = 'projectId-1969970175'

        # Mock exception response
        grpc_stub.ListTraces.side_effect = CustomException()

        paged_list_response = client.list_traces(project_id)
        self.assertRaises(errors.GaxError, list, paged_list_response)
