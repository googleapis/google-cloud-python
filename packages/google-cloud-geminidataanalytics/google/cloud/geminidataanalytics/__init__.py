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
from google.cloud.geminidataanalytics import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.geminidataanalytics_v1alpha.services.context_retrieval_service.async_client import (
    ContextRetrievalServiceAsyncClient,
)
from google.cloud.geminidataanalytics_v1alpha.services.context_retrieval_service.client import (
    ContextRetrievalServiceClient,
)
from google.cloud.geminidataanalytics_v1alpha.services.data_agent_service.async_client import (
    DataAgentServiceAsyncClient,
)
from google.cloud.geminidataanalytics_v1alpha.services.data_agent_service.client import (
    DataAgentServiceClient,
)
from google.cloud.geminidataanalytics_v1alpha.services.data_chat_service.async_client import (
    DataChatServiceAsyncClient,
)
from google.cloud.geminidataanalytics_v1alpha.services.data_chat_service.client import (
    DataChatServiceClient,
)
from google.cloud.geminidataanalytics_v1alpha.types.context import (
    AnalysisOptions,
    ChartOptions,
    Context,
    ConversationOptions,
)
from google.cloud.geminidataanalytics_v1alpha.types.context_retrieval_service import (
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
from google.cloud.geminidataanalytics_v1alpha.types.conversation import (
    Conversation,
    CreateConversationRequest,
    GetConversationRequest,
    ListConversationsRequest,
    ListConversationsResponse,
)
from google.cloud.geminidataanalytics_v1alpha.types.credentials import (
    Credentials,
    OAuthCredentials,
)
from google.cloud.geminidataanalytics_v1alpha.types.data_agent import DataAgent
from google.cloud.geminidataanalytics_v1alpha.types.data_agent_service import (
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
from google.cloud.geminidataanalytics_v1alpha.types.data_analytics_agent import (
    DataAnalyticsAgent,
)
from google.cloud.geminidataanalytics_v1alpha.types.data_chat_service import (
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
from google.cloud.geminidataanalytics_v1alpha.types.datasource import (
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
    "ContextRetrievalServiceClient",
    "ContextRetrievalServiceAsyncClient",
    "DataAgentServiceClient",
    "DataAgentServiceAsyncClient",
    "DataChatServiceClient",
    "DataChatServiceAsyncClient",
    "AnalysisOptions",
    "ChartOptions",
    "Context",
    "ConversationOptions",
    "DirectLookup",
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
    "TableCandidate",
    "Conversation",
    "CreateConversationRequest",
    "GetConversationRequest",
    "ListConversationsRequest",
    "ListConversationsResponse",
    "Credentials",
    "OAuthCredentials",
    "DataAgent",
    "CreateDataAgentRequest",
    "DeleteDataAgentRequest",
    "GetDataAgentRequest",
    "ListAccessibleDataAgentsRequest",
    "ListAccessibleDataAgentsResponse",
    "ListDataAgentsRequest",
    "ListDataAgentsResponse",
    "OperationMetadata",
    "UpdateDataAgentRequest",
    "DataAnalyticsAgent",
    "AnalysisEvent",
    "AnalysisMessage",
    "AnalysisQuery",
    "BigQueryJob",
    "Blob",
    "ChartMessage",
    "ChartQuery",
    "ChartResult",
    "ChatRequest",
    "ConversationReference",
    "DataAgentContext",
    "DataMessage",
    "DataQuery",
    "DataResult",
    "ErrorMessage",
    "ListMessagesRequest",
    "ListMessagesResponse",
    "LookerQuery",
    "Message",
    "SchemaMessage",
    "SchemaQuery",
    "SchemaResult",
    "StorageMessage",
    "SystemMessage",
    "TextMessage",
    "UserMessage",
    "BigQueryTableReference",
    "BigQueryTableReferences",
    "Datasource",
    "DatasourceReferences",
    "Field",
    "LookerExploreReference",
    "LookerExploreReferences",
    "PrivateLookerInstanceInfo",
    "Schema",
    "StudioDatasourceReference",
    "StudioDatasourceReferences",
)
