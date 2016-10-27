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

import os
import unittest

from google.cloud import exceptions
from google.cloud import speech
from google.cloud import storage
from google.cloud.speech.transcript import Transcript

from system_test_utils import unique_resource_id
from retry import RetryErrors

AUDIO_FILE = os.path.join(os.path.dirname(__file__), 'data', 'hello.wav')


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None
    TEST_BUCKET = None


def setUpModule():
    Config.CLIENT = speech.Client()
    # Now create a bucket for GCS stored content.
    storage_client = storage.Client()
    bucket_name = 'new' + unique_resource_id()
    Config.TEST_BUCKET = storage_client.bucket(bucket_name)
    # 429 Too Many Requests in case API requests rate-limited.
    retry_429 = RetryErrors(exceptions.TooManyRequests)
    retry_429(Config.TEST_BUCKET.create)()


def tearDownModule():
    # 409 Conflict if the bucket is full.
    # 429 Too Many Requests in case API requests rate-limited.
    bucket_retry = RetryErrors(
        (exceptions.TooManyRequests, exceptions.Conflict))
    bucket_retry(Config.TEST_BUCKET.delete)(force=True)


class TestSpeechClient(unittest.TestCase):
    ASSERT_TEXT = 'thank you for using Google Cloud platform'

    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _make_sync_request(self, content=None, source_uri=None,
                           max_alternatives=None):
        client = Config.CLIENT
        sample = client.sample(content=content,
                               source_uri=source_uri,
                               encoding=speech.Encoding.LINEAR16,
                               sample_rate=16000)
        result = client.sync_recognize(sample,
                                       language_code='en-US',
                                       max_alternatives=max_alternatives,
                                       profanity_filter=True,
                                       speech_context=['Google', 'cloud'])
        return result

    def _check_best_results(self, results):
        top_result = results[0]
        self.assertIsInstance(top_result, Transcript)
        self.assertEqual(top_result.transcript,
                         'hello ' + self.ASSERT_TEXT)
        self.assertGreater(top_result.confidence, 0.90)

    def test_sync_recognize_local_file(self):
        with open(AUDIO_FILE, 'rb') as file_obj:
            results = self._make_sync_request(content=file_obj.read(),
                                              max_alternatives=2)
            second_alternative = results[1]
            self.assertEqual(len(results), 2)
            self._check_best_results(results)
            self.assertIsInstance(second_alternative, Transcript)
            self.assertEqual(second_alternative.transcript, self.ASSERT_TEXT)
            self.assertEqual(second_alternative.confidence, 0.0)

    def test_sync_recognize_gcs_file(self):
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'hello.wav'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(AUDIO_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)
        result = self._make_sync_request(source_uri=source_uri,
                                         max_alternatives=1)
        self._check_best_results(result)
