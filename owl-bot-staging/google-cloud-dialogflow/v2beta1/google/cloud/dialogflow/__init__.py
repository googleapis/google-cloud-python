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
from google.cloud.dialogflow import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.dialogflow_v2beta1.services.agents.client import AgentsClient
from google.cloud.dialogflow_v2beta1.services.agents.async_client import AgentsAsyncClient
from google.cloud.dialogflow_v2beta1.services.answer_records.client import AnswerRecordsClient
from google.cloud.dialogflow_v2beta1.services.answer_records.async_client import AnswerRecordsAsyncClient
from google.cloud.dialogflow_v2beta1.services.contexts.client import ContextsClient
from google.cloud.dialogflow_v2beta1.services.contexts.async_client import ContextsAsyncClient
from google.cloud.dialogflow_v2beta1.services.conversation_profiles.client import ConversationProfilesClient
from google.cloud.dialogflow_v2beta1.services.conversation_profiles.async_client import ConversationProfilesAsyncClient
from google.cloud.dialogflow_v2beta1.services.conversations.client import ConversationsClient
from google.cloud.dialogflow_v2beta1.services.conversations.async_client import ConversationsAsyncClient
from google.cloud.dialogflow_v2beta1.services.documents.client import DocumentsClient
from google.cloud.dialogflow_v2beta1.services.documents.async_client import DocumentsAsyncClient
from google.cloud.dialogflow_v2beta1.services.encryption_spec_service.client import EncryptionSpecServiceClient
from google.cloud.dialogflow_v2beta1.services.encryption_spec_service.async_client import EncryptionSpecServiceAsyncClient
from google.cloud.dialogflow_v2beta1.services.entity_types.client import EntityTypesClient
from google.cloud.dialogflow_v2beta1.services.entity_types.async_client import EntityTypesAsyncClient
from google.cloud.dialogflow_v2beta1.services.environments.client import EnvironmentsClient
from google.cloud.dialogflow_v2beta1.services.environments.async_client import EnvironmentsAsyncClient
from google.cloud.dialogflow_v2beta1.services.fulfillments.client import FulfillmentsClient
from google.cloud.dialogflow_v2beta1.services.fulfillments.async_client import FulfillmentsAsyncClient
from google.cloud.dialogflow_v2beta1.services.generators.client import GeneratorsClient
from google.cloud.dialogflow_v2beta1.services.generators.async_client import GeneratorsAsyncClient
from google.cloud.dialogflow_v2beta1.services.intents.client import IntentsClient
from google.cloud.dialogflow_v2beta1.services.intents.async_client import IntentsAsyncClient
from google.cloud.dialogflow_v2beta1.services.knowledge_bases.client import KnowledgeBasesClient
from google.cloud.dialogflow_v2beta1.services.knowledge_bases.async_client import KnowledgeBasesAsyncClient
from google.cloud.dialogflow_v2beta1.services.participants.client import ParticipantsClient
from google.cloud.dialogflow_v2beta1.services.participants.async_client import ParticipantsAsyncClient
from google.cloud.dialogflow_v2beta1.services.session_entity_types.client import SessionEntityTypesClient
from google.cloud.dialogflow_v2beta1.services.session_entity_types.async_client import SessionEntityTypesAsyncClient
from google.cloud.dialogflow_v2beta1.services.sessions.client import SessionsClient
from google.cloud.dialogflow_v2beta1.services.sessions.async_client import SessionsAsyncClient
from google.cloud.dialogflow_v2beta1.services.sip_trunks.client import SipTrunksClient
from google.cloud.dialogflow_v2beta1.services.sip_trunks.async_client import SipTrunksAsyncClient
from google.cloud.dialogflow_v2beta1.services.versions.client import VersionsClient
from google.cloud.dialogflow_v2beta1.services.versions.async_client import VersionsAsyncClient

from google.cloud.dialogflow_v2beta1.types.agent import Agent
from google.cloud.dialogflow_v2beta1.types.agent import DeleteAgentRequest
from google.cloud.dialogflow_v2beta1.types.agent import ExportAgentRequest
from google.cloud.dialogflow_v2beta1.types.agent import ExportAgentResponse
from google.cloud.dialogflow_v2beta1.types.agent import GetAgentRequest
from google.cloud.dialogflow_v2beta1.types.agent import GetValidationResultRequest
from google.cloud.dialogflow_v2beta1.types.agent import ImportAgentRequest
from google.cloud.dialogflow_v2beta1.types.agent import RestoreAgentRequest
from google.cloud.dialogflow_v2beta1.types.agent import SearchAgentsRequest
from google.cloud.dialogflow_v2beta1.types.agent import SearchAgentsResponse
from google.cloud.dialogflow_v2beta1.types.agent import SetAgentRequest
from google.cloud.dialogflow_v2beta1.types.agent import SubAgent
from google.cloud.dialogflow_v2beta1.types.agent import TrainAgentRequest
from google.cloud.dialogflow_v2beta1.types.answer_record import AgentAssistantFeedback
from google.cloud.dialogflow_v2beta1.types.answer_record import AgentAssistantRecord
from google.cloud.dialogflow_v2beta1.types.answer_record import AnswerFeedback
from google.cloud.dialogflow_v2beta1.types.answer_record import AnswerRecord
from google.cloud.dialogflow_v2beta1.types.answer_record import GetAnswerRecordRequest
from google.cloud.dialogflow_v2beta1.types.answer_record import ListAnswerRecordsRequest
from google.cloud.dialogflow_v2beta1.types.answer_record import ListAnswerRecordsResponse
from google.cloud.dialogflow_v2beta1.types.answer_record import UpdateAnswerRecordRequest
from google.cloud.dialogflow_v2beta1.types.audio_config import BargeInConfig
from google.cloud.dialogflow_v2beta1.types.audio_config import InputAudioConfig
from google.cloud.dialogflow_v2beta1.types.audio_config import OutputAudioConfig
from google.cloud.dialogflow_v2beta1.types.audio_config import SpeechContext
from google.cloud.dialogflow_v2beta1.types.audio_config import SpeechToTextConfig
from google.cloud.dialogflow_v2beta1.types.audio_config import SpeechWordInfo
from google.cloud.dialogflow_v2beta1.types.audio_config import SynthesizeSpeechConfig
from google.cloud.dialogflow_v2beta1.types.audio_config import TelephonyDtmfEvents
from google.cloud.dialogflow_v2beta1.types.audio_config import VoiceSelectionParams
from google.cloud.dialogflow_v2beta1.types.audio_config import AudioEncoding
from google.cloud.dialogflow_v2beta1.types.audio_config import OutputAudioEncoding
from google.cloud.dialogflow_v2beta1.types.audio_config import SpeechModelVariant
from google.cloud.dialogflow_v2beta1.types.audio_config import SsmlVoiceGender
from google.cloud.dialogflow_v2beta1.types.audio_config import TelephonyDtmf
from google.cloud.dialogflow_v2beta1.types.context import Context
from google.cloud.dialogflow_v2beta1.types.context import CreateContextRequest
from google.cloud.dialogflow_v2beta1.types.context import DeleteAllContextsRequest
from google.cloud.dialogflow_v2beta1.types.context import DeleteContextRequest
from google.cloud.dialogflow_v2beta1.types.context import GetContextRequest
from google.cloud.dialogflow_v2beta1.types.context import ListContextsRequest
from google.cloud.dialogflow_v2beta1.types.context import ListContextsResponse
from google.cloud.dialogflow_v2beta1.types.context import UpdateContextRequest
from google.cloud.dialogflow_v2beta1.types.conversation import BatchCreateMessagesRequest
from google.cloud.dialogflow_v2beta1.types.conversation import BatchCreateMessagesResponse
from google.cloud.dialogflow_v2beta1.types.conversation import CompleteConversationRequest
from google.cloud.dialogflow_v2beta1.types.conversation import Conversation
from google.cloud.dialogflow_v2beta1.types.conversation import ConversationPhoneNumber
from google.cloud.dialogflow_v2beta1.types.conversation import CreateConversationRequest
from google.cloud.dialogflow_v2beta1.types.conversation import CreateMessageRequest
from google.cloud.dialogflow_v2beta1.types.conversation import GenerateStatelessSuggestionRequest
from google.cloud.dialogflow_v2beta1.types.conversation import GenerateStatelessSuggestionResponse
from google.cloud.dialogflow_v2beta1.types.conversation import GenerateStatelessSummaryRequest
from google.cloud.dialogflow_v2beta1.types.conversation import GenerateStatelessSummaryResponse
from google.cloud.dialogflow_v2beta1.types.conversation import GetConversationRequest
from google.cloud.dialogflow_v2beta1.types.conversation import ListConversationsRequest
from google.cloud.dialogflow_v2beta1.types.conversation import ListConversationsResponse
from google.cloud.dialogflow_v2beta1.types.conversation import ListMessagesRequest
from google.cloud.dialogflow_v2beta1.types.conversation import ListMessagesResponse
from google.cloud.dialogflow_v2beta1.types.conversation import SearchKnowledgeAnswer
from google.cloud.dialogflow_v2beta1.types.conversation import SearchKnowledgeRequest
from google.cloud.dialogflow_v2beta1.types.conversation import SearchKnowledgeResponse
from google.cloud.dialogflow_v2beta1.types.conversation import SuggestConversationSummaryRequest
from google.cloud.dialogflow_v2beta1.types.conversation import SuggestConversationSummaryResponse
from google.cloud.dialogflow_v2beta1.types.conversation_event import ConversationEvent
from google.cloud.dialogflow_v2beta1.types.conversation_profile import AutomatedAgentConfig
from google.cloud.dialogflow_v2beta1.types.conversation_profile import ClearSuggestionFeatureConfigOperationMetadata
from google.cloud.dialogflow_v2beta1.types.conversation_profile import ClearSuggestionFeatureConfigRequest
from google.cloud.dialogflow_v2beta1.types.conversation_profile import ConversationProfile
from google.cloud.dialogflow_v2beta1.types.conversation_profile import CreateConversationProfileRequest
from google.cloud.dialogflow_v2beta1.types.conversation_profile import DeleteConversationProfileRequest
from google.cloud.dialogflow_v2beta1.types.conversation_profile import GetConversationProfileRequest
from google.cloud.dialogflow_v2beta1.types.conversation_profile import HumanAgentAssistantConfig
from google.cloud.dialogflow_v2beta1.types.conversation_profile import HumanAgentHandoffConfig
from google.cloud.dialogflow_v2beta1.types.conversation_profile import ListConversationProfilesRequest
from google.cloud.dialogflow_v2beta1.types.conversation_profile import ListConversationProfilesResponse
from google.cloud.dialogflow_v2beta1.types.conversation_profile import LoggingConfig
from google.cloud.dialogflow_v2beta1.types.conversation_profile import NotificationConfig
from google.cloud.dialogflow_v2beta1.types.conversation_profile import SetSuggestionFeatureConfigOperationMetadata
from google.cloud.dialogflow_v2beta1.types.conversation_profile import SetSuggestionFeatureConfigRequest
from google.cloud.dialogflow_v2beta1.types.conversation_profile import UpdateConversationProfileRequest
from google.cloud.dialogflow_v2beta1.types.document import CreateDocumentRequest
from google.cloud.dialogflow_v2beta1.types.document import DeleteDocumentRequest
from google.cloud.dialogflow_v2beta1.types.document import Document
from google.cloud.dialogflow_v2beta1.types.document import ExportOperationMetadata
from google.cloud.dialogflow_v2beta1.types.document import GetDocumentRequest
from google.cloud.dialogflow_v2beta1.types.document import ImportDocumentsRequest
from google.cloud.dialogflow_v2beta1.types.document import ImportDocumentsResponse
from google.cloud.dialogflow_v2beta1.types.document import ImportDocumentTemplate
from google.cloud.dialogflow_v2beta1.types.document import KnowledgeOperationMetadata
from google.cloud.dialogflow_v2beta1.types.document import ListDocumentsRequest
from google.cloud.dialogflow_v2beta1.types.document import ListDocumentsResponse
from google.cloud.dialogflow_v2beta1.types.document import ReloadDocumentRequest
from google.cloud.dialogflow_v2beta1.types.document import UpdateDocumentRequest
from google.cloud.dialogflow_v2beta1.types.encryption_spec import EncryptionSpec
from google.cloud.dialogflow_v2beta1.types.encryption_spec import GetEncryptionSpecRequest
from google.cloud.dialogflow_v2beta1.types.encryption_spec import InitializeEncryptionSpecMetadata
from google.cloud.dialogflow_v2beta1.types.encryption_spec import InitializeEncryptionSpecRequest
from google.cloud.dialogflow_v2beta1.types.encryption_spec import InitializeEncryptionSpecResponse
from google.cloud.dialogflow_v2beta1.types.entity_type import BatchCreateEntitiesRequest
from google.cloud.dialogflow_v2beta1.types.entity_type import BatchDeleteEntitiesRequest
from google.cloud.dialogflow_v2beta1.types.entity_type import BatchDeleteEntityTypesRequest
from google.cloud.dialogflow_v2beta1.types.entity_type import BatchUpdateEntitiesRequest
from google.cloud.dialogflow_v2beta1.types.entity_type import BatchUpdateEntityTypesRequest
from google.cloud.dialogflow_v2beta1.types.entity_type import BatchUpdateEntityTypesResponse
from google.cloud.dialogflow_v2beta1.types.entity_type import CreateEntityTypeRequest
from google.cloud.dialogflow_v2beta1.types.entity_type import DeleteEntityTypeRequest
from google.cloud.dialogflow_v2beta1.types.entity_type import EntityType
from google.cloud.dialogflow_v2beta1.types.entity_type import EntityTypeBatch
from google.cloud.dialogflow_v2beta1.types.entity_type import GetEntityTypeRequest
from google.cloud.dialogflow_v2beta1.types.entity_type import ListEntityTypesRequest
from google.cloud.dialogflow_v2beta1.types.entity_type import ListEntityTypesResponse
from google.cloud.dialogflow_v2beta1.types.entity_type import UpdateEntityTypeRequest
from google.cloud.dialogflow_v2beta1.types.environment import CreateEnvironmentRequest
from google.cloud.dialogflow_v2beta1.types.environment import DeleteEnvironmentRequest
from google.cloud.dialogflow_v2beta1.types.environment import Environment
from google.cloud.dialogflow_v2beta1.types.environment import EnvironmentHistory
from google.cloud.dialogflow_v2beta1.types.environment import GetEnvironmentHistoryRequest
from google.cloud.dialogflow_v2beta1.types.environment import GetEnvironmentRequest
from google.cloud.dialogflow_v2beta1.types.environment import ListEnvironmentsRequest
from google.cloud.dialogflow_v2beta1.types.environment import ListEnvironmentsResponse
from google.cloud.dialogflow_v2beta1.types.environment import TextToSpeechSettings
from google.cloud.dialogflow_v2beta1.types.environment import UpdateEnvironmentRequest
from google.cloud.dialogflow_v2beta1.types.fulfillment import Fulfillment
from google.cloud.dialogflow_v2beta1.types.fulfillment import GetFulfillmentRequest
from google.cloud.dialogflow_v2beta1.types.fulfillment import UpdateFulfillmentRequest
from google.cloud.dialogflow_v2beta1.types.gcs import GcsDestination
from google.cloud.dialogflow_v2beta1.types.gcs import GcsSource
from google.cloud.dialogflow_v2beta1.types.gcs import GcsSources
from google.cloud.dialogflow_v2beta1.types.generator import ConversationContext
from google.cloud.dialogflow_v2beta1.types.generator import CreateGeneratorRequest
from google.cloud.dialogflow_v2beta1.types.generator import DeleteGeneratorRequest
from google.cloud.dialogflow_v2beta1.types.generator import FewShotExample
from google.cloud.dialogflow_v2beta1.types.generator import Generator
from google.cloud.dialogflow_v2beta1.types.generator import GeneratorSuggestion
from google.cloud.dialogflow_v2beta1.types.generator import GetGeneratorRequest
from google.cloud.dialogflow_v2beta1.types.generator import InferenceParameter
from google.cloud.dialogflow_v2beta1.types.generator import ListGeneratorsRequest
from google.cloud.dialogflow_v2beta1.types.generator import ListGeneratorsResponse
from google.cloud.dialogflow_v2beta1.types.generator import MessageEntry
from google.cloud.dialogflow_v2beta1.types.generator import SummarizationContext
from google.cloud.dialogflow_v2beta1.types.generator import SummarizationSection
from google.cloud.dialogflow_v2beta1.types.generator import SummarizationSectionList
from google.cloud.dialogflow_v2beta1.types.generator import SummarySuggestion
from google.cloud.dialogflow_v2beta1.types.generator import UpdateGeneratorRequest
from google.cloud.dialogflow_v2beta1.types.generator import TriggerEvent
from google.cloud.dialogflow_v2beta1.types.human_agent_assistant_event import HumanAgentAssistantEvent
from google.cloud.dialogflow_v2beta1.types.intent import BatchDeleteIntentsRequest
from google.cloud.dialogflow_v2beta1.types.intent import BatchUpdateIntentsRequest
from google.cloud.dialogflow_v2beta1.types.intent import BatchUpdateIntentsResponse
from google.cloud.dialogflow_v2beta1.types.intent import CreateIntentRequest
from google.cloud.dialogflow_v2beta1.types.intent import DeleteIntentRequest
from google.cloud.dialogflow_v2beta1.types.intent import GetIntentRequest
from google.cloud.dialogflow_v2beta1.types.intent import Intent
from google.cloud.dialogflow_v2beta1.types.intent import IntentBatch
from google.cloud.dialogflow_v2beta1.types.intent import ListIntentsRequest
from google.cloud.dialogflow_v2beta1.types.intent import ListIntentsResponse
from google.cloud.dialogflow_v2beta1.types.intent import UpdateIntentRequest
from google.cloud.dialogflow_v2beta1.types.intent import IntentView
from google.cloud.dialogflow_v2beta1.types.knowledge_base import CreateKnowledgeBaseRequest
from google.cloud.dialogflow_v2beta1.types.knowledge_base import DeleteKnowledgeBaseRequest
from google.cloud.dialogflow_v2beta1.types.knowledge_base import GetKnowledgeBaseRequest
from google.cloud.dialogflow_v2beta1.types.knowledge_base import KnowledgeBase
from google.cloud.dialogflow_v2beta1.types.knowledge_base import ListKnowledgeBasesRequest
from google.cloud.dialogflow_v2beta1.types.knowledge_base import ListKnowledgeBasesResponse
from google.cloud.dialogflow_v2beta1.types.knowledge_base import UpdateKnowledgeBaseRequest
from google.cloud.dialogflow_v2beta1.types.participant import AnalyzeContentRequest
from google.cloud.dialogflow_v2beta1.types.participant import AnalyzeContentResponse
from google.cloud.dialogflow_v2beta1.types.participant import AnnotatedMessagePart
from google.cloud.dialogflow_v2beta1.types.participant import ArticleAnswer
from google.cloud.dialogflow_v2beta1.types.participant import AssistQueryParameters
from google.cloud.dialogflow_v2beta1.types.participant import AudioInput
from google.cloud.dialogflow_v2beta1.types.participant import AutomatedAgentReply
from google.cloud.dialogflow_v2beta1.types.participant import CompileSuggestionRequest
from google.cloud.dialogflow_v2beta1.types.participant import CompileSuggestionResponse
from google.cloud.dialogflow_v2beta1.types.participant import CreateParticipantRequest
from google.cloud.dialogflow_v2beta1.types.participant import DialogflowAssistAnswer
from google.cloud.dialogflow_v2beta1.types.participant import DtmfParameters
from google.cloud.dialogflow_v2beta1.types.participant import FaqAnswer
from google.cloud.dialogflow_v2beta1.types.participant import GetParticipantRequest
from google.cloud.dialogflow_v2beta1.types.participant import InputTextConfig
from google.cloud.dialogflow_v2beta1.types.participant import IntentInput
from google.cloud.dialogflow_v2beta1.types.participant import IntentSuggestion
from google.cloud.dialogflow_v2beta1.types.participant import KnowledgeAssistAnswer
from google.cloud.dialogflow_v2beta1.types.participant import ListParticipantsRequest
from google.cloud.dialogflow_v2beta1.types.participant import ListParticipantsResponse
from google.cloud.dialogflow_v2beta1.types.participant import ListSuggestionsRequest
from google.cloud.dialogflow_v2beta1.types.participant import ListSuggestionsResponse
from google.cloud.dialogflow_v2beta1.types.participant import Message
from google.cloud.dialogflow_v2beta1.types.participant import MessageAnnotation
from google.cloud.dialogflow_v2beta1.types.participant import OutputAudio
from google.cloud.dialogflow_v2beta1.types.participant import Participant
from google.cloud.dialogflow_v2beta1.types.participant import ResponseMessage
from google.cloud.dialogflow_v2beta1.types.participant import SmartReplyAnswer
from google.cloud.dialogflow_v2beta1.types.participant import StreamingAnalyzeContentRequest
from google.cloud.dialogflow_v2beta1.types.participant import StreamingAnalyzeContentResponse
from google.cloud.dialogflow_v2beta1.types.participant import SuggestArticlesRequest
from google.cloud.dialogflow_v2beta1.types.participant import SuggestArticlesResponse
from google.cloud.dialogflow_v2beta1.types.participant import SuggestDialogflowAssistsResponse
from google.cloud.dialogflow_v2beta1.types.participant import SuggestFaqAnswersRequest
from google.cloud.dialogflow_v2beta1.types.participant import SuggestFaqAnswersResponse
from google.cloud.dialogflow_v2beta1.types.participant import Suggestion
from google.cloud.dialogflow_v2beta1.types.participant import SuggestionFeature
from google.cloud.dialogflow_v2beta1.types.participant import SuggestionInput
from google.cloud.dialogflow_v2beta1.types.participant import SuggestionResult
from google.cloud.dialogflow_v2beta1.types.participant import SuggestKnowledgeAssistRequest
from google.cloud.dialogflow_v2beta1.types.participant import SuggestKnowledgeAssistResponse
from google.cloud.dialogflow_v2beta1.types.participant import SuggestSmartRepliesRequest
from google.cloud.dialogflow_v2beta1.types.participant import SuggestSmartRepliesResponse
from google.cloud.dialogflow_v2beta1.types.participant import UpdateParticipantRequest
from google.cloud.dialogflow_v2beta1.types.session import CloudConversationDebuggingInfo
from google.cloud.dialogflow_v2beta1.types.session import DetectIntentRequest
from google.cloud.dialogflow_v2beta1.types.session import DetectIntentResponse
from google.cloud.dialogflow_v2beta1.types.session import EventInput
from google.cloud.dialogflow_v2beta1.types.session import KnowledgeAnswers
from google.cloud.dialogflow_v2beta1.types.session import QueryInput
from google.cloud.dialogflow_v2beta1.types.session import QueryParameters
from google.cloud.dialogflow_v2beta1.types.session import QueryResult
from google.cloud.dialogflow_v2beta1.types.session import Sentiment
from google.cloud.dialogflow_v2beta1.types.session import SentimentAnalysisRequestConfig
from google.cloud.dialogflow_v2beta1.types.session import SentimentAnalysisResult
from google.cloud.dialogflow_v2beta1.types.session import StreamingDetectIntentRequest
from google.cloud.dialogflow_v2beta1.types.session import StreamingDetectIntentResponse
from google.cloud.dialogflow_v2beta1.types.session import StreamingRecognitionResult
from google.cloud.dialogflow_v2beta1.types.session import TextInput
from google.cloud.dialogflow_v2beta1.types.session_entity_type import CreateSessionEntityTypeRequest
from google.cloud.dialogflow_v2beta1.types.session_entity_type import DeleteSessionEntityTypeRequest
from google.cloud.dialogflow_v2beta1.types.session_entity_type import GetSessionEntityTypeRequest
from google.cloud.dialogflow_v2beta1.types.session_entity_type import ListSessionEntityTypesRequest
from google.cloud.dialogflow_v2beta1.types.session_entity_type import ListSessionEntityTypesResponse
from google.cloud.dialogflow_v2beta1.types.session_entity_type import SessionEntityType
from google.cloud.dialogflow_v2beta1.types.session_entity_type import UpdateSessionEntityTypeRequest
from google.cloud.dialogflow_v2beta1.types.sip_trunk import Connection
from google.cloud.dialogflow_v2beta1.types.sip_trunk import CreateSipTrunkRequest
from google.cloud.dialogflow_v2beta1.types.sip_trunk import DeleteSipTrunkRequest
from google.cloud.dialogflow_v2beta1.types.sip_trunk import GetSipTrunkRequest
from google.cloud.dialogflow_v2beta1.types.sip_trunk import ListSipTrunksRequest
from google.cloud.dialogflow_v2beta1.types.sip_trunk import ListSipTrunksResponse
from google.cloud.dialogflow_v2beta1.types.sip_trunk import SipTrunk
from google.cloud.dialogflow_v2beta1.types.sip_trunk import UpdateSipTrunkRequest
from google.cloud.dialogflow_v2beta1.types.validation_result import ValidationError
from google.cloud.dialogflow_v2beta1.types.validation_result import ValidationResult
from google.cloud.dialogflow_v2beta1.types.version import CreateVersionRequest
from google.cloud.dialogflow_v2beta1.types.version import DeleteVersionRequest
from google.cloud.dialogflow_v2beta1.types.version import GetVersionRequest
from google.cloud.dialogflow_v2beta1.types.version import ListVersionsRequest
from google.cloud.dialogflow_v2beta1.types.version import ListVersionsResponse
from google.cloud.dialogflow_v2beta1.types.version import UpdateVersionRequest
from google.cloud.dialogflow_v2beta1.types.version import Version
from google.cloud.dialogflow_v2beta1.types.webhook import OriginalDetectIntentRequest
from google.cloud.dialogflow_v2beta1.types.webhook import WebhookRequest
from google.cloud.dialogflow_v2beta1.types.webhook import WebhookResponse

__all__ = ('AgentsClient',
    'AgentsAsyncClient',
    'AnswerRecordsClient',
    'AnswerRecordsAsyncClient',
    'ContextsClient',
    'ContextsAsyncClient',
    'ConversationProfilesClient',
    'ConversationProfilesAsyncClient',
    'ConversationsClient',
    'ConversationsAsyncClient',
    'DocumentsClient',
    'DocumentsAsyncClient',
    'EncryptionSpecServiceClient',
    'EncryptionSpecServiceAsyncClient',
    'EntityTypesClient',
    'EntityTypesAsyncClient',
    'EnvironmentsClient',
    'EnvironmentsAsyncClient',
    'FulfillmentsClient',
    'FulfillmentsAsyncClient',
    'GeneratorsClient',
    'GeneratorsAsyncClient',
    'IntentsClient',
    'IntentsAsyncClient',
    'KnowledgeBasesClient',
    'KnowledgeBasesAsyncClient',
    'ParticipantsClient',
    'ParticipantsAsyncClient',
    'SessionEntityTypesClient',
    'SessionEntityTypesAsyncClient',
    'SessionsClient',
    'SessionsAsyncClient',
    'SipTrunksClient',
    'SipTrunksAsyncClient',
    'VersionsClient',
    'VersionsAsyncClient',
    'Agent',
    'DeleteAgentRequest',
    'ExportAgentRequest',
    'ExportAgentResponse',
    'GetAgentRequest',
    'GetValidationResultRequest',
    'ImportAgentRequest',
    'RestoreAgentRequest',
    'SearchAgentsRequest',
    'SearchAgentsResponse',
    'SetAgentRequest',
    'SubAgent',
    'TrainAgentRequest',
    'AgentAssistantFeedback',
    'AgentAssistantRecord',
    'AnswerFeedback',
    'AnswerRecord',
    'GetAnswerRecordRequest',
    'ListAnswerRecordsRequest',
    'ListAnswerRecordsResponse',
    'UpdateAnswerRecordRequest',
    'BargeInConfig',
    'InputAudioConfig',
    'OutputAudioConfig',
    'SpeechContext',
    'SpeechToTextConfig',
    'SpeechWordInfo',
    'SynthesizeSpeechConfig',
    'TelephonyDtmfEvents',
    'VoiceSelectionParams',
    'AudioEncoding',
    'OutputAudioEncoding',
    'SpeechModelVariant',
    'SsmlVoiceGender',
    'TelephonyDtmf',
    'Context',
    'CreateContextRequest',
    'DeleteAllContextsRequest',
    'DeleteContextRequest',
    'GetContextRequest',
    'ListContextsRequest',
    'ListContextsResponse',
    'UpdateContextRequest',
    'BatchCreateMessagesRequest',
    'BatchCreateMessagesResponse',
    'CompleteConversationRequest',
    'Conversation',
    'ConversationPhoneNumber',
    'CreateConversationRequest',
    'CreateMessageRequest',
    'GenerateStatelessSuggestionRequest',
    'GenerateStatelessSuggestionResponse',
    'GenerateStatelessSummaryRequest',
    'GenerateStatelessSummaryResponse',
    'GetConversationRequest',
    'ListConversationsRequest',
    'ListConversationsResponse',
    'ListMessagesRequest',
    'ListMessagesResponse',
    'SearchKnowledgeAnswer',
    'SearchKnowledgeRequest',
    'SearchKnowledgeResponse',
    'SuggestConversationSummaryRequest',
    'SuggestConversationSummaryResponse',
    'ConversationEvent',
    'AutomatedAgentConfig',
    'ClearSuggestionFeatureConfigOperationMetadata',
    'ClearSuggestionFeatureConfigRequest',
    'ConversationProfile',
    'CreateConversationProfileRequest',
    'DeleteConversationProfileRequest',
    'GetConversationProfileRequest',
    'HumanAgentAssistantConfig',
    'HumanAgentHandoffConfig',
    'ListConversationProfilesRequest',
    'ListConversationProfilesResponse',
    'LoggingConfig',
    'NotificationConfig',
    'SetSuggestionFeatureConfigOperationMetadata',
    'SetSuggestionFeatureConfigRequest',
    'UpdateConversationProfileRequest',
    'CreateDocumentRequest',
    'DeleteDocumentRequest',
    'Document',
    'ExportOperationMetadata',
    'GetDocumentRequest',
    'ImportDocumentsRequest',
    'ImportDocumentsResponse',
    'ImportDocumentTemplate',
    'KnowledgeOperationMetadata',
    'ListDocumentsRequest',
    'ListDocumentsResponse',
    'ReloadDocumentRequest',
    'UpdateDocumentRequest',
    'EncryptionSpec',
    'GetEncryptionSpecRequest',
    'InitializeEncryptionSpecMetadata',
    'InitializeEncryptionSpecRequest',
    'InitializeEncryptionSpecResponse',
    'BatchCreateEntitiesRequest',
    'BatchDeleteEntitiesRequest',
    'BatchDeleteEntityTypesRequest',
    'BatchUpdateEntitiesRequest',
    'BatchUpdateEntityTypesRequest',
    'BatchUpdateEntityTypesResponse',
    'CreateEntityTypeRequest',
    'DeleteEntityTypeRequest',
    'EntityType',
    'EntityTypeBatch',
    'GetEntityTypeRequest',
    'ListEntityTypesRequest',
    'ListEntityTypesResponse',
    'UpdateEntityTypeRequest',
    'CreateEnvironmentRequest',
    'DeleteEnvironmentRequest',
    'Environment',
    'EnvironmentHistory',
    'GetEnvironmentHistoryRequest',
    'GetEnvironmentRequest',
    'ListEnvironmentsRequest',
    'ListEnvironmentsResponse',
    'TextToSpeechSettings',
    'UpdateEnvironmentRequest',
    'Fulfillment',
    'GetFulfillmentRequest',
    'UpdateFulfillmentRequest',
    'GcsDestination',
    'GcsSource',
    'GcsSources',
    'ConversationContext',
    'CreateGeneratorRequest',
    'DeleteGeneratorRequest',
    'FewShotExample',
    'Generator',
    'GeneratorSuggestion',
    'GetGeneratorRequest',
    'InferenceParameter',
    'ListGeneratorsRequest',
    'ListGeneratorsResponse',
    'MessageEntry',
    'SummarizationContext',
    'SummarizationSection',
    'SummarizationSectionList',
    'SummarySuggestion',
    'UpdateGeneratorRequest',
    'TriggerEvent',
    'HumanAgentAssistantEvent',
    'BatchDeleteIntentsRequest',
    'BatchUpdateIntentsRequest',
    'BatchUpdateIntentsResponse',
    'CreateIntentRequest',
    'DeleteIntentRequest',
    'GetIntentRequest',
    'Intent',
    'IntentBatch',
    'ListIntentsRequest',
    'ListIntentsResponse',
    'UpdateIntentRequest',
    'IntentView',
    'CreateKnowledgeBaseRequest',
    'DeleteKnowledgeBaseRequest',
    'GetKnowledgeBaseRequest',
    'KnowledgeBase',
    'ListKnowledgeBasesRequest',
    'ListKnowledgeBasesResponse',
    'UpdateKnowledgeBaseRequest',
    'AnalyzeContentRequest',
    'AnalyzeContentResponse',
    'AnnotatedMessagePart',
    'ArticleAnswer',
    'AssistQueryParameters',
    'AudioInput',
    'AutomatedAgentReply',
    'CompileSuggestionRequest',
    'CompileSuggestionResponse',
    'CreateParticipantRequest',
    'DialogflowAssistAnswer',
    'DtmfParameters',
    'FaqAnswer',
    'GetParticipantRequest',
    'InputTextConfig',
    'IntentInput',
    'IntentSuggestion',
    'KnowledgeAssistAnswer',
    'ListParticipantsRequest',
    'ListParticipantsResponse',
    'ListSuggestionsRequest',
    'ListSuggestionsResponse',
    'Message',
    'MessageAnnotation',
    'OutputAudio',
    'Participant',
    'ResponseMessage',
    'SmartReplyAnswer',
    'StreamingAnalyzeContentRequest',
    'StreamingAnalyzeContentResponse',
    'SuggestArticlesRequest',
    'SuggestArticlesResponse',
    'SuggestDialogflowAssistsResponse',
    'SuggestFaqAnswersRequest',
    'SuggestFaqAnswersResponse',
    'Suggestion',
    'SuggestionFeature',
    'SuggestionInput',
    'SuggestionResult',
    'SuggestKnowledgeAssistRequest',
    'SuggestKnowledgeAssistResponse',
    'SuggestSmartRepliesRequest',
    'SuggestSmartRepliesResponse',
    'UpdateParticipantRequest',
    'CloudConversationDebuggingInfo',
    'DetectIntentRequest',
    'DetectIntentResponse',
    'EventInput',
    'KnowledgeAnswers',
    'QueryInput',
    'QueryParameters',
    'QueryResult',
    'Sentiment',
    'SentimentAnalysisRequestConfig',
    'SentimentAnalysisResult',
    'StreamingDetectIntentRequest',
    'StreamingDetectIntentResponse',
    'StreamingRecognitionResult',
    'TextInput',
    'CreateSessionEntityTypeRequest',
    'DeleteSessionEntityTypeRequest',
    'GetSessionEntityTypeRequest',
    'ListSessionEntityTypesRequest',
    'ListSessionEntityTypesResponse',
    'SessionEntityType',
    'UpdateSessionEntityTypeRequest',
    'Connection',
    'CreateSipTrunkRequest',
    'DeleteSipTrunkRequest',
    'GetSipTrunkRequest',
    'ListSipTrunksRequest',
    'ListSipTrunksResponse',
    'SipTrunk',
    'UpdateSipTrunkRequest',
    'ValidationError',
    'ValidationResult',
    'CreateVersionRequest',
    'DeleteVersionRequest',
    'GetVersionRequest',
    'ListVersionsRequest',
    'ListVersionsResponse',
    'UpdateVersionRequest',
    'Version',
    'OriginalDetectIntentRequest',
    'WebhookRequest',
    'WebhookResponse',
)
