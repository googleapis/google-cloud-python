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


from .services.context_retrieval_service import (
    ContextRetrievalServiceAsyncClient,
    ContextRetrievalServiceClient,
)
from .services.data_agent_service import (
    DataAgentServiceAsyncClient,
    DataAgentServiceClient,
)
from .services.data_chat_service import (
    DataChatServiceAsyncClient,
    DataChatServiceClient,
)
from .types.context import AnalysisOptions, ChartOptions, Context, ConversationOptions
from .types.context_retrieval_service import (
    DirectLookup,
    RetrieveBigQueryRecentRelevantTablesRequest,
    RetrieveBigQueryRecentRelevantTablesResponse,
    RetrieveBigQueryTableContextRequest,
    RetrieveBigQueryTableContextResponse,
    RetrieveBigQueryTableContextsFromRecentTablesRequest,
    RetrieveBigQueryTableContextsFromRecentTablesResponse,
    RetrieveBigQueryTableContextsRequest,
    RetrieveBigQueryTableContextsResponse,
    RetrieveBigQueryTableSuggestedDescriptionsRequest,
    RetrieveBigQueryTableSuggestedDescriptionsResponse,
    RetrieveBigQueryTableSuggestedExamplesRequest,
    RetrieveBigQueryTableSuggestedExamplesResponse,
    TableCandidate,
)
from .types.conversation import (
    Conversation,
    CreateConversationRequest,
    GetConversationRequest,
    ListConversationsRequest,
    ListConversationsResponse,
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
    "ContextRetrievalServiceAsyncClient",
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
    "ContextRetrievalServiceClient",
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
    "DataMessage",
    "DataQuery",
    "DataResult",
    "Datasource",
    "DatasourceReferences",
    "DeleteDataAgentRequest",
    "DirectLookup",
    "ErrorMessage",
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
    "RetrieveBigQueryRecentRelevantTablesRequest",
    "RetrieveBigQueryRecentRelevantTablesResponse",
    "RetrieveBigQueryTableContextRequest",
    "RetrieveBigQueryTableContextResponse",
    "RetrieveBigQueryTableContextsFromRecentTablesRequest",
    "RetrieveBigQueryTableContextsFromRecentTablesResponse",
    "RetrieveBigQueryTableContextsRequest",
    "RetrieveBigQueryTableContextsResponse",
    "RetrieveBigQueryTableSuggestedDescriptionsRequest",
    "RetrieveBigQueryTableSuggestedDescriptionsResponse",
    "RetrieveBigQueryTableSuggestedExamplesRequest",
    "RetrieveBigQueryTableSuggestedExamplesResponse",
    "Schema",
    "SchemaMessage",
    "SchemaQuery",
    "SchemaResult",
    "StorageMessage",
    "StudioDatasourceReference",
    "StudioDatasourceReferences",
    "SystemMessage",
    "TableCandidate",
    "TextMessage",
    "UpdateDataAgentRequest",
    "UserMessage",
)
