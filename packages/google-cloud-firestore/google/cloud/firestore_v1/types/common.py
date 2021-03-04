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


from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.firestore.v1",
    manifest={"DocumentMask", "Precondition", "TransactionOptions",},
)


class DocumentMask(proto.Message):
    r"""A set of field paths on a document. Used to restrict a get or update
    operation on a document to a subset of its fields. This is different
    from standard field masks, as this is always scoped to a
    [Document][google.firestore.v1.Document], and takes in account the
    dynamic nature of [Value][google.firestore.v1.Value].

    Attributes:
        field_paths (Sequence[str]):
            The list of field paths in the mask. See
            [Document.fields][google.firestore.v1.Document.fields] for a
            field path syntax reference.
    """

    field_paths = proto.RepeatedField(proto.STRING, number=1)


class Precondition(proto.Message):
    r"""A precondition on a document, used for conditional
    operations.

    Attributes:
        exists (bool):
            When set to ``true``, the target document must exist. When
            set to ``false``, the target document must not exist.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            When set, the target document must exist and
            have been last updated at that time.
    """

    exists = proto.Field(proto.BOOL, number=1, oneof="condition_type")

    update_time = proto.Field(
        proto.MESSAGE, number=2, oneof="condition_type", message=timestamp.Timestamp,
    )


class TransactionOptions(proto.Message):
    r"""Options for creating a new transaction.

    Attributes:
        read_only (google.cloud.firestore_v1.types.TransactionOptions.ReadOnly):
            The transaction can only be used for read
            operations.
        read_write (google.cloud.firestore_v1.types.TransactionOptions.ReadWrite):
            The transaction can be used for both read and
            write operations.
    """

    class ReadWrite(proto.Message):
        r"""Options for a transaction that can be used to read and write
        documents.

        Attributes:
            retry_transaction (bytes):
                An optional transaction to retry.
        """

        retry_transaction = proto.Field(proto.BYTES, number=1)

    class ReadOnly(proto.Message):
        r"""Options for a transaction that can only be used to read
        documents.

        Attributes:
            read_time (google.protobuf.timestamp_pb2.Timestamp):
                Reads documents at the given time.
                This may not be older than 60 seconds.
        """

        read_time = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="consistency_selector",
            message=timestamp.Timestamp,
        )

    read_only = proto.Field(proto.MESSAGE, number=2, oneof="mode", message=ReadOnly,)

    read_write = proto.Field(proto.MESSAGE, number=3, oneof="mode", message=ReadWrite,)


__all__ = tuple(sorted(__protobuf__.manifest))
