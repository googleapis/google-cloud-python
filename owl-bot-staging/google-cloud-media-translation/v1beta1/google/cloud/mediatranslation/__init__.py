# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from google.cloud.mediatranslation import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.mediatranslation_v1beta1.services.speech_translation_service.client import SpeechTranslationServiceClient
from google.cloud.mediatranslation_v1beta1.services.speech_translation_service.async_client import SpeechTranslationServiceAsyncClient

from google.cloud.mediatranslation_v1beta1.types.media_translation import StreamingTranslateSpeechConfig
from google.cloud.mediatranslation_v1beta1.types.media_translation import StreamingTranslateSpeechRequest
from google.cloud.mediatranslation_v1beta1.types.media_translation import StreamingTranslateSpeechResponse
from google.cloud.mediatranslation_v1beta1.types.media_translation import StreamingTranslateSpeechResult
from google.cloud.mediatranslation_v1beta1.types.media_translation import TranslateSpeechConfig

__all__ = ('SpeechTranslationServiceClient',
    'SpeechTranslationServiceAsyncClient',
    'StreamingTranslateSpeechConfig',
    'StreamingTranslateSpeechRequest',
    'StreamingTranslateSpeechResponse',
    'StreamingTranslateSpeechResult',
    'TranslateSpeechConfig',
)
