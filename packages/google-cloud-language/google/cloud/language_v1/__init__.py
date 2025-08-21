# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.language_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.language_service import LanguageServiceAsyncClient, LanguageServiceClient
from .types.language_service import (
    AnalyzeEntitiesRequest,
    AnalyzeEntitiesResponse,
    AnalyzeEntitySentimentRequest,
    AnalyzeEntitySentimentResponse,
    AnalyzeSentimentRequest,
    AnalyzeSentimentResponse,
    AnalyzeSyntaxRequest,
    AnalyzeSyntaxResponse,
    AnnotateTextRequest,
    AnnotateTextResponse,
    ClassificationCategory,
    ClassificationModelOptions,
    ClassifyTextRequest,
    ClassifyTextResponse,
    DependencyEdge,
    Document,
    EncodingType,
    Entity,
    EntityMention,
    ModerateTextRequest,
    ModerateTextResponse,
    PartOfSpeech,
    Sentence,
    Sentiment,
    TextSpan,
    Token,
)

__all__ = (
    "LanguageServiceAsyncClient",
    "AnalyzeEntitiesRequest",
    "AnalyzeEntitiesResponse",
    "AnalyzeEntitySentimentRequest",
    "AnalyzeEntitySentimentResponse",
    "AnalyzeSentimentRequest",
    "AnalyzeSentimentResponse",
    "AnalyzeSyntaxRequest",
    "AnalyzeSyntaxResponse",
    "AnnotateTextRequest",
    "AnnotateTextResponse",
    "ClassificationCategory",
    "ClassificationModelOptions",
    "ClassifyTextRequest",
    "ClassifyTextResponse",
    "DependencyEdge",
    "Document",
    "EncodingType",
    "Entity",
    "EntityMention",
    "LanguageServiceClient",
    "ModerateTextRequest",
    "ModerateTextResponse",
    "PartOfSpeech",
    "Sentence",
    "Sentiment",
    "TextSpan",
    "Token",
)
