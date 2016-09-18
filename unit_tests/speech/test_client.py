# Copyright 2016 Google Inc. All Rights Reserved.
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


class TestClient(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.speech.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        from google.cloud.speech.connection import Connection

        creds = _Credentials()
        http = object()
        client = self._makeOne(credentials=creds, http=http)
        self.assertTrue(isinstance(client.connection, Connection))
        self.assertTrue(client.connection.credentials is creds)
        self.assertTrue(client.connection.http is http)

    def test_syncrecognize(self):
        from google.cloud.speech.client import Encoding

        creds = _Credentials(object())
        http = _Http(headers={},
                     content={
                         "results": [
                             {
                                 "alternatives": [
                                     {"transcript": "hello",
                                      "confidence": 0.784919}
                                     ]
                             }
                         ]
                     })
        client = self._makeOne(credentials=creds, http=http)

        uri = 'gs://a-bucket/rec_sample.flac'
        encoding = Encoding.FLAC
        sample_rate = 16000
        hints = ["test"]
        speechrecognition_result = client.syncrecognize(None, uri, encoding,
                                                        sample_rate,
                                                        max_alternatives=2,
                                                        speech_context=hints)
        self.assertEqual(speechrecognition_result[0]["transcript"], 'hello')

        b64_speech = "binarycontent"
        speechrecognition_result = client.syncrecognize(b64_speech, None,
                                                        encoding,
                                                        sample_rate,
                                                        max_alternatives=2)
        self.assertEqual(speechrecognition_result[0]["transcript"], 'hello')

    def test_syncrecognize_failure(self):
        creds = _Credentials()
        client = self._makeOne(credentials=creds)

        with self.assertRaises(ValueError):
            client.syncrecognize("content", "uri", None, None)
        with self.assertRaises(ValueError):
            client.syncrecognize(None, None, None, None)
        with self.assertRaises(ValueError):
            client.syncrecognize(None, "uri", None, None)


class _Credentials(object):

    _scopes = ('https://www.googleapis.com/auth/cloud-platform')

    def __init__(self, authorized=None):
        self._authorized = authorized
        self._create_scoped_calls = 0

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response
        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content
