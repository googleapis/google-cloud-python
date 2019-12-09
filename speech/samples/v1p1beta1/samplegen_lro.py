# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

# DO NOT EDIT! This is a generated sample ("LongRunningPromise",  "samplegen_lro")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title: Calling Long-Running API method
#   description: Calling Long-Running API method
#   usage: python3 samples/v1p1beta1/samplegen_lro.py

# [START samplegen_lro]
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums


def sample_long_running_recognize():
    """Calling Long-Running API method"""

    client = speech_v1p1beta1.SpeechClient()

    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {"encoding": encoding}
    uri = "gs://[BUCKET]/[FILENAME]"
    audio = {"uri": uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    # Your audio has been transcribed.
    print(u"Transcript: {}".format(response.results[0].alternatives[0].transcript))


# [END samplegen_lro]


def main():
    sample_long_running_recognize()


if __name__ == "__main__":
    main()
