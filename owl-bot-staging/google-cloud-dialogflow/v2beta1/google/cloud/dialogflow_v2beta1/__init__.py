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
from google.cloud.dialogflow_v2beta1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.agents import AgentsClient
from .services.agents import AgentsAsyncClient
from .services.answer_records import AnswerRecordsClient
from .services.answer_records import AnswerRecordsAsyncClient
from .services.contexts import ContextsClient
from .services.contexts import ContextsAsyncClient
from .services.conversation_profiles import ConversationProfilesClient
from .services.conversation_profiles import ConversationProfilesAsyncClient
from .services.conversations import ConversationsClient
from .services.conversations import ConversationsAsyncClient
from .services.documents import DocumentsClient
from .services.documents import DocumentsAsyncClient
from .services.encryption_spec_service import EncryptionSpecServiceClient
from .services.encryption_spec_service import EncryptionSpecServiceAsyncClient
from .services.entity_types import EntityTypesClient
from .services.entity_types import EntityTypesAsyncClient
from .services.environments import EnvironmentsClient
from .services.environments import EnvironmentsAsyncClient
from .services.fulfillments import FulfillmentsClient
from .services.fulfillments import FulfillmentsAsyncClient
from .services.generators import GeneratorsClient
from .services.generators import GeneratorsAsyncClient
from .services.intents import IntentsClient
from .services.intents import IntentsAsyncClient
from .services.knowledge_bases import KnowledgeBasesClient
from .services.knowledge_bases import KnowledgeBasesAsyncClient
from .services.participants import ParticipantsClient
from .services.participants import ParticipantsAsyncClient
from .services.session_entity_types import SessionEntityTypesClient
from .services.session_entity_types import SessionEntityTypesAsyncClient
from .services.sessions import SessionsClient
from .services.sessions import SessionsAsyncClient
from .services.sip_trunks import SipTrunksClient
from .services.sip_trunks import SipTrunksAsyncClient
from .services.versions import VersionsClient
from .services.versions import VersionsAsyncClient

from .types.agent import Agent
from .types.agent import DeleteAgentRequest
from .types.agent import ExportAgentRequest
from .types.agent import ExportAgentResponse
from .types.agent import GetAgentRequest
from .types.agent import GetValidationResultRequest
from .types.agent import ImportAgentRequest
from .types.agent import RestoreAgentRequest
from .types.agent import SearchAgentsRequest
from .types.agent import SearchAgentsResponse
from .types.agent import SetAgentRequest
from .types.agent import SubAgent
from .types.agent import TrainAgentRequest
from .types.answer_record import AgentAssistantFeedback
from .types.answer_record import AgentAssistantRecord
from .types.answer_record import AnswerFeedback
from .types.answer_record import AnswerRecord
from .types.answer_record import GetAnswerRecordRequest
from .types.answer_record import ListAnswerRecordsRequest
from .types.answer_record import ListAnswerRecordsResponse
from .types.answer_record import UpdateAnswerRecordRequest
from .types.audio_config import BargeInConfig
from .types.audio_config import InputAudioConfig
from .types.audio_config import OutputAudioConfig
from .types.audio_config import SpeechContext
from .types.audio_config import SpeechToTextConfig
from .types.audio_config import SpeechWordInfo
from .types.audio_config import SynthesizeSpeechConfig
from .types.audio_config import TelephonyDtmfEvents
from .types.audio_config import VoiceSelectionParams
from .types.audio_config import AudioEncoding
from .types.audio_config import OutputAudioEncoding
from .types.audio_config import SpeechModelVariant
from .types.audio_config import SsmlVoiceGender
from .types.audio_config import TelephonyDtmf
from .types.context import Context
from .types.context import CreateContextRequest
from .types.context import DeleteAllContextsRequest
from .types.context import DeleteContextRequest
from .types.context import GetContextRequest
from .types.context import ListContextsRequest
from .types.context import ListContextsResponse
from .types.context import UpdateContextRequest
from .types.conversation import BatchCreateMessagesRequest
from .types.conversation import BatchCreateMessagesResponse
from .types.conversation import CompleteConversationRequest
from .types.conversation import Conversation
from .types.conversation import ConversationPhoneNumber
from .types.conversation import CreateConversationRequest
from .types.conversation import CreateMessageRequest
from .types.conversation import GenerateStatelessSuggestionRequest
from .types.conversation import GenerateStatelessSuggestionResponse
from .types.conversation import GenerateStatelessSummaryRequest
from .types.conversation import GenerateStatelessSummaryResponse
from .types.conversation import GetConversationRequest
from .types.conversation import ListConversationsRequest
from .types.conversation import ListConversationsResponse
from .types.conversation import ListMessagesRequest
from .types.conversation import ListMessagesResponse
from .types.conversation import SearchKnowledgeAnswer
from .types.conversation import SearchKnowledgeRequest
from .types.conversation import SearchKnowledgeResponse
from .types.conversation import SuggestConversationSummaryRequest
from .types.conversation import SuggestConversationSummaryResponse
from .types.conversation_event import ConversationEvent
from .types.conversation_profile import AutomatedAgentConfig
from .types.conversation_profile import ClearSuggestionFeatureConfigOperationMetadata
from .types.conversation_profile import ClearSuggestionFeatureConfigRequest
from .types.conversation_profile import ConversationProfile
from .types.conversation_profile import CreateConversationProfileRequest
from .types.conversation_profile import DeleteConversationProfileRequest
from .types.conversation_profile import GetConversationProfileRequest
from .types.conversation_profile import HumanAgentAssistantConfig
from .types.conversation_profile import HumanAgentHandoffConfig
from .types.conversation_profile import ListConversationProfilesRequest
from .types.conversation_profile import ListConversationProfilesResponse
from .types.conversation_profile import LoggingConfig
from .types.conversation_profile import NotificationConfig
from .types.conversation_profile import SetSuggestionFeatureConfigOperationMetadata
from .types.conversation_profile import SetSuggestionFeatureConfigRequest
from .types.conversation_profile import UpdateConversationProfileRequest
from .types.document import CreateDocumentRequest
from .types.document import DeleteDocumentRequest
from .types.document import Document
from .types.document import ExportOperationMetadata
from .types.document import GetDocumentRequest
from .types.document import ImportDocumentsRequest
from .types.document import ImportDocumentsResponse
from .types.document import ImportDocumentTemplate
from .types.document import KnowledgeOperationMetadata
from .types.document import ListDocumentsRequest
from .types.document import ListDocumentsResponse
from .types.document import ReloadDocumentRequest
from .types.document import UpdateDocumentRequest
from .types.encryption_spec import EncryptionSpec
from .types.encryption_spec import GetEncryptionSpecRequest
from .types.encryption_spec import InitializeEncryptionSpecMetadata
from .types.encryption_spec import InitializeEncryptionSpecRequest
from .types.encryption_spec import InitializeEncryptionSpecResponse
from .types.entity_type import BatchCreateEntitiesRequest
from .types.entity_type import BatchDeleteEntitiesRequest
from .types.entity_type import BatchDeleteEntityTypesRequest
from .types.entity_type import BatchUpdateEntitiesRequest
from .types.entity_type import BatchUpdateEntityTypesRequest
from .types.entity_type import BatchUpdateEntityTypesResponse
from .types.entity_type import CreateEntityTypeRequest
from .types.entity_type import DeleteEntityTypeRequest
from .types.entity_type import EntityType
from .types.entity_type import EntityTypeBatch
from .types.entity_type import GetEntityTypeRequest
from .types.entity_type import ListEntityTypesRequest
from .types.entity_type import ListEntityTypesResponse
from .types.entity_type import UpdateEntityTypeRequest
from .types.environment import CreateEnvironmentRequest
from .types.environment import DeleteEnvironmentRequest
from .types.environment import Environment
from .types.environment import EnvironmentHistory
from .types.environment import GetEnvironmentHistoryRequest
from .types.environment import GetEnvironmentRequest
from .types.environment import ListEnvironmentsRequest
from .types.environment import ListEnvironmentsResponse
from .types.environment import TextToSpeechSettings
from .types.environment import UpdateEnvironmentRequest
from .types.fulfillment import Fulfillment
from .types.fulfillment import GetFulfillmentRequest
from .types.fulfillment import UpdateFulfillmentRequest
from .types.gcs import GcsDestination
from .types.gcs import GcsSource
from .types.gcs import GcsSources
from .types.generator import ConversationContext
from .types.generator import CreateGeneratorRequest
from .types.generator import DeleteGeneratorRequest
from .types.generator import FewShotExample
from .types.generator import Generator
from .types.generator import GeneratorSuggestion
from .types.generator import GetGeneratorRequest
from .types.generator import InferenceParameter
from .types.generator import ListGeneratorsRequest
from .types.generator import ListGeneratorsResponse
from .types.generator import MessageEntry
from .types.generator import SummarizationContext
from .types.generator import SummarizationSection
from .types.generator import SummarizationSectionList
from .types.generator import SummarySuggestion
from .types.generator import UpdateGeneratorRequest
from .types.generator import TriggerEvent
from .types.human_agent_assistant_event import HumanAgentAssistantEvent
from .types.intent import BatchDeleteIntentsRequest
from .types.intent import BatchUpdateIntentsRequest
from .types.intent import BatchUpdateIntentsResponse
from .types.intent import CreateIntentRequest
from .types.intent import DeleteIntentRequest
from .types.intent import GetIntentRequest
from .types.intent import Intent
from .types.intent import IntentBatch
from .types.intent import ListIntentsRequest
from .types.intent import ListIntentsResponse
from .types.intent import UpdateIntentRequest
from .types.intent import IntentView
from .types.knowledge_base import CreateKnowledgeBaseRequest
from .types.knowledge_base import DeleteKnowledgeBaseRequest
from .types.knowledge_base import GetKnowledgeBaseRequest
from .types.knowledge_base import KnowledgeBase
from .types.knowledge_base import ListKnowledgeBasesRequest
from .types.knowledge_base import ListKnowledgeBasesResponse
from .types.knowledge_base import UpdateKnowledgeBaseRequest
from .types.participant import AnalyzeContentRequest
from .types.participant import AnalyzeContentResponse
from .types.participant import AnnotatedMessagePart
from .types.participant import ArticleAnswer
from .types.participant import AssistQueryParameters
from .types.participant import AudioInput
from .types.participant import AutomatedAgentReply
from .types.participant import CompileSuggestionRequest
from .types.participant import CompileSuggestionResponse
from .types.participant import CreateParticipantRequest
from .types.participant import DialogflowAssistAnswer
from .types.participant import DtmfParameters
from .types.participant import FaqAnswer
from .types.participant import GetParticipantRequest
from .types.participant import InputTextConfig
from .types.participant import IntentInput
from .types.participant import IntentSuggestion
from .types.participant import KnowledgeAssistAnswer
from .types.participant import ListParticipantsRequest
from .types.participant import ListParticipantsResponse
from .types.participant import ListSuggestionsRequest
from .types.participant import ListSuggestionsResponse
from .types.participant import Message
from .types.participant import MessageAnnotation
from .types.participant import OutputAudio
from .types.participant import Participant
from .types.participant import ResponseMessage
from .types.participant import SmartReplyAnswer
from .types.participant import StreamingAnalyzeContentRequest
from .types.participant import StreamingAnalyzeContentResponse
from .types.participant import SuggestArticlesRequest
from .types.participant import SuggestArticlesResponse
from .types.participant import SuggestDialogflowAssistsResponse
from .types.participant import SuggestFaqAnswersRequest
from .types.participant import SuggestFaqAnswersResponse
from .types.participant import Suggestion
from .types.participant import SuggestionFeature
from .types.participant import SuggestionInput
from .types.participant import SuggestionResult
from .types.participant import SuggestKnowledgeAssistRequest
from .types.participant import SuggestKnowledgeAssistResponse
from .types.participant import SuggestSmartRepliesRequest
from .types.participant import SuggestSmartRepliesResponse
from .types.participant import UpdateParticipantRequest
from .types.session import CloudConversationDebuggingInfo
from .types.session import DetectIntentRequest
from .types.session import DetectIntentResponse
from .types.session import EventInput
from .types.session import KnowledgeAnswers
from .types.session import QueryInput
from .types.session import QueryParameters
from .types.session import QueryResult
from .types.session import Sentiment
from .types.session import SentimentAnalysisRequestConfig
from .types.session import SentimentAnalysisResult
from .types.session import StreamingDetectIntentRequest
from .types.session import StreamingDetectIntentResponse
from .types.session import StreamingRecognitionResult
from .types.session import TextInput
from .types.session_entity_type import CreateSessionEntityTypeRequest
from .types.session_entity_type import DeleteSessionEntityTypeRequest
from .types.session_entity_type import GetSessionEntityTypeRequest
from .types.session_entity_type import ListSessionEntityTypesRequest
from .types.session_entity_type import ListSessionEntityTypesResponse
from .types.session_entity_type import SessionEntityType
from .types.session_entity_type import UpdateSessionEntityTypeRequest
from .types.sip_trunk import Connection
from .types.sip_trunk import CreateSipTrunkRequest
from .types.sip_trunk import DeleteSipTrunkRequest
from .types.sip_trunk import GetSipTrunkRequest
from .types.sip_trunk import ListSipTrunksRequest
from .types.sip_trunk import ListSipTrunksResponse
from .types.sip_trunk import SipTrunk
from .types.sip_trunk import UpdateSipTrunkRequest
from .types.validation_result import ValidationError
from .types.validation_result import ValidationResult
from .types.version import CreateVersionRequest
from .types.version import DeleteVersionRequest
from .types.version import GetVersionRequest
from .types.version import ListVersionsRequest
from .types.version import ListVersionsResponse
from .types.version import UpdateVersionRequest
from .types.version import Version
from .types.webhook import OriginalDetectIntentRequest
from .types.webhook import WebhookRequest
from .types.webhook import WebhookResponse

__all__ = (
    'AgentsAsyncClient',
    'AnswerRecordsAsyncClient',
    'ContextsAsyncClient',
    'ConversationProfilesAsyncClient',
    'ConversationsAsyncClient',
    'DocumentsAsyncClient',
    'EncryptionSpecServiceAsyncClient',
    'EntityTypesAsyncClient',
    'EnvironmentsAsyncClient',
    'FulfillmentsAsyncClient',
    'GeneratorsAsyncClient',
    'IntentsAsyncClient',
    'KnowledgeBasesAsyncClient',
    'ParticipantsAsyncClient',
    'SessionEntityTypesAsyncClient',
    'SessionsAsyncClient',
    'SipTrunksAsyncClient',
    'VersionsAsyncClient',
'Agent',
'AgentAssistantFeedback',
'AgentAssistantRecord',
'AgentsClient',
'AnalyzeContentRequest',
'AnalyzeContentResponse',
'AnnotatedMessagePart',
'AnswerFeedback',
'AnswerRecord',
'AnswerRecordsClient',
'ArticleAnswer',
'AssistQueryParameters',
'AudioEncoding',
'AudioInput',
'AutomatedAgentConfig',
'AutomatedAgentReply',
'BargeInConfig',
'BatchCreateEntitiesRequest',
'BatchCreateMessagesRequest',
'BatchCreateMessagesResponse',
'BatchDeleteEntitiesRequest',
'BatchDeleteEntityTypesRequest',
'BatchDeleteIntentsRequest',
'BatchUpdateEntitiesRequest',
'BatchUpdateEntityTypesRequest',
'BatchUpdateEntityTypesResponse',
'BatchUpdateIntentsRequest',
'BatchUpdateIntentsResponse',
'ClearSuggestionFeatureConfigOperationMetadata',
'ClearSuggestionFeatureConfigRequest',
'CloudConversationDebuggingInfo',
'CompileSuggestionRequest',
'CompileSuggestionResponse',
'CompleteConversationRequest',
'Connection',
'Context',
'ContextsClient',
'Conversation',
'ConversationContext',
'ConversationEvent',
'ConversationPhoneNumber',
'ConversationProfile',
'ConversationProfilesClient',
'ConversationsClient',
'CreateContextRequest',
'CreateConversationProfileRequest',
'CreateConversationRequest',
'CreateDocumentRequest',
'CreateEntityTypeRequest',
'CreateEnvironmentRequest',
'CreateGeneratorRequest',
'CreateIntentRequest',
'CreateKnowledgeBaseRequest',
'CreateMessageRequest',
'CreateParticipantRequest',
'CreateSessionEntityTypeRequest',
'CreateSipTrunkRequest',
'CreateVersionRequest',
'DeleteAgentRequest',
'DeleteAllContextsRequest',
'DeleteContextRequest',
'DeleteConversationProfileRequest',
'DeleteDocumentRequest',
'DeleteEntityTypeRequest',
'DeleteEnvironmentRequest',
'DeleteGeneratorRequest',
'DeleteIntentRequest',
'DeleteKnowledgeBaseRequest',
'DeleteSessionEntityTypeRequest',
'DeleteSipTrunkRequest',
'DeleteVersionRequest',
'DetectIntentRequest',
'DetectIntentResponse',
'DialogflowAssistAnswer',
'Document',
'DocumentsClient',
'DtmfParameters',
'EncryptionSpec',
'EncryptionSpecServiceClient',
'EntityType',
'EntityTypeBatch',
'EntityTypesClient',
'Environment',
'EnvironmentHistory',
'EnvironmentsClient',
'EventInput',
'ExportAgentRequest',
'ExportAgentResponse',
'ExportOperationMetadata',
'FaqAnswer',
'FewShotExample',
'Fulfillment',
'FulfillmentsClient',
'GcsDestination',
'GcsSource',
'GcsSources',
'GenerateStatelessSuggestionRequest',
'GenerateStatelessSuggestionResponse',
'GenerateStatelessSummaryRequest',
'GenerateStatelessSummaryResponse',
'Generator',
'GeneratorSuggestion',
'GeneratorsClient',
'GetAgentRequest',
'GetAnswerRecordRequest',
'GetContextRequest',
'GetConversationProfileRequest',
'GetConversationRequest',
'GetDocumentRequest',
'GetEncryptionSpecRequest',
'GetEntityTypeRequest',
'GetEnvironmentHistoryRequest',
'GetEnvironmentRequest',
'GetFulfillmentRequest',
'GetGeneratorRequest',
'GetIntentRequest',
'GetKnowledgeBaseRequest',
'GetParticipantRequest',
'GetSessionEntityTypeRequest',
'GetSipTrunkRequest',
'GetValidationResultRequest',
'GetVersionRequest',
'HumanAgentAssistantConfig',
'HumanAgentAssistantEvent',
'HumanAgentHandoffConfig',
'ImportAgentRequest',
'ImportDocumentTemplate',
'ImportDocumentsRequest',
'ImportDocumentsResponse',
'InferenceParameter',
'InitializeEncryptionSpecMetadata',
'InitializeEncryptionSpecRequest',
'InitializeEncryptionSpecResponse',
'InputAudioConfig',
'InputTextConfig',
'Intent',
'IntentBatch',
'IntentInput',
'IntentSuggestion',
'IntentView',
'IntentsClient',
'KnowledgeAnswers',
'KnowledgeAssistAnswer',
'KnowledgeBase',
'KnowledgeBasesClient',
'KnowledgeOperationMetadata',
'ListAnswerRecordsRequest',
'ListAnswerRecordsResponse',
'ListContextsRequest',
'ListContextsResponse',
'ListConversationProfilesRequest',
'ListConversationProfilesResponse',
'ListConversationsRequest',
'ListConversationsResponse',
'ListDocumentsRequest',
'ListDocumentsResponse',
'ListEntityTypesRequest',
'ListEntityTypesResponse',
'ListEnvironmentsRequest',
'ListEnvironmentsResponse',
'ListGeneratorsRequest',
'ListGeneratorsResponse',
'ListIntentsRequest',
'ListIntentsResponse',
'ListKnowledgeBasesRequest',
'ListKnowledgeBasesResponse',
'ListMessagesRequest',
'ListMessagesResponse',
'ListParticipantsRequest',
'ListParticipantsResponse',
'ListSessionEntityTypesRequest',
'ListSessionEntityTypesResponse',
'ListSipTrunksRequest',
'ListSipTrunksResponse',
'ListSuggestionsRequest',
'ListSuggestionsResponse',
'ListVersionsRequest',
'ListVersionsResponse',
'LoggingConfig',
'Message',
'MessageAnnotation',
'MessageEntry',
'NotificationConfig',
'OriginalDetectIntentRequest',
'OutputAudio',
'OutputAudioConfig',
'OutputAudioEncoding',
'Participant',
'ParticipantsClient',
'QueryInput',
'QueryParameters',
'QueryResult',
'ReloadDocumentRequest',
'ResponseMessage',
'RestoreAgentRequest',
'SearchAgentsRequest',
'SearchAgentsResponse',
'SearchKnowledgeAnswer',
'SearchKnowledgeRequest',
'SearchKnowledgeResponse',
'Sentiment',
'SentimentAnalysisRequestConfig',
'SentimentAnalysisResult',
'SessionEntityType',
'SessionEntityTypesClient',
'SessionsClient',
'SetAgentRequest',
'SetSuggestionFeatureConfigOperationMetadata',
'SetSuggestionFeatureConfigRequest',
'SipTrunk',
'SipTrunksClient',
'SmartReplyAnswer',
'SpeechContext',
'SpeechModelVariant',
'SpeechToTextConfig',
'SpeechWordInfo',
'SsmlVoiceGender',
'StreamingAnalyzeContentRequest',
'StreamingAnalyzeContentResponse',
'StreamingDetectIntentRequest',
'StreamingDetectIntentResponse',
'StreamingRecognitionResult',
'SubAgent',
'SuggestArticlesRequest',
'SuggestArticlesResponse',
'SuggestConversationSummaryRequest',
'SuggestConversationSummaryResponse',
'SuggestDialogflowAssistsResponse',
'SuggestFaqAnswersRequest',
'SuggestFaqAnswersResponse',
'SuggestKnowledgeAssistRequest',
'SuggestKnowledgeAssistResponse',
'SuggestSmartRepliesRequest',
'SuggestSmartRepliesResponse',
'Suggestion',
'SuggestionFeature',
'SuggestionInput',
'SuggestionResult',
'SummarizationContext',
'SummarizationSection',
'SummarizationSectionList',
'SummarySuggestion',
'SynthesizeSpeechConfig',
'TelephonyDtmf',
'TelephonyDtmfEvents',
'TextInput',
'TextToSpeechSettings',
'TrainAgentRequest',
'TriggerEvent',
'UpdateAnswerRecordRequest',
'UpdateContextRequest',
'UpdateConversationProfileRequest',
'UpdateDocumentRequest',
'UpdateEntityTypeRequest',
'UpdateEnvironmentRequest',
'UpdateFulfillmentRequest',
'UpdateGeneratorRequest',
'UpdateIntentRequest',
'UpdateKnowledgeBaseRequest',
'UpdateParticipantRequest',
'UpdateSessionEntityTypeRequest',
'UpdateSipTrunkRequest',
'UpdateVersionRequest',
'ValidationError',
'ValidationResult',
'Version',
'VersionsClient',
'VoiceSelectionParams',
'WebhookRequest',
'WebhookResponse',
)
