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
from google.cloud.geminidataanalytics_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.data_agent_service import (
    DataAgentServiceAsyncClient,
    DataAgentServiceClient,
)
from .services.data_chat_service import (
    DataChatServiceAsyncClient,
    DataChatServiceClient,
)
from .types.context import (
    AnalysisOptions,
    ChartOptions,
    Context,
    ConversationOptions,
    ExampleQuery,
)
from .types.conversation import (
    Conversation,
    CreateConversationRequest,
    GetConversationRequest,
    ListConversationsRequest,
    ListConversationsResponse,
    UpdateConversationRequest,
)
from .types.credentials import Credentials, OAuthCredentials
from .types.data_agent import DataAgent
from .types.data_agent_service import (
    CreateDataAgentRequest,
    DeleteDataAgentRequest,
    GetDataAgentRequest,
    ListAccessibleDataAgentsRequest,
    ListAccessibleDataAgentsResponse,
    ListDataAgentsRequest,
    ListDataAgentsResponse,
    OperationMetadata,
    UpdateDataAgentRequest,
)
from .types.data_analytics_agent import DataAnalyticsAgent
from .types.data_chat_service import (
    AnalysisEvent,
    AnalysisMessage,
    AnalysisQuery,
    BigQueryJob,
    Blob,
    ChartMessage,
    ChartQuery,
    ChartResult,
    ChatRequest,
    ConversationReference,
    DataAgentContext,
    DataMessage,
    DataQuery,
    DataResult,
    ErrorMessage,
    ExampleQueries,
    ListMessagesRequest,
    ListMessagesResponse,
    LookerQuery,
    Message,
    SchemaMessage,
    SchemaQuery,
    SchemaResult,
    StorageMessage,
    SystemMessage,
    TextMessage,
    UserMessage,
)
from .types.datasource import (
    BigQueryTableReference,
    BigQueryTableReferences,
    DataFilter,
    DataFilterType,
    Datasource,
    DatasourceReferences,
    Field,
    LookerExploreReference,
    LookerExploreReferences,
    PrivateLookerInstanceInfo,
    Schema,
    StudioDatasourceReference,
    StudioDatasourceReferences,
)

__all__ = (
    "DataAgentServiceAsyncClient",
    "DataChatServiceAsyncClient",
    "AnalysisEvent",
    "AnalysisMessage",
    "AnalysisOptions",
    "AnalysisQuery",
    "BigQueryJob",
    "BigQueryTableReference",
    "BigQueryTableReferences",
    "Blob",
    "ChartMessage",
    "ChartOptions",
    "ChartQuery",
    "ChartResult",
    "ChatRequest",
    "Context",
    "Conversation",
    "ConversationOptions",
    "ConversationReference",
    "CreateConversationRequest",
    "CreateDataAgentRequest",
    "Credentials",
    "DataAgent",
    "DataAgentContext",
    "DataAgentServiceClient",
    "DataAnalyticsAgent",
    "DataChatServiceClient",
    "DataFilter",
    "DataFilterType",
    "DataMessage",
    "DataQuery",
    "DataResult",
    "Datasource",
    "DatasourceReferences",
    "DeleteDataAgentRequest",
    "ErrorMessage",
    "ExampleQueries",
    "ExampleQuery",
    "Field",
    "GetConversationRequest",
    "GetDataAgentRequest",
    "ListAccessibleDataAgentsRequest",
    "ListAccessibleDataAgentsResponse",
    "ListConversationsRequest",
    "ListConversationsResponse",
    "ListDataAgentsRequest",
    "ListDataAgentsResponse",
    "ListMessagesRequest",
    "ListMessagesResponse",
    "LookerExploreReference",
    "LookerExploreReferences",
    "LookerQuery",
    "Message",
    "OAuthCredentials",
    "OperationMetadata",
    "PrivateLookerInstanceInfo",
    "Schema",
    "SchemaMessage",
    "SchemaQuery",
    "SchemaResult",
    "StorageMessage",
    "StudioDatasourceReference",
    "StudioDatasourceReferences",
    "SystemMessage",
    "TextMessage",
    "UpdateConversationRequest",
    "UpdateDataAgentRequest",
    "UserMessage",
)
