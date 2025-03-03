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
from google.cloud.contact_center_insights_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.contact_center_insights import ContactCenterInsightsClient
from .services.contact_center_insights import ContactCenterInsightsAsyncClient

from .types.contact_center_insights import BulkAnalyzeConversationsMetadata
from .types.contact_center_insights import BulkAnalyzeConversationsRequest
from .types.contact_center_insights import BulkAnalyzeConversationsResponse
from .types.contact_center_insights import BulkDeleteConversationsMetadata
from .types.contact_center_insights import BulkDeleteConversationsRequest
from .types.contact_center_insights import BulkDeleteConversationsResponse
from .types.contact_center_insights import BulkDownloadFeedbackLabelsMetadata
from .types.contact_center_insights import BulkDownloadFeedbackLabelsRequest
from .types.contact_center_insights import BulkDownloadFeedbackLabelsResponse
from .types.contact_center_insights import BulkUploadFeedbackLabelsMetadata
from .types.contact_center_insights import BulkUploadFeedbackLabelsRequest
from .types.contact_center_insights import BulkUploadFeedbackLabelsResponse
from .types.contact_center_insights import CalculateIssueModelStatsRequest
from .types.contact_center_insights import CalculateIssueModelStatsResponse
from .types.contact_center_insights import CalculateStatsRequest
from .types.contact_center_insights import CalculateStatsResponse
from .types.contact_center_insights import CreateAnalysisOperationMetadata
from .types.contact_center_insights import CreateAnalysisRequest
from .types.contact_center_insights import CreateAnalysisRuleRequest
from .types.contact_center_insights import CreateConversationRequest
from .types.contact_center_insights import CreateFeedbackLabelRequest
from .types.contact_center_insights import CreateIssueModelMetadata
from .types.contact_center_insights import CreateIssueModelRequest
from .types.contact_center_insights import CreatePhraseMatcherRequest
from .types.contact_center_insights import CreateQaQuestionRequest
from .types.contact_center_insights import CreateQaScorecardRequest
from .types.contact_center_insights import CreateQaScorecardRevisionRequest
from .types.contact_center_insights import CreateViewRequest
from .types.contact_center_insights import DeleteAnalysisRequest
from .types.contact_center_insights import DeleteAnalysisRuleRequest
from .types.contact_center_insights import DeleteConversationRequest
from .types.contact_center_insights import DeleteFeedbackLabelRequest
from .types.contact_center_insights import DeleteIssueModelMetadata
from .types.contact_center_insights import DeleteIssueModelRequest
from .types.contact_center_insights import DeleteIssueRequest
from .types.contact_center_insights import DeletePhraseMatcherRequest
from .types.contact_center_insights import DeleteQaQuestionRequest
from .types.contact_center_insights import DeleteQaScorecardRequest
from .types.contact_center_insights import DeleteQaScorecardRevisionRequest
from .types.contact_center_insights import DeleteViewRequest
from .types.contact_center_insights import DeployIssueModelMetadata
from .types.contact_center_insights import DeployIssueModelRequest
from .types.contact_center_insights import DeployIssueModelResponse
from .types.contact_center_insights import DeployQaScorecardRevisionRequest
from .types.contact_center_insights import Dimension
from .types.contact_center_insights import ExportInsightsDataMetadata
from .types.contact_center_insights import ExportInsightsDataRequest
from .types.contact_center_insights import ExportInsightsDataResponse
from .types.contact_center_insights import ExportIssueModelMetadata
from .types.contact_center_insights import ExportIssueModelRequest
from .types.contact_center_insights import ExportIssueModelResponse
from .types.contact_center_insights import GetAnalysisRequest
from .types.contact_center_insights import GetAnalysisRuleRequest
from .types.contact_center_insights import GetConversationRequest
from .types.contact_center_insights import GetEncryptionSpecRequest
from .types.contact_center_insights import GetFeedbackLabelRequest
from .types.contact_center_insights import GetIssueModelRequest
from .types.contact_center_insights import GetIssueRequest
from .types.contact_center_insights import GetPhraseMatcherRequest
from .types.contact_center_insights import GetQaQuestionRequest
from .types.contact_center_insights import GetQaScorecardRequest
from .types.contact_center_insights import GetQaScorecardRevisionRequest
from .types.contact_center_insights import GetSettingsRequest
from .types.contact_center_insights import GetViewRequest
from .types.contact_center_insights import ImportIssueModelMetadata
from .types.contact_center_insights import ImportIssueModelRequest
from .types.contact_center_insights import ImportIssueModelResponse
from .types.contact_center_insights import IngestConversationsMetadata
from .types.contact_center_insights import IngestConversationsRequest
from .types.contact_center_insights import IngestConversationsResponse
from .types.contact_center_insights import InitializeEncryptionSpecMetadata
from .types.contact_center_insights import InitializeEncryptionSpecRequest
from .types.contact_center_insights import InitializeEncryptionSpecResponse
from .types.contact_center_insights import ListAllFeedbackLabelsRequest
from .types.contact_center_insights import ListAllFeedbackLabelsResponse
from .types.contact_center_insights import ListAnalysesRequest
from .types.contact_center_insights import ListAnalysesResponse
from .types.contact_center_insights import ListAnalysisRulesRequest
from .types.contact_center_insights import ListAnalysisRulesResponse
from .types.contact_center_insights import ListConversationsRequest
from .types.contact_center_insights import ListConversationsResponse
from .types.contact_center_insights import ListFeedbackLabelsRequest
from .types.contact_center_insights import ListFeedbackLabelsResponse
from .types.contact_center_insights import ListIssueModelsRequest
from .types.contact_center_insights import ListIssueModelsResponse
from .types.contact_center_insights import ListIssuesRequest
from .types.contact_center_insights import ListIssuesResponse
from .types.contact_center_insights import ListPhraseMatchersRequest
from .types.contact_center_insights import ListPhraseMatchersResponse
from .types.contact_center_insights import ListQaQuestionsRequest
from .types.contact_center_insights import ListQaQuestionsResponse
from .types.contact_center_insights import ListQaScorecardRevisionsRequest
from .types.contact_center_insights import ListQaScorecardRevisionsResponse
from .types.contact_center_insights import ListQaScorecardsRequest
from .types.contact_center_insights import ListQaScorecardsResponse
from .types.contact_center_insights import ListViewsRequest
from .types.contact_center_insights import ListViewsResponse
from .types.contact_center_insights import QueryMetricsMetadata
from .types.contact_center_insights import QueryMetricsRequest
from .types.contact_center_insights import QueryMetricsResponse
from .types.contact_center_insights import TuneQaScorecardRevisionMetadata
from .types.contact_center_insights import TuneQaScorecardRevisionRequest
from .types.contact_center_insights import TuneQaScorecardRevisionResponse
from .types.contact_center_insights import UndeployIssueModelMetadata
from .types.contact_center_insights import UndeployIssueModelRequest
from .types.contact_center_insights import UndeployIssueModelResponse
from .types.contact_center_insights import UndeployQaScorecardRevisionRequest
from .types.contact_center_insights import UpdateAnalysisRuleRequest
from .types.contact_center_insights import UpdateConversationRequest
from .types.contact_center_insights import UpdateFeedbackLabelRequest
from .types.contact_center_insights import UpdateIssueModelRequest
from .types.contact_center_insights import UpdateIssueRequest
from .types.contact_center_insights import UpdatePhraseMatcherRequest
from .types.contact_center_insights import UpdateQaQuestionRequest
from .types.contact_center_insights import UpdateQaScorecardRequest
from .types.contact_center_insights import UpdateSettingsRequest
from .types.contact_center_insights import UpdateViewRequest
from .types.contact_center_insights import UploadConversationMetadata
from .types.contact_center_insights import UploadConversationRequest
from .types.contact_center_insights import ConversationView
from .types.resources import Analysis
from .types.resources import AnalysisResult
from .types.resources import AnalysisRule
from .types.resources import AnnotationBoundary
from .types.resources import AnnotatorSelector
from .types.resources import AnswerFeedback
from .types.resources import ArticleSuggestionData
from .types.resources import CallAnnotation
from .types.resources import Conversation
from .types.resources import ConversationDataSource
from .types.resources import ConversationLevelSentiment
from .types.resources import ConversationLevelSilence
from .types.resources import ConversationParticipant
from .types.resources import ConversationSummarizationSuggestionData
from .types.resources import DialogflowIntent
from .types.resources import DialogflowInteractionData
from .types.resources import DialogflowSource
from .types.resources import EncryptionSpec
from .types.resources import Entity
from .types.resources import EntityMentionData
from .types.resources import ExactMatchConfig
from .types.resources import FaqAnswerData
from .types.resources import FeedbackLabel
from .types.resources import GcsSource
from .types.resources import HoldData
from .types.resources import Intent
from .types.resources import IntentMatchData
from .types.resources import InterruptionData
from .types.resources import Issue
from .types.resources import IssueAssignment
from .types.resources import IssueMatchData
from .types.resources import IssueModel
from .types.resources import IssueModelLabelStats
from .types.resources import IssueModelResult
from .types.resources import PhraseMatchData
from .types.resources import PhraseMatcher
from .types.resources import PhraseMatchRule
from .types.resources import PhraseMatchRuleConfig
from .types.resources import PhraseMatchRuleGroup
from .types.resources import QaAnswer
from .types.resources import QaQuestion
from .types.resources import QaScorecard
from .types.resources import QaScorecardResult
from .types.resources import QaScorecardRevision
from .types.resources import RedactionConfig
from .types.resources import RuntimeAnnotation
from .types.resources import SentimentData
from .types.resources import Settings
from .types.resources import SilenceData
from .types.resources import SmartComposeSuggestionData
from .types.resources import SmartReplyData
from .types.resources import SpeechConfig
from .types.resources import View
from .types.resources import DatasetValidationWarning

__all__ = (
    'ContactCenterInsightsAsyncClient',
'Analysis',
'AnalysisResult',
'AnalysisRule',
'AnnotationBoundary',
'AnnotatorSelector',
'AnswerFeedback',
'ArticleSuggestionData',
'BulkAnalyzeConversationsMetadata',
'BulkAnalyzeConversationsRequest',
'BulkAnalyzeConversationsResponse',
'BulkDeleteConversationsMetadata',
'BulkDeleteConversationsRequest',
'BulkDeleteConversationsResponse',
'BulkDownloadFeedbackLabelsMetadata',
'BulkDownloadFeedbackLabelsRequest',
'BulkDownloadFeedbackLabelsResponse',
'BulkUploadFeedbackLabelsMetadata',
'BulkUploadFeedbackLabelsRequest',
'BulkUploadFeedbackLabelsResponse',
'CalculateIssueModelStatsRequest',
'CalculateIssueModelStatsResponse',
'CalculateStatsRequest',
'CalculateStatsResponse',
'CallAnnotation',
'ContactCenterInsightsClient',
'Conversation',
'ConversationDataSource',
'ConversationLevelSentiment',
'ConversationLevelSilence',
'ConversationParticipant',
'ConversationSummarizationSuggestionData',
'ConversationView',
'CreateAnalysisOperationMetadata',
'CreateAnalysisRequest',
'CreateAnalysisRuleRequest',
'CreateConversationRequest',
'CreateFeedbackLabelRequest',
'CreateIssueModelMetadata',
'CreateIssueModelRequest',
'CreatePhraseMatcherRequest',
'CreateQaQuestionRequest',
'CreateQaScorecardRequest',
'CreateQaScorecardRevisionRequest',
'CreateViewRequest',
'DatasetValidationWarning',
'DeleteAnalysisRequest',
'DeleteAnalysisRuleRequest',
'DeleteConversationRequest',
'DeleteFeedbackLabelRequest',
'DeleteIssueModelMetadata',
'DeleteIssueModelRequest',
'DeleteIssueRequest',
'DeletePhraseMatcherRequest',
'DeleteQaQuestionRequest',
'DeleteQaScorecardRequest',
'DeleteQaScorecardRevisionRequest',
'DeleteViewRequest',
'DeployIssueModelMetadata',
'DeployIssueModelRequest',
'DeployIssueModelResponse',
'DeployQaScorecardRevisionRequest',
'DialogflowIntent',
'DialogflowInteractionData',
'DialogflowSource',
'Dimension',
'EncryptionSpec',
'Entity',
'EntityMentionData',
'ExactMatchConfig',
'ExportInsightsDataMetadata',
'ExportInsightsDataRequest',
'ExportInsightsDataResponse',
'ExportIssueModelMetadata',
'ExportIssueModelRequest',
'ExportIssueModelResponse',
'FaqAnswerData',
'FeedbackLabel',
'GcsSource',
'GetAnalysisRequest',
'GetAnalysisRuleRequest',
'GetConversationRequest',
'GetEncryptionSpecRequest',
'GetFeedbackLabelRequest',
'GetIssueModelRequest',
'GetIssueRequest',
'GetPhraseMatcherRequest',
'GetQaQuestionRequest',
'GetQaScorecardRequest',
'GetQaScorecardRevisionRequest',
'GetSettingsRequest',
'GetViewRequest',
'HoldData',
'ImportIssueModelMetadata',
'ImportIssueModelRequest',
'ImportIssueModelResponse',
'IngestConversationsMetadata',
'IngestConversationsRequest',
'IngestConversationsResponse',
'InitializeEncryptionSpecMetadata',
'InitializeEncryptionSpecRequest',
'InitializeEncryptionSpecResponse',
'Intent',
'IntentMatchData',
'InterruptionData',
'Issue',
'IssueAssignment',
'IssueMatchData',
'IssueModel',
'IssueModelLabelStats',
'IssueModelResult',
'ListAllFeedbackLabelsRequest',
'ListAllFeedbackLabelsResponse',
'ListAnalysesRequest',
'ListAnalysesResponse',
'ListAnalysisRulesRequest',
'ListAnalysisRulesResponse',
'ListConversationsRequest',
'ListConversationsResponse',
'ListFeedbackLabelsRequest',
'ListFeedbackLabelsResponse',
'ListIssueModelsRequest',
'ListIssueModelsResponse',
'ListIssuesRequest',
'ListIssuesResponse',
'ListPhraseMatchersRequest',
'ListPhraseMatchersResponse',
'ListQaQuestionsRequest',
'ListQaQuestionsResponse',
'ListQaScorecardRevisionsRequest',
'ListQaScorecardRevisionsResponse',
'ListQaScorecardsRequest',
'ListQaScorecardsResponse',
'ListViewsRequest',
'ListViewsResponse',
'PhraseMatchData',
'PhraseMatchRule',
'PhraseMatchRuleConfig',
'PhraseMatchRuleGroup',
'PhraseMatcher',
'QaAnswer',
'QaQuestion',
'QaScorecard',
'QaScorecardResult',
'QaScorecardRevision',
'QueryMetricsMetadata',
'QueryMetricsRequest',
'QueryMetricsResponse',
'RedactionConfig',
'RuntimeAnnotation',
'SentimentData',
'Settings',
'SilenceData',
'SmartComposeSuggestionData',
'SmartReplyData',
'SpeechConfig',
'TuneQaScorecardRevisionMetadata',
'TuneQaScorecardRevisionRequest',
'TuneQaScorecardRevisionResponse',
'UndeployIssueModelMetadata',
'UndeployIssueModelRequest',
'UndeployIssueModelResponse',
'UndeployQaScorecardRevisionRequest',
'UpdateAnalysisRuleRequest',
'UpdateConversationRequest',
'UpdateFeedbackLabelRequest',
'UpdateIssueModelRequest',
'UpdateIssueRequest',
'UpdatePhraseMatcherRequest',
'UpdateQaQuestionRequest',
'UpdateQaScorecardRequest',
'UpdateSettingsRequest',
'UpdateViewRequest',
'UploadConversationMetadata',
'UploadConversationRequest',
'View',
)
