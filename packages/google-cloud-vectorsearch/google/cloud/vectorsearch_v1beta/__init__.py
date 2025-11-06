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
from google.cloud.vectorsearch_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.data_object_search_service import (
    DataObjectSearchServiceAsyncClient,
    DataObjectSearchServiceClient,
)
from .services.data_object_service import (
    DataObjectServiceAsyncClient,
    DataObjectServiceClient,
)
from .services.vector_search_service import (
    VectorSearchServiceAsyncClient,
    VectorSearchServiceClient,
)
from .types.common import DistanceMetric
from .types.data_object import DataObject, DenseVector, SparseVector, Vector
from .types.data_object_search_service import (
    AggregateDataObjectsRequest,
    AggregateDataObjectsResponse,
    AggregationMethod,
    BatchSearchDataObjectsRequest,
    BatchSearchDataObjectsResponse,
    OutputFields,
    QueryDataObjectsRequest,
    QueryDataObjectsResponse,
    Ranker,
    ReciprocalRankFusion,
    Search,
    SearchDataObjectsRequest,
    SearchDataObjectsResponse,
    SearchHint,
    SearchResponseMetadata,
    SearchResult,
    SemanticSearch,
    TextSearch,
    VectorSearch,
    VertexRanker,
)
from .types.data_object_service import (
    BatchCreateDataObjectsRequest,
    BatchCreateDataObjectsResponse,
    BatchDeleteDataObjectsRequest,
    BatchUpdateDataObjectsRequest,
    BatchUpdateDataObjectsResponse,
    CreateDataObjectRequest,
    DeleteDataObjectRequest,
    GetDataObjectRequest,
    UpdateDataObjectRequest,
)
from .types.embedding_config import EmbeddingTaskType, VertexEmbeddingConfig
from .types.vectorsearch_service import (
    Collection,
    CreateCollectionRequest,
    CreateIndexRequest,
    DeleteCollectionRequest,
    DeleteIndexRequest,
    DenseVectorField,
    GetCollectionRequest,
    GetIndexRequest,
    ImportDataObjectsMetadata,
    ImportDataObjectsRequest,
    ImportDataObjectsResponse,
    Index,
    ListCollectionsRequest,
    ListCollectionsResponse,
    ListIndexesRequest,
    ListIndexesResponse,
    OperationMetadata,
    SparseVectorField,
    UpdateCollectionRequest,
    VectorField,
)

__all__ = (
    "DataObjectSearchServiceAsyncClient",
    "DataObjectServiceAsyncClient",
    "VectorSearchServiceAsyncClient",
    "AggregateDataObjectsRequest",
    "AggregateDataObjectsResponse",
    "AggregationMethod",
    "BatchCreateDataObjectsRequest",
    "BatchCreateDataObjectsResponse",
    "BatchDeleteDataObjectsRequest",
    "BatchSearchDataObjectsRequest",
    "BatchSearchDataObjectsResponse",
    "BatchUpdateDataObjectsRequest",
    "BatchUpdateDataObjectsResponse",
    "Collection",
    "CreateCollectionRequest",
    "CreateDataObjectRequest",
    "CreateIndexRequest",
    "DataObject",
    "DataObjectSearchServiceClient",
    "DataObjectServiceClient",
    "DeleteCollectionRequest",
    "DeleteDataObjectRequest",
    "DeleteIndexRequest",
    "DenseVector",
    "DenseVectorField",
    "DistanceMetric",
    "EmbeddingTaskType",
    "GetCollectionRequest",
    "GetDataObjectRequest",
    "GetIndexRequest",
    "ImportDataObjectsMetadata",
    "ImportDataObjectsRequest",
    "ImportDataObjectsResponse",
    "Index",
    "ListCollectionsRequest",
    "ListCollectionsResponse",
    "ListIndexesRequest",
    "ListIndexesResponse",
    "OperationMetadata",
    "OutputFields",
    "QueryDataObjectsRequest",
    "QueryDataObjectsResponse",
    "Ranker",
    "ReciprocalRankFusion",
    "Search",
    "SearchDataObjectsRequest",
    "SearchDataObjectsResponse",
    "SearchHint",
    "SearchResponseMetadata",
    "SearchResult",
    "SemanticSearch",
    "SparseVector",
    "SparseVectorField",
    "TextSearch",
    "UpdateCollectionRequest",
    "UpdateDataObjectRequest",
    "Vector",
    "VectorField",
    "VectorSearch",
    "VectorSearchServiceClient",
    "VertexEmbeddingConfig",
    "VertexRanker",
)
