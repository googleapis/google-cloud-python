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
        self.assertIsInstance(client.connection, Connection)
        self.assertTrue(client.connection.credentials is creds)
        self.assertTrue(client.connection.http is http)

    def test_syncrecognize(self):
        from google.cloud.speech.Client import Encoding

        creds = _Credentials()
        client = self._makeOne(credentials=creds, http=object())

        audio = 'gs://my-bucket/audio-sample.flac'
        encoding = Encoding.FLAC
        sampleRate = 16000
        speechRecognitionResult = client.syncrecognize(audio, encoding, sampleRate)

        self.assertEqual(speechRecognitionResult[0][0], 'hello')

    def test_syncrecognize_failure(self):
        creds = _Credentials()
        client = self._makeOne(credentials=creds, http=object())

        with self.assertRaises(ValueError):
            client.syncrecognize(None, None, None)

class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self
