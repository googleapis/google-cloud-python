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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import field_mask_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.discoveryengine_v1beta.types import document as gcd_document

__protobuf__ = proto.module(
    package="google.cloud.discoveryengine.v1beta",
    manifest={
        "GetDocumentRequest",
        "ListDocumentsRequest",
        "ListDocumentsResponse",
        "CreateDocumentRequest",
        "UpdateDocumentRequest",
        "DeleteDocumentRequest",
    },
)


class GetDocumentRequest(proto.Message):
    r"""Request message for
    [DocumentService.GetDocument][google.cloud.discoveryengine.v1beta.DocumentService.GetDocument]
    method.

    Attributes:
        name (str):
            Required. Full resource name of
            [Document][google.cloud.discoveryengine.v1beta.Document],
            such as
            ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}/branches/{branch}/documents/{document}``.

            If the caller does not have permission to access the
            [Document][google.cloud.discoveryengine.v1beta.Document],
            regardless of whether or not it exists, a
            ``PERMISSION_DENIED`` error is returned.

            If the requested
            [Document][google.cloud.discoveryengine.v1beta.Document]
            does not exist, a ``NOT_FOUND`` error is returned.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListDocumentsRequest(proto.Message):
    r"""Request message for
    [DocumentService.ListDocuments][google.cloud.discoveryengine.v1beta.DocumentService.ListDocuments]
    method.

    Attributes:
        parent (str):
            Required. The parent branch resource name, such as
            ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}/branches/{branch}``.
            Use ``default_branch`` as the branch ID, to list documents
            under the default branch.

            If the caller does not have permission to list
            [Document][google.cloud.discoveryengine.v1beta.Document]s
            under this branch, regardless of whether or not this branch
            exists, a ``PERMISSION_DENIED`` error is returned.
        page_size (int):
            Maximum number of
            [Document][google.cloud.discoveryengine.v1beta.Document]s to
            return. If unspecified, defaults to 100. The maximum allowed
            value is 1000. Values above 1000 are set to 1000.

            If this field is negative, an ``INVALID_ARGUMENT`` error is
            returned.
        page_token (str):
            A page token
            [ListDocumentsResponse.next_page_token][google.cloud.discoveryengine.v1beta.ListDocumentsResponse.next_page_token],
            received from a previous
            [DocumentService.ListDocuments][google.cloud.discoveryengine.v1beta.DocumentService.ListDocuments]
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            [DocumentService.ListDocuments][google.cloud.discoveryengine.v1beta.DocumentService.ListDocuments]
            must match the call that provided the page token. Otherwise,
            an ``INVALID_ARGUMENT`` error is returned.
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


class ListDocumentsResponse(proto.Message):
    r"""Response message for
    [DocumentService.ListDocuments][google.cloud.discoveryengine.v1beta.DocumentService.ListDocuments]
    method.

    Attributes:
        documents (MutableSequence[google.cloud.discoveryengine_v1beta.types.Document]):
            The
            [Document][google.cloud.discoveryengine.v1beta.Document]s.
        next_page_token (str):
            A token that can be sent as
            [ListDocumentsRequest.page_token][google.cloud.discoveryengine.v1beta.ListDocumentsRequest.page_token]
            to retrieve the next page. If this field is omitted, there
            are no subsequent pages.
    """

    @property
    def raw_page(self):
        return self

    documents: MutableSequence[gcd_document.Document] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcd_document.Document,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateDocumentRequest(proto.Message):
    r"""Request message for
    [DocumentService.CreateDocument][google.cloud.discoveryengine.v1beta.DocumentService.CreateDocument]
    method.

    Attributes:
        parent (str):
            Required. The parent resource name, such as
            ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}/branches/{branch}``.
        document (google.cloud.discoveryengine_v1beta.types.Document):
            Required. The
            [Document][google.cloud.discoveryengine.v1beta.Document] to
            create.
        document_id (str):
            Required. The ID to use for the
            [Document][google.cloud.discoveryengine.v1beta.Document],
            which becomes the final component of the
            [Document.name][google.cloud.discoveryengine.v1beta.Document.name].

            If the caller does not have permission to create the
            [Document][google.cloud.discoveryengine.v1beta.Document],
            regardless of whether or not it exists, a
            ``PERMISSION_DENIED`` error is returned.

            This field must be unique among all
            [Document][google.cloud.discoveryengine.v1beta.Document]s
            with the same
            [parent][google.cloud.discoveryengine.v1beta.CreateDocumentRequest.parent].
            Otherwise, an ``ALREADY_EXISTS`` error is returned.

            This field must conform to
            `RFC-1034 <https://tools.ietf.org/html/rfc1034>`__ standard
            with a length limit of 63 characters. Otherwise, an
            ``INVALID_ARGUMENT`` error is returned.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    document: gcd_document.Document = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcd_document.Document,
    )
    document_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class UpdateDocumentRequest(proto.Message):
    r"""Request message for
    [DocumentService.UpdateDocument][google.cloud.discoveryengine.v1beta.DocumentService.UpdateDocument]
    method.

    Attributes:
        document (google.cloud.discoveryengine_v1beta.types.Document):
            Required. The document to update/create.

            If the caller does not have permission to update the
            [Document][google.cloud.discoveryengine.v1beta.Document],
            regardless of whether or not it exists, a
            ``PERMISSION_DENIED`` error is returned.

            If the
            [Document][google.cloud.discoveryengine.v1beta.Document] to
            update does not exist and
            [allow_missing][google.cloud.discoveryengine.v1beta.UpdateDocumentRequest.allow_missing]
            is not set, a ``NOT_FOUND`` error is returned.
        allow_missing (bool):
            If set to ``true`` and the
            [Document][google.cloud.discoveryengine.v1beta.Document] is
            not found, a new
            [Document][google.cloud.discoveryengine.v1beta.Document] is
            be created.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Indicates which fields in the provided
            imported 'document' to update. If not set, by
            default updates all fields.
    """

    document: gcd_document.Document = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_document.Document,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=3,
        message=field_mask_pb2.FieldMask,
    )


class DeleteDocumentRequest(proto.Message):
    r"""Request message for
    [DocumentService.DeleteDocument][google.cloud.discoveryengine.v1beta.DocumentService.DeleteDocument]
    method.

    Attributes:
        name (str):
            Required. Full resource name of
            [Document][google.cloud.discoveryengine.v1beta.Document],
            such as
            ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}/branches/{branch}/documents/{document}``.

            If the caller does not have permission to delete the
            [Document][google.cloud.discoveryengine.v1beta.Document],
            regardless of whether or not it exists, a
            ``PERMISSION_DENIED`` error is returned.

            If the
            [Document][google.cloud.discoveryengine.v1beta.Document] to
            delete does not exist, a ``NOT_FOUND`` error is returned.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
