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

import google.protobuf.field_mask_pb2 as field_mask_pb2  # type: ignore
import google.protobuf.struct_pb2 as struct_pb2  # type: ignore
import google.protobuf.timestamp_pb2 as timestamp_pb2  # type: ignore
import google.rpc.status_pb2 as status_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.vectorsearch_v1beta.types import common, embedding_config

__protobuf__ = proto.module(
    package="google.cloud.vectorsearch.v1beta",
    manifest={
        "Collection",
        "VectorField",
        "DenseVectorField",
        "SparseVectorField",
        "ListCollectionsRequest",
        "ListCollectionsResponse",
        "GetCollectionRequest",
        "CreateCollectionRequest",
        "UpdateCollectionRequest",
        "DeleteCollectionRequest",
        "Index",
        "CreateIndexRequest",
        "DeleteIndexRequest",
        "ListIndexesRequest",
        "ListIndexesResponse",
        "GetIndexRequest",
        "OperationMetadata",
        "ImportDataObjectsRequest",
        "ImportDataObjectsMetadata",
        "ImportDataObjectsResponse",
        "ExportDataObjectsRequest",
        "ExportDataObjectsMetadata",
        "ExportDataObjectsResponse",
    },
)


class Collection(proto.Message):
    r"""Message describing Collection object

    Attributes:
        name (str):
            Identifier. name of resource
        display_name (str):
            Optional. User-specified display name of the
            collection
        description (str):
            Optional. User-specified description of the
            collection
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Create time stamp
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Update time stamp
        labels (MutableMapping[str, str]):
            Optional. Labels as key value pairs.
        schema (google.protobuf.struct_pb2.Struct):
            Optional. Deprecated: JSON Schema for data. Please use
            data_schema instead.
        vector_schema (MutableMapping[str, google.cloud.vectorsearch_v1beta.types.VectorField]):
            Optional. Schema for vector fields. Only
            vector fields in this schema will be searchable.
            Field names must contain only alphanumeric
            characters, underscores, and hyphens.
        data_schema (google.protobuf.struct_pb2.Struct):
            Optional. JSON Schema for data.
            Field names must contain only alphanumeric
            characters, underscores, and hyphens.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=8,
    )
    description: str = proto.Field(
        proto.STRING,
        number=9,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    schema: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=5,
        message=struct_pb2.Struct,
    )
    vector_schema: MutableMapping[str, "VectorField"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=7,
        message="VectorField",
    )
    data_schema: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=10,
        message=struct_pb2.Struct,
    )


class VectorField(proto.Message):
    r"""Message describing a vector field.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        dense_vector (google.cloud.vectorsearch_v1beta.types.DenseVectorField):
            Dense vector field.

            This field is a member of `oneof`_ ``vector_type_config``.
        sparse_vector (google.cloud.vectorsearch_v1beta.types.SparseVectorField):
            Sparse vector field.

            This field is a member of `oneof`_ ``vector_type_config``.
    """

    dense_vector: "DenseVectorField" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="vector_type_config",
        message="DenseVectorField",
    )
    sparse_vector: "SparseVectorField" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="vector_type_config",
        message="SparseVectorField",
    )


class DenseVectorField(proto.Message):
    r"""Message describing a dense vector field.

    Attributes:
        dimensions (int):
            Dimensionality of the vector field.
        vertex_embedding_config (google.cloud.vectorsearch_v1beta.types.VertexEmbeddingConfig):
            Optional. Configuration for generating
            embeddings for the vector field. If not
            specified, the embedding field must be populated
            in the DataObject.
    """

    dimensions: int = proto.Field(
        proto.INT32,
        number=1,
    )
    vertex_embedding_config: embedding_config.VertexEmbeddingConfig = proto.Field(
        proto.MESSAGE,
        number=3,
        message=embedding_config.VertexEmbeddingConfig,
    )


class SparseVectorField(proto.Message):
    r"""Message describing a sparse vector field."""


class ListCollectionsRequest(proto.Message):
    r"""Message for requesting list of Collections

    Attributes:
        parent (str):
            Required. Parent value for
            ListCollectionsRequest
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
        filter (str):
            Optional. Filtering results
        order_by (str):
            Optional. Hint for how to order the results
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListCollectionsResponse(proto.Message):
    r"""Message for response to listing Collections

    Attributes:
        collections (MutableSequence[google.cloud.vectorsearch_v1beta.types.Collection]):
            The list of Collection
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Unordered list. Locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    collections: MutableSequence["Collection"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Collection",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetCollectionRequest(proto.Message):
    r"""Message for getting a Collection

    Attributes:
        name (str):
            Required. Name of the resource
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateCollectionRequest(proto.Message):
    r"""Message for creating a Collection

    Attributes:
        parent (str):
            Required. Value for parent.
        collection_id (str):
            Required. ID of the Collection to create. The id must be
            1-63 characters long, and comply with
            `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`__.
            Specifically, it must be 1-63 characters long and match the
            regular expression ``[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?``.
        collection (google.cloud.vectorsearch_v1beta.types.Collection):
            Required. The resource being created
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    collection_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    collection: "Collection" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Collection",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateCollectionRequest(proto.Message):
    r"""Message for updating a Collection

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Field mask is used to specify the fields to be
            overwritten in the Collection resource by the update. The
            fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. If the user does not provide a mask
            then all fields present in the request will be overwritten.

            The following fields support update: ``display_name``,
            ``description``, ``labels``, ``data_schema``,
            ``vector_schema``. For ``data_schema`` and
            ``vector_schema``, fields can only be added, not deleted,
            but ``vertex_embedding_config`` in ``vector_schema`` can be
            added or removed. Partial updates for ``data_schema`` and
            ``vector_schema`` are also supported by using sub-field
            paths in ``update_mask``, e.g.
            ``data_schema.properties.foo`` or
            ``vector_schema.my_vector_field``.

            If ``*`` is provided in the update_mask, full replacement
            will be performed.
        collection (google.cloud.vectorsearch_v1beta.types.Collection):
            Required. The resource being updated
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    collection: "Collection" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Collection",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteCollectionRequest(proto.Message):
    r"""Message for deleting a Collection

    Attributes:
        name (str):
            Required. Name of the resource
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Index(proto.Message):
    r"""Message describing Index object

    Attributes:
        name (str):
            Identifier. name of resource
        display_name (str):
            Optional. User-specified display name of the
            index
        description (str):
            Optional. User-specified description of the
            index
        labels (MutableMapping[str, str]):
            Optional. Labels as key value pairs.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Create time stamp
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Update time stamp
        distance_metric (google.cloud.vectorsearch_v1beta.types.DistanceMetric):
            Optional. Distance metric used for indexing. If not
            specified, will default to DOT_PRODUCT.
        index_field (str):
            Required. The collection schema field to
            index.
        filter_fields (MutableSequence[str]):
            Optional. The fields to push into the index
            to enable fast ANN inline filtering.
        store_fields (MutableSequence[str]):
            Optional. The fields to push into the index
            to enable inline data retrieval.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=8,
    )
    description: str = proto.Field(
        proto.STRING,
        number=9,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=10,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    distance_metric: common.DistanceMetric = proto.Field(
        proto.ENUM,
        number=4,
        enum=common.DistanceMetric,
    )
    index_field: str = proto.Field(
        proto.STRING,
        number=5,
    )
    filter_fields: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    store_fields: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )


class CreateIndexRequest(proto.Message):
    r"""Message for creating an Index.

    Attributes:
        parent (str):
            Required. The resource name of the Collection for which to
            create the Index. Format:
            ``projects/{project}/locations/{location}/collections/{collection}``
        index_id (str):
            Required. ID of the Index to create. The id must be 1-63
            characters long, and comply with
            `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`__.
            Specifically, it must be 1-63 characters long and match the
            regular expression ``[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?``.
        index (google.cloud.vectorsearch_v1beta.types.Index):
            Required. The resource being created
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    index_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    index: "Index" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Index",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class DeleteIndexRequest(proto.Message):
    r"""Message for deleting an Index.

    Attributes:
        name (str):
            Required. The resource name of the Index to delete. Format:
            ``projects/{project}/locations/{location}/collections/{collection}/indexes/{index}``
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListIndexesRequest(proto.Message):
    r"""Message for requesting list of Indexes

    Attributes:
        parent (str):
            Required. Parent value for ListIndexesRequest
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
        filter (str):
            Optional. Filtering results
        order_by (str):
            Optional. Hint for how to order the results
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListIndexesResponse(proto.Message):
    r"""Message for response to listing Indexes

    Attributes:
        indexes (MutableSequence[google.cloud.vectorsearch_v1beta.types.Index]):
            The list of Index
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    indexes: MutableSequence["Index"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Index",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetIndexRequest(proto.Message):
    r"""Message for getting an Index

    Attributes:
        name (str):
            Required. Name of the resource
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have been
            cancelled successfully have
            [google.longrunning.Operation.error][google.longrunning.Operation.error]
            value with a
            [google.rpc.Status.code][google.rpc.Status.code] of ``1``,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


class ImportDataObjectsRequest(proto.Message):
    r"""Request message for
    [VectorSearchService.ImportDataObjects][google.cloud.vectorsearch.v1beta.VectorSearchService.ImportDataObjects].


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_import (google.cloud.vectorsearch_v1beta.types.ImportDataObjectsRequest.GcsImportConfig):
            The Cloud Storage location of the input
            content.

            This field is a member of `oneof`_ ``config``.
        name (str):
            Required. The resource name of the Collection to import
            DataObjects into. Format:
            ``projects/{project}/locations/{location}/collections/{collection}``.
    """

    class GcsImportConfig(proto.Message):
        r"""Google Cloud Storage configuration for the import.

        Attributes:
            contents_uri (str):
                Required. URI prefix of the Cloud Storage
                DataObjects to import.
            error_uri (str):
                Required. URI prefix of the Cloud Storage
                location to write any errors encountered during
                the import.
            output_uri (str):
                Optional. URI prefix of the Cloud Storage location to write
                DataObject ``IDs`` and ``etags`` of DataObjects that were
                successfully imported. The service will write the
                successfully imported DataObjects to sharded files under
                this prefix. If this field is empty, no output will be
                written.
        """

        contents_uri: str = proto.Field(
            proto.STRING,
            number=1,
        )
        error_uri: str = proto.Field(
            proto.STRING,
            number=2,
        )
        output_uri: str = proto.Field(
            proto.STRING,
            number=3,
        )

    gcs_import: GcsImportConfig = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="config",
        message=GcsImportConfig,
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ImportDataObjectsMetadata(proto.Message):
    r"""Metadata for
    [VectorSearchService.ImportDataObjects][google.cloud.vectorsearch.v1beta.VectorSearchService.ImportDataObjects].

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation was last updated.
        success_count (int):
            Number of DataObjects that were processed
            successfully.
        failure_count (int):
            Number of DataObjects that failed during
            processing.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    success_count: int = proto.Field(
        proto.INT64,
        number=3,
    )
    failure_count: int = proto.Field(
        proto.INT64,
        number=4,
    )


class ImportDataObjectsResponse(proto.Message):
    r"""Response for
    [VectorSearchService.ImportDataObjects][google.cloud.vectorsearch.v1beta.VectorSearchService.ImportDataObjects].

    Attributes:
        status (google.rpc.status_pb2.Status):
            Status of the LRO
    """

    status: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=1,
        message=status_pb2.Status,
    )


class ExportDataObjectsRequest(proto.Message):
    r"""Request message for
    [VectorSearchService.ExportDataObjects][google.cloud.vectorsearch.v1beta.VectorSearchService.ExportDataObjects].


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_destination (google.cloud.vectorsearch_v1beta.types.ExportDataObjectsRequest.GcsExportDestination):
            The Cloud Storage location where user wants
            to export Data Objects.

            This field is a member of `oneof`_ ``destination``.
        name (str):
            Required. The resource name of the Collection from which we
            want to export Data Objects. Format:
            ``projects/{project}/locations/{location}/collections/{collection}``.
    """

    class GcsExportDestination(proto.Message):
        r"""Google Cloud Storage configuration for the export.

        Attributes:
            export_uri (str):
                Required. URI prefix of the Cloud Storage
                where to export Data Objects. The bucket is
                required to be in the same region as the
                collection.
            format_ (google.cloud.vectorsearch_v1beta.types.ExportDataObjectsRequest.GcsExportDestination.Format):
                Required. The format of the exported Data
                Objects.
        """

        class Format(proto.Enum):
            r"""Options for the format of the exported Data Objects.
            New formats may be added in the future.

            Values:
                FORMAT_UNSPECIFIED (0):
                    Unspecified format.
                JSON (1):
                    The exported Data Objects will be in JSON
                    format.
            """
            FORMAT_UNSPECIFIED = 0
            JSON = 1

        export_uri: str = proto.Field(
            proto.STRING,
            number=1,
        )
        format_: "ExportDataObjectsRequest.GcsExportDestination.Format" = proto.Field(
            proto.ENUM,
            number=2,
            enum="ExportDataObjectsRequest.GcsExportDestination.Format",
        )

    gcs_destination: GcsExportDestination = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="destination",
        message=GcsExportDestination,
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ExportDataObjectsMetadata(proto.Message):
    r"""Metadata for the ExportDataObjects LRO.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation was created.
        finish_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation finished.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    finish_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


class ExportDataObjectsResponse(proto.Message):
    r"""Response for the ExportDataObjects LRO."""


__all__ = tuple(sorted(__protobuf__.manifest))
