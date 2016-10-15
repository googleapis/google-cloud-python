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

    def test_sync_recognize_local_file(self):
        import io
        from google.cloud import speech
        client = speech.Client()
        file_name = 'system_tests/data/hello.wav'

        with io.open(file_name, 'rb') as file_obj:
            sample = client.sample(content=file_obj.read(),
                                   encoding=speech.Encoding.LINEAR16,
                                   sample_rate=16000)
            res = client.sync_recognize(sample,
                                        language_code='en-US',
                                        max_alternatives=2,
                                        profanity_filter=True,
                                        speech_context=['Google', 'cloud'])
            self.assertEqual(res[0].transcript,
                             'hello thank you for using Google Cloud platform')
            self.assertEqual(len(res), 2)

    def test_sync_recognize_gcs_file(self):
        from google.cloud import speech
        client = speech.Client()
        source_uri = 'gs://ferrous-arena-my-test-bucket/hello.wav'

        sample = client.sample(source_uri=source_uri,
                               encoding=speech.Encoding.LINEAR16,
                               sample_rate=16000)
        res = client.sync_recognize(sample,
                                    language_code='en-US',
                                    max_alternatives=1,
                                    profanity_filter=True,
                                    speech_context=['Google', 'cloud'])
        self.assertEqual(res[0].transcript,
                         'hello thank you for using Google Cloud platform')
        self.assertEqual(len(res), 1)
