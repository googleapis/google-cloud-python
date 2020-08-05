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

from .services.translation_service import TranslationServiceClient
from .types.translation_service import BatchTranslateMetadata
from .types.translation_service import BatchTranslateResponse
from .types.translation_service import BatchTranslateTextRequest
from .types.translation_service import CreateGlossaryMetadata
from .types.translation_service import CreateGlossaryRequest
from .types.translation_service import DeleteGlossaryMetadata
from .types.translation_service import DeleteGlossaryRequest
from .types.translation_service import DeleteGlossaryResponse
from .types.translation_service import DetectLanguageRequest
from .types.translation_service import DetectLanguageResponse
from .types.translation_service import DetectedLanguage
from .types.translation_service import GcsDestination
from .types.translation_service import GcsSource
from .types.translation_service import GetGlossaryRequest
from .types.translation_service import GetSupportedLanguagesRequest
from .types.translation_service import Glossary
from .types.translation_service import GlossaryInputConfig
from .types.translation_service import InputConfig
from .types.translation_service import ListGlossariesRequest
from .types.translation_service import ListGlossariesResponse
from .types.translation_service import OutputConfig
from .types.translation_service import SupportedLanguage
from .types.translation_service import SupportedLanguages
from .types.translation_service import TranslateTextGlossaryConfig
from .types.translation_service import TranslateTextRequest
from .types.translation_service import TranslateTextResponse
from .types.translation_service import Translation


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
    "TranslationServiceClient",
)
