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


def _make_result(alternatives=()):
    from google.cloud.grpc.speech.v1beta1 import cloud_speech_pb2

    return cloud_speech_pb2.SpeechRecognitionResult(
        alternatives=[
            cloud_speech_pb2.SpeechRecognitionAlternative(
                transcript=alternative['transcript'],
                confidence=alternative['confidence'],
            ) for alternative in alternatives
        ],
    )


def _make_streaming_result(alternatives=(), is_final=True, stability=1.0):
    from google.cloud.grpc.speech.v1beta1 import cloud_speech_pb2

    return cloud_speech_pb2.StreamingRecognitionResult(
        alternatives=[
            cloud_speech_pb2.SpeechRecognitionAlternative(
                transcript=alternative['transcript'],
                confidence=alternative['confidence'],
            ) for alternative in alternatives
        ],
        is_final=is_final,
        stability=stability,
    )


def _make_streaming_response(*results):
    from google.cloud.grpc.speech.v1beta1 import cloud_speech_pb2

    response = cloud_speech_pb2.StreamingRecognizeResponse(
        results=results,
    )
    return response


def _make_sync_response(*results):
    from google.cloud.grpc.speech.v1beta1 import cloud_speech_pb2

    response = cloud_speech_pb2.SyncRecognizeResponse(
        results=results,
    )
    return response


class TestClient(unittest.TestCase):
    SAMPLE_RATE = 16000
    HINTS = ['hi']
    AUDIO_SOURCE_URI = 'gs://sample-bucket/sample-recording.flac'
    AUDIO_CONTENT = '/9j/4QNURXhpZgAASUkq'

    @staticmethod
    def _get_target_class():
        from google.cloud.speech.client import Client

        return Client

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        from google.cloud.speech.connection import Connection

        creds = _Credentials()
        http = object()
        client = self._make_one(credentials=creds, http=http)
        self.assertIsInstance(client._connection, Connection)
        self.assertTrue(client._connection.credentials is creds)
        self.assertTrue(client._connection.http is http)

    def test_ctor_use_gax_preset(self):
        creds = _Credentials()
        http = object()
        client = self._make_one(credentials=creds, http=http, use_gax=True)
        self.assertTrue(client._use_gax)

    def test_create_sample_from_client(self):
        from google.cloud import speech
        from google.cloud.speech.sample import Sample

        credentials = _Credentials()
        client = self._make_one(credentials=credentials)

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

    def test_sync_recognize_content_with_optional_params_no_gax(self):
        from base64 import b64encode

        from google.cloud._helpers import _bytes_to_unicode
        from google.cloud._helpers import _to_bytes

        from google.cloud import speech
        from google.cloud.speech.alternative import Alternative
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
        client = self._make_one(credentials=credentials, use_gax=False)
        client._connection = _Connection(RETURNED)

        encoding = speech.Encoding.FLAC

        sample = Sample(content=self.AUDIO_CONTENT, encoding=encoding,
                        sample_rate=self.SAMPLE_RATE)

        response = client.sync_recognize(sample,
                                         language_code='EN',
                                         max_alternatives=2,
                                         profanity_filter=True,
                                         speech_context=self.HINTS)

        self.assertEqual(len(client._connection._requested), 1)
        req = client._connection._requested[0]
        self.assertEqual(len(req), 3)
        self.assertEqual(req['data'], REQUEST)
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], 'speech:syncrecognize')

        alternative = SYNC_RECOGNIZE_RESPONSE['results'][0]['alternatives'][0]
        expected = Alternative.from_api_repr(alternative)
        self.assertEqual(len(response), 1)
        self.assertIsInstance(response[0], Alternative)
        self.assertEqual(response[0].transcript, expected.transcript)
        self.assertEqual(response[0].confidence, expected.confidence)

    def test_sync_recognize_source_uri_without_optional_params_no_gax(self):
        from google.cloud import speech
        from google.cloud.speech.alternative import Alternative
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
        client = self._make_one(credentials=credentials, use_gax=False)
        client._connection = _Connection(RETURNED)

        encoding = speech.Encoding.FLAC

        sample = Sample(source_uri=self.AUDIO_SOURCE_URI, encoding=encoding,
                        sample_rate=self.SAMPLE_RATE)

        response = client.sync_recognize(sample)

        self.assertEqual(len(client._connection._requested), 1)
        req = client._connection._requested[0]
        self.assertEqual(len(req), 3)
        self.assertEqual(req['data'], REQUEST)
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], 'speech:syncrecognize')

        expected = Alternative.from_api_repr(
            SYNC_RECOGNIZE_RESPONSE['results'][0]['alternatives'][0])
        self.assertEqual(len(response), 1)
        self.assertIsInstance(response[0], Alternative)
        self.assertEqual(response[0].transcript, expected.transcript)
        self.assertEqual(response[0].confidence, expected.confidence)

    def test_sync_recognize_with_empty_results_no_gax(self):
        from google.cloud import speech
        from google.cloud.speech.sample import Sample
        from unit_tests._fixtures import SYNC_RECOGNIZE_EMPTY_RESPONSE

        credentials = _Credentials()
        client = self._make_one(credentials=credentials, use_gax=False)
        client._connection = _Connection(SYNC_RECOGNIZE_EMPTY_RESPONSE)

        sample = Sample(source_uri=self.AUDIO_SOURCE_URI,
                        encoding=speech.Encoding.FLAC,
                        sample_rate=self.SAMPLE_RATE)

        with self.assertRaises(ValueError):
            client.sync_recognize(sample)

    def test_sync_recognize_with_empty_results_gax(self):
        from google.cloud._testing import _Monkey

        from google.cloud import speech
        from google.cloud.speech import _gax
        from google.cloud.speech.sample import Sample

        credentials = _Credentials()
        client = self._make_one(credentials=credentials, use_gax=True)
        client._connection = _Connection()
        client._connection.credentials = credentials

        channel_args = []
        channel_obj = object()

        def make_channel(*args):
            channel_args.append(args)
            return channel_obj

        def speech_api(channel=None):
            return _MockGAPICSpeechAPI(response=_make_sync_response(),
                                       channel=channel)

        host = 'foo.apis.invalid'
        speech_api.SERVICE_ADDRESS = host

        with _Monkey(_gax, SpeechApi=speech_api,
                     make_secure_channel=make_channel):
            client._speech_api = _gax.GAPICSpeechAPI(client)

        low_level = client.speech_api._gapic_api
        self.assertIsInstance(low_level, _MockGAPICSpeechAPI)
        self.assertIs(low_level._channel, channel_obj)
        self.assertEqual(
            channel_args,
            [(credentials, _gax.DEFAULT_USER_AGENT, host)])

        sample = Sample(source_uri=self.AUDIO_SOURCE_URI,
                        encoding=speech.Encoding.FLAC,
                        sample_rate=self.SAMPLE_RATE)

        with self.assertRaises(ValueError):
            client.sync_recognize(sample)

    def test_sync_recognize_with_gax(self):
        from google.cloud._testing import _Monkey

        from google.cloud import speech
        from google.cloud.speech import _gax

        creds = _Credentials()
        client = self._make_one(credentials=creds, use_gax=True)
        client._connection = _Connection()
        client._connection.credentials = creds
        client._speech_api = None

        alternatives = [{
            'transcript': 'testing 1 2 3',
            'confidence': 0.9224355,
        }, {
            'transcript': 'testing 4 5 6',
            'confidence': 0.0123456,
        }]
        result = _make_result(alternatives)

        channel_args = []
        channel_obj = object()

        def make_channel(*args):
            channel_args.append(args)
            return channel_obj

        def speech_api(channel=None):
            return _MockGAPICSpeechAPI(
                response=_make_sync_response(result),
                channel=channel)

        host = 'foo.apis.invalid'
        speech_api.SERVICE_ADDRESS = host

        sample = client.sample(source_uri=self.AUDIO_SOURCE_URI,
                               encoding=speech.Encoding.FLAC,
                               sample_rate=self.SAMPLE_RATE)

        with _Monkey(_gax, SpeechApi=speech_api,
                     make_secure_channel=make_channel):
            client._speech_api = _gax.GAPICSpeechAPI(client)

        low_level = client.speech_api._gapic_api
        self.assertIsInstance(low_level, _MockGAPICSpeechAPI)
        self.assertIs(low_level._channel, channel_obj)
        self.assertEqual(
            channel_args,
            [(creds, _gax.DEFAULT_USER_AGENT, host)])

        results = client.sync_recognize(sample)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].transcript,
                         alternatives[0]['transcript'])
        self.assertEqual(results[0].confidence,
                         alternatives[0]['confidence'])
        self.assertEqual(results[1].transcript,
                         alternatives[1]['transcript'])
        self.assertEqual(results[1].confidence,
                         alternatives[1]['confidence'])

    def test_async_supported_encodings(self):
        from google.cloud import speech
        from google.cloud.speech.sample import Sample

        credentials = _Credentials()
        client = self._make_one(credentials=credentials)
        client._connection = _Connection({})

        sample = Sample(source_uri=self.AUDIO_SOURCE_URI,
                        encoding=speech.Encoding.FLAC,
                        sample_rate=self.SAMPLE_RATE)
        with self.assertRaises(ValueError):
            client.async_recognize(sample)

    def test_async_recognize_no_gax(self):
        from google.cloud import speech
        from google.cloud.speech.operation import Operation
        from google.cloud.speech.sample import Sample
        from unit_tests._fixtures import ASYNC_RECOGNIZE_RESPONSE

        RETURNED = ASYNC_RECOGNIZE_RESPONSE

        credentials = _Credentials()
        client = self._make_one(credentials=credentials, use_gax=False)
        client._connection = _Connection(RETURNED)

        sample = Sample(source_uri=self.AUDIO_SOURCE_URI,
                        encoding=speech.Encoding.LINEAR16,
                        sample_rate=self.SAMPLE_RATE)
        operation = client.async_recognize(sample)
        self.assertIsInstance(operation, Operation)
        self.assertIs(operation.client, client)
        self.assertEqual(operation.caller_metadata,
                         {'request_type': 'AsyncRecognize'})
        self.assertFalse(operation.complete)
        self.assertIsNone(operation.metadata)

    def test_async_recognize_with_gax(self):
        from google.cloud._testing import _Monkey

        from google.cloud import speech
        from google.cloud.speech import _gax
        from google.cloud.speech.operation import Operation

        credentials = _Credentials()
        client = self._make_one(credentials=credentials,
                                use_gax=True)
        client._connection = _Connection()
        client._connection.credentials = credentials

        channel_args = []
        channel_obj = object()

        def make_channel(*args):
            channel_args.append(args)
            return channel_obj

        sample = client.sample(source_uri=self.AUDIO_SOURCE_URI,
                               encoding=speech.Encoding.LINEAR16,
                               sample_rate=self.SAMPLE_RATE)

        def speech_api(channel=None):
            return _MockGAPICSpeechAPI(channel=channel)

        host = 'foo.apis.invalid'
        speech_api.SERVICE_ADDRESS = host

        with _Monkey(_gax, SpeechApi=speech_api,
                     make_secure_channel=make_channel):
            api = client.speech_api

        low_level = api._gapic_api
        self.assertIsInstance(low_level, _MockGAPICSpeechAPI)
        self.assertIs(low_level._channel, channel_obj)
        expected = (credentials, _gax.DEFAULT_USER_AGENT,
                    low_level.SERVICE_ADDRESS)
        self.assertEqual(channel_args, [expected])

        operation = client.async_recognize(sample)
        self.assertIsInstance(operation, Operation)
        self.assertFalse(operation.complete)
        self.assertIsNone(operation.response)

    def test_streaming_depends_on_gax(self):
        from google.cloud._testing import _Monkey

        credentials = _Credentials()
        client = self._make_one(credentials=credentials, use_gax=False)
        client.connection = _Connection()

        with self.assertRaises(EnvironmentError):
            list(client.streaming_recognize({}))

    def test_streaming_closed_stream(self):
        from io import BytesIO

        from google.cloud._testing import _Monkey

        from google.cloud.speech import _gax
        from google.cloud.speech.encoding import Encoding

        stream = BytesIO(b'Some audio data...')
        credentials = _Credentials()
        client = self._make_one(credentials=credentials)
        client.connection = _Connection()
        client.connection.credentials = credentials

        channel_args = []
        channel_obj = object()

        def make_channel(*args):
            channel_args.append(args)
            return channel_obj

        def speech_api(channel=None):
            return _MockGAPICSpeechAPI(channel=channel)

        host = 'foo.apis.invalid'
        speech_api.SERVICE_ADDRESS = host

        stream.close()

        sample = client.sample(content=stream,
                               encoding=Encoding.LINEAR16,
                               sample_rate=self.SAMPLE_RATE)

        with _Monkey(_gax, SpeechApi=speech_api,
                     make_secure_channel=make_channel):
            client._speech_api = _gax.GAPICSpeechAPI(client)

        with self.assertRaises(ValueError):
            list(client.streaming_recognize(sample))

    def test_stream_recognize_interim_results(self):
        from io import BytesIO

        from google.cloud._testing import _Monkey

        from google.cloud.speech import _gax
        from google.cloud.speech.encoding import Encoding
        from google.cloud.speech.client import StreamingSpeechResult

        stream = BytesIO(b'Some audio data...')
        credentials = _Credentials()
        client = self._make_one(credentials=credentials)
        client.connection = _Connection()
        client.connection.credentials = credentials

        alternatives = [{
            'transcript': 'testing streaming 1 2 3',
            'confidence': 0.9224355,
        }, {
            'transcript': 'testing streaming 4 5 6',
            'confidence': 0.0123456,
        }]
        first_response = _make_streaming_response(
            _make_streaming_result([], is_final=False, stability=0.122435))
        second_response = _make_streaming_response(
            _make_streaming_result(alternatives, is_final=False,
                                   stability=0.1432343))
        last_response = _make_streaming_response(
            _make_streaming_result(alternatives, is_final=True,
                                   stability=0.9834534))
        responses = [first_response, second_response, last_response]

        channel_args = []
        channel_obj = object()

        def make_channel(*args):
            channel_args.append(args)
            return channel_obj

        def speech_api(channel=None):
            return _MockGAPICSpeechAPI(channel=channel, response=responses)

        host = 'foo.apis.invalid'
        speech_api.SERVICE_ADDRESS = host

        with _Monkey(_gax, SpeechApi=speech_api,
                     make_secure_channel=make_channel):
            client._speech_api = _gax.GAPICSpeechAPI(client)

        sample = client.sample(content=stream,
                               encoding=Encoding.LINEAR16,
                               sample_rate=self.SAMPLE_RATE)

        results = list(client.streaming_recognize(sample,
                                                  interim_results=True))

        self.assertEqual(len(results), 3)
        self.assertIsInstance(results[0], StreamingSpeechResult)
        self.assertEqual(results[0].alternatives, [])
        self.assertFalse(results[0].is_final)
        self.assertEqual(results[0].stability, 0.122435)
        self.assertEqual(results[1].stability, 0.1432343)
        self.assertFalse(results[1].is_final)
        self.assertEqual(results[1].alternatives[0].transcript,
                         alternatives[0]['transcript'])
        self.assertEqual(results[1].alternatives[0].confidence,
                         alternatives[0]['confidence'])
        self.assertEqual(results[1].alternatives[1].transcript,
                         alternatives[1]['transcript'])
        self.assertEqual(results[1].alternatives[1].confidence,
                         alternatives[1]['confidence'])
        self.assertTrue(results[2].is_final)
        self.assertEqual(results[2].stability, 0.9834534)
        self.assertEqual(results[2].alternatives[0].transcript,
                         alternatives[0]['transcript'])
        self.assertEqual(results[2].alternatives[0].confidence,
                         alternatives[0]['confidence'])

    def test_stream_recognize(self):
        from io import BytesIO

        from google.cloud._testing import _Monkey

        from google.cloud.speech import _gax
        from google.cloud.speech.encoding import Encoding

        stream = BytesIO(b'Some audio data...')
        credentials = _Credentials()
        client = self._make_one(credentials=credentials)
        client.connection = _Connection()
        client.connection.credentials = credentials

        alternatives = [{
            'transcript': 'testing streaming 1 2 3',
            'confidence': 0.9224355,
        }, {
            'transcript': 'testing streaming 4 5 6',
            'confidence': 0.0123456,
        }]

        first_response = _make_streaming_response(
            _make_streaming_result(alternatives=alternatives, is_final=False))
        last_response = _make_streaming_response(
            _make_streaming_result(alternatives=alternatives, is_final=True))
        responses = [first_response, last_response]

        channel_args = []
        channel_obj = object()

        def make_channel(*args):
            channel_args.append(args)
            return channel_obj

        def speech_api(channel=None):
            return _MockGAPICSpeechAPI(channel=channel, response=responses)

        host = 'foo.apis.invalid'
        speech_api.SERVICE_ADDRESS = host

        with _Monkey(_gax, SpeechApi=speech_api,
                     make_secure_channel=make_channel):
            client._speech_api = _gax.GAPICSpeechAPI(client)

        sample = client.sample(content=stream,
                               encoding=Encoding.LINEAR16,
                               sample_rate=self.SAMPLE_RATE)

        results = list(client.streaming_recognize(sample))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].alternatives[0].transcript,
                         alternatives[0]['transcript'])
        self.assertEqual(results[0].alternatives[0].confidence,
                         alternatives[0]['confidence'])

    def test_stream_recognize_no_results(self):
        from io import BytesIO

        from google.cloud._testing import _Monkey

        from google.cloud.speech import _gax
        from google.cloud.speech.encoding import Encoding

        stream = BytesIO(b'Some audio data...')
        credentials = _Credentials()
        client = self._make_one(credentials=credentials)
        client.connection = _Connection()
        client.connection.credentials = credentials

        responses = [_make_streaming_response()]

        channel_args = []
        channel_obj = object()

        def make_channel(*args):
            channel_args.append(args)
            return channel_obj

        def speech_api(channel=None):
            return _MockGAPICSpeechAPI(channel=channel, response=responses)

        host = 'foo.apis.invalid'
        speech_api.SERVICE_ADDRESS = host

        with _Monkey(_gax, SpeechApi=speech_api,
                     make_secure_channel=make_channel):
            client._speech_api = _gax.GAPICSpeechAPI(client)

        sample = client.sample(content=stream,
                               encoding=Encoding.LINEAR16,
                               sample_rate=self.SAMPLE_RATE)

        results = list(client.streaming_recognize(sample))
        self.assertEqual(results, [])

    def test_speech_api_with_gax(self):
        from google.cloud._testing import _Monkey

        from google.cloud.speech import _gax

        creds = _Credentials()
        client = self._make_one(credentials=creds, use_gax=True)
        client._connection = _Connection()
        client._connection.credentials = creds

        channel_args = []
        channel_obj = object()

        def make_channel(*args):
            channel_args.append(args)
            return channel_obj

        def speech_api(channel=None):
            return _MockGAPICSpeechAPI(channel=channel)

        host = 'foo.apis.invalid'
        speech_api.SERVICE_ADDRESS = host

        with _Monkey(_gax, SpeechApi=speech_api,
                     make_secure_channel=make_channel):
            client._speech_api = _gax.GAPICSpeechAPI(client)

        low_level = client.speech_api._gapic_api
        self.assertIsInstance(low_level, _MockGAPICSpeechAPI)
        self.assertIs(low_level._channel, channel_obj)
        expected = (creds, _gax.DEFAULT_USER_AGENT,
                    low_level.SERVICE_ADDRESS)
        self.assertEqual(channel_args, [expected])

    def test_speech_api_without_gax(self):
        from google.cloud._http import Connection
        from google.cloud.speech.client import _JSONSpeechAPI

        creds = _Credentials()
        client = self._make_one(credentials=creds, use_gax=False)
        self.assertIsNone(client._speech_api)
        self.assertIsInstance(client.speech_api, _JSONSpeechAPI)
        self.assertIsInstance(client.speech_api._connection, Connection)

    def test_speech_api_preset(self):
        creds = _Credentials()
        client = self._make_one(credentials=creds)
        fake_api = object()
        client._speech_api = fake_api

        self.assertIs(client.speech_api, fake_api)


class _MockGAPICSpeechAPI(object):
    _requests = None
    _response = None
    _results = None
    SERVICE_ADDRESS = 'foo.apis.invalid'

    def __init__(self, response=None, channel=None):
        self._response = response
        self._channel = channel

    def async_recognize(self, config, audio):
        from google.longrunning.operations_pb2 import Operation

        self.config = config
        self.audio = audio
        operation = Operation()
        return operation

    def sync_recognize(self, config, audio):
        self.config = config
        self.audio = audio

        return self._response

    def streaming_recognize(self, requests):
        self._requests = requests
        for response in self._response:
            yield response


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
