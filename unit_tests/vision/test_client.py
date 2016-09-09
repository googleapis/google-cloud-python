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

from google.cloud._helpers import _to_bytes

_IMAGE_CONTENT = _to_bytes('/9j/4QNURXhpZgAASUkq')
_IMAGE_SOURCE = 'gs://some/image.jpg'


class TestClient(unittest.TestCase):
    import base64
    PROJECT = 'PROJECT'
    B64_IMAGE_CONTENT = base64.b64encode(_IMAGE_CONTENT)

    def _getTargetClass(self):
        from google.cloud.vision.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        creds = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=creds)
        self.assertEqual(client.project, self.PROJECT)

    def test_face_annotation(self):
        from google.cloud.vision.feature import Feature, FeatureTypes
        from google.cloud.vision._fixtures import FACE_DETECTION_RESPONSE

        RETURNED = FACE_DETECTION_RESPONSE
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

        features = [Feature(feature_type=FeatureTypes.FACE_DETECTION,
                            max_results=3)]
        image = client.image(content=_IMAGE_CONTENT)
        response = client.annotate(image, features)

        self.assertEqual(REQUEST,
                         client.connection._requested[0]['data'])
        self.assertTrue('faceAnnotations' in response)

    def test_image_with_client(self):
        from google.cloud.vision.image import Image

        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT,
                               credentials=credentials)
        image = client.image(source_uri=_IMAGE_SOURCE)
        self.assertTrue(isinstance(image, Image))

    def test_face_detection_from_source(self):
        from google.cloud.vision.face import Face
        from google.cloud.vision._fixtures import FACE_DETECTION_RESPONSE
        RETURNED = FACE_DETECTION_RESPONSE
        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        image = client.image(source_uri=_IMAGE_SOURCE)
        faces = image.detect_faces(limit=3)
        self.assertEqual(5, len(faces))
        self.assertTrue(isinstance(faces[0], Face))
        image_request = client.connection._requested[0]['data']['requests'][0]
        self.assertEqual(_IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(3, image_request['features'][0]['maxResults'])

    def test_face_detection_from_content(self):
        from google.cloud.vision.face import Face
        from google.cloud.vision._fixtures import FACE_DETECTION_RESPONSE
        RETURNED = FACE_DETECTION_RESPONSE
        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        image = client.image(content=_IMAGE_CONTENT)
        faces = image.detect_faces(limit=5)
        self.assertEqual(5, len(faces))
        self.assertTrue(isinstance(faces[0], Face))
        image_request = client.connection._requested[0]['data']['requests'][0]
        self.assertEqual(self.B64_IMAGE_CONTENT,
                         image_request['image']['content'])
        self.assertEqual(5, image_request['features'][0]['maxResults'])


class TestVisionRequest(unittest.TestCase):
    def _getTargetClass(self):
        from google.cloud.vision.client import VisionRequest
        return VisionRequest

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_make_vision_request(self):
        from google.cloud.vision.feature import Feature, FeatureTypes

        feature = Feature(feature_type=FeatureTypes.FACE_DETECTION,
                          max_results=3)
        vision_request = self._makeOne(_IMAGE_CONTENT, feature)
        self.assertEqual(_IMAGE_CONTENT, vision_request.image)
        self.assertEqual(FeatureTypes.FACE_DETECTION,
                         vision_request.features[0].feature_type)

    def test_make_vision_request_with_bad_feature(self):
        with self.assertRaises(TypeError):
            self._makeOne(_IMAGE_CONTENT, 'nonsensefeature')


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
