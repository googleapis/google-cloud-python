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

import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.bigtable.admin.v2",
    manifest={
        "Type",
    },
)


class Type(proto.Message):
    r"""``Type`` represents the type of data that is written to, read from,
    or stored in Bigtable. It is heavily based on the GoogleSQL standard
    to help maintain familiarity and consistency across products and
    features.

    For compatibility with Bigtable's existing untyped APIs, each
    ``Type`` includes an ``Encoding`` which describes how to convert
    to/from the underlying data. This might involve composing a series
    of steps into an "encoding chain," for example to convert from INT64
    -> STRING -> raw bytes. In most cases, a "link" in the encoding
    chain will be based an on existing GoogleSQL conversion function
    like ``CAST``.

    Each link in the encoding chain also defines the following
    properties:

    -  Natural sort: Does the encoded value sort consistently with the
       original typed value? Note that Bigtable will always sort data
       based on the raw encoded value, *not* the decoded type.

       -  Example: BYTES values sort in the same order as their raw
          encodings.
       -  Counterexample: Encoding INT64 to a fixed-width STRING does
          *not* preserve sort order when dealing with negative numbers.
          INT64(1) > INT64(-1), but STRING("-00001") > STRING("00001).
       -  The overall encoding chain has this property if *every* link
          does.

    -  Self-delimiting: If we concatenate two encoded values, can we
       always tell where the first one ends and the second one begins?

       -  Example: If we encode INT64s to fixed-width STRINGs, the first
          value will always contain exactly N digits, possibly preceded
          by a sign.
       -  Counterexample: If we concatenate two UTF-8 encoded STRINGs,
          we have no way to tell where the first one ends.
       -  The overall encoding chain has this property if *any* link
          does.

    -  Compatibility: Which other systems have matching encoding
       schemes? For example, does this encoding have a GoogleSQL
       equivalent? HBase? Java?

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        bytes_type (google.cloud.bigtable_admin_v2.types.Type.Bytes):
            Bytes

            This field is a member of `oneof`_ ``kind``.
        string_type (google.cloud.bigtable_admin_v2.types.Type.String):
            String

            This field is a member of `oneof`_ ``kind``.
        int64_type (google.cloud.bigtable_admin_v2.types.Type.Int64):
            Int64

            This field is a member of `oneof`_ ``kind``.
        aggregate_type (google.cloud.bigtable_admin_v2.types.Type.Aggregate):
            Aggregate

            This field is a member of `oneof`_ ``kind``.
    """

    class Bytes(proto.Message):
        r"""Bytes Values of type ``Bytes`` are stored in ``Value.bytes_value``.

        Attributes:
            encoding (google.cloud.bigtable_admin_v2.types.Type.Bytes.Encoding):
                The encoding to use when converting to/from
                lower level types.
        """

        class Encoding(proto.Message):
            r"""Rules used to convert to/from lower level types.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                raw (google.cloud.bigtable_admin_v2.types.Type.Bytes.Encoding.Raw):
                    Use ``Raw`` encoding.

                    This field is a member of `oneof`_ ``encoding``.
            """

            class Raw(proto.Message):
                r"""Leaves the value "as-is"

                -  Natural sort? Yes
                -  Self-delimiting? No
                -  Compatibility? N/A

                """

            raw: "Type.Bytes.Encoding.Raw" = proto.Field(
                proto.MESSAGE,
                number=1,
                oneof="encoding",
                message="Type.Bytes.Encoding.Raw",
            )

        encoding: "Type.Bytes.Encoding" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Type.Bytes.Encoding",
        )

    class String(proto.Message):
        r"""String Values of type ``String`` are stored in
        ``Value.string_value``.

        Attributes:
            encoding (google.cloud.bigtable_admin_v2.types.Type.String.Encoding):
                The encoding to use when converting to/from
                lower level types.
        """

        class Encoding(proto.Message):
            r"""Rules used to convert to/from lower level types.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                utf8_raw (google.cloud.bigtable_admin_v2.types.Type.String.Encoding.Utf8Raw):
                    Use ``Utf8Raw`` encoding.

                    This field is a member of `oneof`_ ``encoding``.
            """

            class Utf8Raw(proto.Message):
                r"""UTF-8 encoding

                -  Natural sort? No (ASCII characters only)
                -  Self-delimiting? No
                -  Compatibility?

                   -  BigQuery Federation ``TEXT`` encoding
                   -  HBase ``Bytes.toBytes``
                   -  Java ``String#getBytes(StandardCharsets.UTF_8)``

                """

            utf8_raw: "Type.String.Encoding.Utf8Raw" = proto.Field(
                proto.MESSAGE,
                number=1,
                oneof="encoding",
                message="Type.String.Encoding.Utf8Raw",
            )

        encoding: "Type.String.Encoding" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Type.String.Encoding",
        )

    class Int64(proto.Message):
        r"""Int64 Values of type ``Int64`` are stored in ``Value.int_value``.

        Attributes:
            encoding (google.cloud.bigtable_admin_v2.types.Type.Int64.Encoding):
                The encoding to use when converting to/from
                lower level types.
        """

        class Encoding(proto.Message):
            r"""Rules used to convert to/from lower level types.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                big_endian_bytes (google.cloud.bigtable_admin_v2.types.Type.Int64.Encoding.BigEndianBytes):
                    Use ``BigEndianBytes`` encoding.

                    This field is a member of `oneof`_ ``encoding``.
            """

            class BigEndianBytes(proto.Message):
                r"""Encodes the value as an 8-byte big endian twos complement ``Bytes``
                value.

                -  Natural sort? No (positive values only)
                -  Self-delimiting? Yes
                -  Compatibility?

                   -  BigQuery Federation ``BINARY`` encoding
                   -  HBase ``Bytes.toBytes``
                   -  Java ``ByteBuffer.putLong()`` with ``ByteOrder.BIG_ENDIAN``

                Attributes:
                    bytes_type (google.cloud.bigtable_admin_v2.types.Type.Bytes):
                        The underlying ``Bytes`` type, which may be able to encode
                        further.
                """

                bytes_type: "Type.Bytes" = proto.Field(
                    proto.MESSAGE,
                    number=1,
                    message="Type.Bytes",
                )

            big_endian_bytes: "Type.Int64.Encoding.BigEndianBytes" = proto.Field(
                proto.MESSAGE,
                number=1,
                oneof="encoding",
                message="Type.Int64.Encoding.BigEndianBytes",
            )

        encoding: "Type.Int64.Encoding" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Type.Int64.Encoding",
        )

    class Aggregate(proto.Message):
        r"""A value that combines incremental updates into a summarized value.

        Data is never directly written or read using type ``Aggregate``.
        Writes will provide either the ``input_type`` or ``state_type``, and
        reads will always return the ``state_type`` .


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            input_type (google.cloud.bigtable_admin_v2.types.Type):
                Type of the inputs that are accumulated by this
                ``Aggregate``, which must specify a full encoding. Use
                ``AddInput`` mutations to accumulate new inputs.
            state_type (google.cloud.bigtable_admin_v2.types.Type):
                Output only. Type that holds the internal accumulator state
                for the ``Aggregate``. This is a function of the
                ``input_type`` and ``aggregator`` chosen, and will always
                specify a full encoding.
            sum (google.cloud.bigtable_admin_v2.types.Type.Aggregate.Sum):
                Sum aggregator.

                This field is a member of `oneof`_ ``aggregator``.
        """

        class Sum(proto.Message):
            r"""Computes the sum of the input values. Allowed input: ``Int64``
            State: same as input

            """

        input_type: "Type" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Type",
        )
        state_type: "Type" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="Type",
        )
        sum: "Type.Aggregate.Sum" = proto.Field(
            proto.MESSAGE,
            number=4,
            oneof="aggregator",
            message="Type.Aggregate.Sum",
        )

    bytes_type: Bytes = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="kind",
        message=Bytes,
    )
    string_type: String = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="kind",
        message=String,
    )
    int64_type: Int64 = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="kind",
        message=Int64,
    )
    aggregate_type: Aggregate = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="kind",
        message=Aggregate,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
