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
from google.cloud.dialogflow_v2.services.contexts.async_client import (
    ContextsAsyncClient,
)
from google.cloud.dialogflow_v2.services.contexts.client import ContextsClient
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
from google.cloud.dialogflow_v2.types.audio_config import AudioEncoding
from google.cloud.dialogflow_v2.types.audio_config import InputAudioConfig
from google.cloud.dialogflow_v2.types.audio_config import OutputAudioConfig
from google.cloud.dialogflow_v2.types.audio_config import OutputAudioEncoding
from google.cloud.dialogflow_v2.types.audio_config import SpeechContext
from google.cloud.dialogflow_v2.types.audio_config import SpeechModelVariant
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
    "AgentsAsyncClient",
    "AgentsClient",
    "AudioEncoding",
    "BatchCreateEntitiesRequest",
    "BatchDeleteEntitiesRequest",
    "BatchDeleteEntityTypesRequest",
    "BatchDeleteIntentsRequest",
    "BatchUpdateEntitiesRequest",
    "BatchUpdateEntityTypesRequest",
    "BatchUpdateEntityTypesResponse",
    "BatchUpdateIntentsRequest",
    "BatchUpdateIntentsResponse",
    "Context",
    "ContextsAsyncClient",
    "ContextsClient",
    "CreateContextRequest",
    "CreateEntityTypeRequest",
    "CreateIntentRequest",
    "CreateSessionEntityTypeRequest",
    "DeleteAgentRequest",
    "DeleteAllContextsRequest",
    "DeleteContextRequest",
    "DeleteEntityTypeRequest",
    "DeleteIntentRequest",
    "DeleteSessionEntityTypeRequest",
    "DetectIntentRequest",
    "DetectIntentResponse",
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
    "GetAgentRequest",
    "GetContextRequest",
    "GetEntityTypeRequest",
    "GetIntentRequest",
    "GetSessionEntityTypeRequest",
    "GetValidationResultRequest",
    "ImportAgentRequest",
    "InputAudioConfig",
    "Intent",
    "IntentBatch",
    "IntentView",
    "IntentsAsyncClient",
    "IntentsClient",
    "ListContextsRequest",
    "ListContextsResponse",
    "ListEntityTypesRequest",
    "ListEntityTypesResponse",
    "ListEnvironmentsRequest",
    "ListEnvironmentsResponse",
    "ListIntentsRequest",
    "ListIntentsResponse",
    "ListSessionEntityTypesRequest",
    "ListSessionEntityTypesResponse",
    "OriginalDetectIntentRequest",
    "OutputAudioConfig",
    "OutputAudioEncoding",
    "QueryInput",
    "QueryParameters",
    "QueryResult",
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
    "SpeechWordInfo",
    "SsmlVoiceGender",
    "StreamingDetectIntentRequest",
    "StreamingDetectIntentResponse",
    "StreamingRecognitionResult",
    "SynthesizeSpeechConfig",
    "TextInput",
    "TrainAgentRequest",
    "UpdateContextRequest",
    "UpdateEntityTypeRequest",
    "UpdateIntentRequest",
    "UpdateSessionEntityTypeRequest",
    "ValidationError",
    "ValidationResult",
    "VoiceSelectionParams",
    "WebhookRequest",
    "WebhookResponse",
)
