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

from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.discoveryengine_v1alpha.types import common

__protobuf__ = proto.module(
    package="google.cloud.discoveryengine.v1alpha",
    manifest={
        "Document",
        "ProcessedDocument",
    },
)


class Document(proto.Message):
    r"""Document captures all raw metadata information of items to be
    recommended or searched.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        struct_data (google.protobuf.struct_pb2.Struct):
            The structured JSON data for the document. It should conform
            to the registered
            [Schema][google.cloud.discoveryengine.v1alpha.Schema] or an
            ``INVALID_ARGUMENT`` error is thrown.

            This field is a member of `oneof`_ ``data``.
        json_data (str):
            The JSON string representation of the document. It should
            conform to the registered
            [Schema][google.cloud.discoveryengine.v1alpha.Schema] or an
            ``INVALID_ARGUMENT`` error is thrown.

            This field is a member of `oneof`_ ``data``.
        name (str):
            Immutable. The full resource name of the document. Format:
            ``projects/{project}/locations/{location}/collections/{collection}/dataStores/{data_store}/branches/{branch}/documents/{document_id}``.

            This field must be a UTF-8 encoded string with a length
            limit of 1024 characters.
        id (str):
            Immutable. The identifier of the document.

            Id should conform to
            `RFC-1034 <https://tools.ietf.org/html/rfc1034>`__ standard
            with a length limit of 63 characters.
        schema_id (str):
            The identifier of the schema located in the
            same data store.
        content (google.cloud.discoveryengine_v1alpha.types.Document.Content):
            The unstructured data linked to this document. Content must
            be set if this document is under a ``CONTENT_REQUIRED`` data
            store.
        parent_document_id (str):
            The identifier of the parent document. Currently supports at
            most two level document hierarchy.

            Id should conform to
            `RFC-1034 <https://tools.ietf.org/html/rfc1034>`__ standard
            with a length limit of 63 characters.
        derived_struct_data (google.protobuf.struct_pb2.Struct):
            Output only. This field is OUTPUT_ONLY. It contains derived
            data that are not in the original input document.
        acl_info (google.cloud.discoveryengine_v1alpha.types.Document.AclInfo):
            Access control information for the document.
        index_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last time the document was indexed. If this
            field is set, the document could be returned in search
            results.

            This field is OUTPUT_ONLY. If this field is not populated,
            it means the document has never been indexed.
        index_status (google.cloud.discoveryengine_v1alpha.types.Document.IndexStatus):
            Output only. The index status of the document.

            -  If document is indexed successfully, the index_time field
               is populated.
            -  Otherwise, if document is not indexed due to errors, the
               error_samples field is populated.
            -  Otherwise, index_status is unset.
    """

    class Content(proto.Message):
        r"""Unstructured data linked to this document.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            raw_bytes (bytes):
                The content represented as a stream of bytes. The maximum
                length is 1,000,000 bytes (1 MB / ~0.95 MiB).

                Note: As with all ``bytes`` fields, this field is
                represented as pure binary in Protocol Buffers and
                base64-encoded string in JSON. For example,
                ``abc123!?$*&()'-=@~`` should be represented as
                ``YWJjMTIzIT8kKiYoKSctPUB+`` in JSON. See
                https://developers.google.com/protocol-buffers/docs/proto3#json.

                This field is a member of `oneof`_ ``content``.
            uri (str):
                The URI of the content. Only Cloud Storage URIs (e.g.
                ``gs://bucket-name/path/to/file``) are supported. The
                maximum file size is 2.5 MB for text-based formats, 200 MB
                for other formats.

                This field is a member of `oneof`_ ``content``.
            mime_type (str):
                The MIME type of the content. Supported types:

                -  ``application/pdf`` (PDF, only native PDFs are supported
                   for now)
                -  ``text/html`` (HTML)
                -  ``application/vnd.openxmlformats-officedocument.wordprocessingml.document``
                   (DOCX)
                -  ``application/vnd.openxmlformats-officedocument.presentationml.presentation``
                   (PPTX)
                -  ``text/plain`` (TXT)

                See
                https://www.iana.org/assignments/media-types/media-types.xhtml.
        """

        raw_bytes: bytes = proto.Field(
            proto.BYTES,
            number=2,
            oneof="content",
        )
        uri: str = proto.Field(
            proto.STRING,
            number=3,
            oneof="content",
        )
        mime_type: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class AclInfo(proto.Message):
        r"""ACL Information of the Document.

        Attributes:
            readers (MutableSequence[google.cloud.discoveryengine_v1alpha.types.Document.AclInfo.AccessRestriction]):
                Readers of the document.
        """

        class AccessRestriction(proto.Message):
            r"""AclRestriction to model complex inheritance restrictions.

            Example: Modeling a "Both Permit" inheritance, where to access a
            child document, user needs to have access to parent document.

            Document Hierarchy - Space_S --> Page_P.

            Readers: Space_S: group_1, user_1 Page_P: group_2, group_3, user_2

            Space_S ACL Restriction - { "acl_info": { "readers": [ {
            "principals": [ { "group_id": "group_1" }, { "user_id": "user_1" } ]
            } ] } }

            Page_P ACL Restriction. { "acl_info": { "readers": [ { "principals":
            [ { "group_id": "group_2" }, { "group_id": "group_3" }, { "user_id":
            "user_2" } ], }, { "principals": [ { "group_id": "group_1" }, {
            "user_id": "user_1" } ], } ] } }

            Attributes:
                principals (MutableSequence[google.cloud.discoveryengine_v1alpha.types.Principal]):
                    List of principals.
                idp_wide (bool):
                    All users within the Identity Provider.
            """

            principals: MutableSequence[common.Principal] = proto.RepeatedField(
                proto.MESSAGE,
                number=1,
                message=common.Principal,
            )
            idp_wide: bool = proto.Field(
                proto.BOOL,
                number=2,
            )

        readers: MutableSequence[
            "Document.AclInfo.AccessRestriction"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="Document.AclInfo.AccessRestriction",
        )

    class IndexStatus(proto.Message):
        r"""Index status of the document.

        Attributes:
            index_time (google.protobuf.timestamp_pb2.Timestamp):
                The time when the document was indexed.
                If this field is populated, it means the
                document has been indexed.
            error_samples (MutableSequence[google.rpc.status_pb2.Status]):
                A sample of errors encountered while indexing
                the document. If this field is populated, the
                document is not indexed due to errors.
        """

        index_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=1,
            message=timestamp_pb2.Timestamp,
        )
        error_samples: MutableSequence[status_pb2.Status] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message=status_pb2.Status,
        )

    struct_data: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="data",
        message=struct_pb2.Struct,
    )
    json_data: str = proto.Field(
        proto.STRING,
        number=5,
        oneof="data",
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    schema_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    content: Content = proto.Field(
        proto.MESSAGE,
        number=10,
        message=Content,
    )
    parent_document_id: str = proto.Field(
        proto.STRING,
        number=7,
    )
    derived_struct_data: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=6,
        message=struct_pb2.Struct,
    )
    acl_info: AclInfo = proto.Field(
        proto.MESSAGE,
        number=11,
        message=AclInfo,
    )
    index_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=13,
        message=timestamp_pb2.Timestamp,
    )
    index_status: IndexStatus = proto.Field(
        proto.MESSAGE,
        number=15,
        message=IndexStatus,
    )


class ProcessedDocument(proto.Message):
    r"""Document captures all raw metadata information of items to be
    recommended or searched.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        json_data (str):
            The JSON string representation of the
            processed document.

            This field is a member of `oneof`_ ``processed_data_format``.
        document (str):
            Required. Full resource name of the referenced document, in
            the format
            ``projects/*/locations/*/collections/*/dataStores/*/branches/*/documents/*``.
    """

    json_data: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="processed_data_format",
    )
    document: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
