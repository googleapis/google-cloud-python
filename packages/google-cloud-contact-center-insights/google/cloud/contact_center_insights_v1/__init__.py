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

from .services.contact_center_insights import ContactCenterInsightsClient
from .services.contact_center_insights import ContactCenterInsightsAsyncClient

from .types.contact_center_insights import CalculateIssueModelStatsRequest
from .types.contact_center_insights import CalculateIssueModelStatsResponse
from .types.contact_center_insights import CalculateStatsRequest
from .types.contact_center_insights import CalculateStatsResponse
from .types.contact_center_insights import CreateAnalysisOperationMetadata
from .types.contact_center_insights import CreateAnalysisRequest
from .types.contact_center_insights import CreateConversationRequest
from .types.contact_center_insights import CreateIssueModelMetadata
from .types.contact_center_insights import CreateIssueModelRequest
from .types.contact_center_insights import CreatePhraseMatcherRequest
from .types.contact_center_insights import CreateViewRequest
from .types.contact_center_insights import DeleteAnalysisRequest
from .types.contact_center_insights import DeleteConversationRequest
from .types.contact_center_insights import DeleteIssueModelMetadata
from .types.contact_center_insights import DeleteIssueModelRequest
from .types.contact_center_insights import DeletePhraseMatcherRequest
from .types.contact_center_insights import DeleteViewRequest
from .types.contact_center_insights import DeployIssueModelMetadata
from .types.contact_center_insights import DeployIssueModelRequest
from .types.contact_center_insights import DeployIssueModelResponse
from .types.contact_center_insights import ExportInsightsDataMetadata
from .types.contact_center_insights import ExportInsightsDataRequest
from .types.contact_center_insights import ExportInsightsDataResponse
from .types.contact_center_insights import GetAnalysisRequest
from .types.contact_center_insights import GetConversationRequest
from .types.contact_center_insights import GetIssueModelRequest
from .types.contact_center_insights import GetIssueRequest
from .types.contact_center_insights import GetPhraseMatcherRequest
from .types.contact_center_insights import GetSettingsRequest
from .types.contact_center_insights import GetViewRequest
from .types.contact_center_insights import ListAnalysesRequest
from .types.contact_center_insights import ListAnalysesResponse
from .types.contact_center_insights import ListConversationsRequest
from .types.contact_center_insights import ListConversationsResponse
from .types.contact_center_insights import ListIssueModelsRequest
from .types.contact_center_insights import ListIssueModelsResponse
from .types.contact_center_insights import ListIssuesRequest
from .types.contact_center_insights import ListIssuesResponse
from .types.contact_center_insights import ListPhraseMatchersRequest
from .types.contact_center_insights import ListPhraseMatchersResponse
from .types.contact_center_insights import ListViewsRequest
from .types.contact_center_insights import ListViewsResponse
from .types.contact_center_insights import UndeployIssueModelMetadata
from .types.contact_center_insights import UndeployIssueModelRequest
from .types.contact_center_insights import UndeployIssueModelResponse
from .types.contact_center_insights import UpdateConversationRequest
from .types.contact_center_insights import UpdateIssueModelRequest
from .types.contact_center_insights import UpdateIssueRequest
from .types.contact_center_insights import UpdatePhraseMatcherRequest
from .types.contact_center_insights import UpdateSettingsRequest
from .types.contact_center_insights import UpdateViewRequest
from .types.contact_center_insights import ConversationView
from .types.resources import Analysis
from .types.resources import AnalysisResult
from .types.resources import AnnotationBoundary
from .types.resources import AnswerFeedback
from .types.resources import ArticleSuggestionData
from .types.resources import CallAnnotation
from .types.resources import Conversation
from .types.resources import ConversationDataSource
from .types.resources import ConversationLevelSentiment
from .types.resources import ConversationParticipant
from .types.resources import DialogflowIntent
from .types.resources import DialogflowInteractionData
from .types.resources import DialogflowSource
from .types.resources import Entity
from .types.resources import EntityMentionData
from .types.resources import ExactMatchConfig
from .types.resources import FaqAnswerData
from .types.resources import GcsSource
from .types.resources import HoldData
from .types.resources import Intent
from .types.resources import IntentMatchData
from .types.resources import InterruptionData
from .types.resources import Issue
from .types.resources import IssueAssignment
from .types.resources import IssueModel
from .types.resources import IssueModelLabelStats
from .types.resources import IssueModelResult
from .types.resources import PhraseMatchData
from .types.resources import PhraseMatcher
from .types.resources import PhraseMatchRule
from .types.resources import PhraseMatchRuleConfig
from .types.resources import PhraseMatchRuleGroup
from .types.resources import RuntimeAnnotation
from .types.resources import SentimentData
from .types.resources import Settings
from .types.resources import SilenceData
from .types.resources import SmartComposeSuggestionData
from .types.resources import SmartReplyData
from .types.resources import View

__all__ = (
    "ContactCenterInsightsAsyncClient",
    "Analysis",
    "AnalysisResult",
    "AnnotationBoundary",
    "AnswerFeedback",
    "ArticleSuggestionData",
    "CalculateIssueModelStatsRequest",
    "CalculateIssueModelStatsResponse",
    "CalculateStatsRequest",
    "CalculateStatsResponse",
    "CallAnnotation",
    "ContactCenterInsightsClient",
    "Conversation",
    "ConversationDataSource",
    "ConversationLevelSentiment",
    "ConversationParticipant",
    "ConversationView",
    "CreateAnalysisOperationMetadata",
    "CreateAnalysisRequest",
    "CreateConversationRequest",
    "CreateIssueModelMetadata",
    "CreateIssueModelRequest",
    "CreatePhraseMatcherRequest",
    "CreateViewRequest",
    "DeleteAnalysisRequest",
    "DeleteConversationRequest",
    "DeleteIssueModelMetadata",
    "DeleteIssueModelRequest",
    "DeletePhraseMatcherRequest",
    "DeleteViewRequest",
    "DeployIssueModelMetadata",
    "DeployIssueModelRequest",
    "DeployIssueModelResponse",
    "DialogflowIntent",
    "DialogflowInteractionData",
    "DialogflowSource",
    "Entity",
    "EntityMentionData",
    "ExactMatchConfig",
    "ExportInsightsDataMetadata",
    "ExportInsightsDataRequest",
    "ExportInsightsDataResponse",
    "FaqAnswerData",
    "GcsSource",
    "GetAnalysisRequest",
    "GetConversationRequest",
    "GetIssueModelRequest",
    "GetIssueRequest",
    "GetPhraseMatcherRequest",
    "GetSettingsRequest",
    "GetViewRequest",
    "HoldData",
    "Intent",
    "IntentMatchData",
    "InterruptionData",
    "Issue",
    "IssueAssignment",
    "IssueModel",
    "IssueModelLabelStats",
    "IssueModelResult",
    "ListAnalysesRequest",
    "ListAnalysesResponse",
    "ListConversationsRequest",
    "ListConversationsResponse",
    "ListIssueModelsRequest",
    "ListIssueModelsResponse",
    "ListIssuesRequest",
    "ListIssuesResponse",
    "ListPhraseMatchersRequest",
    "ListPhraseMatchersResponse",
    "ListViewsRequest",
    "ListViewsResponse",
    "PhraseMatchData",
    "PhraseMatchRule",
    "PhraseMatchRuleConfig",
    "PhraseMatchRuleGroup",
    "PhraseMatcher",
    "RuntimeAnnotation",
    "SentimentData",
    "Settings",
    "SilenceData",
    "SmartComposeSuggestionData",
    "SmartReplyData",
    "UndeployIssueModelMetadata",
    "UndeployIssueModelRequest",
    "UndeployIssueModelResponse",
    "UpdateConversationRequest",
    "UpdateIssueModelRequest",
    "UpdateIssueRequest",
    "UpdatePhraseMatcherRequest",
    "UpdateSettingsRequest",
    "UpdateViewRequest",
    "View",
)
