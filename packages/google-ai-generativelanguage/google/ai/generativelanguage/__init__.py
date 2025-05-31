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
from google.ai.generativelanguage import gapic_version as package_version

__version__ = package_version.__version__


from google.ai.generativelanguage_v1.services.generative_service.async_client import (
    GenerativeServiceAsyncClient,
)
from google.ai.generativelanguage_v1.services.generative_service.client import (
    GenerativeServiceClient,
)
from google.ai.generativelanguage_v1.services.model_service.async_client import (
    ModelServiceAsyncClient,
)
from google.ai.generativelanguage_v1.services.model_service.client import (
    ModelServiceClient,
)
from google.ai.generativelanguage_v1.types.citation import (
    CitationMetadata,
    CitationSource,
)
from google.ai.generativelanguage_v1.types.content import (
    Blob,
    Content,
    Modality,
    ModalityTokenCount,
    Part,
)
from google.ai.generativelanguage_v1.types.generative_service import (
    BatchEmbedContentsRequest,
    BatchEmbedContentsResponse,
    Candidate,
    ContentEmbedding,
    CountTokensRequest,
    CountTokensResponse,
    EmbedContentRequest,
    EmbedContentResponse,
    GenerateContentRequest,
    GenerateContentResponse,
    GenerationConfig,
    GroundingChunk,
    GroundingMetadata,
    GroundingSupport,
    LogprobsResult,
    RetrievalMetadata,
    SearchEntryPoint,
    Segment,
    TaskType,
)
from google.ai.generativelanguage_v1.types.model import Model
from google.ai.generativelanguage_v1.types.model_service import (
    GetModelRequest,
    ListModelsRequest,
    ListModelsResponse,
)
from google.ai.generativelanguage_v1.types.safety import (
    HarmCategory,
    SafetyRating,
    SafetySetting,
)

__all__ = (
    "GenerativeServiceClient",
    "GenerativeServiceAsyncClient",
    "ModelServiceClient",
    "ModelServiceAsyncClient",
    "CitationMetadata",
    "CitationSource",
    "Blob",
    "Content",
    "ModalityTokenCount",
    "Part",
    "Modality",
    "BatchEmbedContentsRequest",
    "BatchEmbedContentsResponse",
    "Candidate",
    "ContentEmbedding",
    "CountTokensRequest",
    "CountTokensResponse",
    "EmbedContentRequest",
    "EmbedContentResponse",
    "GenerateContentRequest",
    "GenerateContentResponse",
    "GenerationConfig",
    "GroundingChunk",
    "GroundingMetadata",
    "GroundingSupport",
    "LogprobsResult",
    "RetrievalMetadata",
    "SearchEntryPoint",
    "Segment",
    "TaskType",
    "Model",
    "GetModelRequest",
    "ListModelsRequest",
    "ListModelsResponse",
    "SafetyRating",
    "SafetySetting",
    "HarmCategory",
)
