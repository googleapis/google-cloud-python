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

from google.cloud.dialogflow_v2.services.agents.async_client import AgentsAsyncClient
from google.cloud.dialogflow_v2.services.agents.client import AgentsClient
from google.cloud.dialogflow_v2.services.answer_records.async_client import (
    AnswerRecordsAsyncClient,
)
from google.cloud.dialogflow_v2.services.answer_records.client import (
    AnswerRecordsClient,
)
from google.cloud.dialogflow_v2.services.contexts.async_client import (
    ContextsAsyncClient,
)
from google.cloud.dialogflow_v2.services.contexts.client import ContextsClient
from google.cloud.dialogflow_v2.services.conversation_profiles.async_client import (
    ConversationProfilesAsyncClient,
)
from google.cloud.dialogflow_v2.services.conversation_profiles.client import (
    ConversationProfilesClient,
)
from google.cloud.dialogflow_v2.services.conversations.async_client import (
    ConversationsAsyncClient,
)
from google.cloud.dialogflow_v2.services.conversations.client import ConversationsClient
from google.cloud.dialogflow_v2.services.documents.async_client import (
    DocumentsAsyncClient,
)
from google.cloud.dialogflow_v2.services.documents.client import DocumentsClient
from google.cloud.dialogflow_v2.services.entity_types.async_client import (
    EntityTypesAsyncClient,
)
from google.cloud.dialogflow_v2.services.entity_types.client import EntityTypesClient
from google.cloud.dialogflow_v2.services.environments.async_client import (
    EnvironmentsAsyncClient,
)
from google.cloud.dialogflow_v2.services.environments.client import EnvironmentsClient
from google.cloud.dialogflow_v2.services.intents.async_client import IntentsAsyncClient
from google.cloud.dialogflow_v2.services.intents.client import IntentsClient
from google.cloud.dialogflow_v2.services.knowledge_bases.async_client import (
    KnowledgeBasesAsyncClient,
)
from google.cloud.dialogflow_v2.services.knowledge_bases.client import (
    KnowledgeBasesClient,
)
from google.cloud.dialogflow_v2.services.participants.async_client import (
    ParticipantsAsyncClient,
)
from google.cloud.dialogflow_v2.services.participants.client import ParticipantsClient
from google.cloud.dialogflow_v2.services.session_entity_types.async_client import (
    SessionEntityTypesAsyncClient,
)
from google.cloud.dialogflow_v2.services.session_entity_types.client import (
    SessionEntityTypesClient,
)
from google.cloud.dialogflow_v2.services.sessions.async_client import (
    SessionsAsyncClient,
)
from google.cloud.dialogflow_v2.services.sessions.client import SessionsClient
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
from google.cloud.dialogflow_v2.types.audio_config import AudioEncoding
from google.cloud.dialogflow_v2.types.audio_config import InputAudioConfig
from google.cloud.dialogflow_v2.types.audio_config import OutputAudioConfig
from google.cloud.dialogflow_v2.types.audio_config import OutputAudioEncoding
from google.cloud.dialogflow_v2.types.audio_config import SpeechContext
from google.cloud.dialogflow_v2.types.audio_config import SpeechModelVariant
from google.cloud.dialogflow_v2.types.audio_config import SpeechToTextConfig
from google.cloud.dialogflow_v2.types.audio_config import SpeechWordInfo
from google.cloud.dialogflow_v2.types.audio_config import SsmlVoiceGender
from google.cloud.dialogflow_v2.types.audio_config import SynthesizeSpeechConfig
from google.cloud.dialogflow_v2.types.audio_config import VoiceSelectionParams
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
from google.cloud.dialogflow_v2.types.environment import Environment
from google.cloud.dialogflow_v2.types.environment import ListEnvironmentsRequest
from google.cloud.dialogflow_v2.types.environment import ListEnvironmentsResponse
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
from google.cloud.dialogflow_v2.types.intent import IntentView
from google.cloud.dialogflow_v2.types.intent import ListIntentsRequest
from google.cloud.dialogflow_v2.types.intent import ListIntentsResponse
from google.cloud.dialogflow_v2.types.intent import UpdateIntentRequest
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
from google.cloud.dialogflow_v2.types.webhook import OriginalDetectIntentRequest
from google.cloud.dialogflow_v2.types.webhook import WebhookRequest
from google.cloud.dialogflow_v2.types.webhook import WebhookResponse

__all__ = (
    "Agent",
    "AgentAssistantFeedback",
    "AgentAssistantRecord",
    "AgentsAsyncClient",
    "AgentsClient",
    "AnalyzeContentRequest",
    "AnalyzeContentResponse",
    "AnnotatedMessagePart",
    "AnswerFeedback",
    "AnswerRecord",
    "AnswerRecordsAsyncClient",
    "AnswerRecordsClient",
    "ArticleAnswer",
    "AudioEncoding",
    "AutomatedAgentConfig",
    "AutomatedAgentReply",
    "BatchCreateEntitiesRequest",
    "BatchDeleteEntitiesRequest",
    "BatchDeleteEntityTypesRequest",
    "BatchDeleteIntentsRequest",
    "BatchUpdateEntitiesRequest",
    "BatchUpdateEntityTypesRequest",
    "BatchUpdateEntityTypesResponse",
    "BatchUpdateIntentsRequest",
    "BatchUpdateIntentsResponse",
    "CompleteConversationRequest",
    "Context",
    "ContextsAsyncClient",
    "ContextsClient",
    "Conversation",
    "ConversationEvent",
    "ConversationPhoneNumber",
    "ConversationProfile",
    "ConversationProfilesAsyncClient",
    "ConversationProfilesClient",
    "ConversationsAsyncClient",
    "ConversationsClient",
    "CreateContextRequest",
    "CreateConversationProfileRequest",
    "CreateConversationRequest",
    "CreateDocumentRequest",
    "CreateEntityTypeRequest",
    "CreateIntentRequest",
    "CreateKnowledgeBaseRequest",
    "CreateParticipantRequest",
    "CreateSessionEntityTypeRequest",
    "DeleteAgentRequest",
    "DeleteAllContextsRequest",
    "DeleteContextRequest",
    "DeleteConversationProfileRequest",
    "DeleteDocumentRequest",
    "DeleteEntityTypeRequest",
    "DeleteIntentRequest",
    "DeleteKnowledgeBaseRequest",
    "DeleteSessionEntityTypeRequest",
    "DetectIntentRequest",
    "DetectIntentResponse",
    "Document",
    "DocumentsAsyncClient",
    "DocumentsClient",
    "DtmfParameters",
    "EntityType",
    "EntityTypeBatch",
    "EntityTypesAsyncClient",
    "EntityTypesClient",
    "Environment",
    "EnvironmentsAsyncClient",
    "EnvironmentsClient",
    "EventInput",
    "ExportAgentRequest",
    "ExportAgentResponse",
    "FaqAnswer",
    "GetAgentRequest",
    "GetContextRequest",
    "GetConversationProfileRequest",
    "GetConversationRequest",
    "GetDocumentRequest",
    "GetEntityTypeRequest",
    "GetIntentRequest",
    "GetKnowledgeBaseRequest",
    "GetParticipantRequest",
    "GetSessionEntityTypeRequest",
    "GetValidationResultRequest",
    "HumanAgentAssistantConfig",
    "HumanAgentAssistantEvent",
    "HumanAgentHandoffConfig",
    "ImportAgentRequest",
    "InputAudioConfig",
    "Intent",
    "IntentBatch",
    "IntentView",
    "IntentsAsyncClient",
    "IntentsClient",
    "KnowledgeBase",
    "KnowledgeBasesAsyncClient",
    "KnowledgeBasesClient",
    "KnowledgeOperationMetadata",
    "ListAnswerRecordsRequest",
    "ListAnswerRecordsResponse",
    "ListContextsRequest",
    "ListContextsResponse",
    "ListConversationProfilesRequest",
    "ListConversationProfilesResponse",
    "ListConversationsRequest",
    "ListConversationsResponse",
    "ListDocumentsRequest",
    "ListDocumentsResponse",
    "ListEntityTypesRequest",
    "ListEntityTypesResponse",
    "ListEnvironmentsRequest",
    "ListEnvironmentsResponse",
    "ListIntentsRequest",
    "ListIntentsResponse",
    "ListKnowledgeBasesRequest",
    "ListKnowledgeBasesResponse",
    "ListMessagesRequest",
    "ListMessagesResponse",
    "ListParticipantsRequest",
    "ListParticipantsResponse",
    "ListSessionEntityTypesRequest",
    "ListSessionEntityTypesResponse",
    "LoggingConfig",
    "Message",
    "MessageAnnotation",
    "NotificationConfig",
    "OriginalDetectIntentRequest",
    "OutputAudio",
    "OutputAudioConfig",
    "OutputAudioEncoding",
    "Participant",
    "ParticipantsAsyncClient",
    "ParticipantsClient",
    "QueryInput",
    "QueryParameters",
    "QueryResult",
    "ReloadDocumentRequest",
    "RestoreAgentRequest",
    "SearchAgentsRequest",
    "SearchAgentsResponse",
    "Sentiment",
    "SentimentAnalysisRequestConfig",
    "SentimentAnalysisResult",
    "SessionEntityType",
    "SessionEntityTypesAsyncClient",
    "SessionEntityTypesClient",
    "SessionsAsyncClient",
    "SessionsClient",
    "SetAgentRequest",
    "SpeechContext",
    "SpeechModelVariant",
    "SpeechToTextConfig",
    "SpeechWordInfo",
    "SsmlVoiceGender",
    "StreamingDetectIntentRequest",
    "StreamingDetectIntentResponse",
    "StreamingRecognitionResult",
    "SuggestArticlesRequest",
    "SuggestArticlesResponse",
    "SuggestFaqAnswersRequest",
    "SuggestFaqAnswersResponse",
    "SuggestionFeature",
    "SuggestionResult",
    "SynthesizeSpeechConfig",
    "TextInput",
    "TrainAgentRequest",
    "UpdateAnswerRecordRequest",
    "UpdateContextRequest",
    "UpdateConversationProfileRequest",
    "UpdateDocumentRequest",
    "UpdateEntityTypeRequest",
    "UpdateIntentRequest",
    "UpdateKnowledgeBaseRequest",
    "UpdateParticipantRequest",
    "UpdateSessionEntityTypeRequest",
    "ValidationError",
    "ValidationResult",
    "VoiceSelectionParams",
    "WebhookRequest",
    "WebhookResponse",
)
