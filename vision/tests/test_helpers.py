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

from __future__ import absolute_import
import unittest

import mock

from google.cloud.vision_v1 import ImageAnnotatorClient
from google.cloud.vision_v1 import image_annotator


class TestSingleImageHelper(unittest.TestCase):
    @mock.patch.object(ImageAnnotatorClient, 'batch_annotate_images')
    def test_all_features_default(self, batch_annotate):
        # Set up an image annotation request with no features.
        image = image_annotator.Image(source={
            'image_uri': 'http://foo.com/img.jpg',
        })
        request = image_annotator.AnnotateImageRequest(image=image)
        assert not request.features

        # Perform the single image request.
        client = ImageAnnotatorClient()
        client.annotate_image(request)

        # Evalute the argument sent to batch_annotate_images.
        assert batch_annotate.call_count == 1
        _, args, kwargs = batch_annotate.mock_calls[0]

        # Only a single request object should be sent.
        assert len(args[0]) == 1

        # Evalute the request object to ensure it looks correct.
        request_sent = args[0][0]
        assert request_sent.image is request.image
        assert len(request_sent.features) == len(client._get_all_features())
    

    @mock.patch.object(ImageAnnotatorClient, 'batch_annotate_images')
    def test_explicit_features(self, batch_annotate):
        # Set up an image annotation request with no features.
        image = image_annotator.Image(source={
            'image_uri': 'http://foo.com/img.jpg',
        })
        request = image_annotator.AnnotateImageRequest(
            image=image,
            features=[
                image_annotator.Feature(type=1),
                image_annotator.Feature(type=2),
                image_annotator.Feature(type=3),
            ],
        )

        # Perform the single image request.
        client = ImageAnnotatorClient()
        client.annotate_image(request)

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
