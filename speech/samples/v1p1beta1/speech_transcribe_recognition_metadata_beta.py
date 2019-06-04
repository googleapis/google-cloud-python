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

# DO NOT EDIT! This is a generated sample ("Request",  "speech_transcribe_recognition_metadata_beta")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

import sys

# [START speech_transcribe_recognition_metadata_beta]

from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
import io
import six

def sample_recognize(local_file_path):
  """
    Adds additional details short audio file included in this recognition request

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """
  # [START speech_transcribe_recognition_metadata_beta_core]

  client = speech_v1p1beta1.SpeechClient()

  # local_file_path = 'resources/commercial_mono.wav'

  if isinstance(local_file_path, six.binary_type):
    local_file_path = local_file_path.decode('utf-8')

  # The use case of the audio, e.g. PHONE_CALL, DISCUSSION, PRESENTATION, et al.
  interaction_type = enums.RecognitionMetadata.InteractionType.VOICE_SEARCH

  # The kind of device used to capture the audio
  recording_device_type = enums.RecognitionMetadata.RecordingDeviceType.SMARTPHONE

  # The device used to make the recording.
  # Arbitrary string, e.g. 'Pixel XL', 'VoIP', 'Cardioid Microphone', or other
  # value.
  recording_device_name = 'Pixel 3'
  metadata = {'interaction_type': interaction_type, 'recording_device_type': recording_device_type, 'recording_device_name': recording_device_name}

  # The language of the supplied audio. Even though additional languages are
  # provided by alternative_language_codes, a primary language is still required.
  language_code = 'en-US'
  config = {'metadata': metadata, 'language_code': language_code}
  with io.open(local_file_path, 'rb') as f:
    content = f.read()
  audio = {'content': content}

  response = client.recognize(config, audio)
  for result in response.results:
    # First alternative is the most probable result
    alternative = result.alternatives[0]
    print('Transcript: {}'.format(alternative.transcript))

  # [END speech_transcribe_recognition_metadata_beta_core]
# [END speech_transcribe_recognition_metadata_beta]

def main():
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('--local_file_path', type=str, default='resources/commercial_mono.wav')
  args = parser.parse_args()

  sample_recognize(args.local_file_path)

if __name__ == '__main__':
  main()