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


class TestSpeechGAX(unittest.TestCase):
    SAMPLE_RATE = 16000
    HINTS = ['hi']
    AUDIO_CONTENT = '/9j/4QNURXhpZgAASUkq'

    def _callFUT(self, sample, language_code, max_alternatives,
                 profanity_filter, speech_context, single_utterance,
                 interim_results):
        from google.cloud.speech._gax import _make_streaming_request
        return _make_streaming_request(sample=sample,
                                       language_code=language_code,
                                       max_alternatives=max_alternatives,
                                       profanity_filter=profanity_filter,
                                       speech_context=speech_context,
                                       single_utterance=single_utterance,
                                       interim_results=interim_results)

    def test_ctor(self):
        from google.cloud import speech
        from google.cloud.speech.sample import Sample
        from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
            SpeechContext)
        from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
            RecognitionConfig)
        from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
            StreamingRecognitionConfig)
        from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
            StreamingRecognizeRequest)

        sample = Sample(content=self.AUDIO_CONTENT,
                        encoding=speech.Encoding.FLAC,
                        sample_rate=self.SAMPLE_RATE)
        language_code = 'US-en'
        max_alternatives = 2
        profanity_filter = True
        speech_context = SpeechContext(phrases=self.HINTS)
        single_utterance = True
        interim_results = False

        streaming_request = self._callFUT(sample, language_code,
                                          max_alternatives, profanity_filter,
                                          speech_context, single_utterance,
                                          interim_results)
        self.assertIsInstance(streaming_request, StreamingRecognizeRequest)

        # This isn't set by _make_streaming_request().
        # The first request can only have `streaming_config` set.
        # The following requests can only have `audio_content` set.
        self.assertEqual(streaming_request.audio_content, b'')

        self.assertIsInstance(streaming_request.streaming_config,
                              StreamingRecognitionConfig)
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
