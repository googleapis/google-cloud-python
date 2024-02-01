# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.ai.generativelanguage_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.generative_service import GenerativeServiceClient
from .services.generative_service import GenerativeServiceAsyncClient
from .services.model_service import ModelServiceClient
from .services.model_service import ModelServiceAsyncClient

from .types.citation import CitationMetadata
from .types.citation import CitationSource
from .types.content import Blob
from .types.content import Content
from .types.content import Part
from .types.generative_service import BatchEmbedContentsRequest
from .types.generative_service import BatchEmbedContentsResponse
from .types.generative_service import Candidate
from .types.generative_service import ContentEmbedding
from .types.generative_service import CountTokensRequest
from .types.generative_service import CountTokensResponse
from .types.generative_service import EmbedContentRequest
from .types.generative_service import EmbedContentResponse
from .types.generative_service import GenerateContentRequest
from .types.generative_service import GenerateContentResponse
from .types.generative_service import GenerationConfig
from .types.generative_service import TaskType
from .types.model import Model
from .types.model_service import GetModelRequest
from .types.model_service import ListModelsRequest
from .types.model_service import ListModelsResponse
from .types.safety import SafetyRating
from .types.safety import SafetySetting
from .types.safety import HarmCategory

__all__ = (
    'GenerativeServiceAsyncClient',
    'ModelServiceAsyncClient',
'BatchEmbedContentsRequest',
'BatchEmbedContentsResponse',
'Blob',
'Candidate',
'CitationMetadata',
'CitationSource',
'Content',
'ContentEmbedding',
'CountTokensRequest',
'CountTokensResponse',
'EmbedContentRequest',
'EmbedContentResponse',
'GenerateContentRequest',
'GenerateContentResponse',
'GenerationConfig',
'GenerativeServiceClient',
'GetModelRequest',
'HarmCategory',
'ListModelsRequest',
'ListModelsResponse',
'Model',
'ModelServiceClient',
'Part',
'SafetyRating',
'SafetySetting',
'TaskType',
)
