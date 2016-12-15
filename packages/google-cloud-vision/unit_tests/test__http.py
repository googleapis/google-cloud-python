# Copyright 2016 Google Inc.
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

import base64
import unittest


IMAGE_CONTENT = b'/9j/4QNURXhpZgAASUkq'
PROJECT = 'PROJECT'
B64_IMAGE_CONTENT = base64.b64encode(IMAGE_CONTENT).decode('ascii')


class TestVisionRequest(unittest.TestCase):
    @staticmethod
    def _get_target_function():
        from google.cloud.vision._http import _make_request
        return _make_request

    def _call_fut(self, *args, **kw):
        return self._get_target_function()(*args, **kw)

    def test_call_vision_request(self):
        from google.cloud.vision.feature import Feature
        from google.cloud.vision.feature import FeatureTypes
        from google.cloud.vision.image import Image

        client = object()
        image = Image(client, content=IMAGE_CONTENT)
        feature = Feature(feature_type=FeatureTypes.FACE_DETECTION,
                          max_results=3)
        request = self._call_fut(image, feature)
        self.assertEqual(request['image'].get('content'), B64_IMAGE_CONTENT)
        features = request['features']
        self.assertEqual(len(features), 1)
        feature = features[0]
        print(feature)
        self.assertEqual(feature['type'], FeatureTypes.FACE_DETECTION)
        self.assertEqual(feature['maxResults'], 3)

    def test_call_vision_request_with_not_feature(self):
        from google.cloud.vision.image import Image

        client = object()
        image = Image(client, content=IMAGE_CONTENT)
        with self.assertRaises(TypeError):
            self._call_fut(image, 'nonsensefeature')

    def test_call_vision_request_with_list_bad_features(self):
        from google.cloud.vision.image import Image

        client = object()
        image = Image(client, content=IMAGE_CONTENT)
        with self.assertRaises(TypeError):
            self._call_fut(image, ['nonsensefeature'])
