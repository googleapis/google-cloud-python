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

from google.cloud import vision_v1
from google.cloud.vision_v1.proto import image_annotator_pb2


class CustomException(Exception):
    pass


class TestImageAnnotatorClient(unittest.TestCase):
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_batch_annotate_images(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = vision_v1.ImageAnnotatorClient()

        # Mock request
        requests = []

        # Mock response
        expected_response = {}
        expected_response = image_annotator_pb2.BatchAnnotateImagesResponse(
            **expected_response)
        grpc_stub.BatchAnnotateImages.return_value = expected_response

        response = client.batch_annotate_images(requests)
        self.assertEqual(expected_response, response)

        grpc_stub.BatchAnnotateImages.assert_called_once()
        args, kwargs = grpc_stub.BatchAnnotateImages.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)
        self.assertIn('metadata', kwargs)
        actual_request = args[0]

        expected_request = image_annotator_pb2.BatchAnnotateImagesRequest(
            requests=requests)
        self.assertEqual(expected_request, actual_request)

    @mock.patch('google.gax.config.API_ERRORS', (CustomException, ))
    @mock.patch('google.gax.config.create_stub', spec=True)
    def test_batch_annotate_images_exception(self, mock_create_stub):
        # Mock gRPC layer
        grpc_stub = mock.Mock()
        mock_create_stub.return_value = grpc_stub

        client = vision_v1.ImageAnnotatorClient()

        # Mock request
        requests = []

        # Mock exception response
        grpc_stub.BatchAnnotateImages.side_effect = CustomException()

        self.assertRaises(errors.GaxError, client.batch_annotate_images,
                          requests)
