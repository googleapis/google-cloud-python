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

from google.cloud._helpers import _to_bytes

_AUDIO_CONTENT = _to_bytes('/9j/4QNURXhpZgAASUkq')
_B64_AUDIO_CONTENT = base64.b64encode(_AUDIO_CONTENT)


class TestClient(unittest.TestCase):
    SAMPLE_RATE = 16000
    HINTS = ["hi"]

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

    def test_sync_recognize(self):
        from google.cloud.speech.client import Encoding
        from unit_tests.speech._fixtures import SYNC_RECOGNIZE_RESPONSE

        RETURNED = SYNC_RECOGNIZE_RESPONSE
        REQUEST = {
            "config": {
                "encoding": "FLAC",
                "maxAlternatives": 2,
                "sampleRate": 16000,
                "speechContext": {
                    "phrases": [
                        "hi"
                    ]
                },
                "languageCode": "EN",
                "profanityFilter": True
            },
            "audio": {
                "content": _B64_AUDIO_CONTENT
            }
        }
        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        client.connection = _Connection(RETURNED)

        encoding = Encoding.FLAC

        response = client.sync_recognize(_AUDIO_CONTENT,
                                         encoding,
                                         self.SAMPLE_RATE,
                                         language_code="EN",
                                         max_alternatives=2,
                                         profanity_filter=True,
                                         speech_context=self.HINTS)

        self.assertEqual(REQUEST,
                         client.connection._requested[0]['data'])
        self.assertEqual(response[0]["transcript"], 'hello')

    def test_sync_recognize_without_optional_parameters(self):
        from google.cloud.speech.client import Encoding
        from unit_tests.speech._fixtures import SYNC_RECOGNIZE_RESPONSE

        RETURNED = SYNC_RECOGNIZE_RESPONSE
        REQUEST = {
            "config": {
                "encoding": "FLAC",
                "sampleRate": 16000
            },
            "audio": {
                "content": _B64_AUDIO_CONTENT
            }
        }
        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        client.connection = _Connection(RETURNED)

        encoding = Encoding.FLAC

        response = client.sync_recognize(_AUDIO_CONTENT,
                                         encoding,
                                         self.SAMPLE_RATE)

        self.assertEqual(REQUEST,
                         client.connection._requested[0]['data'])
        self.assertEqual(response[0]["transcript"], 'hello')

    def test_sync_recognize_without_content(self):
        from google.cloud.speech.client import Encoding

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)

        with self.assertRaises(ValueError):
            client.sync_recognize(None, Encoding.FLAC, self.SAMPLE_RATE)

    def test_sync_recognize_without_encoding(self):
        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)

        with self.assertRaises(ValueError):
            client.sync_recognize(_AUDIO_CONTENT, None, self.SAMPLE_RATE)

    def test_sync_recognize_without_samplerate(self):
        from google.cloud.speech.client import Encoding

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)

        with self.assertRaises(ValueError):
            client.sync_recognize(_AUDIO_CONTENT, Encoding.FLAC, None)


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


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
