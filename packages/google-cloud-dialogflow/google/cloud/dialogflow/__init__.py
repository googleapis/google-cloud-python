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

from google.cloud.dialogflow_v2.services.agents.client import AgentsClient
from google.cloud.dialogflow_v2.services.agents.async_client import AgentsAsyncClient
from google.cloud.dialogflow_v2.services.answer_records.client import (
    AnswerRecordsClient,
)
from google.cloud.dialogflow_v2.services.answer_records.async_client import (
    AnswerRecordsAsyncClient,
)
from google.cloud.dialogflow_v2.services.contexts.client import ContextsClient
from google.cloud.dialogflow_v2.services.contexts.async_client import (
    ContextsAsyncClient,
)
from google.cloud.dialogflow_v2.services.conversation_profiles.client import (
    ConversationProfilesClient,
)
from google.cloud.dialogflow_v2.services.conversation_profiles.async_client import (
    ConversationProfilesAsyncClient,
)
from google.cloud.dialogflow_v2.services.conversations.client import ConversationsClient
from google.cloud.dialogflow_v2.services.conversations.async_client import (
    ConversationsAsyncClient,
)
from google.cloud.dialogflow_v2.services.documents.client import DocumentsClient
from google.cloud.dialogflow_v2.services.documents.async_client import (
    DocumentsAsyncClient,
)
from google.cloud.dialogflow_v2.services.entity_types.client import EntityTypesClient
from google.cloud.dialogflow_v2.services.entity_types.async_client import (
    EntityTypesAsyncClient,
)
from google.cloud.dialogflow_v2.services.environments.client import EnvironmentsClient
from google.cloud.dialogflow_v2.services.environments.async_client import (
    EnvironmentsAsyncClient,
)
from google.cloud.dialogflow_v2.services.fulfillments.client import FulfillmentsClient
from google.cloud.dialogflow_v2.services.fulfillments.async_client import (
    FulfillmentsAsyncClient,
)
from google.cloud.dialogflow_v2.services.intents.client import IntentsClient
from google.cloud.dialogflow_v2.services.intents.async_client import IntentsAsyncClient
from google.cloud.dialogflow_v2.services.knowledge_bases.client import (
    KnowledgeBasesClient,
)
from google.cloud.dialogflow_v2.services.knowledge_bases.async_client import (
    KnowledgeBasesAsyncClient,
)
from google.cloud.dialogflow_v2.services.participants.client import ParticipantsClient
from google.cloud.dialogflow_v2.services.participants.async_client import (
    ParticipantsAsyncClient,
)
from google.cloud.dialogflow_v2.services.session_entity_types.client import (
    SessionEntityTypesClient,
)
from google.cloud.dialogflow_v2.services.session_entity_types.async_client import (
    SessionEntityTypesAsyncClient,
)
from google.cloud.dialogflow_v2.services.sessions.client import SessionsClient
from google.cloud.dialogflow_v2.services.sessions.async_client import (
    SessionsAsyncClient,
)
from google.cloud.dialogflow_v2.services.versions.client import VersionsClient
from google.cloud.dialogflow_v2.services.versions.async_client import (
    VersionsAsyncClient,
)

from google.cloud.dialogflow_v2.types.agent import Agent
from google.cloud.dialogflow_v2.types.agent import DeleteAgentRequest
from google.cloud.dialogflow_v2.types.agent import ExportAgentRequest
from google.cloud.dialogflow_v2.types.agent import ExportAgentResponse
from google.cloud.dialogflow_v2.types.agent import GetAgentRequest
from google.cloud.dialogflow_v2.types.agent import GetValidationResultRequest
from google.cloud.dialogflow_v2.types.agent import ImportAgentRequest
from google.cloud.dialogflow_v2.types.agent import RestoreAgentRequest
from google.cloud.dialogflow_v2.types.agent import SearchAgentsRequest
from google.cloud.dialogflow_v2.types.agent import SearchAgentsResponse
from google.cloud.dialogflow_v2.types.agent import SetAgentRequest
from google.cloud.dialogflow_v2.types.agent import TrainAgentRequest
from google.cloud.dialogflow_v2.types.answer_record import AgentAssistantFeedback
from google.cloud.dialogflow_v2.types.answer_record import AgentAssistantRecord
from google.cloud.dialogflow_v2.types.answer_record import AnswerFeedback
from google.cloud.dialogflow_v2.types.answer_record import AnswerRecord
from google.cloud.dialogflow_v2.types.answer_record import ListAnswerRecordsRequest
from google.cloud.dialogflow_v2.types.answer_record import ListAnswerRecordsResponse
from google.cloud.dialogflow_v2.types.answer_record import UpdateAnswerRecordRequest
from google.cloud.dialogflow_v2.types.audio_config import InputAudioConfig
from google.cloud.dialogflow_v2.types.audio_config import OutputAudioConfig
from google.cloud.dialogflow_v2.types.audio_config import SpeechContext
from google.cloud.dialogflow_v2.types.audio_config import SpeechToTextConfig
from google.cloud.dialogflow_v2.types.audio_config import SpeechWordInfo
from google.cloud.dialogflow_v2.types.audio_config import SynthesizeSpeechConfig
from google.cloud.dialogflow_v2.types.audio_config import VoiceSelectionParams
from google.cloud.dialogflow_v2.types.audio_config import AudioEncoding
from google.cloud.dialogflow_v2.types.audio_config import OutputAudioEncoding
from google.cloud.dialogflow_v2.types.audio_config import SpeechModelVariant
from google.cloud.dialogflow_v2.types.audio_config import SsmlVoiceGender
from google.cloud.dialogflow_v2.types.context import Context
from google.cloud.dialogflow_v2.types.context import CreateContextRequest
from google.cloud.dialogflow_v2.types.context import DeleteAllContextsRequest
from google.cloud.dialogflow_v2.types.context import DeleteContextRequest
from google.cloud.dialogflow_v2.types.context import GetContextRequest
from google.cloud.dialogflow_v2.types.context import ListContextsRequest
from google.cloud.dialogflow_v2.types.context import ListContextsResponse
from google.cloud.dialogflow_v2.types.context import UpdateContextRequest
from google.cloud.dialogflow_v2.types.conversation import CompleteConversationRequest
from google.cloud.dialogflow_v2.types.conversation import Conversation
from google.cloud.dialogflow_v2.types.conversation import ConversationPhoneNumber
from google.cloud.dialogflow_v2.types.conversation import CreateConversationRequest
from google.cloud.dialogflow_v2.types.conversation import GetConversationRequest
from google.cloud.dialogflow_v2.types.conversation import ListConversationsRequest
from google.cloud.dialogflow_v2.types.conversation import ListConversationsResponse
from google.cloud.dialogflow_v2.types.conversation import ListMessagesRequest
from google.cloud.dialogflow_v2.types.conversation import ListMessagesResponse
from google.cloud.dialogflow_v2.types.conversation_event import ConversationEvent
from google.cloud.dialogflow_v2.types.conversation_profile import AutomatedAgentConfig
from google.cloud.dialogflow_v2.types.conversation_profile import ConversationProfile
from google.cloud.dialogflow_v2.types.conversation_profile import (
    CreateConversationProfileRequest,
)
from google.cloud.dialogflow_v2.types.conversation_profile import (
    DeleteConversationProfileRequest,
)
from google.cloud.dialogflow_v2.types.conversation_profile import (
    GetConversationProfileRequest,
)
from google.cloud.dialogflow_v2.types.conversation_profile import (
    HumanAgentAssistantConfig,
)
from google.cloud.dialogflow_v2.types.conversation_profile import (
    HumanAgentHandoffConfig,
)
from google.cloud.dialogflow_v2.types.conversation_profile import (
    ListConversationProfilesRequest,
)
from google.cloud.dialogflow_v2.types.conversation_profile import (
    ListConversationProfilesResponse,
)
from google.cloud.dialogflow_v2.types.conversation_profile import LoggingConfig
from google.cloud.dialogflow_v2.types.conversation_profile import NotificationConfig
from google.cloud.dialogflow_v2.types.conversation_profile import SuggestionFeature
from google.cloud.dialogflow_v2.types.conversation_profile import (
    UpdateConversationProfileRequest,
)
from google.cloud.dialogflow_v2.types.document import CreateDocumentRequest
from google.cloud.dialogflow_v2.types.document import DeleteDocumentRequest
from google.cloud.dialogflow_v2.types.document import Document
from google.cloud.dialogflow_v2.types.document import GetDocumentRequest
from google.cloud.dialogflow_v2.types.document import KnowledgeOperationMetadata
from google.cloud.dialogflow_v2.types.document import ListDocumentsRequest
from google.cloud.dialogflow_v2.types.document import ListDocumentsResponse
from google.cloud.dialogflow_v2.types.document import ReloadDocumentRequest
from google.cloud.dialogflow_v2.types.document import UpdateDocumentRequest
from google.cloud.dialogflow_v2.types.entity_type import BatchCreateEntitiesRequest
from google.cloud.dialogflow_v2.types.entity_type import BatchDeleteEntitiesRequest
from google.cloud.dialogflow_v2.types.entity_type import BatchDeleteEntityTypesRequest
from google.cloud.dialogflow_v2.types.entity_type import BatchUpdateEntitiesRequest
from google.cloud.dialogflow_v2.types.entity_type import BatchUpdateEntityTypesRequest
from google.cloud.dialogflow_v2.types.entity_type import BatchUpdateEntityTypesResponse
from google.cloud.dialogflow_v2.types.entity_type import CreateEntityTypeRequest
from google.cloud.dialogflow_v2.types.entity_type import DeleteEntityTypeRequest
from google.cloud.dialogflow_v2.types.entity_type import EntityType
from google.cloud.dialogflow_v2.types.entity_type import EntityTypeBatch
from google.cloud.dialogflow_v2.types.entity_type import GetEntityTypeRequest
from google.cloud.dialogflow_v2.types.entity_type import ListEntityTypesRequest
from google.cloud.dialogflow_v2.types.entity_type import ListEntityTypesResponse
from google.cloud.dialogflow_v2.types.entity_type import UpdateEntityTypeRequest
from google.cloud.dialogflow_v2.types.environment import CreateEnvironmentRequest
from google.cloud.dialogflow_v2.types.environment import DeleteEnvironmentRequest
from google.cloud.dialogflow_v2.types.environment import Environment
from google.cloud.dialogflow_v2.types.environment import EnvironmentHistory
from google.cloud.dialogflow_v2.types.environment import GetEnvironmentHistoryRequest
from google.cloud.dialogflow_v2.types.environment import GetEnvironmentRequest
from google.cloud.dialogflow_v2.types.environment import ListEnvironmentsRequest
from google.cloud.dialogflow_v2.types.environment import ListEnvironmentsResponse
from google.cloud.dialogflow_v2.types.environment import TextToSpeechSettings
from google.cloud.dialogflow_v2.types.environment import UpdateEnvironmentRequest
from google.cloud.dialogflow_v2.types.fulfillment import Fulfillment
from google.cloud.dialogflow_v2.types.fulfillment import GetFulfillmentRequest
from google.cloud.dialogflow_v2.types.fulfillment import UpdateFulfillmentRequest
from google.cloud.dialogflow_v2.types.human_agent_assistant_event import (
    HumanAgentAssistantEvent,
)
from google.cloud.dialogflow_v2.types.intent import BatchDeleteIntentsRequest
from google.cloud.dialogflow_v2.types.intent import BatchUpdateIntentsRequest
from google.cloud.dialogflow_v2.types.intent import BatchUpdateIntentsResponse
from google.cloud.dialogflow_v2.types.intent import CreateIntentRequest
from google.cloud.dialogflow_v2.types.intent import DeleteIntentRequest
from google.cloud.dialogflow_v2.types.intent import GetIntentRequest
from google.cloud.dialogflow_v2.types.intent import Intent
from google.cloud.dialogflow_v2.types.intent import IntentBatch
from google.cloud.dialogflow_v2.types.intent import ListIntentsRequest
from google.cloud.dialogflow_v2.types.intent import ListIntentsResponse
from google.cloud.dialogflow_v2.types.intent import UpdateIntentRequest
from google.cloud.dialogflow_v2.types.intent import IntentView
from google.cloud.dialogflow_v2.types.knowledge_base import CreateKnowledgeBaseRequest
from google.cloud.dialogflow_v2.types.knowledge_base import DeleteKnowledgeBaseRequest
from google.cloud.dialogflow_v2.types.knowledge_base import GetKnowledgeBaseRequest
from google.cloud.dialogflow_v2.types.knowledge_base import KnowledgeBase
from google.cloud.dialogflow_v2.types.knowledge_base import ListKnowledgeBasesRequest
from google.cloud.dialogflow_v2.types.knowledge_base import ListKnowledgeBasesResponse
from google.cloud.dialogflow_v2.types.knowledge_base import UpdateKnowledgeBaseRequest
from google.cloud.dialogflow_v2.types.participant import AnalyzeContentRequest
from google.cloud.dialogflow_v2.types.participant import AnalyzeContentResponse
from google.cloud.dialogflow_v2.types.participant import AnnotatedMessagePart
from google.cloud.dialogflow_v2.types.participant import ArticleAnswer
from google.cloud.dialogflow_v2.types.participant import AutomatedAgentReply
from google.cloud.dialogflow_v2.types.participant import CreateParticipantRequest
from google.cloud.dialogflow_v2.types.participant import DtmfParameters
from google.cloud.dialogflow_v2.types.participant import FaqAnswer
from google.cloud.dialogflow_v2.types.participant import GetParticipantRequest
from google.cloud.dialogflow_v2.types.participant import ListParticipantsRequest
from google.cloud.dialogflow_v2.types.participant import ListParticipantsResponse
from google.cloud.dialogflow_v2.types.participant import Message
from google.cloud.dialogflow_v2.types.participant import MessageAnnotation
from google.cloud.dialogflow_v2.types.participant import OutputAudio
from google.cloud.dialogflow_v2.types.participant import Participant
from google.cloud.dialogflow_v2.types.participant import SuggestArticlesRequest
from google.cloud.dialogflow_v2.types.participant import SuggestArticlesResponse
from google.cloud.dialogflow_v2.types.participant import SuggestFaqAnswersRequest
from google.cloud.dialogflow_v2.types.participant import SuggestFaqAnswersResponse
from google.cloud.dialogflow_v2.types.participant import SuggestionResult
from google.cloud.dialogflow_v2.types.participant import UpdateParticipantRequest
from google.cloud.dialogflow_v2.types.session import DetectIntentRequest
from google.cloud.dialogflow_v2.types.session import DetectIntentResponse
from google.cloud.dialogflow_v2.types.session import EventInput
from google.cloud.dialogflow_v2.types.session import QueryInput
from google.cloud.dialogflow_v2.types.session import QueryParameters
from google.cloud.dialogflow_v2.types.session import QueryResult
from google.cloud.dialogflow_v2.types.session import Sentiment
from google.cloud.dialogflow_v2.types.session import SentimentAnalysisRequestConfig
from google.cloud.dialogflow_v2.types.session import SentimentAnalysisResult
from google.cloud.dialogflow_v2.types.session import StreamingDetectIntentRequest
from google.cloud.dialogflow_v2.types.session import StreamingDetectIntentResponse
from google.cloud.dialogflow_v2.types.session import StreamingRecognitionResult
from google.cloud.dialogflow_v2.types.session import TextInput
from google.cloud.dialogflow_v2.types.session_entity_type import (
    CreateSessionEntityTypeRequest,
)
from google.cloud.dialogflow_v2.types.session_entity_type import (
    DeleteSessionEntityTypeRequest,
)
from google.cloud.dialogflow_v2.types.session_entity_type import (
    GetSessionEntityTypeRequest,
)
from google.cloud.dialogflow_v2.types.session_entity_type import (
    ListSessionEntityTypesRequest,
)
from google.cloud.dialogflow_v2.types.session_entity_type import (
    ListSessionEntityTypesResponse,
)
from google.cloud.dialogflow_v2.types.session_entity_type import SessionEntityType
from google.cloud.dialogflow_v2.types.session_entity_type import (
    UpdateSessionEntityTypeRequest,
)
from google.cloud.dialogflow_v2.types.validation_result import ValidationError
from google.cloud.dialogflow_v2.types.validation_result import ValidationResult
from google.cloud.dialogflow_v2.types.version import CreateVersionRequest
from google.cloud.dialogflow_v2.types.version import DeleteVersionRequest
from google.cloud.dialogflow_v2.types.version import GetVersionRequest
from google.cloud.dialogflow_v2.types.version import ListVersionsRequest
from google.cloud.dialogflow_v2.types.version import ListVersionsResponse
from google.cloud.dialogflow_v2.types.version import UpdateVersionRequest
from google.cloud.dialogflow_v2.types.version import Version
from google.cloud.dialogflow_v2.types.webhook import OriginalDetectIntentRequest
from google.cloud.dialogflow_v2.types.webhook import WebhookRequest
from google.cloud.dialogflow_v2.types.webhook import WebhookResponse

__all__ = (
    "AgentsClient",
    "AgentsAsyncClient",
    "AnswerRecordsClient",
    "AnswerRecordsAsyncClient",
    "ContextsClient",
    "ContextsAsyncClient",
    "ConversationProfilesClient",
    "ConversationProfilesAsyncClient",
    "ConversationsClient",
    "ConversationsAsyncClient",
    "DocumentsClient",
    "DocumentsAsyncClient",
    "EntityTypesClient",
    "EntityTypesAsyncClient",
    "EnvironmentsClient",
    "EnvironmentsAsyncClient",
    "FulfillmentsClient",
    "FulfillmentsAsyncClient",
    "IntentsClient",
    "IntentsAsyncClient",
    "KnowledgeBasesClient",
    "KnowledgeBasesAsyncClient",
    "ParticipantsClient",
    "ParticipantsAsyncClient",
    "SessionEntityTypesClient",
    "SessionEntityTypesAsyncClient",
    "SessionsClient",
    "SessionsAsyncClient",
    "VersionsClient",
    "VersionsAsyncClient",
    "Agent",
    "DeleteAgentRequest",
    "ExportAgentRequest",
    "ExportAgentResponse",
    "GetAgentRequest",
    "GetValidationResultRequest",
    "ImportAgentRequest",
    "RestoreAgentRequest",
    "SearchAgentsRequest",
    "SearchAgentsResponse",
    "SetAgentRequest",
    "TrainAgentRequest",
    "AgentAssistantFeedback",
    "AgentAssistantRecord",
    "AnswerFeedback",
    "AnswerRecord",
    "ListAnswerRecordsRequest",
    "ListAnswerRecordsResponse",
    "UpdateAnswerRecordRequest",
    "InputAudioConfig",
    "OutputAudioConfig",
    "SpeechContext",
    "SpeechToTextConfig",
    "SpeechWordInfo",
    "SynthesizeSpeechConfig",
    "VoiceSelectionParams",
    "AudioEncoding",
    "OutputAudioEncoding",
    "SpeechModelVariant",
    "SsmlVoiceGender",
    "Context",
    "CreateContextRequest",
    "DeleteAllContextsRequest",
    "DeleteContextRequest",
    "GetContextRequest",
    "ListContextsRequest",
    "ListContextsResponse",
    "UpdateContextRequest",
    "CompleteConversationRequest",
    "Conversation",
    "ConversationPhoneNumber",
    "CreateConversationRequest",
    "GetConversationRequest",
    "ListConversationsRequest",
    "ListConversationsResponse",
    "ListMessagesRequest",
    "ListMessagesResponse",
    "ConversationEvent",
    "AutomatedAgentConfig",
    "ConversationProfile",
    "CreateConversationProfileRequest",
    "DeleteConversationProfileRequest",
    "GetConversationProfileRequest",
    "HumanAgentAssistantConfig",
    "HumanAgentHandoffConfig",
    "ListConversationProfilesRequest",
    "ListConversationProfilesResponse",
    "LoggingConfig",
    "NotificationConfig",
    "SuggestionFeature",
    "UpdateConversationProfileRequest",
    "CreateDocumentRequest",
    "DeleteDocumentRequest",
    "Document",
    "GetDocumentRequest",
    "KnowledgeOperationMetadata",
    "ListDocumentsRequest",
    "ListDocumentsResponse",
    "ReloadDocumentRequest",
    "UpdateDocumentRequest",
    "BatchCreateEntitiesRequest",
    "BatchDeleteEntitiesRequest",
    "BatchDeleteEntityTypesRequest",
    "BatchUpdateEntitiesRequest",
    "BatchUpdateEntityTypesRequest",
    "BatchUpdateEntityTypesResponse",
    "CreateEntityTypeRequest",
    "DeleteEntityTypeRequest",
    "EntityType",
    "EntityTypeBatch",
    "GetEntityTypeRequest",
    "ListEntityTypesRequest",
    "ListEntityTypesResponse",
    "UpdateEntityTypeRequest",
    "CreateEnvironmentRequest",
    "DeleteEnvironmentRequest",
    "Environment",
    "EnvironmentHistory",
    "GetEnvironmentHistoryRequest",
    "GetEnvironmentRequest",
    "ListEnvironmentsRequest",
    "ListEnvironmentsResponse",
    "TextToSpeechSettings",
    "UpdateEnvironmentRequest",
    "Fulfillment",
    "GetFulfillmentRequest",
    "UpdateFulfillmentRequest",
    "HumanAgentAssistantEvent",
    "BatchDeleteIntentsRequest",
    "BatchUpdateIntentsRequest",
    "BatchUpdateIntentsResponse",
    "CreateIntentRequest",
    "DeleteIntentRequest",
    "GetIntentRequest",
    "Intent",
    "IntentBatch",
    "ListIntentsRequest",
    "ListIntentsResponse",
    "UpdateIntentRequest",
    "IntentView",
    "CreateKnowledgeBaseRequest",
    "DeleteKnowledgeBaseRequest",
    "GetKnowledgeBaseRequest",
    "KnowledgeBase",
    "ListKnowledgeBasesRequest",
    "ListKnowledgeBasesResponse",
    "UpdateKnowledgeBaseRequest",
    "AnalyzeContentRequest",
    "AnalyzeContentResponse",
    "AnnotatedMessagePart",
    "ArticleAnswer",
    "AutomatedAgentReply",
    "CreateParticipantRequest",
    "DtmfParameters",
    "FaqAnswer",
    "GetParticipantRequest",
    "ListParticipantsRequest",
    "ListParticipantsResponse",
    "Message",
    "MessageAnnotation",
    "OutputAudio",
    "Participant",
    "SuggestArticlesRequest",
    "SuggestArticlesResponse",
    "SuggestFaqAnswersRequest",
    "SuggestFaqAnswersResponse",
    "SuggestionResult",
    "UpdateParticipantRequest",
    "DetectIntentRequest",
    "DetectIntentResponse",
    "EventInput",
    "QueryInput",
    "QueryParameters",
    "QueryResult",
    "Sentiment",
    "SentimentAnalysisRequestConfig",
    "SentimentAnalysisResult",
    "StreamingDetectIntentRequest",
    "StreamingDetectIntentResponse",
    "StreamingRecognitionResult",
    "TextInput",
    "CreateSessionEntityTypeRequest",
    "DeleteSessionEntityTypeRequest",
    "GetSessionEntityTypeRequest",
    "ListSessionEntityTypesRequest",
    "ListSessionEntityTypesResponse",
    "SessionEntityType",
    "UpdateSessionEntityTypeRequest",
    "ValidationError",
    "ValidationResult",
    "CreateVersionRequest",
    "DeleteVersionRequest",
    "GetVersionRequest",
    "ListVersionsRequest",
    "ListVersionsResponse",
    "UpdateVersionRequest",
    "Version",
    "OriginalDetectIntentRequest",
    "WebhookRequest",
    "WebhookResponse",
)
