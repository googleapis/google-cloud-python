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

# DO NOT EDIT! This is a generated sample ("Request",  "samplegen_write_bytes_to_file")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-texttospeech

# sample-metadata
#   title: Synthesize an .mp3 file with audio saying the provided phrase
#   description: Synthesize an .mp3 file with audio saying the provided phrase
#   usage: python3 samples/v1/samplegen_write_bytes_to_file.py

# [START samplegen_write_bytes_to_file]
from google.cloud import texttospeech_v1
from google.cloud.texttospeech_v1 import enums


def sample_synthesize_speech():
    """Synthesize an .mp3 file with audio saying the provided phrase"""

    client = texttospeech_v1.TextToSpeechClient()

    text = "Hello, world!"
    input_ = {"text": text}
    language_code = "en"
    voice = {"language_code": language_code}
    audio_encoding = enums.AudioEncoding.MP3
    audio_config = {"audio_encoding": audio_encoding}

    response = client.synthesize_speech(input_, voice, audio_config)
    print(u"Writing the synthsized results to output.mp3")
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)


# [END samplegen_write_bytes_to_file]


def main():
    sample_synthesize_speech()


if __name__ == "__main__":
    main()
