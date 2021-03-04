# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

import proto  # type: ignore


from google.cloud.firestore_admin_v1.types import field as gfa_field
from google.cloud.firestore_admin_v1.types import index as gfa_index
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


__protobuf__ = proto.module(
    package="google.firestore.admin.v1",
    manifest={
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

    parent = proto.Field(proto.STRING, number=1)

    index = proto.Field(proto.MESSAGE, number=2, message=gfa_index.Index,)


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

    parent = proto.Field(proto.STRING, number=1)

    filter = proto.Field(proto.STRING, number=2)

    page_size = proto.Field(proto.INT32, number=3)

    page_token = proto.Field(proto.STRING, number=4)


class ListIndexesResponse(proto.Message):
    r"""The response for
    [FirestoreAdmin.ListIndexes][google.firestore.admin.v1.FirestoreAdmin.ListIndexes].

    Attributes:
        indexes (Sequence[google.cloud.firestore_admin_v1.types.Index]):
            The requested indexes.
        next_page_token (str):
            A page token that may be used to request
            another page of results. If blank, this is the
            last page.
    """

    @property
    def raw_page(self):
        return self

    indexes = proto.RepeatedField(proto.MESSAGE, number=1, message=gfa_index.Index,)

    next_page_token = proto.Field(proto.STRING, number=2)


class GetIndexRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.GetIndex][google.firestore.admin.v1.FirestoreAdmin.GetIndex].

    Attributes:
        name (str):
            Required. A name of the form
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/indexes/{index_id}``
    """

    name = proto.Field(proto.STRING, number=1)


class DeleteIndexRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.DeleteIndex][google.firestore.admin.v1.FirestoreAdmin.DeleteIndex].

    Attributes:
        name (str):
            Required. A name of the form
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/indexes/{index_id}``
    """

    name = proto.Field(proto.STRING, number=1)


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

    field = proto.Field(proto.MESSAGE, number=1, message=gfa_field.Field,)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class GetFieldRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.GetField][google.firestore.admin.v1.FirestoreAdmin.GetField].

    Attributes:
        name (str):
            Required. A name of the form
            ``projects/{project_id}/databases/{database_id}/collectionGroups/{collection_id}/fields/{field_id}``
    """

    name = proto.Field(proto.STRING, number=1)


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
            with the filter set to
            ``indexConfig.usesAncestorConfig:false``.
        page_size (int):
            The number of results to return.
        page_token (str):
            A page token, returned from a previous call to
            [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields],
            that may be used to get the next page of results.
    """

    parent = proto.Field(proto.STRING, number=1)

    filter = proto.Field(proto.STRING, number=2)

    page_size = proto.Field(proto.INT32, number=3)

    page_token = proto.Field(proto.STRING, number=4)


class ListFieldsResponse(proto.Message):
    r"""The response for
    [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields].

    Attributes:
        fields (Sequence[google.cloud.firestore_admin_v1.types.Field]):
            The requested fields.
        next_page_token (str):
            A page token that may be used to request
            another page of results. If blank, this is the
            last page.
    """

    @property
    def raw_page(self):
        return self

    fields = proto.RepeatedField(proto.MESSAGE, number=1, message=gfa_field.Field,)

    next_page_token = proto.Field(proto.STRING, number=2)


class ExportDocumentsRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.ExportDocuments][google.firestore.admin.v1.FirestoreAdmin.ExportDocuments].

    Attributes:
        name (str):
            Required. Database to export. Should be of the form:
            ``projects/{project_id}/databases/{database_id}``.
        collection_ids (Sequence[str]):
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
    """

    name = proto.Field(proto.STRING, number=1)

    collection_ids = proto.RepeatedField(proto.STRING, number=2)

    output_uri_prefix = proto.Field(proto.STRING, number=3)


class ImportDocumentsRequest(proto.Message):
    r"""The request for
    [FirestoreAdmin.ImportDocuments][google.firestore.admin.v1.FirestoreAdmin.ImportDocuments].

    Attributes:
        name (str):
            Required. Database to import into. Should be of the form:
            ``projects/{project_id}/databases/{database_id}``.
        collection_ids (Sequence[str]):
            Which collection ids to import. Unspecified
            means all collections included in the import.
        input_uri_prefix (str):
            Location of the exported files. This must match the
            output_uri_prefix of an ExportDocumentsResponse from an
            export that has completed successfully. See:
            [google.firestore.admin.v1.ExportDocumentsResponse.output_uri_prefix][google.firestore.admin.v1.ExportDocumentsResponse.output_uri_prefix].
    """

    name = proto.Field(proto.STRING, number=1)

    collection_ids = proto.RepeatedField(proto.STRING, number=2)

    input_uri_prefix = proto.Field(proto.STRING, number=3)


__all__ = tuple(sorted(__protobuf__.manifest))
