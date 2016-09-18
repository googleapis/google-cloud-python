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
import base64
import httplib2


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

        client = self._makeOne()

        uri = 'gs://datatonic-sandbox-shared/rec_sample.flac'
        encoding = Encoding.FLAC
        sample_rate = 16000
        hints = ["test"]
        speechrecognition_result = client.syncrecognize(None, uri, encoding,
                                                        sample_rate,
                                                        max_alternatives=2,
                                                        speech_context=hints)
        self.assertEqual(speechrecognition_result[0]["transcript"], 'hello')

        h = httplib2.Http()
        _, content = h.request('https://storage.googleapis.com/' +
                               'datatonic-sandbox-shared/rec_sample.flac',
                               'GET')
        b64_speech = base64.b64encode(content).decode('UTF-8')
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

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self
