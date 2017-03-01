# Copyright 2017 Google Inc.
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

import unittest

import mock

PROJECT = 'PROJECT'


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestBatch(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.batch import Batch

        return Batch

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        from google.cloud.vision.feature import Feature
        from google.cloud.vision.feature import FeatureTypes
        from google.cloud.vision.image import Image

        client = mock.Mock(spec=[])
        image = Image(client, source_uri='gs://images/imageone.jpg')
        face_feature = Feature(FeatureTypes.FACE_DETECTION, 5)
        logo_feature = Feature(FeatureTypes.LOGO_DETECTION, 3)

        batch = self._make_one(client)
        batch.add_image(image, [logo_feature, face_feature])
        self.assertEqual(len(batch.images), 1)
        self.assertEqual(len(batch.images[0]), 2)
        self.assertIsInstance(batch.images[0][0], Image)
        self.assertEqual(len(batch.images[0][1]), 2)
        self.assertIsInstance(batch.images[0][1][0], Feature)
        self.assertIsInstance(batch.images[0][1][1], Feature)

    def test_batch_from_client(self):
        from google.cloud.vision.client import Client
        from google.cloud.vision.feature import Feature
        from google.cloud.vision.feature import FeatureTypes

        creds = _make_credentials()
        client = Client(project=PROJECT, credentials=creds)

        image_one = client.image(source_uri='gs://images/imageone.jpg')
        image_two = client.image(source_uri='gs://images/imagtwo.jpg')
        face_feature = Feature(FeatureTypes.FACE_DETECTION, 5)
        logo_feature = Feature(FeatureTypes.LOGO_DETECTION, 3)

        # Make mocks.
        annotate = mock.Mock(return_value=True, spec=[])
        vision_api = mock.Mock(annotate=annotate, spec=['annotate'])
        client._vision_api_internal = vision_api

        # Actually  call the partially-mocked method.
        batch = client.batch()
        batch.add_image(image_one, [face_feature])
        batch.add_image(image_two, [logo_feature, face_feature])
        images = batch.images
        self.assertEqual(len(images), 2)
        self.assertTrue(batch.detect())
        self.assertEqual(len(batch.images), 0)
        client._vision_api_internal.annotate.assert_called_with(images)
