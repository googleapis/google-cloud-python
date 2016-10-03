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


class TestStreamingSpeechResponse(unittest.TestCase):
    def _getTargetClass(self):
        from google.cloud.speech.streaming.response import (
            StreamingSpeechResponse)
        return StreamingSpeechResponse

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        response = self._makeOne({}, 'END_OF_UTTERANCE', [], 0)
        self.assertEqual(response.result_index, 0)
