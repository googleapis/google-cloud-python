# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import io
import requests

from google.cloud import speech_v1


class TestSystemSpeech(object):
    def test_recognize(self):

        try:
            BUCKET = os.environ["GOOGLE_CLOUD_TESTS_SPEECH_BUCKET"]
        except KeyError:
            BUCKET = "cloud-samples-tests"

        client = speech_v1.SpeechClient()

        config = {
            "encoding": speech_v1.RecognitionConfig.AudioEncoding.FLAC,
            "language_code": "en-US",
            "sample_rate_hertz": 16000,
        }

        uri = "gs://{}/speech/brooklyn.flac".format(BUCKET)
        audio = {"uri": uri}

        response = client.recognize(config=config, audio=audio)

        assert response.results[0].alternatives[0].transcript is not None

    def test_long_running_recognize(self):

        try:
            BUCKET = os.environ["GOOGLE_CLOUD_TESTS_SPEECH_BUCKET"]
        except KeyError:
            BUCKET = "cloud-samples-tests"

        client = speech_v1.SpeechClient()

        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.FLAC,
            language_code="en-US",
            sample_rate_hertz=16000,
        )

        uri = "gs://{}/speech/brooklyn.flac".format(BUCKET)
        audio = {"uri": uri}

        response = client.long_running_recognize(config=config, audio=audio)

        assert response.result() is not None

    def test_streaming_recognize(self):

        try:
            BUCKET = os.environ["GOOGLE_CLOUD_TESTS_SPEECH_BUCKET"]
        except KeyError:
            BUCKET = "cloud-samples-tests"

        client = speech_v1.SpeechClient()

        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.FLAC,
            language_code="en-US",
            sample_rate_hertz=16000,
        )
        streamingConfig = speech_v1.StreamingRecognitionConfig(config=config)

        uri = "https://storage.googleapis.com/{}/speech/brooklyn.flac".format(BUCKET)
        streaming_requests = [
            speech_v1.StreamingRecognizeRequest(audio_content=requests.get(uri).content)
        ]

        responses = client.streaming_recognize(
            config=streamingConfig, requests=streaming_requests
        )

        for response in responses:
            for result in response.results:
                assert result.alternatives[0].transcript is not None
