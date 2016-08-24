# Copyright 2016 Google Inc. All rights reserved.
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
import base64
import json


class TestClient(unittest.TestCase):
    PROJECT = 'PROJECT'
    IMAGE_SOURCE = 'gs://some/image.jpg'
    IMAGE_CONTENT = '/9j/4QNURXhpZgAASUkq'
    B64_IMAGE_CONTENT = base64.b64encode(IMAGE_CONTENT)

    def _getTargetClass(self):
        from gcloud.vision.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        creds = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=creds)
        self.assertEqual(client.project, self.PROJECT)
        self.assertTrue('annotate' in dir(client))

    def test_face_annotation(self):

        from gcloud.vision.fixtures import FACE_DETECTION_RESPONSE as RETURNED

        REQUEST = {
            "requests": [
                {
                    "image": {
                        "content": self.B64_IMAGE_CONTENT
                    },
                    "features": [
                        {
                            "maxResults": 3,
                            "type": "FACE_DETECTION"
                        }
                    ]
                }
            ]
        }
        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        from gcloud.vision.feature import Feature, FeatureTypes

        features = [Feature(feature_type=FeatureTypes.FACE_DETECTION,
                            max_results=3)]

        response = client.annotate(self.IMAGE_CONTENT, features)

        self.assertEqual(json.dumps(REQUEST),
                         client.connection._requested[0]['data'])

        self.assertTrue('faceAnnotations' in response)


class TestVisionRequest(unittest.TestCase):
    def _getTargetClass(self):
        from gcloud.vision.client import VisionRequest
        return VisionRequest

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_make_vision_request(self):
        IMAGE_CONTENT = '/9j/4QNURXhpZgAASUkq'
        from gcloud.vision.feature import Feature, FeatureTypes
        feature = Feature(feature_type=FeatureTypes.FACE_DETECTION,
                          max_results=3)
        vision_request = self._makeOne(IMAGE_CONTENT, feature)

        self.assertEqual(IMAGE_CONTENT, vision_request.image)
        self.assertEqual(FeatureTypes.FACE_DETECTION,
                         vision_request.features[0].feature_type)

        vision_request = self._makeOne(IMAGE_CONTENT, [feature])

        self.assertEqual(IMAGE_CONTENT, vision_request.image)
        self.assertEqual(FeatureTypes.FACE_DETECTION,
                         vision_request.features[0].feature_type)

        with self.assertRaises(TypeError):
            self._makeOne(IMAGE_CONTENT, 'nonsensefeature')


class VisionJSONEncoder(unittest.TestCase):
        def _getTargetClass(self):
            from gcloud.vision.client import VisionJSONEncoder
            return VisionJSONEncoder

        def _makeOne(self, *args, **kw):
            return self._getTargetClass()(*args, **kw)

        def test_vision_json_encoder(self):
            class CustomJSON(object):
                def as_dict(self):
                    return {'custom': 'encoder'}
            custom_json_class = CustomJSON()

            encoder = self._makeOne()
            self.assertEqual({'custom': 'encoder'},
                             encoder.default(custom_json_class))

            class StandardJSON(object):
                pass

            standard_json_class = StandardJSON()
            self.assertEqual({}, encoder.default(standard_json_class))


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
