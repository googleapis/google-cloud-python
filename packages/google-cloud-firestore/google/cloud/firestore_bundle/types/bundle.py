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

from google.cloud.firestore_v1.types import document as document_pb2  # type: ignore
from google.cloud.firestore_v1.types import query as query_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.firestore.bundle",
    manifest={
        "BundledQuery",
        "NamedQuery",
        "BundledDocumentMetadata",
        "BundleMetadata",
        "BundleElement",
    },
)


class BundledQuery(proto.Message):
    r"""Encodes a query saved in the bundle.
    Attributes:
        parent (str):
            The parent resource name.
        structured_query (google.firestore.v1.query_pb2.StructuredQuery):
            A structured query.
        limit_type (google.cloud.bundle.types.BundledQuery.LimitType):

    """

    class LimitType(proto.Enum):
        r"""If the query is a limit query, should the limit be applied to
        the beginning or the end of results.
        """
        FIRST = 0
        LAST = 1

    parent = proto.Field(proto.STRING, number=1,)
    structured_query = proto.Field(
        proto.MESSAGE, number=2, oneof="query_type", message=query_pb2.StructuredQuery,
    )
    limit_type = proto.Field(proto.ENUM, number=3, enum=LimitType,)


class NamedQuery(proto.Message):
    r"""A Query associated with a name, created as part of the bundle
    file, and can be read by client SDKs once the bundle containing
    them is loaded.

    Attributes:
        name (str):
            Name of the query, such that client can use
            the name to load this query from bundle, and
            resume from when the query results are
            materialized into this bundle.
        bundled_query (google.cloud.bundle.types.BundledQuery):
            The query saved in the bundle.
        read_time (google.protobuf.timestamp_pb2.Timestamp):
            The read time of the query, when it is used
            to build the bundle. This is useful to resume
            the query from the bundle, once it is loaded by
            client SDKs.
    """

    name = proto.Field(proto.STRING, number=1,)
    bundled_query = proto.Field(proto.MESSAGE, number=2, message="BundledQuery",)
    read_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)


class BundledDocumentMetadata(proto.Message):
    r"""Metadata describing a Firestore document saved in the bundle.
    Attributes:
        name (str):
            The document key of a bundled document.
        read_time (google.protobuf.timestamp_pb2.Timestamp):
            The snapshot version of the document data
            bundled.
        exists (bool):
            Whether the document exists.
        queries (Sequence[str]):
            The names of the queries in this bundle that
            this document matches to.
    """

    name = proto.Field(proto.STRING, number=1,)
    read_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    exists = proto.Field(proto.BOOL, number=3,)
    queries = proto.RepeatedField(proto.STRING, number=4,)


class BundleMetadata(proto.Message):
    r"""Metadata describing the bundle file/stream.
    Attributes:
        id (str):
            The ID of the bundle.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Time at which the documents snapshot is taken
            for this bundle.
        version (int):
            The schema version of the bundle.
        total_documents (int):
            The number of documents in the bundle.
        total_bytes (int):
            The size of the bundle in bytes, excluding this
            ``BundleMetadata``.
    """

    id = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    version = proto.Field(proto.UINT32, number=3,)
    total_documents = proto.Field(proto.UINT32, number=4,)
    total_bytes = proto.Field(proto.UINT64, number=5,)


class BundleElement(proto.Message):
    r"""A Firestore bundle is a length-prefixed stream of JSON
    representations of ``BundleElement``. Only one ``BundleMetadata`` is
    expected, and it should be the first element. The named queries
    follow after ``metadata``. Every ``document_metadata`` is
    immediately followed by a ``document``.

    Attributes:
        metadata (google.cloud.bundle.types.BundleMetadata):

        named_query (google.cloud.bundle.types.NamedQuery):

        document_metadata (google.cloud.bundle.types.BundledDocumentMetadata):

        document (google.firestore.v1.document_pb2.Document):

    """

    metadata = proto.Field(
        proto.MESSAGE, number=1, oneof="element_type", message="BundleMetadata",
    )
    named_query = proto.Field(
        proto.MESSAGE, number=2, oneof="element_type", message="NamedQuery",
    )
    document_metadata = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="element_type",
        message="BundledDocumentMetadata",
    )
    document = proto.Field(
        proto.MESSAGE, number=4, oneof="element_type", message=document_pb2.Document,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
