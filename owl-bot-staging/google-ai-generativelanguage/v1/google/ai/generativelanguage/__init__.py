# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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


from google.ai.generativelanguage_v1.services.generative_service.client import GenerativeServiceClient
from google.ai.generativelanguage_v1.services.generative_service.async_client import GenerativeServiceAsyncClient
from google.ai.generativelanguage_v1.services.model_service.client import ModelServiceClient
from google.ai.generativelanguage_v1.services.model_service.async_client import ModelServiceAsyncClient

from google.ai.generativelanguage_v1.types.citation import CitationMetadata
from google.ai.generativelanguage_v1.types.citation import CitationSource
from google.ai.generativelanguage_v1.types.content import Blob
from google.ai.generativelanguage_v1.types.content import Content
from google.ai.generativelanguage_v1.types.content import Part
from google.ai.generativelanguage_v1.types.generative_service import BatchEmbedContentsRequest
from google.ai.generativelanguage_v1.types.generative_service import BatchEmbedContentsResponse
from google.ai.generativelanguage_v1.types.generative_service import Candidate
from google.ai.generativelanguage_v1.types.generative_service import ContentEmbedding
from google.ai.generativelanguage_v1.types.generative_service import CountTokensRequest
from google.ai.generativelanguage_v1.types.generative_service import CountTokensResponse
from google.ai.generativelanguage_v1.types.generative_service import EmbedContentRequest
from google.ai.generativelanguage_v1.types.generative_service import EmbedContentResponse
from google.ai.generativelanguage_v1.types.generative_service import GenerateContentRequest
from google.ai.generativelanguage_v1.types.generative_service import GenerateContentResponse
from google.ai.generativelanguage_v1.types.generative_service import GenerationConfig
from google.ai.generativelanguage_v1.types.generative_service import TaskType
from google.ai.generativelanguage_v1.types.model import Model
from google.ai.generativelanguage_v1.types.model_service import GetModelRequest
from google.ai.generativelanguage_v1.types.model_service import ListModelsRequest
from google.ai.generativelanguage_v1.types.model_service import ListModelsResponse
from google.ai.generativelanguage_v1.types.safety import SafetyRating
from google.ai.generativelanguage_v1.types.safety import SafetySetting
from google.ai.generativelanguage_v1.types.safety import HarmCategory

__all__ = ('GenerativeServiceClient',
    'GenerativeServiceAsyncClient',
    'ModelServiceClient',
    'ModelServiceAsyncClient',
    'CitationMetadata',
    'CitationSource',
    'Blob',
    'Content',
    'Part',
    'BatchEmbedContentsRequest',
    'BatchEmbedContentsResponse',
    'Candidate',
    'ContentEmbedding',
    'CountTokensRequest',
    'CountTokensResponse',
    'EmbedContentRequest',
    'EmbedContentResponse',
    'GenerateContentRequest',
    'GenerateContentResponse',
    'GenerationConfig',
    'TaskType',
    'Model',
    'GetModelRequest',
    'ListModelsRequest',
    'ListModelsResponse',
    'SafetyRating',
    'SafetySetting',
    'HarmCategory',
)
