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

from google.ai.generativelanguage_v1beta import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata

from .services.cache_service import CacheServiceAsyncClient, CacheServiceClient
from .services.discuss_service import DiscussServiceAsyncClient, DiscussServiceClient
from .services.file_service import FileServiceAsyncClient, FileServiceClient
from .services.generative_service import (
    GenerativeServiceAsyncClient,
    GenerativeServiceClient,
)
from .services.model_service import ModelServiceAsyncClient, ModelServiceClient
from .services.permission_service import (
    PermissionServiceAsyncClient,
    PermissionServiceClient,
)
from .services.prediction_service import (
    PredictionServiceAsyncClient,
    PredictionServiceClient,
)
from .services.retriever_service import (
    RetrieverServiceAsyncClient,
    RetrieverServiceClient,
)
from .services.text_service import TextServiceAsyncClient, TextServiceClient
from .types.cache_service import (
    CreateCachedContentRequest,
    DeleteCachedContentRequest,
    GetCachedContentRequest,
    ListCachedContentsRequest,
    ListCachedContentsResponse,
    UpdateCachedContentRequest,
)
from .types.cached_content import CachedContent
from .types.citation import CitationMetadata, CitationSource
from .types.content import (
    Blob,
    CodeExecution,
    CodeExecutionResult,
    Content,
    DynamicRetrievalConfig,
    ExecutableCode,
    FileData,
    FileSearch,
    FunctionCall,
    FunctionCallingConfig,
    FunctionDeclaration,
    FunctionResponse,
    FunctionResponseBlob,
    FunctionResponsePart,
    GoogleMaps,
    GoogleSearchRetrieval,
    GroundingPassage,
    GroundingPassages,
    Modality,
    ModalityTokenCount,
    Part,
    RetrievalConfig,
    Schema,
    Tool,
    ToolConfig,
    Type,
    UrlContext,
    VideoMetadata,
)
from .types.discuss_service import (
    CountMessageTokensRequest,
    CountMessageTokensResponse,
    Example,
    GenerateMessageRequest,
    GenerateMessageResponse,
    Message,
    MessagePrompt,
)
from .types.file import File, VideoFileMetadata
from .types.file_service import (
    CreateFileRequest,
    CreateFileResponse,
    DeleteFileRequest,
    DownloadFileRequest,
    DownloadFileResponse,
    GetFileRequest,
    ListFilesRequest,
    ListFilesResponse,
)
from .types.generative_service import (
    AttributionSourceId,
    AudioTranscriptionConfig,
    BatchEmbedContentsRequest,
    BatchEmbedContentsResponse,
    BidiGenerateContentClientContent,
    BidiGenerateContentClientMessage,
    BidiGenerateContentRealtimeInput,
    BidiGenerateContentServerContent,
    BidiGenerateContentServerMessage,
    BidiGenerateContentSetup,
    BidiGenerateContentSetupComplete,
    BidiGenerateContentToolCall,
    BidiGenerateContentToolCallCancellation,
    BidiGenerateContentToolResponse,
    BidiGenerateContentTranscription,
    Candidate,
    ContentEmbedding,
    ContextWindowCompressionConfig,
    CountTokensRequest,
    CountTokensResponse,
    EmbedContentRequest,
    EmbedContentResponse,
    GenerateAnswerRequest,
    GenerateAnswerResponse,
    GenerateContentRequest,
    GenerateContentResponse,
    GenerationConfig,
    GoAway,
    GroundingAttribution,
    GroundingChunk,
    GroundingMetadata,
    GroundingSupport,
    ImageConfig,
    LogprobsResult,
    MultiSpeakerVoiceConfig,
    PrebuiltVoiceConfig,
    RealtimeInputConfig,
    RetrievalMetadata,
    SearchEntryPoint,
    Segment,
    SemanticRetrieverConfig,
    SessionResumptionConfig,
    SessionResumptionUpdate,
    SpeakerVoiceConfig,
    SpeechConfig,
    TaskType,
    ThinkingConfig,
    UrlContextMetadata,
    UrlMetadata,
    UsageMetadata,
    VoiceConfig,
)
from .types.model import Model
from .types.model_service import (
    CreateTunedModelMetadata,
    CreateTunedModelRequest,
    DeleteTunedModelRequest,
    GetModelRequest,
    GetTunedModelRequest,
    ListModelsRequest,
    ListModelsResponse,
    ListTunedModelsRequest,
    ListTunedModelsResponse,
    UpdateTunedModelRequest,
)
from .types.permission import Permission
from .types.permission_service import (
    CreatePermissionRequest,
    DeletePermissionRequest,
    GetPermissionRequest,
    ListPermissionsRequest,
    ListPermissionsResponse,
    TransferOwnershipRequest,
    TransferOwnershipResponse,
    UpdatePermissionRequest,
)
from .types.prediction_service import (
    Media,
    PredictLongRunningGeneratedVideoResponse,
    PredictLongRunningMetadata,
    PredictLongRunningRequest,
    PredictLongRunningResponse,
    PredictRequest,
    PredictResponse,
    Video,
)
from .types.retriever import (
    Chunk,
    ChunkData,
    Condition,
    Corpus,
    CustomMetadata,
    Document,
    MetadataFilter,
    StringList,
)
from .types.retriever_service import (
    BatchCreateChunksRequest,
    BatchCreateChunksResponse,
    BatchDeleteChunksRequest,
    BatchUpdateChunksRequest,
    BatchUpdateChunksResponse,
    CreateChunkRequest,
    CreateCorpusRequest,
    CreateDocumentRequest,
    DeleteChunkRequest,
    DeleteCorpusRequest,
    DeleteDocumentRequest,
    GetChunkRequest,
    GetCorpusRequest,
    GetDocumentRequest,
    ListChunksRequest,
    ListChunksResponse,
    ListCorporaRequest,
    ListCorporaResponse,
    ListDocumentsRequest,
    ListDocumentsResponse,
    QueryCorpusRequest,
    QueryCorpusResponse,
    QueryDocumentRequest,
    QueryDocumentResponse,
    RelevantChunk,
    UpdateChunkRequest,
    UpdateCorpusRequest,
    UpdateDocumentRequest,
)
from .types.safety import (
    ContentFilter,
    HarmCategory,
    SafetyFeedback,
    SafetyRating,
    SafetySetting,
)
from .types.text_service import (
    BatchEmbedTextRequest,
    BatchEmbedTextResponse,
    CountTextTokensRequest,
    CountTextTokensResponse,
    Embedding,
    EmbedTextRequest,
    EmbedTextResponse,
    GenerateTextRequest,
    GenerateTextResponse,
    TextCompletion,
    TextPrompt,
)
from .types.tuned_model import (
    Dataset,
    Hyperparameters,
    TunedModel,
    TunedModelSource,
    TuningExample,
    TuningExamples,
    TuningSnapshot,
    TuningTask,
)

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.ai.generativelanguage_v1beta")  # type: ignore
    api_core.check_dependency_versions("google.ai.generativelanguage_v1beta")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.ai.generativelanguage_v1beta"
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
    "CacheServiceAsyncClient",
    "DiscussServiceAsyncClient",
    "FileServiceAsyncClient",
    "GenerativeServiceAsyncClient",
    "ModelServiceAsyncClient",
    "PermissionServiceAsyncClient",
    "PredictionServiceAsyncClient",
    "RetrieverServiceAsyncClient",
    "TextServiceAsyncClient",
    "AttributionSourceId",
    "AudioTranscriptionConfig",
    "BatchCreateChunksRequest",
    "BatchCreateChunksResponse",
    "BatchDeleteChunksRequest",
    "BatchEmbedContentsRequest",
    "BatchEmbedContentsResponse",
    "BatchEmbedTextRequest",
    "BatchEmbedTextResponse",
    "BatchUpdateChunksRequest",
    "BatchUpdateChunksResponse",
    "BidiGenerateContentClientContent",
    "BidiGenerateContentClientMessage",
    "BidiGenerateContentRealtimeInput",
    "BidiGenerateContentServerContent",
    "BidiGenerateContentServerMessage",
    "BidiGenerateContentSetup",
    "BidiGenerateContentSetupComplete",
    "BidiGenerateContentToolCall",
    "BidiGenerateContentToolCallCancellation",
    "BidiGenerateContentToolResponse",
    "BidiGenerateContentTranscription",
    "Blob",
    "CacheServiceClient",
    "CachedContent",
    "Candidate",
    "Chunk",
    "ChunkData",
    "CitationMetadata",
    "CitationSource",
    "CodeExecution",
    "CodeExecutionResult",
    "Condition",
    "Content",
    "ContentEmbedding",
    "ContentFilter",
    "ContextWindowCompressionConfig",
    "Corpus",
    "CountMessageTokensRequest",
    "CountMessageTokensResponse",
    "CountTextTokensRequest",
    "CountTextTokensResponse",
    "CountTokensRequest",
    "CountTokensResponse",
    "CreateCachedContentRequest",
    "CreateChunkRequest",
    "CreateCorpusRequest",
    "CreateDocumentRequest",
    "CreateFileRequest",
    "CreateFileResponse",
    "CreatePermissionRequest",
    "CreateTunedModelMetadata",
    "CreateTunedModelRequest",
    "CustomMetadata",
    "Dataset",
    "DeleteCachedContentRequest",
    "DeleteChunkRequest",
    "DeleteCorpusRequest",
    "DeleteDocumentRequest",
    "DeleteFileRequest",
    "DeletePermissionRequest",
    "DeleteTunedModelRequest",
    "DiscussServiceClient",
    "Document",
    "DownloadFileRequest",
    "DownloadFileResponse",
    "DynamicRetrievalConfig",
    "EmbedContentRequest",
    "EmbedContentResponse",
    "EmbedTextRequest",
    "EmbedTextResponse",
    "Embedding",
    "Example",
    "ExecutableCode",
    "File",
    "FileData",
    "FileSearch",
    "FileServiceClient",
    "FunctionCall",
    "FunctionCallingConfig",
    "FunctionDeclaration",
    "FunctionResponse",
    "FunctionResponseBlob",
    "FunctionResponsePart",
    "GenerateAnswerRequest",
    "GenerateAnswerResponse",
    "GenerateContentRequest",
    "GenerateContentResponse",
    "GenerateMessageRequest",
    "GenerateMessageResponse",
    "GenerateTextRequest",
    "GenerateTextResponse",
    "GenerationConfig",
    "GenerativeServiceClient",
    "GetCachedContentRequest",
    "GetChunkRequest",
    "GetCorpusRequest",
    "GetDocumentRequest",
    "GetFileRequest",
    "GetModelRequest",
    "GetPermissionRequest",
    "GetTunedModelRequest",
    "GoAway",
    "GoogleMaps",
    "GoogleSearchRetrieval",
    "GroundingAttribution",
    "GroundingChunk",
    "GroundingMetadata",
    "GroundingPassage",
    "GroundingPassages",
    "GroundingSupport",
    "HarmCategory",
    "Hyperparameters",
    "ImageConfig",
    "ListCachedContentsRequest",
    "ListCachedContentsResponse",
    "ListChunksRequest",
    "ListChunksResponse",
    "ListCorporaRequest",
    "ListCorporaResponse",
    "ListDocumentsRequest",
    "ListDocumentsResponse",
    "ListFilesRequest",
    "ListFilesResponse",
    "ListModelsRequest",
    "ListModelsResponse",
    "ListPermissionsRequest",
    "ListPermissionsResponse",
    "ListTunedModelsRequest",
    "ListTunedModelsResponse",
    "LogprobsResult",
    "Media",
    "Message",
    "MessagePrompt",
    "MetadataFilter",
    "Modality",
    "ModalityTokenCount",
    "Model",
    "ModelServiceClient",
    "MultiSpeakerVoiceConfig",
    "Part",
    "Permission",
    "PermissionServiceClient",
    "PrebuiltVoiceConfig",
    "PredictLongRunningGeneratedVideoResponse",
    "PredictLongRunningMetadata",
    "PredictLongRunningRequest",
    "PredictLongRunningResponse",
    "PredictRequest",
    "PredictResponse",
    "PredictionServiceClient",
    "QueryCorpusRequest",
    "QueryCorpusResponse",
    "QueryDocumentRequest",
    "QueryDocumentResponse",
    "RealtimeInputConfig",
    "RelevantChunk",
    "RetrievalConfig",
    "RetrievalMetadata",
    "RetrieverServiceClient",
    "SafetyFeedback",
    "SafetyRating",
    "SafetySetting",
    "Schema",
    "SearchEntryPoint",
    "Segment",
    "SemanticRetrieverConfig",
    "SessionResumptionConfig",
    "SessionResumptionUpdate",
    "SpeakerVoiceConfig",
    "SpeechConfig",
    "StringList",
    "TaskType",
    "TextCompletion",
    "TextPrompt",
    "TextServiceClient",
    "ThinkingConfig",
    "Tool",
    "ToolConfig",
    "TransferOwnershipRequest",
    "TransferOwnershipResponse",
    "TunedModel",
    "TunedModelSource",
    "TuningExample",
    "TuningExamples",
    "TuningSnapshot",
    "TuningTask",
    "Type",
    "UpdateCachedContentRequest",
    "UpdateChunkRequest",
    "UpdateCorpusRequest",
    "UpdateDocumentRequest",
    "UpdatePermissionRequest",
    "UpdateTunedModelRequest",
    "UrlContext",
    "UrlContextMetadata",
    "UrlMetadata",
    "UsageMetadata",
    "Video",
    "VideoFileMetadata",
    "VideoMetadata",
    "VoiceConfig",
)
