# -*- coding: utf-8 -*-
from .services.language_service import LanguageService
from .types.language_service import AnalyzeEntitiesRequest
from .types.language_service import AnalyzeEntitiesResponse
from .types.language_service import AnalyzeEntitySentimentRequest
from .types.language_service import AnalyzeEntitySentimentResponse
from .types.language_service import AnalyzeSentimentRequest
from .types.language_service import AnalyzeSentimentResponse
from .types.language_service import AnalyzeSyntaxRequest
from .types.language_service import AnalyzeSyntaxResponse
from .types.language_service import AnnotateTextRequest
from .types.language_service import AnnotateTextResponse
from .types.language_service import ClassificationCategory
from .types.language_service import ClassifyTextRequest
from .types.language_service import ClassifyTextResponse
from .types.language_service import DependencyEdge
from .types.language_service import Document
from .types.language_service import Entity
from .types.language_service import EntityMention
from .types.language_service import PartOfSpeech
from .types.language_service import Sentence
from .types.language_service import Sentiment
from .types.language_service import TextSpan
from .types.language_service import Token


__all__ = (
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
    "LanguageService",
)
