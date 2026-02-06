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

from google.cloud.discoveryengine_v1beta import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.completion_service import (
    CompletionServiceAsyncClient,
    CompletionServiceClient,
)
from .services.control_service import ControlServiceAsyncClient, ControlServiceClient
from .services.conversational_search_service import (
    ConversationalSearchServiceAsyncClient,
    ConversationalSearchServiceClient,
)
from .services.data_store_service import (
    DataStoreServiceAsyncClient,
    DataStoreServiceClient,
)
from .services.document_service import DocumentServiceAsyncClient, DocumentServiceClient
from .services.engine_service import EngineServiceAsyncClient, EngineServiceClient
from .services.evaluation_service import (
    EvaluationServiceAsyncClient,
    EvaluationServiceClient,
)
from .services.grounded_generation_service import (
    GroundedGenerationServiceAsyncClient,
    GroundedGenerationServiceClient,
)
from .services.project_service import ProjectServiceAsyncClient, ProjectServiceClient
from .services.rank_service import RankServiceAsyncClient, RankServiceClient
from .services.recommendation_service import (
    RecommendationServiceAsyncClient,
    RecommendationServiceClient,
)
from .services.sample_query_service import (
    SampleQueryServiceAsyncClient,
    SampleQueryServiceClient,
)
from .services.sample_query_set_service import (
    SampleQuerySetServiceAsyncClient,
    SampleQuerySetServiceClient,
)
from .services.schema_service import SchemaServiceAsyncClient, SchemaServiceClient
from .services.search_service import SearchServiceAsyncClient, SearchServiceClient
from .services.search_tuning_service import (
    SearchTuningServiceAsyncClient,
    SearchTuningServiceClient,
)
from .services.serving_config_service import (
    ServingConfigServiceAsyncClient,
    ServingConfigServiceClient,
)
from .services.session_service import SessionServiceAsyncClient, SessionServiceClient
from .services.site_search_engine_service import (
    SiteSearchEngineServiceAsyncClient,
    SiteSearchEngineServiceClient,
)
from .services.user_event_service import (
    UserEventServiceAsyncClient,
    UserEventServiceClient,
)
from .types.answer import Answer
from .types.chunk import Chunk
from .types.common import (
    CustomAttribute,
    DoubleList,
    EmbeddingConfig,
    IndustryVertical,
    Interval,
    SearchAddOn,
    SearchTier,
    SearchUseCase,
    SolutionType,
    UserInfo,
)
from .types.completion import CompletionSuggestion, SuggestionDenyListEntry
from .types.completion_service import (
    AdvancedCompleteQueryRequest,
    AdvancedCompleteQueryResponse,
    CompleteQueryRequest,
    CompleteQueryResponse,
)
from .types.control import Condition, Control
from .types.control_service import (
    CreateControlRequest,
    DeleteControlRequest,
    GetControlRequest,
    ListControlsRequest,
    ListControlsResponse,
    UpdateControlRequest,
)
from .types.conversation import (
    Conversation,
    ConversationContext,
    ConversationMessage,
    Reply,
    TextInput,
)
from .types.conversational_search_service import (
    AnswerQueryRequest,
    AnswerQueryResponse,
    ConverseConversationRequest,
    ConverseConversationResponse,
    CreateConversationRequest,
    CreateSessionRequest,
    DeleteConversationRequest,
    DeleteSessionRequest,
    GetAnswerRequest,
    GetConversationRequest,
    GetSessionRequest,
    ListConversationsRequest,
    ListConversationsResponse,
    ListSessionsRequest,
    ListSessionsResponse,
    UpdateConversationRequest,
    UpdateSessionRequest,
)
from .types.custom_tuning_model import CustomTuningModel
from .types.data_store import (
    DataStore,
    LanguageInfo,
    NaturalLanguageQueryUnderstandingConfig,
    WorkspaceConfig,
)
from .types.data_store_service import (
    CreateDataStoreMetadata,
    CreateDataStoreRequest,
    DeleteDataStoreMetadata,
    DeleteDataStoreRequest,
    GetDataStoreRequest,
    ListDataStoresRequest,
    ListDataStoresResponse,
    UpdateDataStoreRequest,
)
from .types.document import Document
from .types.document_processing_config import DocumentProcessingConfig
from .types.document_service import (
    BatchGetDocumentsMetadataRequest,
    BatchGetDocumentsMetadataResponse,
    CreateDocumentRequest,
    DeleteDocumentRequest,
    GetDocumentRequest,
    ListDocumentsRequest,
    ListDocumentsResponse,
    UpdateDocumentRequest,
)
from .types.engine import Engine
from .types.engine_service import (
    CreateEngineMetadata,
    CreateEngineRequest,
    DeleteEngineMetadata,
    DeleteEngineRequest,
    GetEngineRequest,
    ListEnginesRequest,
    ListEnginesResponse,
    PauseEngineRequest,
    ResumeEngineRequest,
    TuneEngineMetadata,
    TuneEngineRequest,
    TuneEngineResponse,
    UpdateEngineRequest,
)
from .types.evaluation import Evaluation, QualityMetrics
from .types.evaluation_service import (
    CreateEvaluationMetadata,
    CreateEvaluationRequest,
    GetEvaluationRequest,
    ListEvaluationResultsRequest,
    ListEvaluationResultsResponse,
    ListEvaluationsRequest,
    ListEvaluationsResponse,
)
from .types.grounded_generation_service import (
    CheckGroundingRequest,
    CheckGroundingResponse,
    CheckGroundingSpec,
    GenerateGroundedContentRequest,
    GenerateGroundedContentResponse,
    GroundedGenerationContent,
)
from .types.grounding import FactChunk, GroundingConfig, GroundingFact
from .types.import_config import (
    AlloyDbSource,
    BigQuerySource,
    BigtableOptions,
    BigtableSource,
    CloudSqlSource,
    FhirStoreSource,
    FirestoreSource,
    GcsSource,
    ImportCompletionSuggestionsMetadata,
    ImportCompletionSuggestionsRequest,
    ImportCompletionSuggestionsResponse,
    ImportDocumentsMetadata,
    ImportDocumentsRequest,
    ImportDocumentsResponse,
    ImportErrorConfig,
    ImportSampleQueriesMetadata,
    ImportSampleQueriesRequest,
    ImportSampleQueriesResponse,
    ImportSuggestionDenyListEntriesMetadata,
    ImportSuggestionDenyListEntriesRequest,
    ImportSuggestionDenyListEntriesResponse,
    ImportUserEventsMetadata,
    ImportUserEventsRequest,
    ImportUserEventsResponse,
    SpannerSource,
)
from .types.project import Project
from .types.project_service import ProvisionProjectMetadata, ProvisionProjectRequest
from .types.purge_config import (
    PurgeCompletionSuggestionsMetadata,
    PurgeCompletionSuggestionsRequest,
    PurgeCompletionSuggestionsResponse,
    PurgeDocumentsMetadata,
    PurgeDocumentsRequest,
    PurgeDocumentsResponse,
    PurgeErrorConfig,
    PurgeSuggestionDenyListEntriesMetadata,
    PurgeSuggestionDenyListEntriesRequest,
    PurgeSuggestionDenyListEntriesResponse,
    PurgeUserEventsMetadata,
    PurgeUserEventsRequest,
    PurgeUserEventsResponse,
)
from .types.rank_service import RankingRecord, RankRequest, RankResponse
from .types.recommendation_service import RecommendRequest, RecommendResponse
from .types.sample_query import SampleQuery
from .types.sample_query_service import (
    CreateSampleQueryRequest,
    DeleteSampleQueryRequest,
    GetSampleQueryRequest,
    ListSampleQueriesRequest,
    ListSampleQueriesResponse,
    UpdateSampleQueryRequest,
)
from .types.sample_query_set import SampleQuerySet
from .types.sample_query_set_service import (
    CreateSampleQuerySetRequest,
    DeleteSampleQuerySetRequest,
    GetSampleQuerySetRequest,
    ListSampleQuerySetsRequest,
    ListSampleQuerySetsResponse,
    UpdateSampleQuerySetRequest,
)
from .types.schema import Schema
from .types.schema_service import (
    CreateSchemaMetadata,
    CreateSchemaRequest,
    DeleteSchemaMetadata,
    DeleteSchemaRequest,
    GetSchemaRequest,
    ListSchemasRequest,
    ListSchemasResponse,
    UpdateSchemaMetadata,
    UpdateSchemaRequest,
)
from .types.search_service import SearchRequest, SearchResponse
from .types.search_tuning_service import (
    ListCustomModelsRequest,
    ListCustomModelsResponse,
    TrainCustomModelMetadata,
    TrainCustomModelRequest,
    TrainCustomModelResponse,
)
from .types.serving_config import ServingConfig
from .types.serving_config_service import (
    GetServingConfigRequest,
    ListServingConfigsRequest,
    ListServingConfigsResponse,
    UpdateServingConfigRequest,
)
from .types.session import Query, Session
from .types.site_search_engine import (
    Sitemap,
    SiteSearchEngine,
    SiteVerificationInfo,
    TargetSite,
)
from .types.site_search_engine_service import (
    BatchCreateTargetSiteMetadata,
    BatchCreateTargetSitesRequest,
    BatchCreateTargetSitesResponse,
    BatchVerifyTargetSitesMetadata,
    BatchVerifyTargetSitesRequest,
    BatchVerifyTargetSitesResponse,
    CreateSitemapMetadata,
    CreateSitemapRequest,
    CreateTargetSiteMetadata,
    CreateTargetSiteRequest,
    DeleteSitemapMetadata,
    DeleteSitemapRequest,
    DeleteTargetSiteMetadata,
    DeleteTargetSiteRequest,
    DisableAdvancedSiteSearchMetadata,
    DisableAdvancedSiteSearchRequest,
    DisableAdvancedSiteSearchResponse,
    EnableAdvancedSiteSearchMetadata,
    EnableAdvancedSiteSearchRequest,
    EnableAdvancedSiteSearchResponse,
    FetchDomainVerificationStatusRequest,
    FetchDomainVerificationStatusResponse,
    FetchSitemapsRequest,
    FetchSitemapsResponse,
    GetSiteSearchEngineRequest,
    GetTargetSiteRequest,
    ListTargetSitesRequest,
    ListTargetSitesResponse,
    RecrawlUrisMetadata,
    RecrawlUrisRequest,
    RecrawlUrisResponse,
    UpdateTargetSiteMetadata,
    UpdateTargetSiteRequest,
)
from .types.user_event import (
    CompletionInfo,
    DocumentInfo,
    MediaInfo,
    PageInfo,
    PanelInfo,
    SearchInfo,
    TransactionInfo,
    UserEvent,
)
from .types.user_event_service import CollectUserEventRequest, WriteUserEventRequest

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.discoveryengine_v1beta")  # type: ignore
    api_core.check_dependency_versions("google.cloud.discoveryengine_v1beta")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.discoveryengine_v1beta"
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
    "CompletionServiceAsyncClient",
    "ControlServiceAsyncClient",
    "ConversationalSearchServiceAsyncClient",
    "DataStoreServiceAsyncClient",
    "DocumentServiceAsyncClient",
    "EngineServiceAsyncClient",
    "EvaluationServiceAsyncClient",
    "GroundedGenerationServiceAsyncClient",
    "ProjectServiceAsyncClient",
    "RankServiceAsyncClient",
    "RecommendationServiceAsyncClient",
    "SampleQueryServiceAsyncClient",
    "SampleQuerySetServiceAsyncClient",
    "SchemaServiceAsyncClient",
    "SearchServiceAsyncClient",
    "SearchTuningServiceAsyncClient",
    "ServingConfigServiceAsyncClient",
    "SessionServiceAsyncClient",
    "SiteSearchEngineServiceAsyncClient",
    "UserEventServiceAsyncClient",
    "AdvancedCompleteQueryRequest",
    "AdvancedCompleteQueryResponse",
    "AlloyDbSource",
    "Answer",
    "AnswerQueryRequest",
    "AnswerQueryResponse",
    "BatchCreateTargetSiteMetadata",
    "BatchCreateTargetSitesRequest",
    "BatchCreateTargetSitesResponse",
    "BatchGetDocumentsMetadataRequest",
    "BatchGetDocumentsMetadataResponse",
    "BatchVerifyTargetSitesMetadata",
    "BatchVerifyTargetSitesRequest",
    "BatchVerifyTargetSitesResponse",
    "BigQuerySource",
    "BigtableOptions",
    "BigtableSource",
    "CheckGroundingRequest",
    "CheckGroundingResponse",
    "CheckGroundingSpec",
    "Chunk",
    "CloudSqlSource",
    "CollectUserEventRequest",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "CompletionInfo",
    "CompletionServiceClient",
    "CompletionSuggestion",
    "Condition",
    "Control",
    "ControlServiceClient",
    "Conversation",
    "ConversationContext",
    "ConversationMessage",
    "ConversationalSearchServiceClient",
    "ConverseConversationRequest",
    "ConverseConversationResponse",
    "CreateControlRequest",
    "CreateConversationRequest",
    "CreateDataStoreMetadata",
    "CreateDataStoreRequest",
    "CreateDocumentRequest",
    "CreateEngineMetadata",
    "CreateEngineRequest",
    "CreateEvaluationMetadata",
    "CreateEvaluationRequest",
    "CreateSampleQueryRequest",
    "CreateSampleQuerySetRequest",
    "CreateSchemaMetadata",
    "CreateSchemaRequest",
    "CreateSessionRequest",
    "CreateSitemapMetadata",
    "CreateSitemapRequest",
    "CreateTargetSiteMetadata",
    "CreateTargetSiteRequest",
    "CustomAttribute",
    "CustomTuningModel",
    "DataStore",
    "DataStoreServiceClient",
    "DeleteControlRequest",
    "DeleteConversationRequest",
    "DeleteDataStoreMetadata",
    "DeleteDataStoreRequest",
    "DeleteDocumentRequest",
    "DeleteEngineMetadata",
    "DeleteEngineRequest",
    "DeleteSampleQueryRequest",
    "DeleteSampleQuerySetRequest",
    "DeleteSchemaMetadata",
    "DeleteSchemaRequest",
    "DeleteSessionRequest",
    "DeleteSitemapMetadata",
    "DeleteSitemapRequest",
    "DeleteTargetSiteMetadata",
    "DeleteTargetSiteRequest",
    "DisableAdvancedSiteSearchMetadata",
    "DisableAdvancedSiteSearchRequest",
    "DisableAdvancedSiteSearchResponse",
    "Document",
    "DocumentInfo",
    "DocumentProcessingConfig",
    "DocumentServiceClient",
    "DoubleList",
    "EmbeddingConfig",
    "EnableAdvancedSiteSearchMetadata",
    "EnableAdvancedSiteSearchRequest",
    "EnableAdvancedSiteSearchResponse",
    "Engine",
    "EngineServiceClient",
    "Evaluation",
    "EvaluationServiceClient",
    "FactChunk",
    "FetchDomainVerificationStatusRequest",
    "FetchDomainVerificationStatusResponse",
    "FetchSitemapsRequest",
    "FetchSitemapsResponse",
    "FhirStoreSource",
    "FirestoreSource",
    "GcsSource",
    "GenerateGroundedContentRequest",
    "GenerateGroundedContentResponse",
    "GetAnswerRequest",
    "GetControlRequest",
    "GetConversationRequest",
    "GetDataStoreRequest",
    "GetDocumentRequest",
    "GetEngineRequest",
    "GetEvaluationRequest",
    "GetSampleQueryRequest",
    "GetSampleQuerySetRequest",
    "GetSchemaRequest",
    "GetServingConfigRequest",
    "GetSessionRequest",
    "GetSiteSearchEngineRequest",
    "GetTargetSiteRequest",
    "GroundedGenerationContent",
    "GroundedGenerationServiceClient",
    "GroundingConfig",
    "GroundingFact",
    "ImportCompletionSuggestionsMetadata",
    "ImportCompletionSuggestionsRequest",
    "ImportCompletionSuggestionsResponse",
    "ImportDocumentsMetadata",
    "ImportDocumentsRequest",
    "ImportDocumentsResponse",
    "ImportErrorConfig",
    "ImportSampleQueriesMetadata",
    "ImportSampleQueriesRequest",
    "ImportSampleQueriesResponse",
    "ImportSuggestionDenyListEntriesMetadata",
    "ImportSuggestionDenyListEntriesRequest",
    "ImportSuggestionDenyListEntriesResponse",
    "ImportUserEventsMetadata",
    "ImportUserEventsRequest",
    "ImportUserEventsResponse",
    "IndustryVertical",
    "Interval",
    "LanguageInfo",
    "ListControlsRequest",
    "ListControlsResponse",
    "ListConversationsRequest",
    "ListConversationsResponse",
    "ListCustomModelsRequest",
    "ListCustomModelsResponse",
    "ListDataStoresRequest",
    "ListDataStoresResponse",
    "ListDocumentsRequest",
    "ListDocumentsResponse",
    "ListEnginesRequest",
    "ListEnginesResponse",
    "ListEvaluationResultsRequest",
    "ListEvaluationResultsResponse",
    "ListEvaluationsRequest",
    "ListEvaluationsResponse",
    "ListSampleQueriesRequest",
    "ListSampleQueriesResponse",
    "ListSampleQuerySetsRequest",
    "ListSampleQuerySetsResponse",
    "ListSchemasRequest",
    "ListSchemasResponse",
    "ListServingConfigsRequest",
    "ListServingConfigsResponse",
    "ListSessionsRequest",
    "ListSessionsResponse",
    "ListTargetSitesRequest",
    "ListTargetSitesResponse",
    "MediaInfo",
    "NaturalLanguageQueryUnderstandingConfig",
    "PageInfo",
    "PanelInfo",
    "PauseEngineRequest",
    "Project",
    "ProjectServiceClient",
    "ProvisionProjectMetadata",
    "ProvisionProjectRequest",
    "PurgeCompletionSuggestionsMetadata",
    "PurgeCompletionSuggestionsRequest",
    "PurgeCompletionSuggestionsResponse",
    "PurgeDocumentsMetadata",
    "PurgeDocumentsRequest",
    "PurgeDocumentsResponse",
    "PurgeErrorConfig",
    "PurgeSuggestionDenyListEntriesMetadata",
    "PurgeSuggestionDenyListEntriesRequest",
    "PurgeSuggestionDenyListEntriesResponse",
    "PurgeUserEventsMetadata",
    "PurgeUserEventsRequest",
    "PurgeUserEventsResponse",
    "QualityMetrics",
    "Query",
    "RankRequest",
    "RankResponse",
    "RankServiceClient",
    "RankingRecord",
    "RecommendRequest",
    "RecommendResponse",
    "RecommendationServiceClient",
    "RecrawlUrisMetadata",
    "RecrawlUrisRequest",
    "RecrawlUrisResponse",
    "Reply",
    "ResumeEngineRequest",
    "SampleQuery",
    "SampleQueryServiceClient",
    "SampleQuerySet",
    "SampleQuerySetServiceClient",
    "Schema",
    "SchemaServiceClient",
    "SearchAddOn",
    "SearchInfo",
    "SearchRequest",
    "SearchResponse",
    "SearchServiceClient",
    "SearchTier",
    "SearchTuningServiceClient",
    "SearchUseCase",
    "ServingConfig",
    "ServingConfigServiceClient",
    "Session",
    "SessionServiceClient",
    "SiteSearchEngine",
    "SiteSearchEngineServiceClient",
    "SiteVerificationInfo",
    "Sitemap",
    "SolutionType",
    "SpannerSource",
    "SuggestionDenyListEntry",
    "TargetSite",
    "TextInput",
    "TrainCustomModelMetadata",
    "TrainCustomModelRequest",
    "TrainCustomModelResponse",
    "TransactionInfo",
    "TuneEngineMetadata",
    "TuneEngineRequest",
    "TuneEngineResponse",
    "UpdateControlRequest",
    "UpdateConversationRequest",
    "UpdateDataStoreRequest",
    "UpdateDocumentRequest",
    "UpdateEngineRequest",
    "UpdateSampleQueryRequest",
    "UpdateSampleQuerySetRequest",
    "UpdateSchemaMetadata",
    "UpdateSchemaRequest",
    "UpdateServingConfigRequest",
    "UpdateSessionRequest",
    "UpdateTargetSiteMetadata",
    "UpdateTargetSiteRequest",
    "UserEvent",
    "UserEventServiceClient",
    "UserInfo",
    "WorkspaceConfig",
    "WriteUserEventRequest",
)
