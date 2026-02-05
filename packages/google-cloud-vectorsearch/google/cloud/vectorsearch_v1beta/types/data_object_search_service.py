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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import google.protobuf.struct_pb2 as struct_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.vectorsearch_v1beta.types import data_object as gcv_data_object
from google.cloud.vectorsearch_v1beta.types import common
from google.cloud.vectorsearch_v1beta.types import embedding_config

__protobuf__ = proto.module(
    package="google.cloud.vectorsearch.v1beta",
    manifest={
        "AggregationMethod",
        "OutputFields",
        "SearchHint",
        "Search",
        "VectorSearch",
        "SemanticSearch",
        "TextSearch",
        "SearchDataObjectsRequest",
        "SearchResult",
        "SearchResponseMetadata",
        "SearchDataObjectsResponse",
        "AggregateDataObjectsRequest",
        "AggregateDataObjectsResponse",
        "QueryDataObjectsRequest",
        "QueryDataObjectsResponse",
        "BatchSearchDataObjectsRequest",
        "Ranker",
        "ReciprocalRankFusion",
        "VertexRanker",
        "BatchSearchDataObjectsResponse",
    },
)


class AggregationMethod(proto.Enum):
    r"""Aggregation methods.

    Values:
        AGGREGATION_METHOD_UNSPECIFIED (0):
            Should not be used.
        COUNT (1):
            Count the number of data objects that match
            the filter.
    """
    AGGREGATION_METHOD_UNSPECIFIED = 0
    COUNT = 1


class OutputFields(proto.Message):
    r"""Defines a output fields struct for data in DataObject.

    Attributes:
        data_fields (MutableSequence[str]):
            Optional. The fields from the data fields to
            include in the output.
        vector_fields (MutableSequence[str]):
            Optional. The fields from the vector fields
            to include in the output.
        metadata_fields (MutableSequence[str]):
            Optional. The fields from the DataObject
            metadata to include in the output.
    """

    data_fields: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    vector_fields: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    metadata_fields: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class SearchHint(proto.Message):
    r"""Represents a hint to the search index engine.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        use_index (google.cloud.vectorsearch_v1beta.types.SearchHint.IndexHint):
            Optional. Specifies that the search should
            use a particular index.

            This field is a member of `oneof`_ ``index_type``.
        use_knn (bool):
            Optional. If set to true, the search will use
            the system's default K-Nearest Neighbor (KNN)
            index engine.

            This field is a member of `oneof`_ ``index_type``.
    """

    class IndexHint(proto.Message):
        r"""Message to specify the index to use for the search.

        Attributes:
            name (str):
                Required. The resource name of the index to use for the
                search. The index must be in the same project, location, and
                collection. Format:
                ``projects/{project}/locations/{location}/collections/{collection}/indexes/{index}``
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )

    use_index: IndexHint = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="index_type",
        message=IndexHint,
    )
    use_knn: bool = proto.Field(
        proto.BOOL,
        number=2,
        oneof="index_type",
    )


class Search(proto.Message):
    r"""A single search request within a batch operation.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        vector_search (google.cloud.vectorsearch_v1beta.types.VectorSearch):
            A vector-based search.

            This field is a member of `oneof`_ ``search_type``.
        semantic_search (google.cloud.vectorsearch_v1beta.types.SemanticSearch):
            A semantic search.

            This field is a member of `oneof`_ ``search_type``.
        text_search (google.cloud.vectorsearch_v1beta.types.TextSearch):
            A text search operation.

            This field is a member of `oneof`_ ``search_type``.
    """

    vector_search: "VectorSearch" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="search_type",
        message="VectorSearch",
    )
    semantic_search: "SemanticSearch" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="search_type",
        message="SemanticSearch",
    )
    text_search: "TextSearch" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="search_type",
        message="TextSearch",
    )


class VectorSearch(proto.Message):
    r"""Defines a search operation using a query vector.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        vector (google.cloud.vectorsearch_v1beta.types.DenseVector):
            A dense vector for the query.

            This field is a member of `oneof`_ ``vector_type``.
        sparse_vector (google.cloud.vectorsearch_v1beta.types.SparseVector):
            A sparse vector for the query.

            This field is a member of `oneof`_ ``vector_type``.
        search_field (str):
            Required. The vector field to search.
        filter (google.protobuf.struct_pb2.Struct):
            Optional. A JSON filter expression, e.g.
            {"genre": {"$eq": "sci-fi"}}, represented as a
            google.protobuf.Struct.
        top_k (int):
            Optional. The number of nearest neighbors to
            return.

            This field is a member of `oneof`_ ``_top_k``.
        output_fields (google.cloud.vectorsearch_v1beta.types.OutputFields):
            Optional. Mask specifying which fields to
            return.
        search_hint (google.cloud.vectorsearch_v1beta.types.SearchHint):
            Optional. Sets the search hint. If no
            strategy is specified, the service will use an
            index if one is available, and fall back to the
            default KNN search otherwise.
        distance_metric (google.cloud.vectorsearch_v1beta.types.DistanceMetric):
            Optional. The distance metric to use for the KNN search. If
            not specified, DOT_PRODUCT will be used as the default.
    """

    vector: gcv_data_object.DenseVector = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="vector_type",
        message=gcv_data_object.DenseVector,
    )
    sparse_vector: gcv_data_object.SparseVector = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="vector_type",
        message=gcv_data_object.SparseVector,
    )
    search_field: str = proto.Field(
        proto.STRING,
        number=8,
    )
    filter: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=4,
        message=struct_pb2.Struct,
    )
    top_k: int = proto.Field(
        proto.INT32,
        number=5,
        optional=True,
    )
    output_fields: "OutputFields" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="OutputFields",
    )
    search_hint: "SearchHint" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="SearchHint",
    )
    distance_metric: common.DistanceMetric = proto.Field(
        proto.ENUM,
        number=11,
        enum=common.DistanceMetric,
    )


class SemanticSearch(proto.Message):
    r"""Defines a semantic search operation.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        search_text (str):
            Required. The query text, which is used to
            generate an embedding according to the embedding
            model specified in the collection config.
        search_field (str):
            Required. The vector field to search.
        task_type (google.cloud.vectorsearch_v1beta.types.EmbeddingTaskType):
            Optional. The task type of the query
            embedding.
        output_fields (google.cloud.vectorsearch_v1beta.types.OutputFields):
            Optional. The fields to return in the search
            results.
        filter (google.protobuf.struct_pb2.Struct):
            Optional. A JSON filter expression, e.g.
            {"genre": {"$eq": "sci-fi"}}, represented as a
            google.protobuf.Struct.
        top_k (int):
            Optional. The number of data objects to
            return.

            This field is a member of `oneof`_ ``_top_k``.
        search_hint (google.cloud.vectorsearch_v1beta.types.SearchHint):
            Optional. Sets the search hint. If no
            strategy is specified, the service will use an
            index if one is available, and fall back to KNN
            search otherwise.
    """

    search_text: str = proto.Field(
        proto.STRING,
        number=1,
    )
    search_field: str = proto.Field(
        proto.STRING,
        number=2,
    )
    task_type: embedding_config.EmbeddingTaskType = proto.Field(
        proto.ENUM,
        number=5,
        enum=embedding_config.EmbeddingTaskType,
    )
    output_fields: "OutputFields" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="OutputFields",
    )
    filter: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=6,
        message=struct_pb2.Struct,
    )
    top_k: int = proto.Field(
        proto.INT32,
        number=4,
        optional=True,
    )
    search_hint: "SearchHint" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="SearchHint",
    )


class TextSearch(proto.Message):
    r"""Defines a text search operation.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        search_text (str):
            Required. The query text.
        data_field_names (MutableSequence[str]):
            Required. The data field names to search.
        output_fields (google.cloud.vectorsearch_v1beta.types.OutputFields):
            Optional. The fields to return in the search
            results.
        top_k (int):
            Optional. The number of results to return.

            This field is a member of `oneof`_ ``_top_k``.
        filter (google.protobuf.struct_pb2.Struct):
            Optional. A JSON filter expression, e.g.
            ``{"genre": {"$eq": "sci-fi"}}``, represented as a
            ``google.protobuf.Struct``.
    """

    search_text: str = proto.Field(
        proto.STRING,
        number=1,
    )
    data_field_names: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    output_fields: "OutputFields" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="OutputFields",
    )
    top_k: int = proto.Field(
        proto.INT32,
        number=4,
        optional=True,
    )
    filter: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=5,
        message=struct_pb2.Struct,
    )


class SearchDataObjectsRequest(proto.Message):
    r"""Request for performing a single search.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        vector_search (google.cloud.vectorsearch_v1beta.types.VectorSearch):
            A vector search operation.

            This field is a member of `oneof`_ ``search_type``.
        semantic_search (google.cloud.vectorsearch_v1beta.types.SemanticSearch):
            A semantic search operation.

            This field is a member of `oneof`_ ``search_type``.
        text_search (google.cloud.vectorsearch_v1beta.types.TextSearch):
            Optional. A text search operation.

            This field is a member of `oneof`_ ``search_type``.
        parent (str):
            Required. The resource name of the Collection for which to
            search. Format:
            ``projects/{project}/locations/{location}/collections/{collection}``
        page_size (int):
            Optional. The standard list page size.
        page_token (str):
            Optional. The standard list page token. Typically obtained
            via
            [SearchDataObjectsResponse.next_page_token][google.cloud.vectorsearch.v1beta.SearchDataObjectsResponse.next_page_token]
            of the previous
            [DataObjectSearchService.SearchDataObjects][google.cloud.vectorsearch.v1beta.DataObjectSearchService.SearchDataObjects]
            call.
    """

    vector_search: "VectorSearch" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="search_type",
        message="VectorSearch",
    )
    semantic_search: "SemanticSearch" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="search_type",
        message="SemanticSearch",
    )
    text_search: "TextSearch" = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="search_type",
        message="TextSearch",
    )
    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=5,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=6,
    )


class SearchResult(proto.Message):
    r"""A single search result.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        data_object (google.cloud.vectorsearch_v1beta.types.DataObject):
            Output only. The matching data object.
        distance (float):
            Output only. The similarity distance.

            This field is a member of `oneof`_ ``_distance``.
    """

    data_object: gcv_data_object.DataObject = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcv_data_object.DataObject,
    )
    distance: float = proto.Field(
        proto.DOUBLE,
        number=2,
        optional=True,
    )


class SearchResponseMetadata(proto.Message):
    r"""Metadata about the search execution.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        used_index (google.cloud.vectorsearch_v1beta.types.SearchResponseMetadata.IndexInfo):
            Indicates that the search used a particular
            index.

            This field is a member of `oneof`_ ``index_type``.
        used_knn (bool):
            Output only. If true, the search used the
            system's default K-Nearest Neighbor (KNN) index
            engine.

            This field is a member of `oneof`_ ``index_type``.
    """

    class IndexInfo(proto.Message):
        r"""Message that indicates the index used for the search.

        Attributes:
            name (str):
                Output only. The resource name of the index used for the
                search. Format:
                ``projects/{project}/locations/{location}/collections/{collection}/indexes/{index}``
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )

    used_index: IndexInfo = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="index_type",
        message=IndexInfo,
    )
    used_knn: bool = proto.Field(
        proto.BOOL,
        number=2,
        oneof="index_type",
    )


class SearchDataObjectsResponse(proto.Message):
    r"""Response for a search request.

    Attributes:
        results (MutableSequence[google.cloud.vectorsearch_v1beta.types.SearchResult]):
            Output only. The list of dataObjects that
            match the search criteria.
        next_page_token (str):
            Output only. A token to retrieve next page of results. Pass
            to
            [DataObjectSearchService.SearchDataObjectsRequest.page_token][]
            to obtain that page.
        search_response_metadata (google.cloud.vectorsearch_v1beta.types.SearchResponseMetadata):
            Output only. Metadata about the search
            execution.
    """

    @property
    def raw_page(self):
        return self

    results: MutableSequence["SearchResult"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="SearchResult",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    search_response_metadata: "SearchResponseMetadata" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="SearchResponseMetadata",
    )


class AggregateDataObjectsRequest(proto.Message):
    r"""Request message for
    [DataObjectSearchService.AggregateDataObjects][google.cloud.vectorsearch.v1beta.DataObjectSearchService.AggregateDataObjects].

    Attributes:
        parent (str):
            Required. The resource name of the Collection for which to
            query. Format:
            ``projects/{project}/locations/{location}/collections/{collection}``
        filter (google.protobuf.struct_pb2.Struct):
            Optional. A JSON filter expression, e.g.
            {"genre": {"$eq": "sci-fi"}}, represented as a
            google.protobuf.Struct.
        aggregate (google.cloud.vectorsearch_v1beta.types.AggregationMethod):
            Required. The aggregation method to apply to
            the query.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Struct,
    )
    aggregate: "AggregationMethod" = proto.Field(
        proto.ENUM,
        number=3,
        enum="AggregationMethod",
    )


class AggregateDataObjectsResponse(proto.Message):
    r"""Response message for
    [DataObjectSearchService.AggregateDataObjects][google.cloud.vectorsearch.v1beta.DataObjectSearchService.AggregateDataObjects].

    Attributes:
        aggregate_results (MutableSequence[google.protobuf.struct_pb2.Struct]):
            The aggregated results of the query.
    """

    aggregate_results: MutableSequence[struct_pb2.Struct] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=struct_pb2.Struct,
    )


class QueryDataObjectsRequest(proto.Message):
    r"""Request message for
    [DataObjectSearchService.QueryDataObjects][google.cloud.vectorsearch.v1beta.DataObjectSearchService.QueryDataObjects].

    Attributes:
        parent (str):
            Required. The resource name of the Collection for which to
            query. Format:
            ``projects/{project}/locations/{location}/collections/{collection}``
        filter (google.protobuf.struct_pb2.Struct):
            Optional. A JSON filter expression, e.g.
            {"genre": {"$eq": "sci-fi"}}, represented as a
            google.protobuf.Struct.
        output_fields (google.cloud.vectorsearch_v1beta.types.OutputFields):
            Optional. Mask specifying which fields to
            return.
        page_size (int):
            Optional. The standard list page size.
        page_token (str):
            Optional. The standard list page token. Typically obtained
            via
            [QueryDataObjectsResponse.next_page_token][google.cloud.vectorsearch.v1beta.QueryDataObjectsResponse.next_page_token]
            of the previous
            [DataObjectSearchService.QueryDataObjects][google.cloud.vectorsearch.v1beta.DataObjectSearchService.QueryDataObjects]
            call.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Struct,
    )
    output_fields: "OutputFields" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="OutputFields",
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=5,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=6,
    )


class QueryDataObjectsResponse(proto.Message):
    r"""Response message for
    [DataObjectSearchService.QueryDataObjects][google.cloud.vectorsearch.v1beta.DataObjectSearchService.QueryDataObjects].

    Attributes:
        data_objects (MutableSequence[google.cloud.vectorsearch_v1beta.types.DataObject]):
            The list of dataObjects that match the query.
        next_page_token (str):
            A token to retrieve next page of results. Pass to
            [DataObjectSearchService.QueryDataObjectsRequest.page_token][]
            to obtain that page.
    """

    @property
    def raw_page(self):
        return self

    data_objects: MutableSequence[gcv_data_object.DataObject] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=gcv_data_object.DataObject,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class BatchSearchDataObjectsRequest(proto.Message):
    r"""A request to perform a batch of search operations.

    Attributes:
        parent (str):
            Required. The resource name of the Collection for which to
            search. Format:
            ``projects/{project}/locations/{location}/collections/{collection}``
        searches (MutableSequence[google.cloud.vectorsearch_v1beta.types.Search]):
            Required. A list of search requests to
            execute in parallel.
        combine (google.cloud.vectorsearch_v1beta.types.BatchSearchDataObjectsRequest.CombineResultsOptions):
            Optional. Options for combining the results
            of the batch search operations.
    """

    class CombineResultsOptions(proto.Message):
        r"""Options for combining the results of the batch search
        operations.

        Attributes:
            ranker (google.cloud.vectorsearch_v1beta.types.Ranker):
                Required. The ranker to use for combining the
                results.
            output_fields (google.cloud.vectorsearch_v1beta.types.OutputFields):
                Optional. Mask specifying which fields to
                return.
            top_k (int):
                Optional. The number of results to return. If
                not set, a default value will be used.
        """

        ranker: "Ranker" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Ranker",
        )
        output_fields: "OutputFields" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="OutputFields",
        )
        top_k: int = proto.Field(
            proto.INT32,
            number=3,
        )

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    searches: MutableSequence["Search"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Search",
    )
    combine: CombineResultsOptions = proto.Field(
        proto.MESSAGE,
        number=3,
        message=CombineResultsOptions,
    )


class Ranker(proto.Message):
    r"""Defines a ranker to combine results from multiple searches.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        rrf (google.cloud.vectorsearch_v1beta.types.ReciprocalRankFusion):
            Reciprocal Rank Fusion ranking.

            This field is a member of `oneof`_ ``ranker``.
        vertex (google.cloud.vectorsearch_v1beta.types.VertexRanker):
            Vertex AI ranking.

            This field is a member of `oneof`_ ``ranker``.
    """

    rrf: "ReciprocalRankFusion" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="ranker",
        message="ReciprocalRankFusion",
    )
    vertex: "VertexRanker" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="ranker",
        message="VertexRanker",
    )


class ReciprocalRankFusion(proto.Message):
    r"""Defines the Reciprocal Rank Fusion (RRF) algorithm for result
    ranking.

    Attributes:
        weights (MutableSequence[float]):
            Required. The weights to apply to each search
            result set during fusion.
    """

    weights: MutableSequence[float] = proto.RepeatedField(
        proto.DOUBLE,
        number=1,
    )


class VertexRanker(proto.Message):
    r"""Defines a ranker using the Vertex AI ranking service.
    See
    https://cloud.google.com/generative-ai-app-builder/docs/ranking
    for details.

    Attributes:
        query (str):
            Required. The query against which the records
            are ranked and scored.
        title_template (str):
            Optional. The template used to generate the
            record's title.
        content_template (str):
            Optional. The template used to generate the
            record's content.
        model (str):
            Required. The model used for ranking
            documents. If no model is specified, then
            semantic-ranker-default@latest is used.
    """

    query: str = proto.Field(
        proto.STRING,
        number=1,
    )
    title_template: str = proto.Field(
        proto.STRING,
        number=2,
    )
    content_template: str = proto.Field(
        proto.STRING,
        number=3,
    )
    model: str = proto.Field(
        proto.STRING,
        number=4,
    )


class BatchSearchDataObjectsResponse(proto.Message):
    r"""A response from a batch search operation.

    Attributes:
        results (MutableSequence[google.cloud.vectorsearch_v1beta.types.SearchDataObjectsResponse]):
            Output only. A list of search responses, one
            for each request in the batch. If a ranker is
            used, a single ranked list of results is
            returned.
    """

    results: MutableSequence["SearchDataObjectsResponse"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="SearchDataObjectsResponse",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
