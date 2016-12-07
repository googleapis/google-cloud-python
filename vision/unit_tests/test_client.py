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

import mock


IMAGE_CONTENT = b'/9j/4QNURXhpZgAASUkq'
IMAGE_SOURCE = 'gs://some/image.jpg'
PROJECT = 'PROJECT'
B64_IMAGE_CONTENT = base64.b64encode(IMAGE_CONTENT).decode('ascii')


def _make_credentials():
    import google.auth.credentials
    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestClient(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.client import Client
        return Client

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        creds = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=creds)
        self.assertEqual(client.project, PROJECT)

    def test_face_annotation(self):
        from google.cloud.vision.feature import Feature, FeatureTypes
        from unit_tests._fixtures import FACE_DETECTION_RESPONSE

        RETURNED = FACE_DETECTION_RESPONSE
        REQUEST = {
            "requests": [
                {
                    "image": {
                        "content": B64_IMAGE_CONTENT
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
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        features = [Feature(feature_type=FeatureTypes.FACE_DETECTION,
                            max_results=3)]
        image = client.image(content=IMAGE_CONTENT)
        response = client.annotate(image, features)

        self.assertEqual(REQUEST,
                         client._connection._requested[0]['data'])
        self.assertTrue('faceAnnotations' in response)

    def test_image_with_client_gcs_source(self):
        from google.cloud.vision.image import Image

        credentials = _make_credentials()
        client = self._make_one(project=PROJECT,
                                credentials=credentials)
        gcs_image = client.image(source_uri=IMAGE_SOURCE)
        self.assertIsInstance(gcs_image, Image)
        self.assertEqual(gcs_image.source, IMAGE_SOURCE)

    def test_image_with_client_raw_content(self):
        from google.cloud.vision.image import Image

        credentials = _make_credentials()
        client = self._make_one(project=PROJECT,
                                credentials=credentials)
        raw_image = client.image(content=IMAGE_CONTENT)
        self.assertIsInstance(raw_image, Image)
        self.assertEqual(raw_image.content, B64_IMAGE_CONTENT)

    def test_image_with_client_filename(self):
        from mock import mock_open
        from mock import patch
        from google.cloud.vision.image import Image

        credentials = _make_credentials()
        client = self._make_one(project=PROJECT,
                                credentials=credentials)
        with patch('google.cloud.vision.image.open',
                   mock_open(read_data=IMAGE_CONTENT)) as m:
            file_image = client.image(filename='my_image.jpg')
        m.assert_called_once_with('my_image.jpg', 'rb')
        self.assertIsInstance(file_image, Image)
        self.assertEqual(file_image.content, B64_IMAGE_CONTENT)

    def test_multiple_detection_from_content(self):
        import copy
        from google.cloud.vision.feature import Feature
        from google.cloud.vision.feature import FeatureTypes
        from unit_tests._fixtures import LABEL_DETECTION_RESPONSE
        from unit_tests._fixtures import LOGO_DETECTION_RESPONSE

        returned = copy.deepcopy(LABEL_DETECTION_RESPONSE)
        logos = copy.deepcopy(LOGO_DETECTION_RESPONSE['responses'][0])
        returned['responses'][0]['logoAnnotations'] = logos['logoAnnotations']

        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(returned)

        limit = 2
        label_feature = Feature(FeatureTypes.LABEL_DETECTION, limit)
        logo_feature = Feature(FeatureTypes.LOGO_DETECTION, limit)
        features = [label_feature, logo_feature]
        image = client.image(content=IMAGE_CONTENT)
        items = image.detect(features)

        self.assertEqual(len(items.logos), 2)
        self.assertEqual(len(items.labels), 3)
        first_logo = items.logos[0]
        second_logo = items.logos[1]
        self.assertEqual(first_logo.description, 'Brand1')
        self.assertEqual(first_logo.score, 0.63192177)
        self.assertEqual(second_logo.description, 'Brand2')
        self.assertEqual(second_logo.score, 0.5492993)

        first_label = items.labels[0]
        second_label = items.labels[1]
        third_label = items.labels[2]
        self.assertEqual(first_label.description, 'automobile')
        self.assertEqual(first_label.score, 0.9776855)
        self.assertEqual(second_label.description, 'vehicle')
        self.assertEqual(second_label.score, 0.947987)
        self.assertEqual(third_label.description, 'truck')
        self.assertEqual(third_label.score, 0.88429511)

        requested = client._connection._requested
        requests = requested[0]['data']['requests']
        image_request = requests[0]
        label_request = image_request['features'][0]
        logo_request = image_request['features'][1]

        self.assertEqual(B64_IMAGE_CONTENT,
                         image_request['image']['content'])
        self.assertEqual(label_request['maxResults'], 2)
        self.assertEqual(label_request['type'], 'LABEL_DETECTION')
        self.assertEqual(logo_request['maxResults'], 2)
        self.assertEqual(logo_request['type'], 'LOGO_DETECTION')

    def test_face_detection_from_source(self):
        from google.cloud.vision.face import Face
        from unit_tests._fixtures import FACE_DETECTION_RESPONSE
        RETURNED = FACE_DETECTION_RESPONSE
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(source_uri=IMAGE_SOURCE)
        faces = image.detect_faces(limit=3)
        self.assertEqual(5, len(faces))
        self.assertIsInstance(faces[0], Face)
        image_request = client._connection._requested[0]['data']['requests'][0]
        self.assertEqual(IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(3, image_request['features'][0]['maxResults'])

    def test_face_detection_from_content(self):
        from google.cloud.vision.face import Face
        from unit_tests._fixtures import FACE_DETECTION_RESPONSE
        RETURNED = FACE_DETECTION_RESPONSE
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(content=IMAGE_CONTENT)
        faces = image.detect_faces(limit=5)
        self.assertEqual(5, len(faces))
        self.assertIsInstance(faces[0], Face)
        image_request = client._connection._requested[0]['data']['requests'][0]

        self.assertEqual(B64_IMAGE_CONTENT,
                         image_request['image']['content'])
        self.assertEqual(5, image_request['features'][0]['maxResults'])

    def test_face_detection_from_content_no_results(self):
        RETURNED = {
            'responses': [{}]
        }
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(content=IMAGE_CONTENT)
        faces = image.detect_faces(limit=5)
        self.assertEqual(faces, ())
        self.assertEqual(len(faces), 0)
        image_request = client._connection._requested[0]['data']['requests'][0]

        self.assertEqual(B64_IMAGE_CONTENT,
                         image_request['image']['content'])
        self.assertEqual(5, image_request['features'][0]['maxResults'])

    def test_label_detection_from_source(self):
        from google.cloud.vision.entity import EntityAnnotation
        from unit_tests._fixtures import (
            LABEL_DETECTION_RESPONSE as RETURNED)

        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(source_uri=IMAGE_SOURCE)
        labels = image.detect_labels(limit=3)
        self.assertEqual(3, len(labels))
        self.assertIsInstance(labels[0], EntityAnnotation)
        image_request = client._connection._requested[0]['data']['requests'][0]
        self.assertEqual(IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(3, image_request['features'][0]['maxResults'])
        self.assertEqual('automobile', labels[0].description)
        self.assertEqual('vehicle', labels[1].description)
        self.assertEqual('/m/0k4j', labels[0].mid)
        self.assertEqual('/m/07yv9', labels[1].mid)

    def test_label_detection_no_results(self):
        RETURNED = {
            'responses': [{}]
        }
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(content=IMAGE_CONTENT)
        labels = image.detect_labels()
        self.assertEqual(labels, ())
        self.assertEqual(len(labels), 0)

    def test_landmark_detection_from_source(self):
        from google.cloud.vision.entity import EntityAnnotation
        from unit_tests._fixtures import (
            LANDMARK_DETECTION_RESPONSE as RETURNED)

        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(source_uri=IMAGE_SOURCE)
        landmarks = image.detect_landmarks(limit=3)
        self.assertEqual(2, len(landmarks))
        self.assertIsInstance(landmarks[0], EntityAnnotation)
        image_request = client._connection._requested[0]['data']['requests'][0]
        self.assertEqual(IMAGE_SOURCE,
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

        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(content=IMAGE_CONTENT)
        landmarks = image.detect_landmarks(limit=5)
        self.assertEqual(2, len(landmarks))
        self.assertIsInstance(landmarks[0], EntityAnnotation)
        image_request = client._connection._requested[0]['data']['requests'][0]
        self.assertEqual(B64_IMAGE_CONTENT,
                         image_request['image']['content'])
        self.assertEqual(5, image_request['features'][0]['maxResults'])

    def test_landmark_detection_no_results(self):
        RETURNED = {
            'responses': [{}]
        }
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(content=IMAGE_CONTENT)
        landmarks = image.detect_landmarks()
        self.assertEqual(landmarks, ())
        self.assertEqual(len(landmarks), 0)

    def test_logo_detection_from_source(self):
        from google.cloud.vision.entity import EntityAnnotation
        from unit_tests._fixtures import LOGO_DETECTION_RESPONSE
        RETURNED = LOGO_DETECTION_RESPONSE
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(source_uri=IMAGE_SOURCE)
        logos = image.detect_logos(limit=3)
        self.assertEqual(2, len(logos))
        self.assertIsInstance(logos[0], EntityAnnotation)
        image_request = client._connection._requested[0]['data']['requests'][0]
        self.assertEqual(IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(3, image_request['features'][0]['maxResults'])

    def test_logo_detection_from_content(self):
        from google.cloud.vision.entity import EntityAnnotation
        from unit_tests._fixtures import LOGO_DETECTION_RESPONSE
        RETURNED = LOGO_DETECTION_RESPONSE
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(content=IMAGE_CONTENT)
        logos = image.detect_logos(limit=5)
        self.assertEqual(2, len(logos))
        self.assertIsInstance(logos[0], EntityAnnotation)
        image_request = client._connection._requested[0]['data']['requests'][0]
        self.assertEqual(B64_IMAGE_CONTENT,
                         image_request['image']['content'])
        self.assertEqual(5, image_request['features'][0]['maxResults'])

    def test_text_detection_from_source(self):
        from google.cloud.vision.entity import EntityAnnotation
        from unit_tests._fixtures import (
            TEXT_DETECTION_RESPONSE as RETURNED)

        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(source_uri=IMAGE_SOURCE)
        text = image.detect_text(limit=3)
        self.assertEqual(3, len(text))
        self.assertIsInstance(text[0], EntityAnnotation)
        image_request = client._connection._requested[0]['data']['requests'][0]
        self.assertEqual(IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(3, image_request['features'][0]['maxResults'])
        self.assertEqual('en', text[0].locale)
        self.assertEqual('Google CloudPlatform\n', text[0].description)
        self.assertEqual('Google', text[1].description)
        self.assertEqual(694, text[0].bounds.vertices[0].y_coordinate)

    def test_safe_search_detection_from_source(self):
        from google.cloud.vision.likelihood import Likelihood
        from google.cloud.vision.safe import SafeSearchAnnotation
        from unit_tests._fixtures import SAFE_SEARCH_DETECTION_RESPONSE

        RETURNED = SAFE_SEARCH_DETECTION_RESPONSE
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(source_uri=IMAGE_SOURCE)
        safe_search = image.detect_safe_search()[0]
        self.assertIsInstance(safe_search, SafeSearchAnnotation)
        image_request = client._connection._requested[0]['data']['requests'][0]
        self.assertEqual(IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(safe_search.adult, Likelihood.VERY_UNLIKELY)
        self.assertEqual(safe_search.spoof, Likelihood.UNLIKELY)
        self.assertEqual(safe_search.medical, Likelihood.POSSIBLE)
        self.assertEqual(safe_search.violence, Likelihood.VERY_UNLIKELY)

    def test_safe_search_no_results(self):
        RETURNED = {
            'responses': [{}]
        }
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(content=IMAGE_CONTENT)
        safe_search = image.detect_safe_search()
        self.assertEqual(safe_search, ())
        self.assertEqual(len(safe_search), 0)

    def test_image_properties_detection_from_source(self):
        from google.cloud.vision.color import ImagePropertiesAnnotation
        from unit_tests._fixtures import IMAGE_PROPERTIES_RESPONSE

        RETURNED = IMAGE_PROPERTIES_RESPONSE
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(source_uri=IMAGE_SOURCE)
        image_properties = image.detect_properties()[0]
        self.assertIsInstance(image_properties, ImagePropertiesAnnotation)
        image_request = client._connection._requested[0]['data']['requests'][0]
        self.assertEqual(IMAGE_SOURCE,
                         image_request['image']['source']['gcs_image_uri'])
        self.assertEqual(0.42258179, image_properties.colors[0].score)
        self.assertEqual(0.025376344,
                         image_properties.colors[0].pixel_fraction)
        self.assertEqual(253, image_properties.colors[0].color.red)
        self.assertEqual(203, image_properties.colors[0].color.green)
        self.assertEqual(65, image_properties.colors[0].color.blue)
        self.assertEqual(0.0, image_properties.colors[0].color.alpha)

    def test_image_properties_no_results(self):
        RETURNED = {
            'responses': [{}]
        }
        credentials = _make_credentials()
        client = self._make_one(project=PROJECT, credentials=credentials)
        client._connection = _Connection(RETURNED)

        image = client.image(content=IMAGE_CONTENT)
        image_properties = image.detect_properties()
        self.assertEqual(image_properties, ())
        self.assertEqual(len(image_properties), 0)


class TestVisionRequest(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.client import VisionRequest
        return VisionRequest

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_make_vision_request(self):
        from google.cloud.vision.feature import Feature, FeatureTypes

        feature = Feature(feature_type=FeatureTypes.FACE_DETECTION,
                          max_results=3)
        vision_request = self._make_one(IMAGE_CONTENT, feature)
        self.assertEqual(IMAGE_CONTENT, vision_request.image)
        self.assertEqual(FeatureTypes.FACE_DETECTION,
                         vision_request.features[0].feature_type)

    def test_make_vision_request_with_bad_feature(self):
        with self.assertRaises(TypeError):
            self._make_one(IMAGE_CONTENT, 'nonsensefeature')


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        import json
        json.dumps(kw.get('data', ''))  # Simulate JSON encoding.
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
