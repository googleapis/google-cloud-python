# Copyright 2017, Google Inc. All rights reserved.
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
import unittest

import mock

from google.auth.credentials import Credentials

from google.cloud.speech_v1 import SpeechClient
from google.cloud.speech_v1 import types


class HelperTests(unittest.TestCase):
    def setUp(self):
        credentials = mock.Mock(spec=Credentials)
        self.client = SpeechClient(credentials=credentials)

    def test_inherited_method(self):
        config = types.RecognitionConfig(encoding='FLAC')
        audio = types.RecognitionAudio(uri='http://foo.com/bar.wav')
        with mock.patch.object(self.client, '_recognize') as recognize:
            self.client.recognize(config, audio)

            # Assert that the underlying GAPIC method was called as expected.
            recognize.assert_called_once_with(types.RecognizeRequest(
                config=config,
                audio=audio,
            ), None)

    def test_streaming(self):
        pass
