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
        from unit_tests._fixtures import FACE_DETECTION_RESPONSE

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
        self.assertIsInstance(image, Image)

    def test_face_detection_from_source(self):
        from google.cloud.vision.face import Face
        from unit_tests._fixtures import FACE_DETECTION_RESPONSE
        RETURNED = FACE_DETECTION_RESPONSE
        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        image = client.image(source_uri=_IMAGE_SOURCE)
        faces = image.detect_faces(limit=3)
        self.assertEqual(5, len(faces))
        self.assertIsInstance(faces[0], Face)
        image_request = client.connection._requested[0]['data']['requests'][0]
        self.assertEqual(_IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(3, image_request['features'][0]['maxResults'])

    def test_face_detection_from_content(self):
        from google.cloud.vision.face import Face
        from unit_tests._fixtures import FACE_DETECTION_RESPONSE
        RETURNED = FACE_DETECTION_RESPONSE
        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        image = client.image(content=_IMAGE_CONTENT)
        faces = image.detect_faces(limit=5)
        self.assertEqual(5, len(faces))
        self.assertIsInstance(faces[0], Face)
        image_request = client.connection._requested[0]['data']['requests'][0]
        self.assertEqual(self.B64_IMAGE_CONTENT,
                         image_request['image']['content'])
        self.assertEqual(5, image_request['features'][0]['maxResults'])

    def test_label_detection_from_source(self):
        from google.cloud.vision.entity import EntityAnnotation
        from unit_tests._fixtures import (
            LABEL_DETECTION_RESPONSE as RETURNED)

        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        image = client.image(source_uri=_IMAGE_SOURCE)
        labels = image.detect_labels(limit=3)
        self.assertEqual(3, len(labels))
        self.assertIsInstance(labels[0], EntityAnnotation)
        image_request = client.connection._requested[0]['data']['requests'][0]
        self.assertEqual(_IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(3, image_request['features'][0]['maxResults'])
        self.assertEqual('automobile', labels[0].description)
        self.assertEqual('vehicle', labels[1].description)
        self.assertEqual('/m/0k4j', labels[0].mid)
        self.assertEqual('/m/07yv9', labels[1].mid)

    def test_landmark_detection_from_source(self):
        from google.cloud.vision.entity import EntityAnnotation
        from unit_tests._fixtures import (
            LANDMARK_DETECTION_RESPONSE as RETURNED)

        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        image = client.image(source_uri=_IMAGE_SOURCE)
        landmarks = image.detect_landmarks(limit=3)
        self.assertEqual(2, len(landmarks))
        self.assertIsInstance(landmarks[0], EntityAnnotation)
        image_request = client.connection._requested[0]['data']['requests'][0]
        self.assertEqual(_IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(3, image_request['features'][0]['maxResults'])
        self.assertEqual(48.861013, landmarks[0].locations[0].latitude)
        self.assertEqual(2.335818, landmarks[0].locations[0].longitude)
        self.assertEqual('/m/04gdr', landmarks[0].mid)
        self.assertEqual('/m/094llg', landmarks[1].mid)

    def test_landmark_detection_from_content(self):
        from google.cloud.vision.entity import EntityAnnotation
        from unit_tests._fixtures import (
            LANDMARK_DETECTION_RESPONSE as RETURNED)

        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        image = client.image(content=_IMAGE_CONTENT)
        landmarks = image.detect_landmarks(limit=5)
        self.assertEqual(2, len(landmarks))
        self.assertIsInstance(landmarks[0], EntityAnnotation)
        image_request = client.connection._requested[0]['data']['requests'][0]
        self.assertEqual(self.B64_IMAGE_CONTENT,
                         image_request['image']['content'])
        self.assertEqual(5, image_request['features'][0]['maxResults'])

    def test_logo_detection_from_source(self):
        from google.cloud.vision.entity import EntityAnnotation
        from unit_tests._fixtures import LOGO_DETECTION_RESPONSE
        RETURNED = LOGO_DETECTION_RESPONSE
        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        image = client.image(source_uri=_IMAGE_SOURCE)
        logos = image.detect_logos(limit=3)
        self.assertEqual(2, len(logos))
        self.assertIsInstance(logos[0], EntityAnnotation)
        image_request = client.connection._requested[0]['data']['requests'][0]
        self.assertEqual(_IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(3, image_request['features'][0]['maxResults'])

    def test_logo_detection_from_content(self):
        from google.cloud.vision.entity import EntityAnnotation
        from unit_tests._fixtures import LOGO_DETECTION_RESPONSE
        RETURNED = LOGO_DETECTION_RESPONSE
        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        image = client.image(content=_IMAGE_CONTENT)
        logos = image.detect_logos(limit=5)
        self.assertEqual(2, len(logos))
        self.assertIsInstance(logos[0], EntityAnnotation)
        image_request = client.connection._requested[0]['data']['requests'][0]
        self.assertEqual(self.B64_IMAGE_CONTENT,
                         image_request['image']['content'])
        self.assertEqual(5, image_request['features'][0]['maxResults'])

    def test_text_detection_from_source(self):
        from google.cloud.vision.entity import EntityAnnotation
        from unit_tests._fixtures import (
            TEXT_DETECTION_RESPONSE as RETURNED)

        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        image = client.image(source_uri=_IMAGE_SOURCE)
        text = image.detect_text(limit=3)
        self.assertEqual(3, len(text))
        self.assertIsInstance(text[0], EntityAnnotation)
        image_request = client.connection._requested[0]['data']['requests'][0]
        self.assertEqual(_IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(3, image_request['features'][0]['maxResults'])
        self.assertEqual('en', text[0].locale)
        self.assertEqual('Google CloudPlatform\n', text[0].description)
        self.assertEqual('Google', text[1].description)
        self.assertEqual(694, text[0].bounds.vertices[0].y_coordinate)

    def test_safe_search_detection_from_source(self):
        from google.cloud.vision.safe import SafeSearchAnnotation
        from unit_tests._fixtures import SAFE_SEARCH_DETECTION_RESPONSE

        RETURNED = SAFE_SEARCH_DETECTION_RESPONSE
        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        image = client.image(source_uri=_IMAGE_SOURCE)
        safe_search = image.detect_safe_search()
        self.assertIsInstance(safe_search, SafeSearchAnnotation)
        image_request = client.connection._requested[0]['data']['requests'][0]
        self.assertEqual(_IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual('VERY_UNLIKELY', safe_search.adult)
        self.assertEqual('UNLIKELY', safe_search.spoof)
        self.assertEqual('POSSIBLE', safe_search.medical)
        self.assertEqual('VERY_UNLIKELY', safe_search.violence)

    def test_image_properties_detection_from_source(self):
        from google.cloud.vision.color import ImagePropertiesAnnotation
        from unit_tests._fixtures import IMAGE_PROPERTIES_RESPONSE

        RETURNED = IMAGE_PROPERTIES_RESPONSE
        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        image = client.image(source_uri=_IMAGE_SOURCE)
        image_properties = image.detect_properties()
        self.assertIsInstance(image_properties, ImagePropertiesAnnotation)
        image_request = client.connection._requested[0]['data']['requests'][0]
        self.assertEqual(_IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(0.42258179, image_properties.colors[0].score)
        self.assertEqual(0.025376344,
                         image_properties.colors[0].pixel_fraction)
        self.assertEqual(253, image_properties.colors[0].color.red)
        self.assertEqual(203, image_properties.colors[0].color.green)
        self.assertEqual(65, image_properties.colors[0].color.blue)
        self.assertEqual(0.0, image_properties.colors[0].color.alpha)


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
