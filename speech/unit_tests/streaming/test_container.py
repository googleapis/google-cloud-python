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


class TestStreamingContainer(unittest.TestCase):
    def _getTargetClass(self):
        from google.cloud.speech.streaming.container import (
            StreamingResponseContainer)
        return StreamingResponseContainer

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        streaming_container = self._makeOne()
        self.assertEqual(streaming_container.responses, {})
        streaming_container.add_response(_MockGAPICSpeechResponse())
        self.assertEqual(len(streaming_container.responses), 1)

    def test_is_not_finished(self):
        true_result = _MockGAPICSpeechResult()
        true_result.is_final = True

        false_result = _MockGAPICSpeechResult()
        false_result.is_final = False

        first_response = _MockGAPICSpeechResponse()
        first_response.results.append(true_result)
        first_response.results.append(false_result)

        second_response = _MockGAPICSpeechResponse()
        second_response.results.append(true_result)
        second_response.results.append(true_result)

        streaming_container = self._makeOne()
        streaming_container.add_response(first_response)
        streaming_container.add_response(second_response)

        self.assertFalse(streaming_container.is_finished)

    def test_is_finished(self):
        true_result = _MockGAPICSpeechResult()
        true_result.is_final = True

        first_response = _MockGAPICSpeechResponse()
        first_response.results.append(true_result)
        first_response.results.append(true_result)

        second_response = _MockGAPICSpeechResponse()
        second_response.results.append(true_result)
        second_response.results.append(true_result)
        second_response.result_index = 1

        streaming_container = self._makeOne()
        streaming_container.add_response(first_response)
        streaming_container.add_response(second_response)

        self.assertTrue(streaming_container.is_finished)

    def test_get_full_text(self):
        first_part = _MockGAPICSpeechResultAlternative(transcript='testing')
        second_part = _MockGAPICSpeechResultAlternative(transcript=' 1 2 3')

        first_result = _MockGAPICSpeechResult(alternatives=[first_part])
        first_result.is_final = True

        second_result = _MockGAPICSpeechResult(alternatives=[second_part])
        second_result.is_final = True

        response = _MockGAPICSpeechResponse()
        response.results.append(first_result)
        response.results.append(second_result)

        streaming_container = self._makeOne()
        streaming_container.add_response(response)

        self.assertEqual(streaming_container.get_full_text(), 'testing 1 2 3')

    def test_unfinshed_full_test(self):
        first_part = _MockGAPICSpeechResultAlternative(transcript='testing')

        first_result = _MockGAPICSpeechResult(alternatives=[first_part])
        first_result.is_final = False

        response = _MockGAPICSpeechResponse()
        response.results.append(first_result)

        streaming_container = self._makeOne()
        streaming_container.add_response(response)

        self.assertIsNone(streaming_container.get_full_text())


class _MockGAPICSpeechResultAlternative(object):
    def __init__(self, transcript='', confidence=0):
        self.transcript = transcript
        self.confidence = confidence


class _MockGAPICSpeechResult(object):
    def __init__(self, alternatives=None):
        self.alternatives = alternatives or []
    stability = 0
    is_final = False


class _MockGAPICSpeechResponse(object):
    error = None
    endpointer_type = None
    results = []
    result_index = 0
