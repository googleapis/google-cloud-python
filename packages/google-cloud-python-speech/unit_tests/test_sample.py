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


class TestSample(unittest.TestCase):
    SAMPLE_RATE = 16000
    AUDIO_SOURCE_URI = 'gs://sample-bucket/sample-recording.flac'

    @staticmethod
    def _get_target_class():
        from google.cloud.speech.sample import Sample
        return Sample

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_initialize_sample(self):
        from google.cloud.speech.encoding import Encoding

        sample = self._make_one(source_uri=self.AUDIO_SOURCE_URI,
                                encoding=Encoding.FLAC,
                                sample_rate=self.SAMPLE_RATE)
        self.assertEqual(sample.source_uri, self.AUDIO_SOURCE_URI)
        self.assertEqual(sample.encoding, Encoding.FLAC)
        self.assertEqual(sample.sample_rate, self.SAMPLE_RATE)

    def test_content_and_source_uri(self):
        with self.assertRaises(ValueError):
            self._make_one(content='awefawagaeragere',
                           source_uri=self.AUDIO_SOURCE_URI)

    def test_sample_rates(self):
        from google.cloud.speech.encoding import Encoding

        with self.assertRaises(ValueError):
            self._make_one(source_uri=self.AUDIO_SOURCE_URI,
                           sample_rate=7999)
        with self.assertRaises(ValueError):
            self._make_one(source_uri=self.AUDIO_SOURCE_URI,
                           sample_rate=48001)

        sample = self._make_one(source_uri=self.AUDIO_SOURCE_URI,
                                sample_rate=self.SAMPLE_RATE,
                                encoding=Encoding.FLAC)
        self.assertEqual(sample.sample_rate, self.SAMPLE_RATE)
        self.assertEqual(sample.encoding, Encoding.FLAC)

        sample = self._make_one(source_uri=self.AUDIO_SOURCE_URI,
                                encoding=Encoding.FLAC)
        self.assertEqual(sample.sample_rate, self.SAMPLE_RATE)

    def test_encoding(self):
        from google.cloud.speech.encoding import Encoding

        with self.assertRaises(ValueError):
            self._make_one(source_uri=self.AUDIO_SOURCE_URI,
                           sample_rate=self.SAMPLE_RATE,
                           encoding='OGG')
        with self.assertRaises(ValueError):
            self._make_one(source_uri=self.AUDIO_SOURCE_URI,
                           sample_rate=self.SAMPLE_RATE)
        sample = self._make_one(source_uri=self.AUDIO_SOURCE_URI,
                                sample_rate=self.SAMPLE_RATE,
                                encoding=Encoding.FLAC)
        self.assertEqual(sample.encoding, Encoding.FLAC)
