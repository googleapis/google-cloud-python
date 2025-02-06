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
from google.cloud.contact_center_insights import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.contact_center_insights_v1.services.contact_center_insights.client import ContactCenterInsightsClient
from google.cloud.contact_center_insights_v1.services.contact_center_insights.async_client import ContactCenterInsightsAsyncClient

from google.cloud.contact_center_insights_v1.types.contact_center_insights import BulkAnalyzeConversationsMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import BulkAnalyzeConversationsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import BulkAnalyzeConversationsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import BulkDeleteConversationsMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import BulkDeleteConversationsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import BulkDeleteConversationsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import BulkDownloadFeedbackLabelsMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import BulkDownloadFeedbackLabelsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import BulkDownloadFeedbackLabelsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import BulkUploadFeedbackLabelsMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import BulkUploadFeedbackLabelsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import BulkUploadFeedbackLabelsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CalculateIssueModelStatsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CalculateIssueModelStatsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CalculateStatsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CalculateStatsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CreateAnalysisOperationMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CreateAnalysisRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CreateAnalysisRuleRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CreateConversationRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CreateFeedbackLabelRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CreateIssueModelMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CreateIssueModelRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CreatePhraseMatcherRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CreateQaQuestionRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CreateQaScorecardRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CreateQaScorecardRevisionRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import CreateViewRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeleteAnalysisRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeleteAnalysisRuleRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeleteConversationRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeleteFeedbackLabelRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeleteIssueModelMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeleteIssueModelRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeleteIssueRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeletePhraseMatcherRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeleteQaQuestionRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeleteQaScorecardRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeleteQaScorecardRevisionRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeleteViewRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeployIssueModelMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeployIssueModelRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeployIssueModelResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import DeployQaScorecardRevisionRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import Dimension
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ExportInsightsDataMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ExportInsightsDataRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ExportInsightsDataResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ExportIssueModelMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ExportIssueModelRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ExportIssueModelResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetAnalysisRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetAnalysisRuleRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetConversationRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetEncryptionSpecRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetFeedbackLabelRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetIssueModelRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetIssueRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetPhraseMatcherRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetQaQuestionRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetQaScorecardRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetQaScorecardRevisionRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetSettingsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import GetViewRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ImportIssueModelMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ImportIssueModelRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ImportIssueModelResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import IngestConversationsMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import IngestConversationsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import IngestConversationsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import InitializeEncryptionSpecMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import InitializeEncryptionSpecRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import InitializeEncryptionSpecResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListAllFeedbackLabelsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListAllFeedbackLabelsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListAnalysesRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListAnalysesResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListAnalysisRulesRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListAnalysisRulesResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListConversationsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListConversationsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListFeedbackLabelsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListFeedbackLabelsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListIssueModelsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListIssueModelsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListIssuesRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListIssuesResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListPhraseMatchersRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListPhraseMatchersResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListQaQuestionsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListQaQuestionsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListQaScorecardRevisionsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListQaScorecardRevisionsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListQaScorecardsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListQaScorecardsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListViewsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ListViewsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import QueryMetricsMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import QueryMetricsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import QueryMetricsResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import TuneQaScorecardRevisionMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import TuneQaScorecardRevisionRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import TuneQaScorecardRevisionResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UndeployIssueModelMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UndeployIssueModelRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UndeployIssueModelResponse
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UndeployQaScorecardRevisionRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UpdateAnalysisRuleRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UpdateConversationRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UpdateFeedbackLabelRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UpdateIssueModelRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UpdateIssueRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UpdatePhraseMatcherRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UpdateQaQuestionRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UpdateQaScorecardRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UpdateSettingsRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UpdateViewRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UploadConversationMetadata
from google.cloud.contact_center_insights_v1.types.contact_center_insights import UploadConversationRequest
from google.cloud.contact_center_insights_v1.types.contact_center_insights import ConversationView
from google.cloud.contact_center_insights_v1.types.resources import Analysis
from google.cloud.contact_center_insights_v1.types.resources import AnalysisResult
from google.cloud.contact_center_insights_v1.types.resources import AnalysisRule
from google.cloud.contact_center_insights_v1.types.resources import AnnotationBoundary
from google.cloud.contact_center_insights_v1.types.resources import AnnotatorSelector
from google.cloud.contact_center_insights_v1.types.resources import AnswerFeedback
from google.cloud.contact_center_insights_v1.types.resources import ArticleSuggestionData
from google.cloud.contact_center_insights_v1.types.resources import CallAnnotation
from google.cloud.contact_center_insights_v1.types.resources import Conversation
from google.cloud.contact_center_insights_v1.types.resources import ConversationDataSource
from google.cloud.contact_center_insights_v1.types.resources import ConversationLevelSentiment
from google.cloud.contact_center_insights_v1.types.resources import ConversationLevelSilence
from google.cloud.contact_center_insights_v1.types.resources import ConversationParticipant
from google.cloud.contact_center_insights_v1.types.resources import ConversationSummarizationSuggestionData
from google.cloud.contact_center_insights_v1.types.resources import DialogflowIntent
from google.cloud.contact_center_insights_v1.types.resources import DialogflowInteractionData
from google.cloud.contact_center_insights_v1.types.resources import DialogflowSource
from google.cloud.contact_center_insights_v1.types.resources import EncryptionSpec
from google.cloud.contact_center_insights_v1.types.resources import Entity
from google.cloud.contact_center_insights_v1.types.resources import EntityMentionData
from google.cloud.contact_center_insights_v1.types.resources import ExactMatchConfig
from google.cloud.contact_center_insights_v1.types.resources import FaqAnswerData
from google.cloud.contact_center_insights_v1.types.resources import FeedbackLabel
from google.cloud.contact_center_insights_v1.types.resources import GcsSource
from google.cloud.contact_center_insights_v1.types.resources import HoldData
from google.cloud.contact_center_insights_v1.types.resources import Intent
from google.cloud.contact_center_insights_v1.types.resources import IntentMatchData
from google.cloud.contact_center_insights_v1.types.resources import InterruptionData
from google.cloud.contact_center_insights_v1.types.resources import Issue
from google.cloud.contact_center_insights_v1.types.resources import IssueAssignment
from google.cloud.contact_center_insights_v1.types.resources import IssueMatchData
from google.cloud.contact_center_insights_v1.types.resources import IssueModel
from google.cloud.contact_center_insights_v1.types.resources import IssueModelLabelStats
from google.cloud.contact_center_insights_v1.types.resources import IssueModelResult
from google.cloud.contact_center_insights_v1.types.resources import PhraseMatchData
from google.cloud.contact_center_insights_v1.types.resources import PhraseMatcher
from google.cloud.contact_center_insights_v1.types.resources import PhraseMatchRule
from google.cloud.contact_center_insights_v1.types.resources import PhraseMatchRuleConfig
from google.cloud.contact_center_insights_v1.types.resources import PhraseMatchRuleGroup
from google.cloud.contact_center_insights_v1.types.resources import QaAnswer
from google.cloud.contact_center_insights_v1.types.resources import QaQuestion
from google.cloud.contact_center_insights_v1.types.resources import QaScorecard
from google.cloud.contact_center_insights_v1.types.resources import QaScorecardResult
from google.cloud.contact_center_insights_v1.types.resources import QaScorecardRevision
from google.cloud.contact_center_insights_v1.types.resources import RedactionConfig
from google.cloud.contact_center_insights_v1.types.resources import RuntimeAnnotation
from google.cloud.contact_center_insights_v1.types.resources import SentimentData
from google.cloud.contact_center_insights_v1.types.resources import Settings
from google.cloud.contact_center_insights_v1.types.resources import SilenceData
from google.cloud.contact_center_insights_v1.types.resources import SmartComposeSuggestionData
from google.cloud.contact_center_insights_v1.types.resources import SmartReplyData
from google.cloud.contact_center_insights_v1.types.resources import SpeechConfig
from google.cloud.contact_center_insights_v1.types.resources import View
from google.cloud.contact_center_insights_v1.types.resources import DatasetValidationWarning

__all__ = ('ContactCenterInsightsClient',
    'ContactCenterInsightsAsyncClient',
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
    'Dimension',
    'ExportInsightsDataMetadata',
    'ExportInsightsDataRequest',
    'ExportInsightsDataResponse',
    'ExportIssueModelMetadata',
    'ExportIssueModelRequest',
    'ExportIssueModelResponse',
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
    'ImportIssueModelMetadata',
    'ImportIssueModelRequest',
    'ImportIssueModelResponse',
    'IngestConversationsMetadata',
    'IngestConversationsRequest',
    'IngestConversationsResponse',
    'InitializeEncryptionSpecMetadata',
    'InitializeEncryptionSpecRequest',
    'InitializeEncryptionSpecResponse',
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
    'QueryMetricsMetadata',
    'QueryMetricsRequest',
    'QueryMetricsResponse',
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
    'ConversationView',
    'Analysis',
    'AnalysisResult',
    'AnalysisRule',
    'AnnotationBoundary',
    'AnnotatorSelector',
    'AnswerFeedback',
    'ArticleSuggestionData',
    'CallAnnotation',
    'Conversation',
    'ConversationDataSource',
    'ConversationLevelSentiment',
    'ConversationLevelSilence',
    'ConversationParticipant',
    'ConversationSummarizationSuggestionData',
    'DialogflowIntent',
    'DialogflowInteractionData',
    'DialogflowSource',
    'EncryptionSpec',
    'Entity',
    'EntityMentionData',
    'ExactMatchConfig',
    'FaqAnswerData',
    'FeedbackLabel',
    'GcsSource',
    'HoldData',
    'Intent',
    'IntentMatchData',
    'InterruptionData',
    'Issue',
    'IssueAssignment',
    'IssueMatchData',
    'IssueModel',
    'IssueModelLabelStats',
    'IssueModelResult',
    'PhraseMatchData',
    'PhraseMatcher',
    'PhraseMatchRule',
    'PhraseMatchRuleConfig',
    'PhraseMatchRuleGroup',
    'QaAnswer',
    'QaQuestion',
    'QaScorecard',
    'QaScorecardResult',
    'QaScorecardRevision',
    'RedactionConfig',
    'RuntimeAnnotation',
    'SentimentData',
    'Settings',
    'SilenceData',
    'SmartComposeSuggestionData',
    'SmartReplyData',
    'SpeechConfig',
    'View',
    'DatasetValidationWarning',
)
