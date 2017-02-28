# Copyright 2017 Google Inc.
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


class TestResult(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.speech.result import Result

        return Result

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        result = self._make_one([])
        self.assertIsInstance(result, self._get_target_class())

    def test_from_pb(self):
        from google.cloud.proto.speech.v1beta1 import cloud_speech_pb2

        confidence = 0.625
        transcript = 'this is a test transcript'
        alternative = cloud_speech_pb2.SpeechRecognitionAlternative(
            transcript=transcript, confidence=confidence)
        result_pb = cloud_speech_pb2.SpeechRecognitionResult(
            alternatives=[alternative])

        result = self._get_target_class().from_pb(result_pb)
        self.assertEqual(result.confidence, confidence)
        self.assertEqual(result.transcript, transcript)

    def test_from_api_repr(self):
        confidence = 0.625
        transcript = 'this is a test'
        response = {
            'alternatives': [
                {
                    'confidence': confidence,
                    'transcript': transcript,
                },
            ],
        }

        result = self._get_target_class().from_api_repr(response)
        self.assertEqual(result.confidence, confidence)
        self.assertEqual(result.transcript, transcript)
