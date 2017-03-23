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
PROJECT = 'PROJECT'
B64_IMAGE_CONTENT = base64.b64encode(IMAGE_CONTENT).decode('ascii')


class TestConnection(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.vision._http import Connection

        return Connection

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_default_url(self):
        client = object()
        conn = self._make_one(client)
        self.assertEqual(conn._client, client)

    def test_extra_headers(self):
        from google.cloud import _http as base_http
        from google.cloud.vision import _http as MUT

        http = mock.Mock(spec=['request'])
        response = mock.Mock(status=200, spec=['status'])
        data = b'brent-spiner'
        http.request.return_value = response, data
        client = mock.Mock(_http=http, spec=['_http'])

        conn = self._make_one(client)
        req_data = 'req-data-boring'
        result = conn.api_request(
            'GET', '/rainbow', data=req_data, expect_json=False)
        self.assertEqual(result, data)

        expected_headers = {
            'Content-Length': str(len(req_data)),
            'Accept-Encoding': 'gzip',
            base_http.CLIENT_INFO_HEADER: MUT._CLIENT_INFO,
            'User-Agent': conn.USER_AGENT,
        }
        expected_uri = conn.build_api_url('/rainbow')
        http.request.assert_called_once_with(
            body=req_data,
            headers=expected_headers,
            method='GET',
            uri=expected_uri,
        )


class Test_HTTPVisionAPI(unittest.TestCase):
    def _get_target_class(self):
        from google.cloud.vision._http import _HTTPVisionAPI

        return _HTTPVisionAPI

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_call_annotate_with_no_results(self):
        from google.cloud.vision.feature import Feature
        from google.cloud.vision.feature import FeatureTypes
        from google.cloud.vision.image import Image

        client = mock.Mock(spec_set=['_connection'])
        feature = Feature(FeatureTypes.LABEL_DETECTION, 5)
        image_content = b'abc 1 2 3'
        image = Image(client, content=image_content)

        http_api = self._make_one(client)
        http_api._connection = mock.Mock(spec_set=['api_request'])
        http_api._connection.api_request.return_value = {'responses': []}
        images = ((image, [feature]),)
        response = http_api.annotate(images)
        self.assertEqual(len(response), 0)
        self.assertIsInstance(response, list)

    def test_call_annotate_with_no_parameters(self):
        client = mock.Mock(spec_set=['_connection'])
        http_api = self._make_one(client)
        http_api._connection = mock.Mock(spec_set=['api_request'])

        results = http_api.annotate()
        self.assertEqual(results, [])
        http_api._connection.api_request.assert_not_called()

    def test_call_annotate_with_pb_requests_results(self):
        from google.cloud.proto.vision.v1 import image_annotator_pb2

        client = mock.Mock(spec_set=['_connection'])

        feature_type = image_annotator_pb2.Feature.CROP_HINTS
        feature = image_annotator_pb2.Feature(type=feature_type, max_results=2)

        image = image_annotator_pb2.Image(content=IMAGE_CONTENT)

        aspect_ratios = [1.3333, 1.7777]
        crop_hints_params = image_annotator_pb2.CropHintsParams(
            aspect_ratios=aspect_ratios)
        image_context = image_annotator_pb2.ImageContext(
            crop_hints_params=crop_hints_params)
        request = image_annotator_pb2.AnnotateImageRequest(
            image=image, features=[feature], image_context=image_context)

        http_api = self._make_one(client)
        http_api._connection = mock.Mock(spec_set=['api_request'])
        http_api._connection.api_request.return_value = {'responses': []}

        responses = http_api.annotate(requests_pb=[request])

        # Establish that one and exactly one api_request call was made.
        self.assertEqual(http_api._connection.api_request.call_count, 1)

        # Establish that the basic keyword arguments look correct.
        call = http_api._connection.api_request.mock_calls[0]
        self.assertEqual(call[2]['method'], 'POST')
        self.assertEqual(call[2]['path'], '/images:annotate')

        # Establish that the responses look correct.
        self.assertEqual(responses, [])
        self.assertEqual(len(responses), 0)

    def test_call_annotate_with_more_than_one_result(self):
        from google.cloud.vision.feature import Feature
        from google.cloud.vision.feature import FeatureTypes
        from google.cloud.vision.image import Image
        from google.cloud.vision.likelihood import Likelihood
        from tests.unit._fixtures import MULTIPLE_RESPONSE

        client = mock.Mock(spec_set=['_connection'])
        feature = Feature(FeatureTypes.LABEL_DETECTION, 5)
        image_content = b'abc 1 2 3'
        image = Image(client, content=image_content)

        http_api = self._make_one(client)
        http_api._connection = mock.Mock(spec_set=['api_request'])
        http_api._connection.api_request.return_value = MULTIPLE_RESPONSE
        images = ((image, [feature]),)
        responses = http_api.annotate(images)

        self.assertEqual(len(responses), 2)
        image_one = responses[0]
        image_two = responses[1]
        self.assertEqual(len(image_one.labels), 3)
        self.assertIsInstance(image_one.safe_searches, tuple)
        self.assertEqual(image_two.safe_searches.adult,
                         Likelihood.VERY_UNLIKELY)
        self.assertEqual(len(image_two.labels), 0)


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
