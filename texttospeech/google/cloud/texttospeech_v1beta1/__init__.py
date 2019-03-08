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

from __future__ import absolute_import

from google.cloud.texttospeech_v1beta1 import types
from google.cloud.texttospeech_v1beta1.gapic import enums
from google.cloud.texttospeech_v1beta1.gapic import text_to_speech_client


class TextToSpeechClient(text_to_speech_client.TextToSpeechClient):
    __doc__ = text_to_speech_client.TextToSpeechClient.__doc__
    enums = enums


__all__ = ("enums", "types", "TextToSpeechClient")
