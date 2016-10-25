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


class TestTranscript(unittest.TestCase):
    def _getTargetClass(self):
        from google.cloud.speech.transcript import Transcript
        return Transcript

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor(self):
        from unit_tests._fixtures import OPERATION_COMPLETE_RESPONSE as DATA
        TRANSCRIPT_DATA = DATA['response']['results'][0]['alternatives'][0]
        transcript = self._makeOne(TRANSCRIPT_DATA['transcript'],
                                   TRANSCRIPT_DATA['confidence'])
        self.assertEqual('how old is the Brooklyn Bridge',
                         transcript.transcript)
        self.assertEqual(0.98267895, transcript.confidence)
