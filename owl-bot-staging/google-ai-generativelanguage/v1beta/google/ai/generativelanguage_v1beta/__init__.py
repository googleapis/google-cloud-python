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
from google.ai.generativelanguage_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.cache_service import CacheServiceClient
from .services.cache_service import CacheServiceAsyncClient
from .services.discuss_service import DiscussServiceClient
from .services.discuss_service import DiscussServiceAsyncClient
from .services.file_service import FileServiceClient
from .services.file_service import FileServiceAsyncClient
from .services.generative_service import GenerativeServiceClient
from .services.generative_service import GenerativeServiceAsyncClient
from .services.model_service import ModelServiceClient
from .services.model_service import ModelServiceAsyncClient
from .services.permission_service import PermissionServiceClient
from .services.permission_service import PermissionServiceAsyncClient
from .services.retriever_service import RetrieverServiceClient
from .services.retriever_service import RetrieverServiceAsyncClient
from .services.text_service import TextServiceClient
from .services.text_service import TextServiceAsyncClient

from .types.cache_service import CreateCachedContentRequest
from .types.cache_service import DeleteCachedContentRequest
from .types.cache_service import GetCachedContentRequest
from .types.cache_service import ListCachedContentsRequest
from .types.cache_service import ListCachedContentsResponse
from .types.cache_service import UpdateCachedContentRequest
from .types.cached_content import CachedContent
from .types.citation import CitationMetadata
from .types.citation import CitationSource
from .types.content import Blob
from .types.content import Content
from .types.content import FileData
from .types.content import FunctionCall
from .types.content import FunctionCallingConfig
from .types.content import FunctionDeclaration
from .types.content import FunctionResponse
from .types.content import GroundingPassage
from .types.content import GroundingPassages
from .types.content import Part
from .types.content import Schema
from .types.content import Tool
from .types.content import ToolConfig
from .types.content import Type
from .types.discuss_service import CountMessageTokensRequest
from .types.discuss_service import CountMessageTokensResponse
from .types.discuss_service import Example
from .types.discuss_service import GenerateMessageRequest
from .types.discuss_service import GenerateMessageResponse
from .types.discuss_service import Message
from .types.discuss_service import MessagePrompt
from .types.file import File
from .types.file import VideoMetadata
from .types.file_service import CreateFileRequest
from .types.file_service import CreateFileResponse
from .types.file_service import DeleteFileRequest
from .types.file_service import GetFileRequest
from .types.file_service import ListFilesRequest
from .types.file_service import ListFilesResponse
from .types.generative_service import AttributionSourceId
from .types.generative_service import BatchEmbedContentsRequest
from .types.generative_service import BatchEmbedContentsResponse
from .types.generative_service import Candidate
from .types.generative_service import ContentEmbedding
from .types.generative_service import CountTokensRequest
from .types.generative_service import CountTokensResponse
from .types.generative_service import EmbedContentRequest
from .types.generative_service import EmbedContentResponse
from .types.generative_service import GenerateAnswerRequest
from .types.generative_service import GenerateAnswerResponse
from .types.generative_service import GenerateContentRequest
from .types.generative_service import GenerateContentResponse
from .types.generative_service import GenerationConfig
from .types.generative_service import GroundingAttribution
from .types.generative_service import SemanticRetrieverConfig
from .types.generative_service import TaskType
from .types.model import Model
from .types.model_service import CreateTunedModelMetadata
from .types.model_service import CreateTunedModelRequest
from .types.model_service import DeleteTunedModelRequest
from .types.model_service import GetModelRequest
from .types.model_service import GetTunedModelRequest
from .types.model_service import ListModelsRequest
from .types.model_service import ListModelsResponse
from .types.model_service import ListTunedModelsRequest
from .types.model_service import ListTunedModelsResponse
from .types.model_service import UpdateTunedModelRequest
from .types.permission import Permission
from .types.permission_service import CreatePermissionRequest
from .types.permission_service import DeletePermissionRequest
from .types.permission_service import GetPermissionRequest
from .types.permission_service import ListPermissionsRequest
from .types.permission_service import ListPermissionsResponse
from .types.permission_service import TransferOwnershipRequest
from .types.permission_service import TransferOwnershipResponse
from .types.permission_service import UpdatePermissionRequest
from .types.retriever import Chunk
from .types.retriever import ChunkData
from .types.retriever import Condition
from .types.retriever import Corpus
from .types.retriever import CustomMetadata
from .types.retriever import Document
from .types.retriever import MetadataFilter
from .types.retriever import StringList
from .types.retriever_service import BatchCreateChunksRequest
from .types.retriever_service import BatchCreateChunksResponse
from .types.retriever_service import BatchDeleteChunksRequest
from .types.retriever_service import BatchUpdateChunksRequest
from .types.retriever_service import BatchUpdateChunksResponse
from .types.retriever_service import CreateChunkRequest
from .types.retriever_service import CreateCorpusRequest
from .types.retriever_service import CreateDocumentRequest
from .types.retriever_service import DeleteChunkRequest
from .types.retriever_service import DeleteCorpusRequest
from .types.retriever_service import DeleteDocumentRequest
from .types.retriever_service import GetChunkRequest
from .types.retriever_service import GetCorpusRequest
from .types.retriever_service import GetDocumentRequest
from .types.retriever_service import ListChunksRequest
from .types.retriever_service import ListChunksResponse
from .types.retriever_service import ListCorporaRequest
from .types.retriever_service import ListCorporaResponse
from .types.retriever_service import ListDocumentsRequest
from .types.retriever_service import ListDocumentsResponse
from .types.retriever_service import QueryCorpusRequest
from .types.retriever_service import QueryCorpusResponse
from .types.retriever_service import QueryDocumentRequest
from .types.retriever_service import QueryDocumentResponse
from .types.retriever_service import RelevantChunk
from .types.retriever_service import UpdateChunkRequest
from .types.retriever_service import UpdateCorpusRequest
from .types.retriever_service import UpdateDocumentRequest
from .types.safety import ContentFilter
from .types.safety import SafetyFeedback
from .types.safety import SafetyRating
from .types.safety import SafetySetting
from .types.safety import HarmCategory
from .types.text_service import BatchEmbedTextRequest
from .types.text_service import BatchEmbedTextResponse
from .types.text_service import CountTextTokensRequest
from .types.text_service import CountTextTokensResponse
from .types.text_service import Embedding
from .types.text_service import EmbedTextRequest
from .types.text_service import EmbedTextResponse
from .types.text_service import GenerateTextRequest
from .types.text_service import GenerateTextResponse
from .types.text_service import TextCompletion
from .types.text_service import TextPrompt
from .types.tuned_model import Dataset
from .types.tuned_model import Hyperparameters
from .types.tuned_model import TunedModel
from .types.tuned_model import TunedModelSource
from .types.tuned_model import TuningExample
from .types.tuned_model import TuningExamples
from .types.tuned_model import TuningSnapshot
from .types.tuned_model import TuningTask

__all__ = (
    'CacheServiceAsyncClient',
    'DiscussServiceAsyncClient',
    'FileServiceAsyncClient',
    'GenerativeServiceAsyncClient',
    'ModelServiceAsyncClient',
    'PermissionServiceAsyncClient',
    'RetrieverServiceAsyncClient',
    'TextServiceAsyncClient',
'AttributionSourceId',
'BatchCreateChunksRequest',
'BatchCreateChunksResponse',
'BatchDeleteChunksRequest',
'BatchEmbedContentsRequest',
'BatchEmbedContentsResponse',
'BatchEmbedTextRequest',
'BatchEmbedTextResponse',
'BatchUpdateChunksRequest',
'BatchUpdateChunksResponse',
'Blob',
'CacheServiceClient',
'CachedContent',
'Candidate',
'Chunk',
'ChunkData',
'CitationMetadata',
'CitationSource',
'Condition',
'Content',
'ContentEmbedding',
'ContentFilter',
'Corpus',
'CountMessageTokensRequest',
'CountMessageTokensResponse',
'CountTextTokensRequest',
'CountTextTokensResponse',
'CountTokensRequest',
'CountTokensResponse',
'CreateCachedContentRequest',
'CreateChunkRequest',
'CreateCorpusRequest',
'CreateDocumentRequest',
'CreateFileRequest',
'CreateFileResponse',
'CreatePermissionRequest',
'CreateTunedModelMetadata',
'CreateTunedModelRequest',
'CustomMetadata',
'Dataset',
'DeleteCachedContentRequest',
'DeleteChunkRequest',
'DeleteCorpusRequest',
'DeleteDocumentRequest',
'DeleteFileRequest',
'DeletePermissionRequest',
'DeleteTunedModelRequest',
'DiscussServiceClient',
'Document',
'EmbedContentRequest',
'EmbedContentResponse',
'EmbedTextRequest',
'EmbedTextResponse',
'Embedding',
'Example',
'File',
'FileData',
'FileServiceClient',
'FunctionCall',
'FunctionCallingConfig',
'FunctionDeclaration',
'FunctionResponse',
'GenerateAnswerRequest',
'GenerateAnswerResponse',
'GenerateContentRequest',
'GenerateContentResponse',
'GenerateMessageRequest',
'GenerateMessageResponse',
'GenerateTextRequest',
'GenerateTextResponse',
'GenerationConfig',
'GenerativeServiceClient',
'GetCachedContentRequest',
'GetChunkRequest',
'GetCorpusRequest',
'GetDocumentRequest',
'GetFileRequest',
'GetModelRequest',
'GetPermissionRequest',
'GetTunedModelRequest',
'GroundingAttribution',
'GroundingPassage',
'GroundingPassages',
'HarmCategory',
'Hyperparameters',
'ListCachedContentsRequest',
'ListCachedContentsResponse',
'ListChunksRequest',
'ListChunksResponse',
'ListCorporaRequest',
'ListCorporaResponse',
'ListDocumentsRequest',
'ListDocumentsResponse',
'ListFilesRequest',
'ListFilesResponse',
'ListModelsRequest',
'ListModelsResponse',
'ListPermissionsRequest',
'ListPermissionsResponse',
'ListTunedModelsRequest',
'ListTunedModelsResponse',
'Message',
'MessagePrompt',
'MetadataFilter',
'Model',
'ModelServiceClient',
'Part',
'Permission',
'PermissionServiceClient',
'QueryCorpusRequest',
'QueryCorpusResponse',
'QueryDocumentRequest',
'QueryDocumentResponse',
'RelevantChunk',
'RetrieverServiceClient',
'SafetyFeedback',
'SafetyRating',
'SafetySetting',
'Schema',
'SemanticRetrieverConfig',
'StringList',
'TaskType',
'TextCompletion',
'TextPrompt',
'TextServiceClient',
'Tool',
'ToolConfig',
'TransferOwnershipRequest',
'TransferOwnershipResponse',
'TunedModel',
'TunedModelSource',
'TuningExample',
'TuningExamples',
'TuningSnapshot',
'TuningTask',
'Type',
'UpdateCachedContentRequest',
'UpdateChunkRequest',
'UpdateCorpusRequest',
'UpdateDocumentRequest',
'UpdatePermissionRequest',
'UpdateTunedModelRequest',
'VideoMetadata',
)
