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

# DO NOT EDIT! This is a generated sample ("Request",  "samplegen_repeated_fields")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title: Showing repeated fields (in request and response)
#   description: Showing repeated fields (in request and response)
#   usage: python3 samples/v1p1beta1/samplegen_repeated_fields.py

# [START samplegen_repeated_fields]
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums


def sample_recognize():
    """Showing repeated fields (in request and response)"""

    client = speech_v1p1beta1.SpeechClient()

    encoding = enums.RecognitionConfig.AudioEncoding.MP3

    # A list of strings containing words and phrases "hints"
    phrases_element = "Fox in socks"
    phrases_element_2 = "Knox in box"
    phrases = [phrases_element, phrases_element_2]
    speech_contexts_element = {"phrases": phrases}
    speech_contexts = [speech_contexts_element]
    config = {"encoding": encoding, "speech_contexts": speech_contexts}
    uri = "gs://[BUCKET]/[FILENAME]"
    audio = {"uri": uri}

    response = client.recognize(config, audio)
    # Loop over all transcription results
    for result in response.results:
        # The first "alternative" of each result contains most likely transcription
        alternative = result.alternatives[0]
        print(u"Transcription of result: {}".format(alternative.transcript))


# [END samplegen_repeated_fields]


def main():
    sample_recognize()


if __name__ == "__main__":
    main()
