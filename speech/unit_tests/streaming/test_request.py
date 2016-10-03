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


class TestStreamingSpeechRequestHelpers(unittest.TestCase):
    def test_make_request_stream(self):
        from io import BytesIO
        from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
            StreamingRecognizeRequest)
        from google.cloud.speech.streaming.request import _make_request_stream
        from google.cloud.speech.sample import Sample

        stream = BytesIO(b'g' * 1702)  # Something bigger than a chunk.
        sample = Sample(stream=stream, encoding='LINEAR16')

        request_count = 0
        for req in _make_request_stream(sample):
            request_count += 1
            self.assertIsInstance(req, StreamingRecognizeRequest)
        self.assertEqual(request_count, 3)

    def test_make_request_stream_short(self):
        from io import BytesIO
        from google.cloud.grpc.speech.v1beta1.cloud_speech_pb2 import (
            StreamingRecognizeRequest)
        from google.cloud.speech.streaming.request import _make_request_stream
        from google.cloud.speech.sample import Sample

        stream = BytesIO(b'g' * (1599 * 2))  # Something bigger than a chunk.
        sample = Sample(stream=stream, encoding='LINEAR16')

        request_count = 0
        for req in _make_request_stream(sample):
            request_count += 1
            self.assertIsInstance(req, StreamingRecognizeRequest)

        self.assertEqual(request_count, 3)
