# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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

from google.cloud.ces_v1 import gapic_version as package_version

__version__ = package_version.__version__

from importlib import metadata

# PEP 0810: Explicit Lazy Imports
# Python 3.15+ natively intercepts and defers these imports.
# Developers can disable this behavior and force eager imports.
# For more information, see:
# https://docs.python.org/3.15/library/sys.html#sys.set_lazy_imports_filter
# Older Python versions safely ignore this variable.
__lazy_modules__ = {
    "google.cloud.ces_v1.services.agent_service",
    "google.cloud.ces_v1.services.session_service",
    "google.cloud.ces_v1.services.tool_service",
    "google.cloud.ces_v1.services.widget_service",
    "google.cloud.ces_v1.types.agent",
    "google.cloud.ces_v1.types.agent_card",
    "google.cloud.ces_v1.types.agent_service",
    "google.cloud.ces_v1.types.agent_tool",
    "google.cloud.ces_v1.types.agent_transfers",
    "google.cloud.ces_v1.types.app",
    "google.cloud.ces_v1.types.app_version",
    "google.cloud.ces_v1.types.auth",
    "google.cloud.ces_v1.types.bigquery_export",
    "google.cloud.ces_v1.types.changelog",
    "google.cloud.ces_v1.types.client_function",
    "google.cloud.ces_v1.types.common",
    "google.cloud.ces_v1.types.connector_tool",
    "google.cloud.ces_v1.types.connector_toolset",
    "google.cloud.ces_v1.types.conversation",
    "google.cloud.ces_v1.types.data_store",
    "google.cloud.ces_v1.types.data_store_tool",
    "google.cloud.ces_v1.types.deployment",
    "google.cloud.ces_v1.types.example",
    "google.cloud.ces_v1.types.fakes",
    "google.cloud.ces_v1.types.file_search_tool",
    "google.cloud.ces_v1.types.google_search_tool",
    "google.cloud.ces_v1.types.guardrail",
    "google.cloud.ces_v1.types.mcp_tool",
    "google.cloud.ces_v1.types.mcp_toolset",
    "google.cloud.ces_v1.types.mocks",
    "google.cloud.ces_v1.types.omnichannel",
    "google.cloud.ces_v1.types.omnichannel_service",
    "google.cloud.ces_v1.types.open_api_tool",
    "google.cloud.ces_v1.types.open_api_toolset",
    "google.cloud.ces_v1.types.python_function",
    "google.cloud.ces_v1.types.schema",
    "google.cloud.ces_v1.types.search_suggestions",
    "google.cloud.ces_v1.types.security_settings",
    "google.cloud.ces_v1.types.session_service",
    "google.cloud.ces_v1.types.system_tool",
    "google.cloud.ces_v1.types.tool",
    "google.cloud.ces_v1.types.tool_service",
    "google.cloud.ces_v1.types.toolset",
    "google.cloud.ces_v1.types.toolset_tool",
    "google.cloud.ces_v1.types.widget_service",
    "google.cloud.ces_v1.types.widget_tool",
}


from .services.agent_service import AgentServiceAsyncClient, AgentServiceClient
from .services.session_service import SessionServiceAsyncClient, SessionServiceClient
from .services.tool_service import ToolServiceAsyncClient, ToolServiceClient
from .services.widget_service import WidgetServiceAsyncClient, WidgetServiceClient
from .types.agent import Agent
from .types.agent_card import AgentCard, AgentInterface, AgentSkill, RemoteAgentTool
from .types.agent_service import (
    BatchDeleteConversationsRequest,
    BatchDeleteConversationsResponse,
    CreateAgentRequest,
    CreateAppRequest,
    CreateAppVersionRequest,
    CreateDeploymentRequest,
    CreateExampleRequest,
    CreateGuardrailRequest,
    CreateToolRequest,
    CreateToolsetRequest,
    DeleteAgentRequest,
    DeleteAppRequest,
    DeleteAppVersionRequest,
    DeleteConversationRequest,
    DeleteDeploymentRequest,
    DeleteExampleRequest,
    DeleteGuardrailRequest,
    DeleteToolRequest,
    DeleteToolsetRequest,
    ExportAppRequest,
    ExportAppResponse,
    GetAgentRequest,
    GetAppRequest,
    GetAppVersionRequest,
    GetChangelogRequest,
    GetConversationRequest,
    GetDeploymentRequest,
    GetExampleRequest,
    GetGuardrailRequest,
    GetToolRequest,
    GetToolsetRequest,
    ImportAppRequest,
    ImportAppResponse,
    ListAgentsRequest,
    ListAgentsResponse,
    ListAppsRequest,
    ListAppsResponse,
    ListAppVersionsRequest,
    ListAppVersionsResponse,
    ListChangelogsRequest,
    ListChangelogsResponse,
    ListConversationsRequest,
    ListConversationsResponse,
    ListDeploymentsRequest,
    ListDeploymentsResponse,
    ListExamplesRequest,
    ListExamplesResponse,
    ListGuardrailsRequest,
    ListGuardrailsResponse,
    ListToolsetsRequest,
    ListToolsetsResponse,
    ListToolsRequest,
    ListToolsResponse,
    OperationMetadata,
    RestoreAppVersionRequest,
    RestoreAppVersionResponse,
    UpdateAgentRequest,
    UpdateAppRequest,
    UpdateDeploymentRequest,
    UpdateExampleRequest,
    UpdateGuardrailRequest,
    UpdateToolRequest,
    UpdateToolsetRequest,
)
from .types.agent_tool import AgentTool
from .types.agent_transfers import (
    ExpressionCondition,
    PythonCodeCondition,
    TransferRule,
)
from .types.app import (
    AmbientSoundConfig,
    App,
    AudioProcessingConfig,
    AudioRecordingConfig,
    BargeInConfig,
    ClientCertificateSettings,
    CloudLoggingSettings,
    ConversationLoggingSettings,
    DataStoreSettings,
    ErrorHandlingSettings,
    EvaluationMetricsThresholds,
    LanguageSettings,
    LoggingSettings,
    MetricAnalysisSettings,
    RedactionConfig,
    SynthesizeSpeechConfig,
    TimeZoneSettings,
    VpcScSettings,
)
from .types.app_version import AppSnapshot, AppVersion
from .types.auth import (
    ApiAuthentication,
    ApiKeyConfig,
    BearerTokenConfig,
    EndUserAuthConfig,
    OAuthConfig,
    ServiceAccountAuthConfig,
    ServiceAgentIdTokenAuthConfig,
)
from .types.bigquery_export import BigQueryExportSettings
from .types.changelog import Changelog
from .types.client_function import ClientFunction
from .types.common import (
    Callback,
    ChannelProfile,
    ExecutionType,
    ModelSettings,
    ServiceDirectoryConfig,
    Span,
    TlsConfig,
    TriggerAction,
)
from .types.connector_tool import Action, ConnectorTool
from .types.connector_toolset import ConnectorToolset
from .types.conversation import Conversation
from .types.data_store import DataStore
from .types.data_store_tool import DataStoreTool
from .types.deployment import (
    Deployment,
    ExperimentConfig,
    InstagramCredentials,
    WhatsAppCredentials,
)
from .types.example import (
    AgentTransfer,
    Blob,
    Chunk,
    Example,
    Image,
    Message,
    ToolCall,
    ToolResponse,
)
from .types.fakes import CodeBlock, ToolFakeConfig
from .types.file_search_tool import FileSearchTool
from .types.google_search_tool import GoogleSearchTool
from .types.guardrail import Guardrail
from .types.mcp_tool import McpTool
from .types.mcp_toolset import McpToolDefinition, McpToolOverride, McpToolset
from .types.mocks import MockedToolCall
from .types.omnichannel import Omnichannel, OmnichannelIntegrationConfig
from .types.omnichannel_service import OmnichannelOperationMetadata
from .types.open_api_tool import OpenApiTool
from .types.open_api_toolset import OpenApiToolset
from .types.python_function import PythonFunction
from .types.schema import Schema
from .types.search_suggestions import GoogleSearchSuggestions, WebSearchQuery
from .types.security_settings import EndpointControlPolicy, SecuritySettings
from .types.session_service import (
    AudioEncoding,
    BidiSessionClientMessage,
    BidiSessionServerMessage,
    Citations,
    EndSession,
    Event,
    GoAway,
    InputAudioConfig,
    InterruptionSignal,
    MockConfig,
    OutputAudioConfig,
    RecognitionResult,
    RunSessionRequest,
    RunSessionResponse,
    SessionConfig,
    SessionInput,
    SessionOutput,
    ToolCalls,
    ToolResponses,
)
from .types.system_tool import SystemTool
from .types.tool import Tool
from .types.tool_service import (
    ExecuteToolRequest,
    ExecuteToolResponse,
    RetrieveToolSchemaRequest,
    RetrieveToolSchemaResponse,
    RetrieveToolsRequest,
    RetrieveToolsResponse,
)
from .types.toolset import Toolset
from .types.toolset_tool import ToolsetTool
from .types.widget_service import GenerateChatTokenRequest, GenerateChatTokenResponse
from .types.widget_tool import WidgetTool

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.ces_v1")  # type: ignore
    api_core.check_dependency_versions("google.cloud.ces_v1")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.ces_v1"
        if sys.version_info < (3, 10):
            warnings.warn(
                "You are using a non-supported Python version "
                + f"({_py_version_str}).  Google will not post any further "
                + f"updates to {_package_label} supporting this Python version. "
                + "Please upgrade to the latest Python version, or at "
                + f"least to Python 3.10, and then update {_package_label}.",
                FutureWarning,
            )

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "6.33.5" -> (6, 33, 5)
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
        _next_supported_version = "6.33.5"
        _next_supported_version_tuple = (6, 33, 5)
        _recommendation = " (we recommend 7.x)"
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
    "AgentServiceAsyncClient",
    "SessionServiceAsyncClient",
    "ToolServiceAsyncClient",
    "WidgetServiceAsyncClient",
    "Action",
    "Agent",
    "AgentCard",
    "AgentInterface",
    "AgentServiceClient",
    "AgentSkill",
    "AgentTool",
    "AgentTransfer",
    "AmbientSoundConfig",
    "ApiAuthentication",
    "ApiKeyConfig",
    "App",
    "AppSnapshot",
    "AppVersion",
    "AudioEncoding",
    "AudioProcessingConfig",
    "AudioRecordingConfig",
    "BargeInConfig",
    "BatchDeleteConversationsRequest",
    "BatchDeleteConversationsResponse",
    "BearerTokenConfig",
    "BidiSessionClientMessage",
    "BidiSessionServerMessage",
    "BigQueryExportSettings",
    "Blob",
    "Callback",
    "Changelog",
    "ChannelProfile",
    "Chunk",
    "Citations",
    "ClientCertificateSettings",
    "ClientFunction",
    "CloudLoggingSettings",
    "CodeBlock",
    "ConnectorTool",
    "ConnectorToolset",
    "Conversation",
    "ConversationLoggingSettings",
    "CreateAgentRequest",
    "CreateAppRequest",
    "CreateAppVersionRequest",
    "CreateDeploymentRequest",
    "CreateExampleRequest",
    "CreateGuardrailRequest",
    "CreateToolRequest",
    "CreateToolsetRequest",
    "DataStore",
    "DataStoreSettings",
    "DataStoreTool",
    "DeleteAgentRequest",
    "DeleteAppRequest",
    "DeleteAppVersionRequest",
    "DeleteConversationRequest",
    "DeleteDeploymentRequest",
    "DeleteExampleRequest",
    "DeleteGuardrailRequest",
    "DeleteToolRequest",
    "DeleteToolsetRequest",
    "Deployment",
    "EndSession",
    "EndUserAuthConfig",
    "EndpointControlPolicy",
    "ErrorHandlingSettings",
    "EvaluationMetricsThresholds",
    "Event",
    "Example",
    "ExecuteToolRequest",
    "ExecuteToolResponse",
    "ExecutionType",
    "ExperimentConfig",
    "ExportAppRequest",
    "ExportAppResponse",
    "ExpressionCondition",
    "FileSearchTool",
    "GenerateChatTokenRequest",
    "GenerateChatTokenResponse",
    "GetAgentRequest",
    "GetAppRequest",
    "GetAppVersionRequest",
    "GetChangelogRequest",
    "GetConversationRequest",
    "GetDeploymentRequest",
    "GetExampleRequest",
    "GetGuardrailRequest",
    "GetToolRequest",
    "GetToolsetRequest",
    "GoAway",
    "GoogleSearchSuggestions",
    "GoogleSearchTool",
    "Guardrail",
    "Image",
    "ImportAppRequest",
    "ImportAppResponse",
    "InputAudioConfig",
    "InstagramCredentials",
    "InterruptionSignal",
    "LanguageSettings",
    "ListAgentsRequest",
    "ListAgentsResponse",
    "ListAppVersionsRequest",
    "ListAppVersionsResponse",
    "ListAppsRequest",
    "ListAppsResponse",
    "ListChangelogsRequest",
    "ListChangelogsResponse",
    "ListConversationsRequest",
    "ListConversationsResponse",
    "ListDeploymentsRequest",
    "ListDeploymentsResponse",
    "ListExamplesRequest",
    "ListExamplesResponse",
    "ListGuardrailsRequest",
    "ListGuardrailsResponse",
    "ListToolsRequest",
    "ListToolsResponse",
    "ListToolsetsRequest",
    "ListToolsetsResponse",
    "LoggingSettings",
    "McpTool",
    "McpToolDefinition",
    "McpToolOverride",
    "McpToolset",
    "Message",
    "MetricAnalysisSettings",
    "MockConfig",
    "MockedToolCall",
    "ModelSettings",
    "OAuthConfig",
    "Omnichannel",
    "OmnichannelIntegrationConfig",
    "OmnichannelOperationMetadata",
    "OpenApiTool",
    "OpenApiToolset",
    "OperationMetadata",
    "OutputAudioConfig",
    "PythonCodeCondition",
    "PythonFunction",
    "RecognitionResult",
    "RedactionConfig",
    "RemoteAgentTool",
    "RestoreAppVersionRequest",
    "RestoreAppVersionResponse",
    "RetrieveToolSchemaRequest",
    "RetrieveToolSchemaResponse",
    "RetrieveToolsRequest",
    "RetrieveToolsResponse",
    "RunSessionRequest",
    "RunSessionResponse",
    "Schema",
    "SecuritySettings",
    "ServiceAccountAuthConfig",
    "ServiceAgentIdTokenAuthConfig",
    "ServiceDirectoryConfig",
    "SessionConfig",
    "SessionInput",
    "SessionOutput",
    "SessionServiceClient",
    "Span",
    "SynthesizeSpeechConfig",
    "SystemTool",
    "TimeZoneSettings",
    "TlsConfig",
    "Tool",
    "ToolCall",
    "ToolCalls",
    "ToolFakeConfig",
    "ToolResponse",
    "ToolResponses",
    "ToolServiceClient",
    "Toolset",
    "ToolsetTool",
    "TransferRule",
    "TriggerAction",
    "UpdateAgentRequest",
    "UpdateAppRequest",
    "UpdateDeploymentRequest",
    "UpdateExampleRequest",
    "UpdateGuardrailRequest",
    "UpdateToolRequest",
    "UpdateToolsetRequest",
    "VpcScSettings",
    "WebSearchQuery",
    "WhatsAppCredentials",
    "WidgetServiceClient",
    "WidgetTool",
)
