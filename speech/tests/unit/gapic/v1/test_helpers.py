# Copyright 2017, Google LLC All rights reserved.
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

from __future__ import absolute_import
from types import GeneratorType
import unittest

import mock


class TestSpeechClient(unittest.TestCase):

    @staticmethod
    def _make_one():
        import google.auth.credentials
        from google.cloud.speech_v1 import SpeechClient

        credentials = mock.Mock(spec=google.auth.credentials.Credentials)
        return SpeechClient(credentials=credentials)

    def test_inherited_method(self):
        from google.cloud.speech_v1 import types

        client = self._make_one()

        config = types.RecognitionConfig(encoding='FLAC')
        audio = types.RecognitionAudio(uri='http://foo.com/bar.wav')
        patch = mock.patch.object(client, '_recognize', autospec=True)
        with patch as recognize:
            client.recognize(config, audio)

            # Assert that the underlying GAPIC method was called as expected.
            assert recognize.call_count == 1
            _, args, _ = recognize.mock_calls[0]
            assert args[0] == types.RecognizeRequest(
                config=config,
                audio=audio,
            )

    def test_streaming_recognize(self):
        from google.cloud.speech_v1 import types

        client = self._make_one()

        config = types.StreamingRecognitionConfig()
        requests = [types.StreamingRecognizeRequest(audio_content=b'...')]
        patch = mock.patch.object(
            client, '_streaming_recognize', autospec=True)
        with patch as sr:
            client.streaming_recognize(config, requests)

            # Assert that we called streaming recognize with an iterable
            # that evalutes to the correct format.
            _, args, _ = sr.mock_calls[0]
            api_requests = args[0]
            assert isinstance(api_requests, GeneratorType)
            assert list(api_requests) == [
                types.StreamingRecognizeRequest(streaming_config=config),
                requests[0],
            ]
