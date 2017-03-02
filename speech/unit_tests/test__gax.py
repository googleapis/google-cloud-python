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

import mock


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestGAPICSpeechAPI(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.speech._gax import GAPICSpeechAPI

        return GAPICSpeechAPI

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    @mock.patch(
        'google.cloud._helpers.make_secure_channel',
        return_value=mock.sentinel.channel)
    @mock.patch(
        'google.cloud.gapic.speech.v1beta1.speech_client.SpeechClient',
        SERVICE_ADDRESS='hey.you.guys')
    @mock.patch(
        'google.cloud._helpers.make_secure_stub',
        return_value=mock.sentinel.stub)
    def test_constructor(self, mocked_stub, mocked_cls, mocked_channel):
        from google.longrunning import operations_grpc
        from google.cloud._http import DEFAULT_USER_AGENT
        from google.cloud.speech import __version__
        from google.cloud.speech._gax import OPERATIONS_API_HOST

        credentials = _make_credentials()
        mock_cnxn = mock.Mock(credentials=credentials, spec=['credentials'])
        mock_client = mock.Mock(
            _connection=mock_cnxn, _credentials=credentials,
            spec=['_connection', '_credentials'])

        speech_api = self._make_one(mock_client)
        self.assertIs(speech_api._client, mock_client)
        self.assertIs(speech_api._gapic_api, mocked_cls.return_value)

        mocked_stub.assert_called_once_with(
            mock_cnxn.credentials, DEFAULT_USER_AGENT,
            operations_grpc.OperationsStub, OPERATIONS_API_HOST)
        mocked_cls.assert_called_once_with(
            channel=mock.sentinel.channel, lib_name='gccl',
            lib_version=__version__)
        mocked_channel.assert_called_once_with(
            mock_cnxn.credentials, DEFAULT_USER_AGENT,
            mocked_cls.SERVICE_ADDRESS)


class TestSpeechGAXMakeRequests(unittest.TestCase):
    SAMPLE_RATE = 16000
    HINTS = ['hi']
    AUDIO_CONTENT = b'/9j/4QNURXhpZgAASUkq'

    def _call_fut(self, sample, language_code, max_alternatives,
                  profanity_filter, speech_context, single_utterance,
                  interim_results):
        from google.cloud.speech._gax import _make_streaming_request

        return _make_streaming_request(
            sample=sample, language_code=language_code,
            max_alternatives=max_alternatives,
            profanity_filter=profanity_filter, speech_context=speech_context,
            single_utterance=single_utterance, interim_results=interim_results)

    def test_ctor(self):
        from google.cloud import speech
        from google.cloud.speech.sample import Sample
        from google.cloud.proto.speech.v1beta1.cloud_speech_pb2 import (
            RecognitionConfig, SpeechContext, StreamingRecognitionConfig,
            StreamingRecognizeRequest)

        sample = Sample(
            content=self.AUDIO_CONTENT, encoding=speech.Encoding.FLAC,
            sample_rate=self.SAMPLE_RATE)
        language_code = 'US-en'
        max_alternatives = 2
        profanity_filter = True
        speech_context = SpeechContext(phrases=self.HINTS)
        single_utterance = True
        interim_results = False

        streaming_request = self._call_fut(
            sample, language_code, max_alternatives, profanity_filter,
            speech_context, single_utterance, interim_results)
        self.assertIsInstance(streaming_request, StreamingRecognizeRequest)

        # This isn't set by _make_streaming_request().
        # The first request can only have `streaming_config` set.
        # The following requests can only have `audio_content` set.
        self.assertEqual(streaming_request.audio_content, b'')

        self.assertIsInstance(
            streaming_request.streaming_config, StreamingRecognitionConfig)
        streaming_config = streaming_request.streaming_config
        self.assertTrue(streaming_config.single_utterance)
        self.assertFalse(streaming_config.interim_results)
        config = streaming_config.config
        self.assertIsInstance(config, RecognitionConfig)
        self.assertEqual(config.encoding, 2)  # speech.Encoding.FLAC maps to 2.
        self.assertEqual(config.sample_rate, self.SAMPLE_RATE)
        self.assertEqual(config.language_code, language_code)
        self.assertEqual(config.max_alternatives, max_alternatives)
        self.assertTrue(config.profanity_filter)
        self.assertEqual(config.speech_context.phrases, self.HINTS)


class TestSpeechGAXMakeRequestsStream(unittest.TestCase):
    SAMPLE_RATE = 16000
    HINTS = ['hi']
    AUDIO_CONTENT = b'/9j/4QNURXhpZgAASUkq'

    def _call_fut(self, sample, language_code, max_alternatives,
                  profanity_filter, speech_context, single_utterance,
                  interim_results):
        from google.cloud.speech._gax import _stream_requests

        return _stream_requests(
            sample=sample, language_code=language_code,
            max_alternatives=max_alternatives,
            profanity_filter=profanity_filter, speech_context=speech_context,
            single_utterance=single_utterance, interim_results=interim_results)

    def test_stream_requests(self):
        from io import BytesIO
        from google.cloud import speech
        from google.cloud.speech.sample import Sample
        from google.cloud.proto.speech.v1beta1.cloud_speech_pb2 import (
            StreamingRecognitionConfig, StreamingRecognizeRequest)

        sample = Sample(
            stream=BytesIO(self.AUDIO_CONTENT), encoding=speech.Encoding.FLAC,
            sample_rate=self.SAMPLE_RATE)
        language_code = 'US-en'
        max_alternatives = 2
        profanity_filter = True
        speech_context = self.HINTS
        single_utterance = True
        interim_results = False
        streaming_requests = self._call_fut(
            sample, language_code, max_alternatives, profanity_filter,
            speech_context, single_utterance, interim_results)
        all_requests = []
        for streaming_request in streaming_requests:
            self.assertIsInstance(streaming_request, StreamingRecognizeRequest)
            all_requests.append(streaming_request)

        self.assertEqual(len(all_requests), 2)

        config_request = all_requests[0]
        streaming_request = all_requests[1]
        # This isn't set by _make_streaming_request().
        # The first request can only have `streaming_config` set.
        # The following requests can only have `audio_content` set.
        self.assertEqual(config_request.audio_content, b'')
        self.assertEqual(streaming_request.audio_content, self.AUDIO_CONTENT)
        self.assertIsInstance(
            config_request.streaming_config, StreamingRecognitionConfig)
