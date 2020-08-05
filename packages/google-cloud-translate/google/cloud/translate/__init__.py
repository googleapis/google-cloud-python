# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

from google.cloud.translate_v3.services.translation_service.async_client import (
    TranslationServiceAsyncClient,
)
from google.cloud.translate_v3.services.translation_service.client import (
    TranslationServiceClient,
)
from google.cloud.translate_v3.types.translation_service import BatchTranslateMetadata
from google.cloud.translate_v3.types.translation_service import BatchTranslateResponse
from google.cloud.translate_v3.types.translation_service import (
    BatchTranslateTextRequest,
)
from google.cloud.translate_v3.types.translation_service import CreateGlossaryMetadata
from google.cloud.translate_v3.types.translation_service import CreateGlossaryRequest
from google.cloud.translate_v3.types.translation_service import DeleteGlossaryMetadata
from google.cloud.translate_v3.types.translation_service import DeleteGlossaryRequest
from google.cloud.translate_v3.types.translation_service import DeleteGlossaryResponse
from google.cloud.translate_v3.types.translation_service import DetectLanguageRequest
from google.cloud.translate_v3.types.translation_service import DetectLanguageResponse
from google.cloud.translate_v3.types.translation_service import DetectedLanguage
from google.cloud.translate_v3.types.translation_service import GcsDestination
from google.cloud.translate_v3.types.translation_service import GcsSource
from google.cloud.translate_v3.types.translation_service import GetGlossaryRequest
from google.cloud.translate_v3.types.translation_service import (
    GetSupportedLanguagesRequest,
)
from google.cloud.translate_v3.types.translation_service import Glossary
from google.cloud.translate_v3.types.translation_service import GlossaryInputConfig
from google.cloud.translate_v3.types.translation_service import InputConfig
from google.cloud.translate_v3.types.translation_service import ListGlossariesRequest
from google.cloud.translate_v3.types.translation_service import ListGlossariesResponse
from google.cloud.translate_v3.types.translation_service import OutputConfig
from google.cloud.translate_v3.types.translation_service import SupportedLanguage
from google.cloud.translate_v3.types.translation_service import SupportedLanguages
from google.cloud.translate_v3.types.translation_service import (
    TranslateTextGlossaryConfig,
)
from google.cloud.translate_v3.types.translation_service import TranslateTextRequest
from google.cloud.translate_v3.types.translation_service import TranslateTextResponse
from google.cloud.translate_v3.types.translation_service import Translation

__all__ = (
    "BatchTranslateMetadata",
    "BatchTranslateResponse",
    "BatchTranslateTextRequest",
    "CreateGlossaryMetadata",
    "CreateGlossaryRequest",
    "DeleteGlossaryMetadata",
    "DeleteGlossaryRequest",
    "DeleteGlossaryResponse",
    "DetectLanguageRequest",
    "DetectLanguageResponse",
    "DetectedLanguage",
    "GcsDestination",
    "GcsSource",
    "GetGlossaryRequest",
    "GetSupportedLanguagesRequest",
    "Glossary",
    "GlossaryInputConfig",
    "InputConfig",
    "ListGlossariesRequest",
    "ListGlossariesResponse",
    "OutputConfig",
    "SupportedLanguage",
    "SupportedLanguages",
    "TranslateTextGlossaryConfig",
    "TranslateTextRequest",
    "TranslateTextResponse",
    "Translation",
    "TranslationServiceAsyncClient",
    "TranslationServiceClient",
)
