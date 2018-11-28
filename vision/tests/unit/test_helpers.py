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

from __future__ import absolute_import
import io
import unittest

import mock

from google.auth.credentials import Credentials

from google.cloud.vision_v1 import ImageAnnotatorClient
from google.cloud.vision_v1 import types


class TestSingleImageHelper(unittest.TestCase):
    def setUp(self):
        credentials = mock.Mock(spec=Credentials)
        self.client = ImageAnnotatorClient(credentials=credentials)

    @mock.patch.object(ImageAnnotatorClient, "batch_annotate_images")
    def test_all_features_default(self, batch_annotate):
        # Set up an image annotation request with no features.
        image = types.Image(source={"image_uri": "http://foo.com/img.jpg"})
        request = types.AnnotateImageRequest(image=image)
        assert not request.features

        # Perform the single image request.
        self.client.annotate_image(request)

        # Evalute the argument sent to batch_annotate_images.
        assert batch_annotate.call_count == 1
        _, args, kwargs = batch_annotate.mock_calls[0]

        # Only a single request object should be sent.
        assert len(args[0]) == 1

        # Evalute the request object to ensure it looks correct.
        request_sent = args[0][0]
        all_features = self.client._get_all_features()
        assert request_sent.image is request.image
        assert len(request_sent.features) == len(all_features)

    @mock.patch.object(ImageAnnotatorClient, "batch_annotate_images")
    def test_explicit_features(self, batch_annotate):
        # Set up an image annotation request with no features.
        image = types.Image(source={"image_uri": "http://foo.com/img.jpg"})
        request = types.AnnotateImageRequest(
            image=image,
            features=[
                types.Feature(type=1),
                types.Feature(type=2),
                types.Feature(type=3),
            ],
        )

        # Perform the single image request.
        self.client.annotate_image(request)

        # Evalute the argument sent to batch_annotate_images.
        assert batch_annotate.call_count == 1
        _, args, kwargs = batch_annotate.mock_calls[0]

        # Only a single request object should be sent.
        assert len(args[0]) == 1

        # Evalute the request object to ensure it looks correct.
        request_sent = args[0][0]
        assert request_sent.image is request.image
        assert len(request_sent.features) == 3
        for feature, i in zip(request_sent.features, range(1, 4)):
            assert feature.type == i
            assert feature.max_results == 0

    @mock.patch.object(ImageAnnotatorClient, "batch_annotate_images")
    def test_image_file_handler(self, batch_annotate):
        # Set up a file handler.
        file_ = io.BytesIO(b"bogus==")

        # Perform the single image request.
        self.client.annotate_image({"image": file_})

        # Evaluate the argument sent to batch_annotate_images.
        assert batch_annotate.call_count == 1
        _, args, kwargs = batch_annotate.mock_calls[0]

        # Only a single request object should be sent.
        assert len(args[0]) == 1

        # Evalute the request object to ensure it looks correct.
        request_sent = args[0][0]
        assert request_sent["image"]["content"] == b"bogus=="

    @mock.patch.object(ImageAnnotatorClient, "batch_annotate_images")
    @mock.patch.object(io, "open")
    def test_image_filename(self, io_open, batch_annotate):
        # Make io.open send back a mock with a read method.
        file_ = mock.MagicMock(spec=io.BytesIO)
        io_open.return_value = file_
        file_.__enter__.return_value = file_
        file_.read.return_value = b"imagefile=="

        # Perform the single image request using a filename.
        self.client.annotate_image({"image": {"source": {"filename": "image.jpeg"}}})

        # Establish that my file was opened.
        io_open.assert_called_once_with("image.jpeg", "rb")

        # Evalute the argument sent to batch_annotate_images.
        assert batch_annotate.call_count == 1
        _, args, kwargs = batch_annotate.mock_calls[0]

        # Only a single request object should be sent.
        assert len(args[0]) == 1

        # Evalute the request object to ensure it looks correct.
        request_sent = args[0][0]
        assert request_sent["image"]["content"] == b"imagefile=="
