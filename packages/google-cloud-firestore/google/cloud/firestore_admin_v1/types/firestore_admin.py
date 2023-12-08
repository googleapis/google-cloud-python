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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.cloud.firestore_admin_v1.types import database as gfa_database
from google.cloud.firestore_admin_v1.types import field as gfa_field
from google.cloud.firestore_admin_v1.types import index as gfa_index
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.firestore.admin.v1",
    manifest={
        "ListDatabasesRequest",
        "CreateDatabaseRequest",
        "CreateDatabaseMetadata",
        "ListDatabasesResponse",
        "GetDatabaseRequest",
        "UpdateDatabaseRequest",
        "UpdateDatabaseMetadata",
        "CreateIndexRequest",
        "ListIndexesRequest",
        "ListIndexesResponse",
        "GetIndexRequest",
        "DeleteIndexRequest",
        "UpdateFieldRequest",
        "GetFieldRequest",
        "ListFieldsRequest",
        "ListFieldsResponse",
        "ExportDocumentsRequest",
        "ImportDocumentsRequest",
    },
)


class ListDatabasesRequest(proto.Message):
    r"""A request to list the Firestore Databases in all locations
    for a project.

    Attributes:
        parent (str):
            Required. A parent name of the form
            ``projects/{project_id}``
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateDatabaseRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.CreateDatabase][google.firestore.admin.v1.FirestoreAdmin.CreateDatabase].

    Attributes:
        parent (str):
            Required. A parent name of the form
            ``projects/{project_id}``
        database (google.cloud.firestore_admin_v1.types.Database):
            Required. The Database to create.
        database_id (str):
            Required. The ID to use for the database,
            which will become the final component of the
            database's resource name.

            The value must be set to "(default)".
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    database: gfa_database.Database = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gfa_database.Database,
    )
    database_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class CreateDatabaseMetadata(proto.Message):
    r"""Metadata related to the create database operation."""


class ListDatabasesResponse(proto.Message):
    r"""The list of databases for a project.

    Attributes:
        databases (MutableSequence[google.cloud.firestore_admin_v1.types.Database]):
            The databases in the project.
    """

    databases: MutableSequence[gfa_database.Database] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gfa_database.Database,
    )


class GetDatabaseRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.GetDatabase][google.firestore.admin.v1.FirestoreAdmin.GetDatabase].

    Attributes:
        name (str):
            Required. A name of the form
            ``projects/{project_id}/databases/{database_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateDatabaseRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.UpdateDatabase][google.firestore.admin.v1.FirestoreAdmin.UpdateDatabase].

    Attributes:
        database (google.cloud.firestore_admin_v1.types.Database):
            Required. The database to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated.
    """

    database: gfa_database.Database = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gfa_database.Database,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class UpdateDatabaseMetadata(proto.Message):
    r"""Metadata related to the update database operation."""


class CreateIndexRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.CreateIndex][google.firestore.admin.v1.FirestoreAdmin.CreateIndex].

    Attributes:
        parent (str):
            Required. A parent name of the form
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}``
        index (google.cloud.firestore_admin_v1.types.Index):
            Required. The composite index to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    index: gfa_index.Index = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gfa_index.Index,
    )


class ListIndexesRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.ListIndexes][google.firestore.admin.v1.FirestoreAdmin.ListIndexes].

    Attributes:
        parent (str):
            Required. A parent name of the form
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}``
        filter (str):
            The filter to apply to list results.
        page_size (int):
            The number of results to return.
        page_token (str):
            A page token, returned from a previous call to
            [FirestoreAdmin.ListIndexes][google.firestore.admin.v1.FirestoreAdmin.ListIndexes],
            that may be used to get the next page of results.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=2,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListIndexesResponse(proto.Message):
    r"""The response for
    [FirestoreAdmin.ListIndexes][google.firestore.admin.v1.FirestoreAdmin.ListIndexes].

    Attributes:
        indexes (MutableSequence[google.cloud.firestore_admin_v1.types.Index]):
            The requested indexes.
        next_page_token (str):
            A page token that may be used to request
            another page of results. If blank, this is the
            last page.
    """

    @property
    def raw_page(self):
        return self

    indexes: MutableSequence[gfa_index.Index] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gfa_index.Index,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetIndexRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.GetIndex][google.firestore.admin.v1.FirestoreAdmin.GetIndex].

    Attributes:
        name (str):
            Required. A name of the form
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/indexes/{index_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteIndexRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.DeleteIndex][google.firestore.admin.v1.FirestoreAdmin.DeleteIndex].

    Attributes:
        name (str):
            Required. A name of the form
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/indexes/{index_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateFieldRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.UpdateField][google.firestore.admin.v1.FirestoreAdmin.UpdateField].

    Attributes:
        field (google.cloud.firestore_admin_v1.types.Field):
            Required. The field to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            A mask, relative to the field. If specified, only
            configuration specified by this field_mask will be updated
            in the field.
    """

    field: gfa_field.Field = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gfa_field.Field,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class GetFieldRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.GetField][google.firestore.admin.v1.FirestoreAdmin.GetField].

    Attributes:
        name (str):
            Required. A name of the form
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/fields/{field_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListFieldsRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields].

    Attributes:
        parent (str):
            Required. A parent name of the form
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}``
        filter (str):
            The filter to apply to list results. Currently,
            [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields]
            only supports listing fields that have been explicitly
            overridden. To issue this query, call
            [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields]
            with a filter that includes
            ``indexConfig.usesAncestorConfig:false`` .
        page_size (int):
            The number of results to return.
        page_token (str):
            A page token, returned from a previous call to
            [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields],
            that may be used to get the next page of results.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=2,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListFieldsResponse(proto.Message):
    r"""The response for
    [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields].

    Attributes:
        fields (MutableSequence[google.cloud.firestore_admin_v1.types.Field]):
            The requested fields.
        next_page_token (str):
            A page token that may be used to request
            another page of results. If blank, this is the
            last page.
    """

    @property
    def raw_page(self):
        return self

    fields: MutableSequence[gfa_field.Field] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gfa_field.Field,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ExportDocumentsRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.ExportDocuments][google.firestore.admin.v1.FirestoreAdmin.ExportDocuments].

    Attributes:
        name (str):
            Required. Database to export. Should be of the form:
            ``projects/{project_id}/databases/{database_id}``.
        collection_ids (MutableSequence[str]):
            Which collection ids to export. Unspecified
            means all collections.
        output_uri_prefix (str):
            The output URI. Currently only supports Google Cloud Storage
            URIs of the form: ``gs://BUCKET_NAME[/NAMESPACE_PATH]``,
            where ``BUCKET_NAME`` is the name of the Google Cloud
            Storage bucket and ``NAMESPACE_PATH`` is an optional Google
            Cloud Storage namespace path. When choosing a name, be sure
            to consider Google Cloud Storage naming guidelines:
            https://cloud.google.com/storage/docs/naming. If the URI is
            a bucket (without a namespace path), a prefix will be
            generated based on the start time.
        namespace_ids (MutableSequence[str]):
            Unspecified means all namespaces. This is the
            preferred usage for databases that don't use
            namespaces.

            An empty string element represents the default
            namespace. This should be used if the database
            has data in non-default namespaces, but doesn't
            want to include them. Each namespace in this
            list must be unique.
        snapshot_time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp that corresponds to the version of the
            database to be exported. The timestamp must be in the past,
            rounded to the minute and not older than
            [earliestVersionTime][google.firestore.admin.v1.Database.earliest_version_time].
            If specified, then the exported documents will represent a
            consistent view of the database at the provided time.
            Otherwise, there are no guarantees about the consistency of
            the exported documents.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    collection_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    output_uri_prefix: str = proto.Field(
        proto.STRING,
        number=3,
    )
    namespace_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    snapshot_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )


class ImportDocumentsRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.ImportDocuments][google.firestore.admin.v1.FirestoreAdmin.ImportDocuments].

    Attributes:
        name (str):
            Required. Database to import into. Should be of the form:
            ``projects/{project_id}/databases/{database_id}``.
        collection_ids (MutableSequence[str]):
            Which collection ids to import. Unspecified
            means all collections included in the import.
        input_uri_prefix (str):
            Location of the exported files. This must match the
            output_uri_prefix of an ExportDocumentsResponse from an
            export that has completed successfully. See:
            [google.firestore.admin.v1.ExportDocumentsResponse.output_uri_prefix][google.firestore.admin.v1.ExportDocumentsResponse.output_uri_prefix].
        namespace_ids (MutableSequence[str]):
            Unspecified means all namespaces. This is the
            preferred usage for databases that don't use
            namespaces.

            An empty string element represents the default
            namespace. This should be used if the database
            has data in non-default namespaces, but doesn't
            want to include them. Each namespace in this
            list must be unique.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    collection_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    input_uri_prefix: str = proto.Field(
        proto.STRING,
        number=3,
    )
    namespace_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
