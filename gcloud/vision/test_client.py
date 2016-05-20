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

import unittest2
import base64
import json


class TestClient(unittest2.TestCase):
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

    def test_label_annotation(self):
        RETURNED = {
            "responses": [
                {
                    "labelAnnotations": [
                        {
                            "mid": "/m/0k4j",
                            "description": "automobile",
                            "score": 0.9776855
                        },
                        {
                            "mid": "/m/07yv9",
                            "description": "vehicle",
                            "score": 0.947987
                        },
                        {
                            "mid": "/m/07r04",
                            "description": "truck",
                            "score": 0.88429511
                        }
                    ]
                }
            ]
        }

        REQUEST = {
            "requests": [
                {
                    "image": {
                        "content": self.B64_IMAGE_CONTENT
                    },
                    "features": [
                        {
                            "maxResults": 3,
                            "type": "LABEL_DETECTION"
                        }
                    ]
                }
            ]
        }
        credentials = _Credentials()
        client = self._makeOne(project=self.PROJECT, credentials=credentials)
        client.connection = _Connection(RETURNED)

        from gcloud.vision.feature import FeatureTypes
        max_results = 3
        responses = client.annotate(self.IMAGE_CONTENT,
                                    FeatureTypes.LABEL_DETECTION, max_results)

        print json.dumps(REQUEST)
        self.assertEqual(json.dumps(REQUEST),
                         client.connection._requested[0]['data'])

        # self.assertEqual(type(responses[0]), LabelAnnotation)
        self.assertTrue('labelAnnotations' in responses[0])


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
