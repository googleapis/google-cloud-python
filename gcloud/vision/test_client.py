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
    PROJECT = "PROJECT"
    IMAGE_SOURCE = "gs://some/image.jpg"
    IMAGE_CONTENT = "/9j/4QNURXhpZgAASUkq"
    IMAGE_CONTENT = "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"
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
