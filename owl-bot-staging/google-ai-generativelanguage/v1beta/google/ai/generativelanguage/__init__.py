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


from google.ai.generativelanguage_v1beta.services.discuss_service.client import DiscussServiceClient
from google.ai.generativelanguage_v1beta.services.discuss_service.async_client import DiscussServiceAsyncClient
from google.ai.generativelanguage_v1beta.services.generative_service.client import GenerativeServiceClient
from google.ai.generativelanguage_v1beta.services.generative_service.async_client import GenerativeServiceAsyncClient
from google.ai.generativelanguage_v1beta.services.model_service.client import ModelServiceClient
from google.ai.generativelanguage_v1beta.services.model_service.async_client import ModelServiceAsyncClient
from google.ai.generativelanguage_v1beta.services.permission_service.client import PermissionServiceClient
from google.ai.generativelanguage_v1beta.services.permission_service.async_client import PermissionServiceAsyncClient
from google.ai.generativelanguage_v1beta.services.retriever_service.client import RetrieverServiceClient
from google.ai.generativelanguage_v1beta.services.retriever_service.async_client import RetrieverServiceAsyncClient
from google.ai.generativelanguage_v1beta.services.text_service.client import TextServiceClient
from google.ai.generativelanguage_v1beta.services.text_service.async_client import TextServiceAsyncClient

from google.ai.generativelanguage_v1beta.types.citation import CitationMetadata
from google.ai.generativelanguage_v1beta.types.citation import CitationSource
from google.ai.generativelanguage_v1beta.types.content import Blob
from google.ai.generativelanguage_v1beta.types.content import Content
from google.ai.generativelanguage_v1beta.types.content import FunctionCall
from google.ai.generativelanguage_v1beta.types.content import FunctionDeclaration
from google.ai.generativelanguage_v1beta.types.content import FunctionResponse
from google.ai.generativelanguage_v1beta.types.content import GroundingPassage
from google.ai.generativelanguage_v1beta.types.content import GroundingPassages
from google.ai.generativelanguage_v1beta.types.content import Part
from google.ai.generativelanguage_v1beta.types.content import Schema
from google.ai.generativelanguage_v1beta.types.content import Tool
from google.ai.generativelanguage_v1beta.types.content import Type
from google.ai.generativelanguage_v1beta.types.discuss_service import CountMessageTokensRequest
from google.ai.generativelanguage_v1beta.types.discuss_service import CountMessageTokensResponse
from google.ai.generativelanguage_v1beta.types.discuss_service import Example
from google.ai.generativelanguage_v1beta.types.discuss_service import GenerateMessageRequest
from google.ai.generativelanguage_v1beta.types.discuss_service import GenerateMessageResponse
from google.ai.generativelanguage_v1beta.types.discuss_service import Message
from google.ai.generativelanguage_v1beta.types.discuss_service import MessagePrompt
from google.ai.generativelanguage_v1beta.types.generative_service import AttributionSourceId
from google.ai.generativelanguage_v1beta.types.generative_service import BatchEmbedContentsRequest
from google.ai.generativelanguage_v1beta.types.generative_service import BatchEmbedContentsResponse
from google.ai.generativelanguage_v1beta.types.generative_service import Candidate
from google.ai.generativelanguage_v1beta.types.generative_service import ContentEmbedding
from google.ai.generativelanguage_v1beta.types.generative_service import CountTokensRequest
from google.ai.generativelanguage_v1beta.types.generative_service import CountTokensResponse
from google.ai.generativelanguage_v1beta.types.generative_service import EmbedContentRequest
from google.ai.generativelanguage_v1beta.types.generative_service import EmbedContentResponse
from google.ai.generativelanguage_v1beta.types.generative_service import GenerateAnswerRequest
from google.ai.generativelanguage_v1beta.types.generative_service import GenerateAnswerResponse
from google.ai.generativelanguage_v1beta.types.generative_service import GenerateContentRequest
from google.ai.generativelanguage_v1beta.types.generative_service import GenerateContentResponse
from google.ai.generativelanguage_v1beta.types.generative_service import GenerationConfig
from google.ai.generativelanguage_v1beta.types.generative_service import GroundingAttribution
from google.ai.generativelanguage_v1beta.types.generative_service import SemanticRetrieverConfig
from google.ai.generativelanguage_v1beta.types.generative_service import TaskType
from google.ai.generativelanguage_v1beta.types.model import Model
from google.ai.generativelanguage_v1beta.types.model_service import CreateTunedModelMetadata
from google.ai.generativelanguage_v1beta.types.model_service import CreateTunedModelRequest
from google.ai.generativelanguage_v1beta.types.model_service import DeleteTunedModelRequest
from google.ai.generativelanguage_v1beta.types.model_service import GetModelRequest
from google.ai.generativelanguage_v1beta.types.model_service import GetTunedModelRequest
from google.ai.generativelanguage_v1beta.types.model_service import ListModelsRequest
from google.ai.generativelanguage_v1beta.types.model_service import ListModelsResponse
from google.ai.generativelanguage_v1beta.types.model_service import ListTunedModelsRequest
from google.ai.generativelanguage_v1beta.types.model_service import ListTunedModelsResponse
from google.ai.generativelanguage_v1beta.types.model_service import UpdateTunedModelRequest
from google.ai.generativelanguage_v1beta.types.permission import Permission
from google.ai.generativelanguage_v1beta.types.permission_service import CreatePermissionRequest
from google.ai.generativelanguage_v1beta.types.permission_service import DeletePermissionRequest
from google.ai.generativelanguage_v1beta.types.permission_service import GetPermissionRequest
from google.ai.generativelanguage_v1beta.types.permission_service import ListPermissionsRequest
from google.ai.generativelanguage_v1beta.types.permission_service import ListPermissionsResponse
from google.ai.generativelanguage_v1beta.types.permission_service import TransferOwnershipRequest
from google.ai.generativelanguage_v1beta.types.permission_service import TransferOwnershipResponse
from google.ai.generativelanguage_v1beta.types.permission_service import UpdatePermissionRequest
from google.ai.generativelanguage_v1beta.types.retriever import Chunk
from google.ai.generativelanguage_v1beta.types.retriever import ChunkData
from google.ai.generativelanguage_v1beta.types.retriever import Condition
from google.ai.generativelanguage_v1beta.types.retriever import Corpus
from google.ai.generativelanguage_v1beta.types.retriever import CustomMetadata
from google.ai.generativelanguage_v1beta.types.retriever import Document
from google.ai.generativelanguage_v1beta.types.retriever import MetadataFilter
from google.ai.generativelanguage_v1beta.types.retriever import StringList
from google.ai.generativelanguage_v1beta.types.retriever_service import BatchCreateChunksRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import BatchCreateChunksResponse
from google.ai.generativelanguage_v1beta.types.retriever_service import BatchDeleteChunksRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import BatchUpdateChunksRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import BatchUpdateChunksResponse
from google.ai.generativelanguage_v1beta.types.retriever_service import CreateChunkRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import CreateCorpusRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import CreateDocumentRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import DeleteChunkRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import DeleteCorpusRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import DeleteDocumentRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import GetChunkRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import GetCorpusRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import GetDocumentRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import ListChunksRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import ListChunksResponse
from google.ai.generativelanguage_v1beta.types.retriever_service import ListCorporaRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import ListCorporaResponse
from google.ai.generativelanguage_v1beta.types.retriever_service import ListDocumentsRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import ListDocumentsResponse
from google.ai.generativelanguage_v1beta.types.retriever_service import QueryCorpusRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import QueryCorpusResponse
from google.ai.generativelanguage_v1beta.types.retriever_service import QueryDocumentRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import QueryDocumentResponse
from google.ai.generativelanguage_v1beta.types.retriever_service import RelevantChunk
from google.ai.generativelanguage_v1beta.types.retriever_service import UpdateChunkRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import UpdateCorpusRequest
from google.ai.generativelanguage_v1beta.types.retriever_service import UpdateDocumentRequest
from google.ai.generativelanguage_v1beta.types.safety import ContentFilter
from google.ai.generativelanguage_v1beta.types.safety import SafetyFeedback
from google.ai.generativelanguage_v1beta.types.safety import SafetyRating
from google.ai.generativelanguage_v1beta.types.safety import SafetySetting
from google.ai.generativelanguage_v1beta.types.safety import HarmCategory
from google.ai.generativelanguage_v1beta.types.text_service import BatchEmbedTextRequest
from google.ai.generativelanguage_v1beta.types.text_service import BatchEmbedTextResponse
from google.ai.generativelanguage_v1beta.types.text_service import CountTextTokensRequest
from google.ai.generativelanguage_v1beta.types.text_service import CountTextTokensResponse
from google.ai.generativelanguage_v1beta.types.text_service import Embedding
from google.ai.generativelanguage_v1beta.types.text_service import EmbedTextRequest
from google.ai.generativelanguage_v1beta.types.text_service import EmbedTextResponse
from google.ai.generativelanguage_v1beta.types.text_service import GenerateTextRequest
from google.ai.generativelanguage_v1beta.types.text_service import GenerateTextResponse
from google.ai.generativelanguage_v1beta.types.text_service import TextCompletion
from google.ai.generativelanguage_v1beta.types.text_service import TextPrompt
from google.ai.generativelanguage_v1beta.types.tuned_model import Dataset
from google.ai.generativelanguage_v1beta.types.tuned_model import Hyperparameters
from google.ai.generativelanguage_v1beta.types.tuned_model import TunedModel
from google.ai.generativelanguage_v1beta.types.tuned_model import TunedModelSource
from google.ai.generativelanguage_v1beta.types.tuned_model import TuningExample
from google.ai.generativelanguage_v1beta.types.tuned_model import TuningExamples
from google.ai.generativelanguage_v1beta.types.tuned_model import TuningSnapshot
from google.ai.generativelanguage_v1beta.types.tuned_model import TuningTask

__all__ = ('DiscussServiceClient',
    'DiscussServiceAsyncClient',
    'GenerativeServiceClient',
    'GenerativeServiceAsyncClient',
    'ModelServiceClient',
    'ModelServiceAsyncClient',
    'PermissionServiceClient',
    'PermissionServiceAsyncClient',
    'RetrieverServiceClient',
    'RetrieverServiceAsyncClient',
    'TextServiceClient',
    'TextServiceAsyncClient',
    'CitationMetadata',
    'CitationSource',
    'Blob',
    'Content',
    'FunctionCall',
    'FunctionDeclaration',
    'FunctionResponse',
    'GroundingPassage',
    'GroundingPassages',
    'Part',
    'Schema',
    'Tool',
    'Type',
    'CountMessageTokensRequest',
    'CountMessageTokensResponse',
    'Example',
    'GenerateMessageRequest',
    'GenerateMessageResponse',
    'Message',
    'MessagePrompt',
    'AttributionSourceId',
    'BatchEmbedContentsRequest',
    'BatchEmbedContentsResponse',
    'Candidate',
    'ContentEmbedding',
    'CountTokensRequest',
    'CountTokensResponse',
    'EmbedContentRequest',
    'EmbedContentResponse',
    'GenerateAnswerRequest',
    'GenerateAnswerResponse',
    'GenerateContentRequest',
    'GenerateContentResponse',
    'GenerationConfig',
    'GroundingAttribution',
    'SemanticRetrieverConfig',
    'TaskType',
    'Model',
    'CreateTunedModelMetadata',
    'CreateTunedModelRequest',
    'DeleteTunedModelRequest',
    'GetModelRequest',
    'GetTunedModelRequest',
    'ListModelsRequest',
    'ListModelsResponse',
    'ListTunedModelsRequest',
    'ListTunedModelsResponse',
    'UpdateTunedModelRequest',
    'Permission',
    'CreatePermissionRequest',
    'DeletePermissionRequest',
    'GetPermissionRequest',
    'ListPermissionsRequest',
    'ListPermissionsResponse',
    'TransferOwnershipRequest',
    'TransferOwnershipResponse',
    'UpdatePermissionRequest',
    'Chunk',
    'ChunkData',
    'Condition',
    'Corpus',
    'CustomMetadata',
    'Document',
    'MetadataFilter',
    'StringList',
    'BatchCreateChunksRequest',
    'BatchCreateChunksResponse',
    'BatchDeleteChunksRequest',
    'BatchUpdateChunksRequest',
    'BatchUpdateChunksResponse',
    'CreateChunkRequest',
    'CreateCorpusRequest',
    'CreateDocumentRequest',
    'DeleteChunkRequest',
    'DeleteCorpusRequest',
    'DeleteDocumentRequest',
    'GetChunkRequest',
    'GetCorpusRequest',
    'GetDocumentRequest',
    'ListChunksRequest',
    'ListChunksResponse',
    'ListCorporaRequest',
    'ListCorporaResponse',
    'ListDocumentsRequest',
    'ListDocumentsResponse',
    'QueryCorpusRequest',
    'QueryCorpusResponse',
    'QueryDocumentRequest',
    'QueryDocumentResponse',
    'RelevantChunk',
    'UpdateChunkRequest',
    'UpdateCorpusRequest',
    'UpdateDocumentRequest',
    'ContentFilter',
    'SafetyFeedback',
    'SafetyRating',
    'SafetySetting',
    'HarmCategory',
    'BatchEmbedTextRequest',
    'BatchEmbedTextResponse',
    'CountTextTokensRequest',
    'CountTextTokensResponse',
    'Embedding',
    'EmbedTextRequest',
    'EmbedTextResponse',
    'GenerateTextRequest',
    'GenerateTextResponse',
    'TextCompletion',
    'TextPrompt',
    'Dataset',
    'Hyperparameters',
    'TunedModel',
    'TunedModelSource',
    'TuningExample',
    'TuningExamples',
    'TuningSnapshot',
    'TuningTask',
)
