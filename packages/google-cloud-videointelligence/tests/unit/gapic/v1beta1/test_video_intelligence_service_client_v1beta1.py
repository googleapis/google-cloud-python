# Copyright 2017, Google Inc. All rights reserved.
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
from google.rpc import status_pb2

from google.cloud import videointelligence_v1beta1
from google.cloud.videointelligence_v1beta1.proto import video_intelligence_pb2
from google.longrunning import operations_pb2


class CustomException(Exception):
    pass


class TestVideoIntelligenceServiceClient(unittest.TestCase):
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_annotate_video(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = videointelligence_v1beta1.VideoIntelligenceServiceClient()

        # Mock request
        input_uri = 'inputUri1707300727'
        features = []

        # Mock response
        expected_response = {}
        expected_response = video_intelligence_pb2.AnnotateVideoResponse(
            **expected_response)
        operation = operations_pb2.Operation(
            name='operations/test_annotate_video', done=True)
        operation.response.Pack(expected_response)
        grpc_stub.AnnotateVideo.return_value = operation

        response = client.annotate_video(input_uri, features)
        self.assertEqual(expected_response, response.result())

        grpc_stub.AnnotateVideo.assert_called_once()
        args, kwargs = grpc_stub.AnnotateVideo.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = video_intelligence_pb2.AnnotateVideoRequest(
            input_uri=input_uri, features=features)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_annotate_video_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = videointelligence_v1beta1.VideoIntelligenceServiceClient()

        # Mock request
        input_uri = 'inputUri1707300727'
        features = []

        # Mock exception response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name='operations/test_annotate_video_exception', done=True)
        operation.error.CopyFrom(error)
        grpc_stub.AnnotateVideo.return_value = operation

        response = client.annotate_video(input_uri, features)
        self.assertEqual(error, response.exception())
