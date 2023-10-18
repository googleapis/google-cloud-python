# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
#
from google.cloud.texttospeech_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.text_to_speech import TextToSpeechClient
from .services.text_to_speech import TextToSpeechAsyncClient
from .services.text_to_speech_long_audio_synthesize import TextToSpeechLongAudioSynthesizeClient
from .services.text_to_speech_long_audio_synthesize import TextToSpeechLongAudioSynthesizeAsyncClient

from .types.cloud_tts import AudioConfig
from .types.cloud_tts import CustomVoiceParams
from .types.cloud_tts import ListVoicesRequest
from .types.cloud_tts import ListVoicesResponse
from .types.cloud_tts import SynthesisInput
from .types.cloud_tts import SynthesizeSpeechRequest
from .types.cloud_tts import SynthesizeSpeechResponse
from .types.cloud_tts import Voice
from .types.cloud_tts import VoiceSelectionParams
from .types.cloud_tts import AudioEncoding
from .types.cloud_tts import SsmlVoiceGender
from .types.cloud_tts_lrs import SynthesizeLongAudioMetadata
from .types.cloud_tts_lrs import SynthesizeLongAudioRequest
from .types.cloud_tts_lrs import SynthesizeLongAudioResponse

__all__ = (
    'TextToSpeechAsyncClient',
    'TextToSpeechLongAudioSynthesizeAsyncClient',
'AudioConfig',
'AudioEncoding',
'CustomVoiceParams',
'ListVoicesRequest',
'ListVoicesResponse',
'SsmlVoiceGender',
'SynthesisInput',
'SynthesizeLongAudioMetadata',
'SynthesizeLongAudioRequest',
'SynthesizeLongAudioResponse',
'SynthesizeSpeechRequest',
'SynthesizeSpeechResponse',
'TextToSpeechClient',
'TextToSpeechLongAudioSynthesizeClient',
'Voice',
'VoiceSelectionParams',
)
