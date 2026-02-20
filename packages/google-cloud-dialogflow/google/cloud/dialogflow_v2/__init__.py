# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import sys

import google.api_core as api_core

from google.cloud.dialogflow_v2 import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.agents import AgentsAsyncClient, AgentsClient
from .services.answer_records import AnswerRecordsAsyncClient, AnswerRecordsClient
from .services.contexts import ContextsAsyncClient, ContextsClient
from .services.conversation_datasets import (
    ConversationDatasetsAsyncClient,
    ConversationDatasetsClient,
)
from .services.conversation_models import (
    ConversationModelsAsyncClient,
    ConversationModelsClient,
)
from .services.conversation_profiles import (
    ConversationProfilesAsyncClient,
    ConversationProfilesClient,
)
from .services.conversations import ConversationsAsyncClient, ConversationsClient
from .services.documents import DocumentsAsyncClient, DocumentsClient
from .services.encryption_spec_service import (
    EncryptionSpecServiceAsyncClient,
    EncryptionSpecServiceClient,
)
from .services.entity_types import EntityTypesAsyncClient, EntityTypesClient
from .services.environments import EnvironmentsAsyncClient, EnvironmentsClient
from .services.fulfillments import FulfillmentsAsyncClient, FulfillmentsClient
from .services.generator_evaluations import (
    GeneratorEvaluationsAsyncClient,
    GeneratorEvaluationsClient,
)
from .services.generators import GeneratorsAsyncClient, GeneratorsClient
from .services.intents import IntentsAsyncClient, IntentsClient
from .services.knowledge_bases import KnowledgeBasesAsyncClient, KnowledgeBasesClient
from .services.participants import ParticipantsAsyncClient, ParticipantsClient
from .services.session_entity_types import (
    SessionEntityTypesAsyncClient,
    SessionEntityTypesClient,
)
from .services.sessions import SessionsAsyncClient, SessionsClient
from .services.sip_trunks import SipTrunksAsyncClient, SipTrunksClient
from .services.tools import ToolsAsyncClient, ToolsClient
from .services.versions import VersionsAsyncClient, VersionsClient
from .types.agent import (
    Agent,
    DeleteAgentRequest,
    ExportAgentRequest,
    ExportAgentResponse,
    GetAgentRequest,
    GetValidationResultRequest,
    ImportAgentRequest,
    RestoreAgentRequest,
    SearchAgentsRequest,
    SearchAgentsResponse,
    SetAgentRequest,
    TrainAgentRequest,
)
from .types.agent_coaching_instruction import AgentCoachingInstruction
from .types.answer_record import (
    AgentAssistantFeedback,
    AgentAssistantRecord,
    AnswerFeedback,
    AnswerRecord,
    ListAnswerRecordsRequest,
    ListAnswerRecordsResponse,
    UpdateAnswerRecordRequest,
)
from .types.audio_config import (
    AudioEncoding,
    CustomPronunciationParams,
    InputAudioConfig,
    OutputAudioConfig,
    OutputAudioEncoding,
    SpeechContext,
    SpeechModelVariant,
    SpeechToTextConfig,
    SpeechWordInfo,
    SsmlVoiceGender,
    SynthesizeSpeechConfig,
    TelephonyDtmf,
    TelephonyDtmfEvents,
    VoiceSelectionParams,
)
from .types.context import (
    Context,
    CreateContextRequest,
    DeleteAllContextsRequest,
    DeleteContextRequest,
    GetContextRequest,
    ListContextsRequest,
    ListContextsResponse,
    UpdateContextRequest,
)
from .types.conversation import (
    CompleteConversationRequest,
    Conversation,
    ConversationPhoneNumber,
    CreateConversationRequest,
    GenerateStatelessSuggestionRequest,
    GenerateStatelessSuggestionResponse,
    GenerateStatelessSummaryRequest,
    GenerateStatelessSummaryResponse,
    GenerateSuggestionsRequest,
    GetConversationRequest,
    IngestContextReferencesRequest,
    IngestContextReferencesResponse,
    ListConversationsRequest,
    ListConversationsResponse,
    ListMessagesRequest,
    ListMessagesResponse,
    SearchKnowledgeAnswer,
    SearchKnowledgeRequest,
    SearchKnowledgeResponse,
    SuggestConversationSummaryRequest,
    SuggestConversationSummaryResponse,
)
from .types.conversation_dataset import (
    ConversationDataset,
    ConversationInfo,
    CreateConversationDatasetOperationMetadata,
    CreateConversationDatasetRequest,
    DeleteConversationDatasetOperationMetadata,
    DeleteConversationDatasetRequest,
    GetConversationDatasetRequest,
    ImportConversationDataOperationMetadata,
    ImportConversationDataOperationResponse,
    ImportConversationDataRequest,
    InputConfig,
    ListConversationDatasetsRequest,
    ListConversationDatasetsResponse,
)
from .types.conversation_event import ConversationEvent
from .types.conversation_model import (
    ArticleSuggestionModelMetadata,
    ConversationModel,
    ConversationModelEvaluation,
    CreateConversationModelEvaluationOperationMetadata,
    CreateConversationModelEvaluationRequest,
    CreateConversationModelOperationMetadata,
    CreateConversationModelRequest,
    DeleteConversationModelOperationMetadata,
    DeleteConversationModelRequest,
    DeployConversationModelOperationMetadata,
    DeployConversationModelRequest,
    EvaluationConfig,
    GetConversationModelEvaluationRequest,
    GetConversationModelRequest,
    InputDataset,
    ListConversationModelEvaluationsRequest,
    ListConversationModelEvaluationsResponse,
    ListConversationModelsRequest,
    ListConversationModelsResponse,
    SmartReplyMetrics,
    SmartReplyModelMetadata,
    UndeployConversationModelOperationMetadata,
    UndeployConversationModelRequest,
)
from .types.conversation_profile import (
    AutomatedAgentConfig,
    ClearSuggestionFeatureConfigOperationMetadata,
    ClearSuggestionFeatureConfigRequest,
    ConversationProfile,
    CreateConversationProfileRequest,
    DeleteConversationProfileRequest,
    GetConversationProfileRequest,
    HumanAgentAssistantConfig,
    HumanAgentHandoffConfig,
    ListConversationProfilesRequest,
    ListConversationProfilesResponse,
    LoggingConfig,
    NotificationConfig,
    SetSuggestionFeatureConfigOperationMetadata,
    SetSuggestionFeatureConfigRequest,
    SuggestionFeature,
    UpdateConversationProfileRequest,
)
from .types.document import (
    CreateDocumentRequest,
    DeleteDocumentRequest,
    Document,
    ExportDocumentRequest,
    ExportOperationMetadata,
    GetDocumentRequest,
    ImportDocumentsRequest,
    ImportDocumentsResponse,
    ImportDocumentTemplate,
    KnowledgeOperationMetadata,
    ListDocumentsRequest,
    ListDocumentsResponse,
    ReloadDocumentRequest,
    UpdateDocumentRequest,
)
from .types.encryption_spec import (
    EncryptionSpec,
    GetEncryptionSpecRequest,
    InitializeEncryptionSpecMetadata,
    InitializeEncryptionSpecRequest,
    InitializeEncryptionSpecResponse,
)
from .types.entity_type import (
    BatchCreateEntitiesRequest,
    BatchDeleteEntitiesRequest,
    BatchDeleteEntityTypesRequest,
    BatchUpdateEntitiesRequest,
    BatchUpdateEntityTypesRequest,
    BatchUpdateEntityTypesResponse,
    CreateEntityTypeRequest,
    DeleteEntityTypeRequest,
    EntityType,
    EntityTypeBatch,
    GetEntityTypeRequest,
    ListEntityTypesRequest,
    ListEntityTypesResponse,
    UpdateEntityTypeRequest,
)
from .types.environment import (
    CreateEnvironmentRequest,
    DeleteEnvironmentRequest,
    Environment,
    EnvironmentHistory,
    GetEnvironmentHistoryRequest,
    GetEnvironmentRequest,
    ListEnvironmentsRequest,
    ListEnvironmentsResponse,
    TextToSpeechSettings,
    UpdateEnvironmentRequest,
)
from .types.fulfillment import (
    Fulfillment,
    GetFulfillmentRequest,
    UpdateFulfillmentRequest,
)
from .types.gcs import GcsDestination, GcsSources
from .types.generator import (
    AgentCoachingContext,
    AgentCoachingSuggestion,
    ConversationContext,
    CreateGeneratorRequest,
    DeleteGeneratorRequest,
    FewShotExample,
    FreeFormContext,
    FreeFormSuggestion,
    Generator,
    GeneratorSuggestion,
    GetGeneratorRequest,
    InferenceParameter,
    ListGeneratorsRequest,
    ListGeneratorsResponse,
    MessageEntry,
    RaiSettings,
    SuggestionDedupingConfig,
    SummarizationContext,
    SummarizationSection,
    SummarizationSectionList,
    SummarySuggestion,
    TriggerEvent,
    UpdateGeneratorRequest,
)
from .types.generator_evaluation import (
    CreateGeneratorEvaluationRequest,
    DeleteGeneratorEvaluationRequest,
    EvaluationStatus,
    GeneratorEvaluation,
    GeneratorEvaluationConfig,
    GetGeneratorEvaluationRequest,
    ListGeneratorEvaluationsRequest,
    ListGeneratorEvaluationsResponse,
    SummarizationEvaluationMetrics,
)
from .types.human_agent_assistant_event import HumanAgentAssistantEvent
from .types.intent import (
    BatchDeleteIntentsRequest,
    BatchUpdateIntentsRequest,
    BatchUpdateIntentsResponse,
    CreateIntentRequest,
    DeleteIntentRequest,
    GetIntentRequest,
    Intent,
    IntentBatch,
    IntentView,
    ListIntentsRequest,
    ListIntentsResponse,
    UpdateIntentRequest,
)
from .types.knowledge_base import (
    CreateKnowledgeBaseRequest,
    DeleteKnowledgeBaseRequest,
    GetKnowledgeBaseRequest,
    KnowledgeBase,
    ListKnowledgeBasesRequest,
    ListKnowledgeBasesResponse,
    UpdateKnowledgeBaseRequest,
)
from .types.operations import GeneratorEvaluationOperationMetadata
from .types.participant import (
    AnalyzeContentRequest,
    AnalyzeContentResponse,
    AnnotatedMessagePart,
    ArticleAnswer,
    AssistQueryParameters,
    AudioInput,
    AutomatedAgentReply,
    CreateParticipantRequest,
    DialogflowAssistAnswer,
    DtmfParameters,
    FaqAnswer,
    GenerateSuggestionsResponse,
    GetParticipantRequest,
    InputTextConfig,
    IntentSuggestion,
    KnowledgeAssistAnswer,
    ListParticipantsRequest,
    ListParticipantsResponse,
    Message,
    MessageAnnotation,
    OutputAudio,
    Participant,
    SmartReplyAnswer,
    StreamingAnalyzeContentRequest,
    StreamingAnalyzeContentResponse,
    SuggestArticlesRequest,
    SuggestArticlesResponse,
    SuggestFaqAnswersRequest,
    SuggestFaqAnswersResponse,
    SuggestionInput,
    SuggestionResult,
    SuggestKnowledgeAssistRequest,
    SuggestKnowledgeAssistResponse,
    SuggestSmartRepliesRequest,
    SuggestSmartRepliesResponse,
    UpdateParticipantRequest,
)
from .types.session import (
    CloudConversationDebuggingInfo,
    DetectIntentRequest,
    DetectIntentResponse,
    EventInput,
    QueryInput,
    QueryParameters,
    QueryResult,
    Sentiment,
    SentimentAnalysisRequestConfig,
    SentimentAnalysisResult,
    StreamingDetectIntentRequest,
    StreamingDetectIntentResponse,
    StreamingRecognitionResult,
    TextInput,
)
from .types.session_entity_type import (
    CreateSessionEntityTypeRequest,
    DeleteSessionEntityTypeRequest,
    GetSessionEntityTypeRequest,
    ListSessionEntityTypesRequest,
    ListSessionEntityTypesResponse,
    SessionEntityType,
    UpdateSessionEntityTypeRequest,
)
from .types.sip_trunk import (
    Connection,
    CreateSipTrunkRequest,
    DeleteSipTrunkRequest,
    GetSipTrunkRequest,
    ListSipTrunksRequest,
    ListSipTrunksResponse,
    SipTrunk,
    UpdateSipTrunkRequest,
)
from .types.tool import (
    CreateToolRequest,
    DeleteToolRequest,
    GetToolRequest,
    ListToolsRequest,
    ListToolsResponse,
    Tool,
    UpdateToolRequest,
)
from .types.tool_call import ToolCall, ToolCallResult
from .types.validation_result import ValidationError, ValidationResult
from .types.version import (
    CreateVersionRequest,
    DeleteVersionRequest,
    GetVersionRequest,
    ListVersionsRequest,
    ListVersionsResponse,
    UpdateVersionRequest,
    Version,
)
from .types.webhook import OriginalDetectIntentRequest, WebhookRequest, WebhookResponse

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.dialogflow_v2")  # type: ignore
    api_core.check_dependency_versions("google.cloud.dialogflow_v2")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.dialogflow_v2"
        if sys.version_info < (3, 9):
            warnings.warn(
                "You are using a non-supported Python version "
                + f"({_py_version_str}).  Google will not post any further "
                + f"updates to {_package_label} supporting this Python version. "
                + "Please upgrade to the latest Python version, or at "
                + f"least to Python 3.9, and then update {_package_label}.",
                FutureWarning,
            )
        if sys.version_info[:2] == (3, 9):
            warnings.warn(
                f"You are using a Python version ({_py_version_str}) "
                + f"which Google will stop supporting in {_package_label} in "
                + "January 2026. Please "
                + "upgrade to the latest Python version, or at "
                + "least to Python 3.10, before then, and "
                + f"then update {_package_label}.",
                FutureWarning,
            )

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "4.25.8" -> (4, 25, 8)
            Ignores non-numeric parts and handles common version formats.
            Args:
                version_string: Version string in the format "x.y.z" or "x.y.z<suffix>"
            Returns:
                Tuple of integers for the parsed version string.
            """
            parts = []
            for part in version_string.split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    # If it's a non-numeric part (e.g., '1.0.0b1' -> 'b1'), stop here.
                    # This is a simplification compared to 'packaging.parse_version', but sufficient
                    # for comparing strictly numeric semantic versions.
                    break
            return tuple(parts)

        def _get_version(dependency_name):
            try:
                version_string: str = metadata.version(dependency_name)
                parsed_version = parse_version_to_tuple(version_string)
                return (parsed_version, version_string)
            except Exception:
                # Catch exceptions from metadata.version() (e.g., PackageNotFoundError)
                # or errors during parse_version_to_tuple
                return (None, "--")

        _dependency_package = "google.protobuf"
        _next_supported_version = "4.25.8"
        _next_supported_version_tuple = (4, 25, 8)
        _recommendation = " (we recommend 6.x)"
        (_version_used, _version_used_string) = _get_version(_dependency_package)
        if _version_used and _version_used < _next_supported_version_tuple:
            warnings.warn(
                f"Package {_package_label} depends on "
                + f"{_dependency_package}, currently installed at version "
                + f"{_version_used_string}. Future updates to "
                + f"{_package_label} will require {_dependency_package} at "
                + f"version {_next_supported_version} or higher{_recommendation}."
                + " Please ensure "
                + "that either (a) your Python environment doesn't pin the "
                + f"version of {_dependency_package}, so that updates to "
                + f"{_package_label} can require the higher version, or "
                + "(b) you manually update your Python environment to use at "
                + f"least version {_next_supported_version} of "
                + f"{_dependency_package}.",
                FutureWarning,
            )
    except Exception:
        warnings.warn(
            "Could not determine the version of Python "
            + "currently being used. To continue receiving "
            + "updates for {_package_label}, ensure you are "
            + "using a supported version of Python; see "
            + "https://devguide.python.org/versions/"
        )

__all__ = (
    "AgentsAsyncClient",
    "AnswerRecordsAsyncClient",
    "ContextsAsyncClient",
    "ConversationDatasetsAsyncClient",
    "ConversationModelsAsyncClient",
    "ConversationProfilesAsyncClient",
    "ConversationsAsyncClient",
    "DocumentsAsyncClient",
    "EncryptionSpecServiceAsyncClient",
    "EntityTypesAsyncClient",
    "EnvironmentsAsyncClient",
    "FulfillmentsAsyncClient",
    "GeneratorEvaluationsAsyncClient",
    "GeneratorsAsyncClient",
    "IntentsAsyncClient",
    "KnowledgeBasesAsyncClient",
    "ParticipantsAsyncClient",
    "SessionEntityTypesAsyncClient",
    "SessionsAsyncClient",
    "SipTrunksAsyncClient",
    "ToolsAsyncClient",
    "VersionsAsyncClient",
    "Agent",
    "AgentAssistantFeedback",
    "AgentAssistantRecord",
    "AgentCoachingContext",
    "AgentCoachingInstruction",
    "AgentCoachingSuggestion",
    "AgentsClient",
    "AnalyzeContentRequest",
    "AnalyzeContentResponse",
    "AnnotatedMessagePart",
    "AnswerFeedback",
    "AnswerRecord",
    "AnswerRecordsClient",
    "ArticleAnswer",
    "ArticleSuggestionModelMetadata",
    "AssistQueryParameters",
    "AudioEncoding",
    "AudioInput",
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
    "ClearSuggestionFeatureConfigOperationMetadata",
    "ClearSuggestionFeatureConfigRequest",
    "CloudConversationDebuggingInfo",
    "CompleteConversationRequest",
    "Connection",
    "Context",
    "ContextsClient",
    "Conversation",
    "ConversationContext",
    "ConversationDataset",
    "ConversationDatasetsClient",
    "ConversationEvent",
    "ConversationInfo",
    "ConversationModel",
    "ConversationModelEvaluation",
    "ConversationModelsClient",
    "ConversationPhoneNumber",
    "ConversationProfile",
    "ConversationProfilesClient",
    "ConversationsClient",
    "CreateContextRequest",
    "CreateConversationDatasetOperationMetadata",
    "CreateConversationDatasetRequest",
    "CreateConversationModelEvaluationOperationMetadata",
    "CreateConversationModelEvaluationRequest",
    "CreateConversationModelOperationMetadata",
    "CreateConversationModelRequest",
    "CreateConversationProfileRequest",
    "CreateConversationRequest",
    "CreateDocumentRequest",
    "CreateEntityTypeRequest",
    "CreateEnvironmentRequest",
    "CreateGeneratorEvaluationRequest",
    "CreateGeneratorRequest",
    "CreateIntentRequest",
    "CreateKnowledgeBaseRequest",
    "CreateParticipantRequest",
    "CreateSessionEntityTypeRequest",
    "CreateSipTrunkRequest",
    "CreateToolRequest",
    "CreateVersionRequest",
    "CustomPronunciationParams",
    "DeleteAgentRequest",
    "DeleteAllContextsRequest",
    "DeleteContextRequest",
    "DeleteConversationDatasetOperationMetadata",
    "DeleteConversationDatasetRequest",
    "DeleteConversationModelOperationMetadata",
    "DeleteConversationModelRequest",
    "DeleteConversationProfileRequest",
    "DeleteDocumentRequest",
    "DeleteEntityTypeRequest",
    "DeleteEnvironmentRequest",
    "DeleteGeneratorEvaluationRequest",
    "DeleteGeneratorRequest",
    "DeleteIntentRequest",
    "DeleteKnowledgeBaseRequest",
    "DeleteSessionEntityTypeRequest",
    "DeleteSipTrunkRequest",
    "DeleteToolRequest",
    "DeleteVersionRequest",
    "DeployConversationModelOperationMetadata",
    "DeployConversationModelRequest",
    "DetectIntentRequest",
    "DetectIntentResponse",
    "DialogflowAssistAnswer",
    "Document",
    "DocumentsClient",
    "DtmfParameters",
    "EncryptionSpec",
    "EncryptionSpecServiceClient",
    "EntityType",
    "EntityTypeBatch",
    "EntityTypesClient",
    "Environment",
    "EnvironmentHistory",
    "EnvironmentsClient",
    "EvaluationConfig",
    "EvaluationStatus",
    "EventInput",
    "ExportAgentRequest",
    "ExportAgentResponse",
    "ExportDocumentRequest",
    "ExportOperationMetadata",
    "FaqAnswer",
    "FewShotExample",
    "FreeFormContext",
    "FreeFormSuggestion",
    "Fulfillment",
    "FulfillmentsClient",
    "GcsDestination",
    "GcsSources",
    "GenerateStatelessSuggestionRequest",
    "GenerateStatelessSuggestionResponse",
    "GenerateStatelessSummaryRequest",
    "GenerateStatelessSummaryResponse",
    "GenerateSuggestionsRequest",
    "GenerateSuggestionsResponse",
    "Generator",
    "GeneratorEvaluation",
    "GeneratorEvaluationConfig",
    "GeneratorEvaluationOperationMetadata",
    "GeneratorEvaluationsClient",
    "GeneratorSuggestion",
    "GeneratorsClient",
    "GetAgentRequest",
    "GetContextRequest",
    "GetConversationDatasetRequest",
    "GetConversationModelEvaluationRequest",
    "GetConversationModelRequest",
    "GetConversationProfileRequest",
    "GetConversationRequest",
    "GetDocumentRequest",
    "GetEncryptionSpecRequest",
    "GetEntityTypeRequest",
    "GetEnvironmentHistoryRequest",
    "GetEnvironmentRequest",
    "GetFulfillmentRequest",
    "GetGeneratorEvaluationRequest",
    "GetGeneratorRequest",
    "GetIntentRequest",
    "GetKnowledgeBaseRequest",
    "GetParticipantRequest",
    "GetSessionEntityTypeRequest",
    "GetSipTrunkRequest",
    "GetToolRequest",
    "GetValidationResultRequest",
    "GetVersionRequest",
    "HumanAgentAssistantConfig",
    "HumanAgentAssistantEvent",
    "HumanAgentHandoffConfig",
    "ImportAgentRequest",
    "ImportConversationDataOperationMetadata",
    "ImportConversationDataOperationResponse",
    "ImportConversationDataRequest",
    "ImportDocumentTemplate",
    "ImportDocumentsRequest",
    "ImportDocumentsResponse",
    "InferenceParameter",
    "IngestContextReferencesRequest",
    "IngestContextReferencesResponse",
    "InitializeEncryptionSpecMetadata",
    "InitializeEncryptionSpecRequest",
    "InitializeEncryptionSpecResponse",
    "InputAudioConfig",
    "InputConfig",
    "InputDataset",
    "InputTextConfig",
    "Intent",
    "IntentBatch",
    "IntentSuggestion",
    "IntentView",
    "IntentsClient",
    "KnowledgeAssistAnswer",
    "KnowledgeBase",
    "KnowledgeBasesClient",
    "KnowledgeOperationMetadata",
    "ListAnswerRecordsRequest",
    "ListAnswerRecordsResponse",
    "ListContextsRequest",
    "ListContextsResponse",
    "ListConversationDatasetsRequest",
    "ListConversationDatasetsResponse",
    "ListConversationModelEvaluationsRequest",
    "ListConversationModelEvaluationsResponse",
    "ListConversationModelsRequest",
    "ListConversationModelsResponse",
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
    "ListGeneratorEvaluationsRequest",
    "ListGeneratorEvaluationsResponse",
    "ListGeneratorsRequest",
    "ListGeneratorsResponse",
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
    "ListSipTrunksRequest",
    "ListSipTrunksResponse",
    "ListToolsRequest",
    "ListToolsResponse",
    "ListVersionsRequest",
    "ListVersionsResponse",
    "LoggingConfig",
    "Message",
    "MessageAnnotation",
    "MessageEntry",
    "NotificationConfig",
    "OriginalDetectIntentRequest",
    "OutputAudio",
    "OutputAudioConfig",
    "OutputAudioEncoding",
    "Participant",
    "ParticipantsClient",
    "QueryInput",
    "QueryParameters",
    "QueryResult",
    "RaiSettings",
    "ReloadDocumentRequest",
    "RestoreAgentRequest",
    "SearchAgentsRequest",
    "SearchAgentsResponse",
    "SearchKnowledgeAnswer",
    "SearchKnowledgeRequest",
    "SearchKnowledgeResponse",
    "Sentiment",
    "SentimentAnalysisRequestConfig",
    "SentimentAnalysisResult",
    "SessionEntityType",
    "SessionEntityTypesClient",
    "SessionsClient",
    "SetAgentRequest",
    "SetSuggestionFeatureConfigOperationMetadata",
    "SetSuggestionFeatureConfigRequest",
    "SipTrunk",
    "SipTrunksClient",
    "SmartReplyAnswer",
    "SmartReplyMetrics",
    "SmartReplyModelMetadata",
    "SpeechContext",
    "SpeechModelVariant",
    "SpeechToTextConfig",
    "SpeechWordInfo",
    "SsmlVoiceGender",
    "StreamingAnalyzeContentRequest",
    "StreamingAnalyzeContentResponse",
    "StreamingDetectIntentRequest",
    "StreamingDetectIntentResponse",
    "StreamingRecognitionResult",
    "SuggestArticlesRequest",
    "SuggestArticlesResponse",
    "SuggestConversationSummaryRequest",
    "SuggestConversationSummaryResponse",
    "SuggestFaqAnswersRequest",
    "SuggestFaqAnswersResponse",
    "SuggestKnowledgeAssistRequest",
    "SuggestKnowledgeAssistResponse",
    "SuggestSmartRepliesRequest",
    "SuggestSmartRepliesResponse",
    "SuggestionDedupingConfig",
    "SuggestionFeature",
    "SuggestionInput",
    "SuggestionResult",
    "SummarizationContext",
    "SummarizationEvaluationMetrics",
    "SummarizationSection",
    "SummarizationSectionList",
    "SummarySuggestion",
    "SynthesizeSpeechConfig",
    "TelephonyDtmf",
    "TelephonyDtmfEvents",
    "TextInput",
    "TextToSpeechSettings",
    "Tool",
    "ToolCall",
    "ToolCallResult",
    "ToolsClient",
    "TrainAgentRequest",
    "TriggerEvent",
    "UndeployConversationModelOperationMetadata",
    "UndeployConversationModelRequest",
    "UpdateAnswerRecordRequest",
    "UpdateContextRequest",
    "UpdateConversationProfileRequest",
    "UpdateDocumentRequest",
    "UpdateEntityTypeRequest",
    "UpdateEnvironmentRequest",
    "UpdateFulfillmentRequest",
    "UpdateGeneratorRequest",
    "UpdateIntentRequest",
    "UpdateKnowledgeBaseRequest",
    "UpdateParticipantRequest",
    "UpdateSessionEntityTypeRequest",
    "UpdateSipTrunkRequest",
    "UpdateToolRequest",
    "UpdateVersionRequest",
    "ValidationError",
    "ValidationResult",
    "Version",
    "VersionsClient",
    "VoiceSelectionParams",
    "WebhookRequest",
    "WebhookResponse",
)
