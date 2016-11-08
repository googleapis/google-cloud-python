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
from google.cloud.speech.alternative import Alternative

from system_test_utils import unique_resource_id
from retry import RetryErrors
from retry import RetryResult


AUDIO_FILE = os.path.join(os.path.dirname(__file__), 'data', 'hello.wav')


def _operation_complete(result):
    """Return operation result."""
    return result


def _wait_until_complete(operation, max_attempts=5):
    """Wait until an operation has completed.

    :type operation: :class:`google.cloud.operation.Operation`
    :param operation: Operation that has not completed.

    :type max_attempts: int
    :param max_attempts: (Optional) The maximum number of times to check if
                         the operation has completed. Defaults to 5.

    :rtype: bool
    :returns: Boolean indicating if the operation is complete.
    """
    retry = RetryResult(_operation_complete, max_tries=max_attempts)
    return retry(operation.poll)()


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None
    TEST_BUCKET = None
    USE_GAX = True


def setUpModule():
    Config.CLIENT = speech.Client()
    Config.USE_GAX = Config.CLIENT._use_gax
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
        return client.sync_recognize(sample,
                                     language_code='en-US',
                                     max_alternatives=max_alternatives,
                                     profanity_filter=True,
                                     speech_context=['Google', 'cloud'])

    def _make_async_request(self, content=None, source_uri=None,
                            max_alternatives=None):
        client = Config.CLIENT
        sample = client.sample(content=content,
                               source_uri=source_uri,
                               encoding=speech.Encoding.LINEAR16,
                               sample_rate=16000)
        return client.async_recognize(sample,
                                      language_code='en-US',
                                      max_alternatives=max_alternatives,
                                      profanity_filter=True,
                                      speech_context=['Google', 'cloud'])

    def _make_streaming_request(self, file_obj, single_utterance=True,
                                interim_results=False):
        client = Config.CLIENT
        sample = client.sample(content=file_obj,
                               encoding=speech.Encoding.LINEAR16,
                               sample_rate=16000)
        return client.streaming_recognize(sample,
                                          single_utterance=single_utterance,
                                          interim_results=interim_results)

    def _check_results(self, results, num_results=1):
        self.assertEqual(len(results), num_results)
        top_result = results[0]
        self.assertIsInstance(top_result, Alternative)
        self.assertEqual(top_result.transcript,
                         'hello ' + self.ASSERT_TEXT)
        self.assertGreater(top_result.confidence, 0.90)
        if num_results == 2:
            second_alternative = results[1]
            self.assertIsInstance(second_alternative, Alternative)
            self.assertEqual(second_alternative.transcript, self.ASSERT_TEXT)
            self.assertIsNone(second_alternative.confidence)

    def test_sync_recognize_local_file(self):
        with open(AUDIO_FILE, 'rb') as file_obj:
            content = file_obj.read()

        results = self._make_sync_request(content=content,
                                          max_alternatives=2)
        self._check_results(results, 2)

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
        self._check_results(result)

    def test_async_recognize_local_file(self):
        with open(AUDIO_FILE, 'rb') as file_obj:
            content = file_obj.read()

        operation = self._make_async_request(content=content,
                                             max_alternatives=2)

        _wait_until_complete(operation)
        self._check_results(operation.results, 2)

    def test_async_recognize_gcs_file(self):
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'hello.wav'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        with open(AUDIO_FILE, 'rb') as file_obj:
            blob.upload_from_file(file_obj)

        source_uri = 'gs://%s/%s' % (bucket_name, blob_name)
        operation = self._make_async_request(source_uri=source_uri,
                                             max_alternatives=2)

        _wait_until_complete(operation)
        self._check_results(operation.results, 2)

    def test_stream_recognize(self):
        if not Config.USE_GAX:
            self.skipTest('gRPC is required for Speech Streaming Recognize.')

        with open(AUDIO_FILE, 'rb') as file_obj:
            for results in self._make_streaming_request(file_obj):
                self._check_results(results)

    def test_stream_recognize_interim_results(self):
        if not Config.USE_GAX:
            self.skipTest('gRPC is required for Speech Streaming Recognize.')

        # These extra words are interim_results that the API returns as it's
        # deciphering the speech audio. This has a high probability of becoming
        # out of date and causing the test to fail.
        extras = ' Google Now who hello thank you for you for use hello '
        with open(AUDIO_FILE, 'rb') as file_obj:
            recognize = self._make_streaming_request(file_obj,
                                                     interim_results=True)
            responses = list(recognize)
            for response in responses:
                if response[0].transcript:
                    self.assertIn(response[0].transcript,
                                  extras + self.ASSERT_TEXT)

            self.assertGreater(len(responses), 5)
            self._check_results(responses[-1])

    def test_stream_recognize_single_utterance(self):
        if not Config.USE_GAX:
            self.skipTest('gRPC is required for Speech Streaming Recognize.')

        with open(AUDIO_FILE, 'rb') as file_obj:
            for results in self._make_streaming_request(
                    file_obj, single_utterance=False):
                self._check_results(results)
