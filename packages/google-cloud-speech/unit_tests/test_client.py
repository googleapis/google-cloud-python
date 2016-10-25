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


class TestClient(unittest.TestCase):
    SAMPLE_RATE = 16000
    HINTS = ['hi']
    AUDIO_SOURCE_URI = 'gs://sample-bucket/sample-recording.flac'
    AUDIO_CONTENT = '/9j/4QNURXhpZgAASUkq'

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

    def test_create_sample_from_client(self):
        from google.cloud import speech
        from google.cloud.speech.sample import Sample

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)

        sample = client.sample(source_uri=self.AUDIO_SOURCE_URI,
                               encoding=speech.Encoding.FLAC,
                               sample_rate=self.SAMPLE_RATE)
        self.assertIsInstance(sample, Sample)
        self.assertEqual(sample.source_uri, self.AUDIO_SOURCE_URI)
        self.assertEqual(sample.sample_rate, self.SAMPLE_RATE)
        self.assertEqual(sample.encoding, speech.Encoding.FLAC)

        content_sample = client.sample(content=self.AUDIO_CONTENT,
                                       encoding=speech.Encoding.FLAC,
                                       sample_rate=self.SAMPLE_RATE)
        self.assertEqual(content_sample.content, self.AUDIO_CONTENT)
        self.assertEqual(content_sample.sample_rate, self.SAMPLE_RATE)
        self.assertEqual(content_sample.encoding, speech.Encoding.FLAC)

    def test_sync_recognize_content_with_optional_parameters(self):
        from base64 import b64encode
        from google.cloud._helpers import _to_bytes
        from google.cloud._helpers import _bytes_to_unicode

        from google.cloud import speech
        from google.cloud.speech.sample import Sample
        from google.cloud.speech.transcript import Transcript
        from unit_tests._fixtures import SYNC_RECOGNIZE_RESPONSE

        _AUDIO_CONTENT = _to_bytes(self.AUDIO_CONTENT)
        _B64_AUDIO_CONTENT = _bytes_to_unicode(b64encode(_AUDIO_CONTENT))
        RETURNED = SYNC_RECOGNIZE_RESPONSE
        REQUEST = {
            'config': {
                'encoding': 'FLAC',
                'maxAlternatives': 2,
                'sampleRate': 16000,
                'speechContext': {
                    'phrases': [
                        'hi',
                    ]
                },
                'languageCode': 'EN',
                'profanityFilter': True,
            },
            'audio': {
                'content': _B64_AUDIO_CONTENT,
            }
        }
        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        client.connection = _Connection(RETURNED)

        encoding = speech.Encoding.FLAC

        sample = Sample(content=self.AUDIO_CONTENT, encoding=encoding,
                        sample_rate=self.SAMPLE_RATE)
        response = client.sync_recognize(sample,
                                         language_code='EN',
                                         max_alternatives=2,
                                         profanity_filter=True,
                                         speech_context=self.HINTS)

        self.assertEqual(len(client.connection._requested), 1)
        req = client.connection._requested[0]
        self.assertEqual(len(req), 3)
        self.assertEqual(req['data'], REQUEST)
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], 'speech:syncrecognize')

        alternative = SYNC_RECOGNIZE_RESPONSE['results'][0]['alternatives'][0]
        expected = Transcript.from_api_repr(alternative)
        self.assertEqual(len(response), 1)
        self.assertIsInstance(response[0], Transcript)
        self.assertEqual(response[0].transcript, expected.transcript)
        self.assertEqual(response[0].confidence, expected.confidence)

    def test_sync_recognize_source_uri_without_optional_parameters(self):
        from google.cloud import speech
        from google.cloud.speech.sample import Sample
        from google.cloud.speech.transcript import Transcript
        from unit_tests._fixtures import SYNC_RECOGNIZE_RESPONSE

        RETURNED = SYNC_RECOGNIZE_RESPONSE
        REQUEST = {
            'config': {
                'encoding': 'FLAC',
                'sampleRate': 16000,
            },
            'audio': {
                'uri': self.AUDIO_SOURCE_URI,
            }
        }
        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        client.connection = _Connection(RETURNED)

        encoding = speech.Encoding.FLAC

        sample = Sample(source_uri=self.AUDIO_SOURCE_URI, encoding=encoding,
                        sample_rate=self.SAMPLE_RATE)
        response = client.sync_recognize(sample)

        self.assertEqual(len(client.connection._requested), 1)
        req = client.connection._requested[0]
        self.assertEqual(len(req), 3)
        self.assertEqual(req['data'], REQUEST)
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], 'speech:syncrecognize')

        expected = Transcript.from_api_repr(
            SYNC_RECOGNIZE_RESPONSE['results'][0]['alternatives'][0])
        self.assertEqual(len(response), 1)
        self.assertIsInstance(response[0], Transcript)
        self.assertEqual(response[0].transcript, expected.transcript)
        self.assertEqual(response[0].confidence, expected.confidence)

    def test_sync_recognize_with_empty_results(self):
        from google.cloud import speech
        from google.cloud.speech.sample import Sample
        from unit_tests._fixtures import SYNC_RECOGNIZE_EMPTY_RESPONSE

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        client.connection = _Connection(SYNC_RECOGNIZE_EMPTY_RESPONSE)

        with self.assertRaises(ValueError):
            sample = Sample(source_uri=self.AUDIO_SOURCE_URI,
                            encoding=speech.Encoding.FLAC,
                            sample_rate=self.SAMPLE_RATE)
            client.sync_recognize(sample)

    def test_async_supported_encodings(self):
        from google.cloud import speech
        from google.cloud.speech.sample import Sample

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        client.connection = _Connection({})

        sample = Sample(source_uri=self.AUDIO_SOURCE_URI,
                        encoding=speech.Encoding.FLAC,
                        sample_rate=self.SAMPLE_RATE)
        with self.assertRaises(ValueError):
            client.async_recognize(sample)

    def test_async_recognize(self):
        from unit_tests._fixtures import ASYNC_RECOGNIZE_RESPONSE
        from google.cloud import speech
        from google.cloud.speech.operation import Operation
        from google.cloud.speech.sample import Sample
        RETURNED = ASYNC_RECOGNIZE_RESPONSE

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        client.connection = _Connection(RETURNED)

        sample = Sample(source_uri=self.AUDIO_SOURCE_URI,
                        encoding=speech.Encoding.LINEAR16,
                        sample_rate=self.SAMPLE_RATE)
        operation = client.async_recognize(sample)
        self.assertIsInstance(operation, Operation)
        self.assertFalse(operation.complete)
        self.assertIsNone(operation.metadata)


class _Credentials(object):

    _scopes = ('https://www.googleapis.com/auth/cloud-platform',)

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
