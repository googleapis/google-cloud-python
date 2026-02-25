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

from google.cloud.ces_v1beta import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.agent_service import AgentServiceAsyncClient, AgentServiceClient
from .services.evaluation_service import (
    EvaluationServiceAsyncClient,
    EvaluationServiceClient,
)
from .services.session_service import SessionServiceAsyncClient, SessionServiceClient
from .services.tool_service import ToolServiceAsyncClient, ToolServiceClient
from .services.widget_service import WidgetServiceAsyncClient, WidgetServiceClient
from .types.agent import Agent
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
    GenerateAppResourceResponse,
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
    EvaluationPersona,
    EvaluationSettings,
    LanguageSettings,
    LoggingSettings,
    MetricAnalysisSettings,
    RedactionConfig,
    SynthesizeSpeechConfig,
    TimeZoneSettings,
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
from .types.deployment import Deployment
from .types.evaluation import (
    AggregatedMetrics,
    Evaluation,
    EvaluationConfig,
    EvaluationDataset,
    EvaluationErrorInfo,
    EvaluationExpectation,
    EvaluationResult,
    EvaluationRun,
    LatencyReport,
    OptimizationConfig,
    PersonaRunConfig,
    RunEvaluationRequest,
    ScheduledEvaluationRun,
)
from .types.evaluation_service import (
    CreateEvaluationDatasetRequest,
    CreateEvaluationExpectationRequest,
    CreateEvaluationRequest,
    CreateScheduledEvaluationRunRequest,
    DeleteEvaluationDatasetRequest,
    DeleteEvaluationExpectationRequest,
    DeleteEvaluationRequest,
    DeleteEvaluationResultRequest,
    DeleteEvaluationRunOperationMetadata,
    DeleteEvaluationRunRequest,
    DeleteScheduledEvaluationRunRequest,
    GenerateEvaluationOperationMetadata,
    GenerateEvaluationRequest,
    GetEvaluationDatasetRequest,
    GetEvaluationExpectationRequest,
    GetEvaluationRequest,
    GetEvaluationResultRequest,
    GetEvaluationRunRequest,
    GetScheduledEvaluationRunRequest,
    ImportEvaluationsOperationMetadata,
    ImportEvaluationsRequest,
    ImportEvaluationsResponse,
    ListEvaluationDatasetsRequest,
    ListEvaluationDatasetsResponse,
    ListEvaluationExpectationsRequest,
    ListEvaluationExpectationsResponse,
    ListEvaluationResultsRequest,
    ListEvaluationResultsResponse,
    ListEvaluationRunsRequest,
    ListEvaluationRunsResponse,
    ListEvaluationsRequest,
    ListEvaluationsResponse,
    ListScheduledEvaluationRunsRequest,
    ListScheduledEvaluationRunsResponse,
    RunEvaluationOperationMetadata,
    RunEvaluationResponse,
    TestPersonaVoiceRequest,
    TestPersonaVoiceResponse,
    UpdateEvaluationDatasetRequest,
    UpdateEvaluationExpectationRequest,
    UpdateEvaluationRequest,
    UpdateScheduledEvaluationRunRequest,
    UploadEvaluationAudioRequest,
    UploadEvaluationAudioResponse,
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
from .types.fakes import CodeBlock, EvaluationToolCallBehaviour, ToolFakeConfig
from .types.file_search_tool import FileSearchTool
from .types.golden_run import GoldenRunMethod
from .types.google_search_tool import GoogleSearchTool
from .types.guardrail import Guardrail
from .types.mcp_tool import McpTool
from .types.mcp_toolset import McpToolset
from .types.omnichannel import Omnichannel, OmnichannelIntegrationConfig
from .types.omnichannel_service import OmnichannelOperationMetadata
from .types.open_api_tool import OpenApiTool
from .types.open_api_toolset import OpenApiToolset
from .types.python_function import PythonFunction
from .types.schema import Schema
from .types.search_suggestions import GoogleSearchSuggestions, WebSearchQuery
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
    api_core.check_python_version("google.cloud.ces_v1beta")  # type: ignore
    api_core.check_dependency_versions("google.cloud.ces_v1beta")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.ces_v1beta"
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
    "AgentServiceAsyncClient",
    "EvaluationServiceAsyncClient",
    "SessionServiceAsyncClient",
    "ToolServiceAsyncClient",
    "WidgetServiceAsyncClient",
    "Action",
    "Agent",
    "AgentServiceClient",
    "AgentTransfer",
    "AggregatedMetrics",
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
    "CreateEvaluationDatasetRequest",
    "CreateEvaluationExpectationRequest",
    "CreateEvaluationRequest",
    "CreateExampleRequest",
    "CreateGuardrailRequest",
    "CreateScheduledEvaluationRunRequest",
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
    "DeleteEvaluationDatasetRequest",
    "DeleteEvaluationExpectationRequest",
    "DeleteEvaluationRequest",
    "DeleteEvaluationResultRequest",
    "DeleteEvaluationRunOperationMetadata",
    "DeleteEvaluationRunRequest",
    "DeleteExampleRequest",
    "DeleteGuardrailRequest",
    "DeleteScheduledEvaluationRunRequest",
    "DeleteToolRequest",
    "DeleteToolsetRequest",
    "Deployment",
    "EndSession",
    "EndUserAuthConfig",
    "ErrorHandlingSettings",
    "Evaluation",
    "EvaluationConfig",
    "EvaluationDataset",
    "EvaluationErrorInfo",
    "EvaluationExpectation",
    "EvaluationMetricsThresholds",
    "EvaluationPersona",
    "EvaluationResult",
    "EvaluationRun",
    "EvaluationServiceClient",
    "EvaluationSettings",
    "EvaluationToolCallBehaviour",
    "Event",
    "Example",
    "ExecuteToolRequest",
    "ExecuteToolResponse",
    "ExecutionType",
    "ExportAppRequest",
    "ExportAppResponse",
    "ExpressionCondition",
    "FileSearchTool",
    "GenerateAppResourceResponse",
    "GenerateChatTokenRequest",
    "GenerateChatTokenResponse",
    "GenerateEvaluationOperationMetadata",
    "GenerateEvaluationRequest",
    "GetAgentRequest",
    "GetAppRequest",
    "GetAppVersionRequest",
    "GetChangelogRequest",
    "GetConversationRequest",
    "GetDeploymentRequest",
    "GetEvaluationDatasetRequest",
    "GetEvaluationExpectationRequest",
    "GetEvaluationRequest",
    "GetEvaluationResultRequest",
    "GetEvaluationRunRequest",
    "GetExampleRequest",
    "GetGuardrailRequest",
    "GetScheduledEvaluationRunRequest",
    "GetToolRequest",
    "GetToolsetRequest",
    "GoAway",
    "GoldenRunMethod",
    "GoogleSearchSuggestions",
    "GoogleSearchTool",
    "Guardrail",
    "Image",
    "ImportAppRequest",
    "ImportAppResponse",
    "ImportEvaluationsOperationMetadata",
    "ImportEvaluationsRequest",
    "ImportEvaluationsResponse",
    "InputAudioConfig",
    "InterruptionSignal",
    "LanguageSettings",
    "LatencyReport",
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
    "ListEvaluationDatasetsRequest",
    "ListEvaluationDatasetsResponse",
    "ListEvaluationExpectationsRequest",
    "ListEvaluationExpectationsResponse",
    "ListEvaluationResultsRequest",
    "ListEvaluationResultsResponse",
    "ListEvaluationRunsRequest",
    "ListEvaluationRunsResponse",
    "ListEvaluationsRequest",
    "ListEvaluationsResponse",
    "ListExamplesRequest",
    "ListExamplesResponse",
    "ListGuardrailsRequest",
    "ListGuardrailsResponse",
    "ListScheduledEvaluationRunsRequest",
    "ListScheduledEvaluationRunsResponse",
    "ListToolsRequest",
    "ListToolsResponse",
    "ListToolsetsRequest",
    "ListToolsetsResponse",
    "LoggingSettings",
    "McpTool",
    "McpToolset",
    "Message",
    "MetricAnalysisSettings",
    "ModelSettings",
    "OAuthConfig",
    "Omnichannel",
    "OmnichannelIntegrationConfig",
    "OmnichannelOperationMetadata",
    "OpenApiTool",
    "OpenApiToolset",
    "OperationMetadata",
    "OptimizationConfig",
    "OutputAudioConfig",
    "PersonaRunConfig",
    "PythonCodeCondition",
    "PythonFunction",
    "RecognitionResult",
    "RedactionConfig",
    "RestoreAppVersionRequest",
    "RestoreAppVersionResponse",
    "RetrieveToolSchemaRequest",
    "RetrieveToolSchemaResponse",
    "RetrieveToolsRequest",
    "RetrieveToolsResponse",
    "RunEvaluationOperationMetadata",
    "RunEvaluationRequest",
    "RunEvaluationResponse",
    "RunSessionRequest",
    "RunSessionResponse",
    "ScheduledEvaluationRun",
    "Schema",
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
    "TestPersonaVoiceRequest",
    "TestPersonaVoiceResponse",
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
    "UpdateEvaluationDatasetRequest",
    "UpdateEvaluationExpectationRequest",
    "UpdateEvaluationRequest",
    "UpdateExampleRequest",
    "UpdateGuardrailRequest",
    "UpdateScheduledEvaluationRunRequest",
    "UpdateToolRequest",
    "UpdateToolsetRequest",
    "UploadEvaluationAudioRequest",
    "UploadEvaluationAudioResponse",
    "WebSearchQuery",
    "WidgetServiceClient",
    "WidgetTool",
)
