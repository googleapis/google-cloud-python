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
from google.cloud.language_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.language_service import LanguageServiceClient
from .services.language_service import LanguageServiceAsyncClient

from .types.language_service import AnalyzeEntitiesRequest
from .types.language_service import AnalyzeEntitiesResponse
from .types.language_service import AnalyzeSentimentRequest
from .types.language_service import AnalyzeSentimentResponse
from .types.language_service import AnnotateTextRequest
from .types.language_service import AnnotateTextResponse
from .types.language_service import ClassificationCategory
from .types.language_service import ClassifyTextRequest
from .types.language_service import ClassifyTextResponse
from .types.language_service import Document
from .types.language_service import Entity
from .types.language_service import EntityMention
from .types.language_service import ModerateTextRequest
from .types.language_service import ModerateTextResponse
from .types.language_service import Sentence
from .types.language_service import Sentiment
from .types.language_service import TextSpan
from .types.language_service import EncodingType

__all__ = (
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
'EncodingType',
'Entity',
'EntityMention',
'LanguageServiceClient',
'ModerateTextRequest',
'ModerateTextResponse',
'Sentence',
'Sentiment',
'TextSpan',
)
