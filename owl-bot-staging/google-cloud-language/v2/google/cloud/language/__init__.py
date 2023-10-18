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
from google.cloud.language import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.language_v2.services.language_service.client import LanguageServiceClient
from google.cloud.language_v2.services.language_service.async_client import LanguageServiceAsyncClient

from google.cloud.language_v2.types.language_service import AnalyzeEntitiesRequest
from google.cloud.language_v2.types.language_service import AnalyzeEntitiesResponse
from google.cloud.language_v2.types.language_service import AnalyzeSentimentRequest
from google.cloud.language_v2.types.language_service import AnalyzeSentimentResponse
from google.cloud.language_v2.types.language_service import AnnotateTextRequest
from google.cloud.language_v2.types.language_service import AnnotateTextResponse
from google.cloud.language_v2.types.language_service import ClassificationCategory
from google.cloud.language_v2.types.language_service import ClassifyTextRequest
from google.cloud.language_v2.types.language_service import ClassifyTextResponse
from google.cloud.language_v2.types.language_service import Document
from google.cloud.language_v2.types.language_service import Entity
from google.cloud.language_v2.types.language_service import EntityMention
from google.cloud.language_v2.types.language_service import ModerateTextRequest
from google.cloud.language_v2.types.language_service import ModerateTextResponse
from google.cloud.language_v2.types.language_service import Sentence
from google.cloud.language_v2.types.language_service import Sentiment
from google.cloud.language_v2.types.language_service import TextSpan
from google.cloud.language_v2.types.language_service import EncodingType

__all__ = ('LanguageServiceClient',
    'LanguageServiceAsyncClient',
    'AnalyzeEntitiesRequest',
    'AnalyzeEntitiesResponse',
    'AnalyzeSentimentRequest',
    'AnalyzeSentimentResponse',
    'AnnotateTextRequest',
    'AnnotateTextResponse',
    'ClassificationCategory',
    'ClassifyTextRequest',
    'ClassifyTextResponse',
    'Document',
    'Entity',
    'EntityMention',
    'ModerateTextRequest',
    'ModerateTextResponse',
    'Sentence',
    'Sentiment',
    'TextSpan',
    'EncodingType',
)
