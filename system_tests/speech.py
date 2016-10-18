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


class TestSpeechClient(unittest.TestCase):

    def _make_sync_request(self, content=None, source_uri=None,
                           max_alternatives=None):
        from google.cloud.speech.encoding import Encoding
        from google.cloud import speech

        client = speech.Client()
        sample = client.sample(content=content,
                               source_uri=source_uri,
                               encoding=Encoding.LINEAR16,
                               sample_rate=16000)
        result = client.sync_recognize(sample,
                                       language_code='en-US',
                                       max_alternatives=max_alternatives,
                                       profanity_filter=True,
                                       speech_context=['Google',
                                                       'cloud'])
        return result

    def test_sync_recognize_local_file(self):
        file_name = 'system_tests/data/hello.wav'

        with open(file_name, 'rb') as file_obj:
            result = self._make_sync_request(content=file_obj.read(),
                                             max_alternatives=2)

            self.assertEqual(result[0]['transcript'],
                             'hello thank you for using Google Cloud platform')
            self.assertGreater(result[0]['confidence'], .90)
            self.assertEqual(result[1]['transcript'],
                             'thank you for using Google Cloud platform')
            self.assertEqual(len(result), 2)

    def test_sync_recognize_gcs_file(self):
        import os

        source_uri = os.getenv('SPEECH_GCS_URI')
        result = self._make_sync_request(source_uri=source_uri,
                                         max_alternatives=1)
        self.assertEqual(result[0]['transcript'],
                         'hello thank you for using Google Cloud platform')
        self.assertGreater(result[0]['confidence'], .90)
        self.assertEqual(len(result), 1)
