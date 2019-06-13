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

# DO NOT EDIT! This is a generated sample ("Request",  "speech_quickstart_beta")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title:
#   description: Performs synchronous speech recognition on an audio file.
#   usage: python3 samples/v1p1beta1/speech_quickstart_beta.py [--sample_rate_hertz 44100] [--language_code "en-US"] [--uri_path "gs://cloud-samples-data/speech/brooklyn_bridge.mp3"]
import sys

# [START speech_quickstart_beta]

from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums


def sample_recognize(sample_rate_hertz, language_code, uri_path):
    """
    Performs synchronous speech recognition on an audio file.

    Args:
      sample_rate_hertz Sample rate in Hertz of the audio data sent in all
      `RecognitionAudio` messages. Valid values are: 8000-48000.
      language_code The language of the supplied audio.
      uri_path Path to the audio file stored on GCS.
    """

    client = speech_v1p1beta1.SpeechClient()

    # sample_rate_hertz = 44100
    # language_code = 'en-US'
    # uri_path = 'gs://cloud-samples-data/speech/brooklyn_bridge.mp3'
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {
        "encoding": encoding,
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
    }
    audio = {"uri": uri_path}

    response = client.recognize(config, audio)
    for result in response.results:
        transcript = result.alternatives[0].transcript
        print(u"Transcript: {}".format(transcript))


# [END speech_quickstart_beta]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sample_rate_hertz", type=int, default=44100)
    parser.add_argument("--language_code", type=str, default="en-US")
    parser.add_argument(
        "--uri_path",
        type=str,
        default="gs://cloud-samples-data/speech/brooklyn_bridge.mp3",
    )
    args = parser.parse_args()

    sample_recognize(args.sample_rate_hertz, args.language_code, args.uri_path)


if __name__ == "__main__":
    main()
