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
        from google.cloud.speech.encoding import Encoding
        from google.cloud.speech.sample import Sample

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)

        sample = client.sample(source_uri=self.AUDIO_SOURCE_URI,
                               encoding=Encoding.FLAC,
                               sample_rate=self.SAMPLE_RATE)
        self.assertIsInstance(sample, Sample)
        self.assertEqual(sample.source_uri, self.AUDIO_SOURCE_URI)
        self.assertEqual(sample.sample_rate, self.SAMPLE_RATE)
        self.assertEqual(sample.encoding, Encoding.FLAC)

        content_sample = client.sample(content=self.AUDIO_CONTENT,
                                       encoding=Encoding.FLAC,
                                       sample_rate=self.SAMPLE_RATE)
        self.assertEqual(content_sample.content, self.AUDIO_CONTENT)
        self.assertEqual(content_sample.sample_rate, self.SAMPLE_RATE)
        self.assertEqual(content_sample.encoding, Encoding.FLAC)

    def test_sync_recognize_content_with_optional_parameters(self):
        from base64 import b64encode
        from google.cloud._helpers import _to_bytes
        from google.cloud._helpers import _bytes_to_unicode

        from google.cloud.speech.encoding import Encoding
        from google.cloud.speech.sample import Sample
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

        encoding = Encoding.FLAC

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

        expected = SYNC_RECOGNIZE_RESPONSE['results'][0]['alternatives']
        self.assertEqual(response, expected)

    def test_sync_recognize_source_uri_without_optional_parameters(self):
        from google.cloud.speech.encoding import Encoding
        from google.cloud.speech.sample import Sample
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

        encoding = Encoding.FLAC

        sample = Sample(source_uri=self.AUDIO_SOURCE_URI, encoding=encoding,
                        sample_rate=self.SAMPLE_RATE)
        response = client.sync_recognize(sample)

        self.assertEqual(len(client.connection._requested), 1)
        req = client.connection._requested[0]
        self.assertEqual(len(req), 3)
        self.assertEqual(req['data'], REQUEST)
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], 'speech:syncrecognize')

        expected = SYNC_RECOGNIZE_RESPONSE['results'][0]['alternatives']
        self.assertEqual(response, expected)

    def test_sync_recognize_with_empty_results(self):
        from google.cloud.speech.encoding import Encoding
        from google.cloud.speech.sample import Sample
        from unit_tests._fixtures import SYNC_RECOGNIZE_EMPTY_RESPONSE

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        client.connection = _Connection(SYNC_RECOGNIZE_EMPTY_RESPONSE)

        with self.assertRaises(ValueError):
            sample = Sample(source_uri=self.AUDIO_SOURCE_URI,
                            encoding=Encoding.FLAC,
                            sample_rate=self.SAMPLE_RATE)
            client.sync_recognize(sample)

    def test_async_supported_encodings(self):
        from google.cloud.speech.encoding import Encoding
        from google.cloud.speech.sample import Sample

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        client.connection = _Connection({})

        sample = Sample(source_uri=self.AUDIO_SOURCE_URI,
                        encoding=Encoding.FLAC,
                        sample_rate=self.SAMPLE_RATE)
        with self.assertRaises(ValueError):
            client.async_recognize(sample)

    def test_async_recognize(self):
        from unit_tests._fixtures import ASYNC_RECOGNIZE_RESPONSE
        from google.cloud.speech.encoding import Encoding
        from google.cloud.speech.operation import Operation
        from google.cloud.speech.sample import Sample
        RETURNED = ASYNC_RECOGNIZE_RESPONSE

        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        client.connection = _Connection(RETURNED)

        sample = Sample(source_uri=self.AUDIO_SOURCE_URI,
                        encoding=Encoding.LINEAR16,
                        sample_rate=self.SAMPLE_RATE)
        operation = client.async_recognize(sample)
        self.assertIsInstance(operation, Operation)
        self.assertFalse(operation.complete)
        self.assertIsNone(operation.metadata)

    def test_streaming_depends_on_gax(self):
        from google.cloud.speech import client as MUT
        from google.cloud._testing import _Monkey
        creds = _Credentials()
        client = self._makeOne(credentials=creds)
        client.connection = _Connection()

        with _Monkey(MUT, _USE_GAX=False):
            with self.assertRaises(EnvironmentError):
                next(client.stream_recognize({}))

    def test_set_speech_api(self):
        from google.cloud.speech import client as MUT
        from google.cloud._testing import _Monkey
        creds = _Credentials()
        client = self._makeOne(credentials=creds)
        client.connection = _Connection()

        with _Monkey(MUT, SpeechApi=_MockGAPICSpeechAPI):
            client._speech_api = None
            speech_api = client.speech_api
            self.assertIsInstance(speech_api, _MockGAPICSpeechAPI)

    def test_streaming_with_empty_response(self):
        from io import BytesIO
        from google.cloud.speech.encoding import Encoding

        stream = BytesIO(b'Some audio data...')
        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        client.connection = _Connection()
        client._speech_api = _MockGAPICSpeechAPI()
        client._speech_api._responses = []

        sample = client.sample(stream=stream,
                               encoding=Encoding.LINEAR16,
                               sample_rate=self.SAMPLE_RATE)
        results = client.stream_recognize(sample)
        with self.assertRaises(StopIteration):
            next(results)

    def test_stream_recognize(self):
        from io import BytesIO
        from google.cloud.speech.encoding import Encoding
        from google.cloud.speech.streaming_response import (
            StreamingSpeechResponse)

        stream = BytesIO(b'Some audio data...')
        credentials = _Credentials()
        client = self._makeOne(credentials=credentials)
        client.connection = _Connection()
        client._speech_api = _MockGAPICSpeechAPI()

        sample = client.sample(stream=stream,
                               encoding=Encoding.LINEAR16,
                               sample_rate=self.SAMPLE_RATE)
        results = client.stream_recognize(sample)

        self.assertIsInstance(next(results), StreamingSpeechResponse)
        requests = []
        for req in client.speech_api._requests:
            requests.append(req)
        self.assertEqual(len(requests), 2)


class _MockGAPICSpeechResponse(object):
    error = None
    endpointer_type = None
    results = []
    result_index = 0


class _MockGAPICSpeechAPI(object):
    _requests = None
    _responses = [None, _MockGAPICSpeechResponse()]

    def streaming_recognize(self, requests):
        self._requests = requests
        return self._responses


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
