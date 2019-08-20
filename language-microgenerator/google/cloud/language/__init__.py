# -*- coding: utf-8 -*-
from google.cloud.language_v1.services.language_service.client import LanguageService
from google.cloud.language_v1.types.language_service import AnalyzeEntitiesRequest
from google.cloud.language_v1.types.language_service import AnalyzeEntitiesResponse
from google.cloud.language_v1.types.language_service import (
    AnalyzeEntitySentimentRequest,
)
from google.cloud.language_v1.types.language_service import (
    AnalyzeEntitySentimentResponse,
)
from google.cloud.language_v1.types.language_service import AnalyzeSentimentRequest
from google.cloud.language_v1.types.language_service import AnalyzeSentimentResponse
from google.cloud.language_v1.types.language_service import AnalyzeSyntaxRequest
from google.cloud.language_v1.types.language_service import AnalyzeSyntaxResponse
from google.cloud.language_v1.types.language_service import AnnotateTextRequest
from google.cloud.language_v1.types.language_service import AnnotateTextResponse
from google.cloud.language_v1.types.language_service import ClassificationCategory
from google.cloud.language_v1.types.language_service import ClassifyTextRequest
from google.cloud.language_v1.types.language_service import ClassifyTextResponse
from google.cloud.language_v1.types.language_service import DependencyEdge
from google.cloud.language_v1.types.language_service import Document
from google.cloud.language_v1.types.language_service import Entity
from google.cloud.language_v1.types.language_service import EntityMention
from google.cloud.language_v1.types.language_service import PartOfSpeech
from google.cloud.language_v1.types.language_service import Sentence
from google.cloud.language_v1.types.language_service import Sentiment
from google.cloud.language_v1.types.language_service import TextSpan
from google.cloud.language_v1.types.language_service import Token


__all__ = (
    "LanguageService",
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
    "ClassifyTextRequest",
    "ClassifyTextResponse",
    "DependencyEdge",
    "Document",
    "Entity",
    "EntityMention",
    "PartOfSpeech",
    "Sentence",
    "Sentiment",
    "TextSpan",
    "Token",
)
