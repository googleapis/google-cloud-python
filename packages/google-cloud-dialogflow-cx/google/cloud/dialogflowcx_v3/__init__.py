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

from google.cloud.dialogflowcx_v3 import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.agents import AgentsAsyncClient, AgentsClient
from .services.changelogs import ChangelogsAsyncClient, ChangelogsClient
from .services.deployments import DeploymentsAsyncClient, DeploymentsClient
from .services.entity_types import EntityTypesAsyncClient, EntityTypesClient
from .services.environments import EnvironmentsAsyncClient, EnvironmentsClient
from .services.examples import ExamplesAsyncClient, ExamplesClient
from .services.experiments import ExperimentsAsyncClient, ExperimentsClient
from .services.flows import FlowsAsyncClient, FlowsClient
from .services.generators import GeneratorsAsyncClient, GeneratorsClient
from .services.intents import IntentsAsyncClient, IntentsClient
from .services.pages import PagesAsyncClient, PagesClient
from .services.playbooks import PlaybooksAsyncClient, PlaybooksClient
from .services.security_settings_service import (
    SecuritySettingsServiceAsyncClient,
    SecuritySettingsServiceClient,
)
from .services.session_entity_types import (
    SessionEntityTypesAsyncClient,
    SessionEntityTypesClient,
)
from .services.sessions import SessionsAsyncClient, SessionsClient
from .services.test_cases import TestCasesAsyncClient, TestCasesClient
from .services.tools import ToolsAsyncClient, ToolsClient
from .services.transition_route_groups import (
    TransitionRouteGroupsAsyncClient,
    TransitionRouteGroupsClient,
)
from .services.versions import VersionsAsyncClient, VersionsClient
from .services.webhooks import WebhooksAsyncClient, WebhooksClient
from .types.advanced_settings import AdvancedSettings
from .types.agent import (
    Agent,
    AgentValidationResult,
    CreateAgentRequest,
    DeleteAgentRequest,
    ExportAgentRequest,
    ExportAgentResponse,
    GetAgentRequest,
    GetAgentValidationResultRequest,
    GetGenerativeSettingsRequest,
    ListAgentsRequest,
    ListAgentsResponse,
    RestoreAgentRequest,
    SpeechToTextSettings,
    UpdateAgentRequest,
    UpdateGenerativeSettingsRequest,
    ValidateAgentRequest,
)
from .types.audio_config import (
    AudioEncoding,
    BargeInConfig,
    InputAudioConfig,
    OutputAudioConfig,
    OutputAudioEncoding,
    SpeechModelVariant,
    SpeechWordInfo,
    SsmlVoiceGender,
    SynthesizeSpeechConfig,
    TextToSpeechSettings,
    VoiceSelectionParams,
)
from .types.changelog import (
    Changelog,
    GetChangelogRequest,
    ListChangelogsRequest,
    ListChangelogsResponse,
)
from .types.code_block import CodeBlock
from .types.data_store_connection import (
    DataStoreConnection,
    DataStoreConnectionSignals,
    DataStoreType,
    DocumentProcessingMode,
)
from .types.deployment import (
    Deployment,
    GetDeploymentRequest,
    ListDeploymentsRequest,
    ListDeploymentsResponse,
)
from .types.entity_type import (
    CreateEntityTypeRequest,
    DeleteEntityTypeRequest,
    EntityType,
    ExportEntityTypesMetadata,
    ExportEntityTypesRequest,
    ExportEntityTypesResponse,
    GetEntityTypeRequest,
    ImportEntityTypesMetadata,
    ImportEntityTypesRequest,
    ImportEntityTypesResponse,
    ListEntityTypesRequest,
    ListEntityTypesResponse,
    UpdateEntityTypeRequest,
)
from .types.environment import (
    ContinuousTestResult,
    CreateEnvironmentRequest,
    DeleteEnvironmentRequest,
    DeployFlowMetadata,
    DeployFlowRequest,
    DeployFlowResponse,
    Environment,
    GetEnvironmentRequest,
    ListContinuousTestResultsRequest,
    ListContinuousTestResultsResponse,
    ListEnvironmentsRequest,
    ListEnvironmentsResponse,
    LookupEnvironmentHistoryRequest,
    LookupEnvironmentHistoryResponse,
    RunContinuousTestMetadata,
    RunContinuousTestRequest,
    RunContinuousTestResponse,
    UpdateEnvironmentRequest,
)
from .types.example import (
    CreateExampleRequest,
    DeleteExampleRequest,
    Example,
    GetExampleRequest,
    ListExamplesRequest,
    ListExamplesResponse,
    UpdateExampleRequest,
)
from .types.experiment import (
    CreateExperimentRequest,
    DeleteExperimentRequest,
    Experiment,
    GetExperimentRequest,
    ListExperimentsRequest,
    ListExperimentsResponse,
    RolloutConfig,
    RolloutState,
    StartExperimentRequest,
    StopExperimentRequest,
    UpdateExperimentRequest,
    VariantsHistory,
    VersionVariants,
)
from .types.flow import (
    CreateFlowRequest,
    DeleteFlowRequest,
    ExportFlowRequest,
    ExportFlowResponse,
    Flow,
    FlowImportStrategy,
    FlowValidationResult,
    GetFlowRequest,
    GetFlowValidationResultRequest,
    ImportFlowRequest,
    ImportFlowResponse,
    ListFlowsRequest,
    ListFlowsResponse,
    NluSettings,
    TrainFlowRequest,
    UpdateFlowRequest,
    ValidateFlowRequest,
)
from .types.fulfillment import Fulfillment
from .types.gcs import GcsDestination
from .types.generative_settings import GenerativeSettings, LlmModelSettings
from .types.generator import (
    CreateGeneratorRequest,
    DeleteGeneratorRequest,
    Generator,
    GetGeneratorRequest,
    ListGeneratorsRequest,
    ListGeneratorsResponse,
    Phrase,
    UpdateGeneratorRequest,
)
from .types.import_strategy import ImportStrategy
from .types.inline import InlineDestination, InlineSource
from .types.intent import (
    CreateIntentRequest,
    DeleteIntentRequest,
    ExportIntentsMetadata,
    ExportIntentsRequest,
    ExportIntentsResponse,
    GetIntentRequest,
    ImportIntentsMetadata,
    ImportIntentsRequest,
    ImportIntentsResponse,
    Intent,
    IntentView,
    ListIntentsRequest,
    ListIntentsResponse,
    UpdateIntentRequest,
)
from .types.page import (
    CreatePageRequest,
    DeletePageRequest,
    EventHandler,
    Form,
    GetPageRequest,
    KnowledgeConnectorSettings,
    ListPagesRequest,
    ListPagesResponse,
    Page,
    TransitionRoute,
    UpdatePageRequest,
)
from .types.parameter_definition import (
    DataType,
    InlineSchema,
    ParameterDefinition,
    TypeSchema,
)
from .types.playbook import (
    CreatePlaybookRequest,
    CreatePlaybookVersionRequest,
    DeletePlaybookRequest,
    DeletePlaybookVersionRequest,
    ExportPlaybookRequest,
    ExportPlaybookResponse,
    GetPlaybookRequest,
    GetPlaybookVersionRequest,
    Handler,
    ImportPlaybookRequest,
    ImportPlaybookResponse,
    ListPlaybooksRequest,
    ListPlaybooksResponse,
    ListPlaybookVersionsRequest,
    ListPlaybookVersionsResponse,
    Playbook,
    PlaybookImportStrategy,
    PlaybookVersion,
    RestorePlaybookVersionRequest,
    RestorePlaybookVersionResponse,
    UpdatePlaybookRequest,
)
from .types.response_message import ResponseMessage
from .types.safety_settings import SafetySettings
from .types.security_settings import (
    CreateSecuritySettingsRequest,
    DeleteSecuritySettingsRequest,
    GetSecuritySettingsRequest,
    ListSecuritySettingsRequest,
    ListSecuritySettingsResponse,
    SecuritySettings,
    UpdateSecuritySettingsRequest,
)
from .types.session import (
    AnswerFeedback,
    AudioInput,
    BoostSpec,
    BoostSpecs,
    CloudConversationDebuggingInfo,
    DetectIntentRequest,
    DetectIntentResponse,
    DetectIntentResponseView,
    DtmfInput,
    EventInput,
    FilterSpecs,
    FulfillIntentRequest,
    FulfillIntentResponse,
    IntentInput,
    Match,
    MatchIntentRequest,
    MatchIntentResponse,
    QueryInput,
    QueryParameters,
    QueryResult,
    SearchConfig,
    SentimentAnalysisResult,
    StreamingDetectIntentRequest,
    StreamingDetectIntentResponse,
    StreamingRecognitionResult,
    SubmitAnswerFeedbackRequest,
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
from .types.test_case import (
    BatchDeleteTestCasesRequest,
    BatchRunTestCasesMetadata,
    BatchRunTestCasesRequest,
    BatchRunTestCasesResponse,
    CalculateCoverageRequest,
    CalculateCoverageResponse,
    ConversationTurn,
    CreateTestCaseRequest,
    ExportTestCasesMetadata,
    ExportTestCasesRequest,
    ExportTestCasesResponse,
    GetTestCaseRequest,
    GetTestCaseResultRequest,
    ImportTestCasesMetadata,
    ImportTestCasesRequest,
    ImportTestCasesResponse,
    IntentCoverage,
    ListTestCaseResultsRequest,
    ListTestCaseResultsResponse,
    ListTestCasesRequest,
    ListTestCasesResponse,
    RunTestCaseMetadata,
    RunTestCaseRequest,
    RunTestCaseResponse,
    TestCase,
    TestCaseError,
    TestCaseResult,
    TestConfig,
    TestError,
    TestResult,
    TestRunDifference,
    TransitionCoverage,
    TransitionRouteGroupCoverage,
    UpdateTestCaseRequest,
)
from .types.tool import (
    CreateToolRequest,
    CreateToolVersionRequest,
    DeleteToolRequest,
    DeleteToolVersionRequest,
    GetToolRequest,
    GetToolVersionRequest,
    ListToolsRequest,
    ListToolsResponse,
    ListToolVersionsRequest,
    ListToolVersionsResponse,
    RestoreToolVersionRequest,
    RestoreToolVersionResponse,
    Tool,
    ToolVersion,
    UpdateToolRequest,
)
from .types.tool_call import ToolCall, ToolCallResult
from .types.trace import (
    Action,
    AgentUtterance,
    FlowInvocation,
    FlowTransition,
    OutputState,
    PlaybookInput,
    PlaybookInvocation,
    PlaybookOutput,
    PlaybookTransition,
    ToolUse,
    UserUtterance,
)
from .types.transition_route_group import (
    CreateTransitionRouteGroupRequest,
    DeleteTransitionRouteGroupRequest,
    GetTransitionRouteGroupRequest,
    ListTransitionRouteGroupsRequest,
    ListTransitionRouteGroupsResponse,
    TransitionRouteGroup,
    UpdateTransitionRouteGroupRequest,
)
from .types.validation_message import ResourceName, ValidationMessage
from .types.version import (
    CompareVersionsRequest,
    CompareVersionsResponse,
    CreateVersionOperationMetadata,
    CreateVersionRequest,
    DeleteVersionRequest,
    GetVersionRequest,
    ListVersionsRequest,
    ListVersionsResponse,
    LoadVersionRequest,
    UpdateVersionRequest,
    Version,
)
from .types.webhook import (
    CreateWebhookRequest,
    DeleteWebhookRequest,
    GetWebhookRequest,
    LanguageInfo,
    ListWebhooksRequest,
    ListWebhooksResponse,
    PageInfo,
    SessionInfo,
    UpdateWebhookRequest,
    Webhook,
    WebhookRequest,
    WebhookResponse,
)

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.dialogflowcx_v3")  # type: ignore
    api_core.check_dependency_versions("google.cloud.dialogflowcx_v3")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.dialogflowcx_v3"
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
    "ChangelogsAsyncClient",
    "DeploymentsAsyncClient",
    "EntityTypesAsyncClient",
    "EnvironmentsAsyncClient",
    "ExamplesAsyncClient",
    "ExperimentsAsyncClient",
    "FlowsAsyncClient",
    "GeneratorsAsyncClient",
    "IntentsAsyncClient",
    "PagesAsyncClient",
    "PlaybooksAsyncClient",
    "SecuritySettingsServiceAsyncClient",
    "SessionEntityTypesAsyncClient",
    "SessionsAsyncClient",
    "TestCasesAsyncClient",
    "ToolsAsyncClient",
    "TransitionRouteGroupsAsyncClient",
    "VersionsAsyncClient",
    "WebhooksAsyncClient",
    "Action",
    "AdvancedSettings",
    "Agent",
    "AgentUtterance",
    "AgentValidationResult",
    "AgentsClient",
    "AnswerFeedback",
    "AudioEncoding",
    "AudioInput",
    "BargeInConfig",
    "BatchDeleteTestCasesRequest",
    "BatchRunTestCasesMetadata",
    "BatchRunTestCasesRequest",
    "BatchRunTestCasesResponse",
    "BoostSpec",
    "BoostSpecs",
    "CalculateCoverageRequest",
    "CalculateCoverageResponse",
    "Changelog",
    "ChangelogsClient",
    "CloudConversationDebuggingInfo",
    "CodeBlock",
    "CompareVersionsRequest",
    "CompareVersionsResponse",
    "ContinuousTestResult",
    "ConversationTurn",
    "CreateAgentRequest",
    "CreateEntityTypeRequest",
    "CreateEnvironmentRequest",
    "CreateExampleRequest",
    "CreateExperimentRequest",
    "CreateFlowRequest",
    "CreateGeneratorRequest",
    "CreateIntentRequest",
    "CreatePageRequest",
    "CreatePlaybookRequest",
    "CreatePlaybookVersionRequest",
    "CreateSecuritySettingsRequest",
    "CreateSessionEntityTypeRequest",
    "CreateTestCaseRequest",
    "CreateToolRequest",
    "CreateToolVersionRequest",
    "CreateTransitionRouteGroupRequest",
    "CreateVersionOperationMetadata",
    "CreateVersionRequest",
    "CreateWebhookRequest",
    "DataStoreConnection",
    "DataStoreConnectionSignals",
    "DataStoreType",
    "DataType",
    "DeleteAgentRequest",
    "DeleteEntityTypeRequest",
    "DeleteEnvironmentRequest",
    "DeleteExampleRequest",
    "DeleteExperimentRequest",
    "DeleteFlowRequest",
    "DeleteGeneratorRequest",
    "DeleteIntentRequest",
    "DeletePageRequest",
    "DeletePlaybookRequest",
    "DeletePlaybookVersionRequest",
    "DeleteSecuritySettingsRequest",
    "DeleteSessionEntityTypeRequest",
    "DeleteToolRequest",
    "DeleteToolVersionRequest",
    "DeleteTransitionRouteGroupRequest",
    "DeleteVersionRequest",
    "DeleteWebhookRequest",
    "DeployFlowMetadata",
    "DeployFlowRequest",
    "DeployFlowResponse",
    "Deployment",
    "DeploymentsClient",
    "DetectIntentRequest",
    "DetectIntentResponse",
    "DetectIntentResponseView",
    "DocumentProcessingMode",
    "DtmfInput",
    "EntityType",
    "EntityTypesClient",
    "Environment",
    "EnvironmentsClient",
    "EventHandler",
    "EventInput",
    "Example",
    "ExamplesClient",
    "Experiment",
    "ExperimentsClient",
    "ExportAgentRequest",
    "ExportAgentResponse",
    "ExportEntityTypesMetadata",
    "ExportEntityTypesRequest",
    "ExportEntityTypesResponse",
    "ExportFlowRequest",
    "ExportFlowResponse",
    "ExportIntentsMetadata",
    "ExportIntentsRequest",
    "ExportIntentsResponse",
    "ExportPlaybookRequest",
    "ExportPlaybookResponse",
    "ExportTestCasesMetadata",
    "ExportTestCasesRequest",
    "ExportTestCasesResponse",
    "FilterSpecs",
    "Flow",
    "FlowImportStrategy",
    "FlowInvocation",
    "FlowTransition",
    "FlowValidationResult",
    "FlowsClient",
    "Form",
    "FulfillIntentRequest",
    "FulfillIntentResponse",
    "Fulfillment",
    "GcsDestination",
    "GenerativeSettings",
    "Generator",
    "GeneratorsClient",
    "GetAgentRequest",
    "GetAgentValidationResultRequest",
    "GetChangelogRequest",
    "GetDeploymentRequest",
    "GetEntityTypeRequest",
    "GetEnvironmentRequest",
    "GetExampleRequest",
    "GetExperimentRequest",
    "GetFlowRequest",
    "GetFlowValidationResultRequest",
    "GetGenerativeSettingsRequest",
    "GetGeneratorRequest",
    "GetIntentRequest",
    "GetPageRequest",
    "GetPlaybookRequest",
    "GetPlaybookVersionRequest",
    "GetSecuritySettingsRequest",
    "GetSessionEntityTypeRequest",
    "GetTestCaseRequest",
    "GetTestCaseResultRequest",
    "GetToolRequest",
    "GetToolVersionRequest",
    "GetTransitionRouteGroupRequest",
    "GetVersionRequest",
    "GetWebhookRequest",
    "Handler",
    "ImportEntityTypesMetadata",
    "ImportEntityTypesRequest",
    "ImportEntityTypesResponse",
    "ImportFlowRequest",
    "ImportFlowResponse",
    "ImportIntentsMetadata",
    "ImportIntentsRequest",
    "ImportIntentsResponse",
    "ImportPlaybookRequest",
    "ImportPlaybookResponse",
    "ImportStrategy",
    "ImportTestCasesMetadata",
    "ImportTestCasesRequest",
    "ImportTestCasesResponse",
    "InlineDestination",
    "InlineSchema",
    "InlineSource",
    "InputAudioConfig",
    "Intent",
    "IntentCoverage",
    "IntentInput",
    "IntentView",
    "IntentsClient",
    "KnowledgeConnectorSettings",
    "LanguageInfo",
    "ListAgentsRequest",
    "ListAgentsResponse",
    "ListChangelogsRequest",
    "ListChangelogsResponse",
    "ListContinuousTestResultsRequest",
    "ListContinuousTestResultsResponse",
    "ListDeploymentsRequest",
    "ListDeploymentsResponse",
    "ListEntityTypesRequest",
    "ListEntityTypesResponse",
    "ListEnvironmentsRequest",
    "ListEnvironmentsResponse",
    "ListExamplesRequest",
    "ListExamplesResponse",
    "ListExperimentsRequest",
    "ListExperimentsResponse",
    "ListFlowsRequest",
    "ListFlowsResponse",
    "ListGeneratorsRequest",
    "ListGeneratorsResponse",
    "ListIntentsRequest",
    "ListIntentsResponse",
    "ListPagesRequest",
    "ListPagesResponse",
    "ListPlaybookVersionsRequest",
    "ListPlaybookVersionsResponse",
    "ListPlaybooksRequest",
    "ListPlaybooksResponse",
    "ListSecuritySettingsRequest",
    "ListSecuritySettingsResponse",
    "ListSessionEntityTypesRequest",
    "ListSessionEntityTypesResponse",
    "ListTestCaseResultsRequest",
    "ListTestCaseResultsResponse",
    "ListTestCasesRequest",
    "ListTestCasesResponse",
    "ListToolVersionsRequest",
    "ListToolVersionsResponse",
    "ListToolsRequest",
    "ListToolsResponse",
    "ListTransitionRouteGroupsRequest",
    "ListTransitionRouteGroupsResponse",
    "ListVersionsRequest",
    "ListVersionsResponse",
    "ListWebhooksRequest",
    "ListWebhooksResponse",
    "LlmModelSettings",
    "LoadVersionRequest",
    "LookupEnvironmentHistoryRequest",
    "LookupEnvironmentHistoryResponse",
    "Match",
    "MatchIntentRequest",
    "MatchIntentResponse",
    "NluSettings",
    "OutputAudioConfig",
    "OutputAudioEncoding",
    "OutputState",
    "Page",
    "PageInfo",
    "PagesClient",
    "ParameterDefinition",
    "Phrase",
    "Playbook",
    "PlaybookImportStrategy",
    "PlaybookInput",
    "PlaybookInvocation",
    "PlaybookOutput",
    "PlaybookTransition",
    "PlaybookVersion",
    "PlaybooksClient",
    "QueryInput",
    "QueryParameters",
    "QueryResult",
    "ResourceName",
    "ResponseMessage",
    "RestoreAgentRequest",
    "RestorePlaybookVersionRequest",
    "RestorePlaybookVersionResponse",
    "RestoreToolVersionRequest",
    "RestoreToolVersionResponse",
    "RolloutConfig",
    "RolloutState",
    "RunContinuousTestMetadata",
    "RunContinuousTestRequest",
    "RunContinuousTestResponse",
    "RunTestCaseMetadata",
    "RunTestCaseRequest",
    "RunTestCaseResponse",
    "SafetySettings",
    "SearchConfig",
    "SecuritySettings",
    "SecuritySettingsServiceClient",
    "SentimentAnalysisResult",
    "SessionEntityType",
    "SessionEntityTypesClient",
    "SessionInfo",
    "SessionsClient",
    "SpeechModelVariant",
    "SpeechToTextSettings",
    "SpeechWordInfo",
    "SsmlVoiceGender",
    "StartExperimentRequest",
    "StopExperimentRequest",
    "StreamingDetectIntentRequest",
    "StreamingDetectIntentResponse",
    "StreamingRecognitionResult",
    "SubmitAnswerFeedbackRequest",
    "SynthesizeSpeechConfig",
    "TestCase",
    "TestCaseError",
    "TestCaseResult",
    "TestCasesClient",
    "TestConfig",
    "TestError",
    "TestResult",
    "TestRunDifference",
    "TextInput",
    "TextToSpeechSettings",
    "Tool",
    "ToolCall",
    "ToolCallResult",
    "ToolUse",
    "ToolVersion",
    "ToolsClient",
    "TrainFlowRequest",
    "TransitionCoverage",
    "TransitionRoute",
    "TransitionRouteGroup",
    "TransitionRouteGroupCoverage",
    "TransitionRouteGroupsClient",
    "TypeSchema",
    "UpdateAgentRequest",
    "UpdateEntityTypeRequest",
    "UpdateEnvironmentRequest",
    "UpdateExampleRequest",
    "UpdateExperimentRequest",
    "UpdateFlowRequest",
    "UpdateGenerativeSettingsRequest",
    "UpdateGeneratorRequest",
    "UpdateIntentRequest",
    "UpdatePageRequest",
    "UpdatePlaybookRequest",
    "UpdateSecuritySettingsRequest",
    "UpdateSessionEntityTypeRequest",
    "UpdateTestCaseRequest",
    "UpdateToolRequest",
    "UpdateTransitionRouteGroupRequest",
    "UpdateVersionRequest",
    "UpdateWebhookRequest",
    "UserUtterance",
    "ValidateAgentRequest",
    "ValidateFlowRequest",
    "ValidationMessage",
    "VariantsHistory",
    "Version",
    "VersionVariants",
    "VersionsClient",
    "VoiceSelectionParams",
    "Webhook",
    "WebhookRequest",
    "WebhookResponse",
    "WebhooksClient",
)
