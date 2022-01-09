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

from google.cloud.contact_center_insights_v1.services.contact_center_insights.client import (
    ContactCenterInsightsClient,
)
from google.cloud.contact_center_insights_v1.services.contact_center_insights.async_client import (
    ContactCenterInsightsAsyncClient,
)

from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    CalculateIssueModelStatsRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    CalculateIssueModelStatsResponse,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    CalculateStatsRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    CalculateStatsResponse,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    CreateAnalysisOperationMetadata,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    CreateAnalysisRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    CreateConversationRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    CreateIssueModelMetadata,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    CreateIssueModelRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    CreatePhraseMatcherRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    CreateViewRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    DeleteAnalysisRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    DeleteConversationRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    DeleteIssueModelMetadata,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    DeleteIssueModelRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    DeletePhraseMatcherRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    DeleteViewRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    DeployIssueModelMetadata,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    DeployIssueModelRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    DeployIssueModelResponse,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ExportInsightsDataMetadata,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ExportInsightsDataRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ExportInsightsDataResponse,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    GetAnalysisRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    GetConversationRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    GetIssueModelRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    GetIssueRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    GetPhraseMatcherRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    GetSettingsRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    GetViewRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ListAnalysesRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ListAnalysesResponse,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ListConversationsRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ListConversationsResponse,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ListIssueModelsRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ListIssueModelsResponse,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ListIssuesRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ListIssuesResponse,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ListPhraseMatchersRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ListPhraseMatchersResponse,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ListViewsRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ListViewsResponse,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    UndeployIssueModelMetadata,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    UndeployIssueModelRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    UndeployIssueModelResponse,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    UpdateConversationRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    UpdateIssueModelRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    UpdateIssueRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    UpdatePhraseMatcherRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    UpdateSettingsRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    UpdateViewRequest,
)
from google.cloud.contact_center_insights_v1.types.contact_center_insights import (
    ConversationView,
)
from google.cloud.contact_center_insights_v1.types.resources import Analysis
from google.cloud.contact_center_insights_v1.types.resources import AnalysisResult
from google.cloud.contact_center_insights_v1.types.resources import AnnotationBoundary
from google.cloud.contact_center_insights_v1.types.resources import AnswerFeedback
from google.cloud.contact_center_insights_v1.types.resources import (
    ArticleSuggestionData,
)
from google.cloud.contact_center_insights_v1.types.resources import CallAnnotation
from google.cloud.contact_center_insights_v1.types.resources import Conversation
from google.cloud.contact_center_insights_v1.types.resources import (
    ConversationDataSource,
)
from google.cloud.contact_center_insights_v1.types.resources import (
    ConversationLevelSentiment,
)
from google.cloud.contact_center_insights_v1.types.resources import (
    ConversationParticipant,
)
from google.cloud.contact_center_insights_v1.types.resources import DialogflowIntent
from google.cloud.contact_center_insights_v1.types.resources import (
    DialogflowInteractionData,
)
from google.cloud.contact_center_insights_v1.types.resources import DialogflowSource
from google.cloud.contact_center_insights_v1.types.resources import Entity
from google.cloud.contact_center_insights_v1.types.resources import EntityMentionData
from google.cloud.contact_center_insights_v1.types.resources import ExactMatchConfig
from google.cloud.contact_center_insights_v1.types.resources import FaqAnswerData
from google.cloud.contact_center_insights_v1.types.resources import GcsSource
from google.cloud.contact_center_insights_v1.types.resources import HoldData
from google.cloud.contact_center_insights_v1.types.resources import Intent
from google.cloud.contact_center_insights_v1.types.resources import IntentMatchData
from google.cloud.contact_center_insights_v1.types.resources import InterruptionData
from google.cloud.contact_center_insights_v1.types.resources import Issue
from google.cloud.contact_center_insights_v1.types.resources import IssueAssignment
from google.cloud.contact_center_insights_v1.types.resources import IssueModel
from google.cloud.contact_center_insights_v1.types.resources import IssueModelLabelStats
from google.cloud.contact_center_insights_v1.types.resources import IssueModelResult
from google.cloud.contact_center_insights_v1.types.resources import PhraseMatchData
from google.cloud.contact_center_insights_v1.types.resources import PhraseMatcher
from google.cloud.contact_center_insights_v1.types.resources import PhraseMatchRule
from google.cloud.contact_center_insights_v1.types.resources import (
    PhraseMatchRuleConfig,
)
from google.cloud.contact_center_insights_v1.types.resources import PhraseMatchRuleGroup
from google.cloud.contact_center_insights_v1.types.resources import RuntimeAnnotation
from google.cloud.contact_center_insights_v1.types.resources import SentimentData
from google.cloud.contact_center_insights_v1.types.resources import Settings
from google.cloud.contact_center_insights_v1.types.resources import SilenceData
from google.cloud.contact_center_insights_v1.types.resources import (
    SmartComposeSuggestionData,
)
from google.cloud.contact_center_insights_v1.types.resources import SmartReplyData
from google.cloud.contact_center_insights_v1.types.resources import View

__all__ = (
    "ContactCenterInsightsClient",
    "ContactCenterInsightsAsyncClient",
    "CalculateIssueModelStatsRequest",
    "CalculateIssueModelStatsResponse",
    "CalculateStatsRequest",
    "CalculateStatsResponse",
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
    "ExportInsightsDataMetadata",
    "ExportInsightsDataRequest",
    "ExportInsightsDataResponse",
    "GetAnalysisRequest",
    "GetConversationRequest",
    "GetIssueModelRequest",
    "GetIssueRequest",
    "GetPhraseMatcherRequest",
    "GetSettingsRequest",
    "GetViewRequest",
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
    "UndeployIssueModelMetadata",
    "UndeployIssueModelRequest",
    "UndeployIssueModelResponse",
    "UpdateConversationRequest",
    "UpdateIssueModelRequest",
    "UpdateIssueRequest",
    "UpdatePhraseMatcherRequest",
    "UpdateSettingsRequest",
    "UpdateViewRequest",
    "ConversationView",
    "Analysis",
    "AnalysisResult",
    "AnnotationBoundary",
    "AnswerFeedback",
    "ArticleSuggestionData",
    "CallAnnotation",
    "Conversation",
    "ConversationDataSource",
    "ConversationLevelSentiment",
    "ConversationParticipant",
    "DialogflowIntent",
    "DialogflowInteractionData",
    "DialogflowSource",
    "Entity",
    "EntityMentionData",
    "ExactMatchConfig",
    "FaqAnswerData",
    "GcsSource",
    "HoldData",
    "Intent",
    "IntentMatchData",
    "InterruptionData",
    "Issue",
    "IssueAssignment",
    "IssueModel",
    "IssueModelLabelStats",
    "IssueModelResult",
    "PhraseMatchData",
    "PhraseMatcher",
    "PhraseMatchRule",
    "PhraseMatchRuleConfig",
    "PhraseMatchRuleGroup",
    "RuntimeAnnotation",
    "SentimentData",
    "Settings",
    "SilenceData",
    "SmartComposeSuggestionData",
    "SmartReplyData",
    "View",
)
