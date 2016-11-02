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

    def test_constructor(self):
        text = 'hello goodbye upstairs'
        confidence = 0.5546875
        transcript = self._makeOne(text, confidence)
        self.assertEqual(transcript._transcript, text)
        self.assertEqual(transcript._confidence, confidence)

    def test_transcript_property(self):
        text = 'is this thing on?'
        transcript = self._makeOne(text, None)
        self.assertEqual(transcript.transcript, text)

    def test_confidence_property(self):
        confidence = 0.412109375
        transcript = self._makeOne(None, confidence)
        self.assertEqual(transcript.confidence, confidence)

    def test_from_api_repr_with_no_confidence(self):
        data = {
            'transcript': 'testing 1 2 3',
        }

        klass = self._getTargetClass()
        transcript = klass.from_api_repr(data)
        self.assertEqual(transcript.transcript, data['transcript'])
        self.assertIsNone(transcript.confidence)

    def test_from_pb_with_no_confidence(self):
        from google.cloud.grpc.speech.v1beta1 import cloud_speech_pb2

        text = 'the double trouble'
        pb_value = cloud_speech_pb2.SpeechRecognitionAlternative(
            transcript=text)
        self.assertEqual(pb_value.confidence, 0.0)

        klass = self._getTargetClass()
        transcript = klass.from_pb(pb_value)
        self.assertEqual(transcript.transcript, text)
        self.assertIsNone(transcript.confidence)
