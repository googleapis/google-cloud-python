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


from google.protobuf import struct_pb2 as struct  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.type import latlng_pb2 as latlng  # type: ignore


__protobuf__ = proto.module(
    package="google.firestore.v1",
    manifest={"Document", "Value", "ArrayValue", "MapValue",},
)


class Document(proto.Message):
    r"""A Firestore document.
    Must not exceed 1 MiB - 4 bytes.

    Attributes:
        name (str):
            The resource name of the document, for example
            ``projects/{project_id}/databases/{database_id}/documents/{document_path}``.
        fields (Sequence[~.document.Document.FieldsEntry]):
            The document's fields.

            The map keys represent field names.

            A simple field name contains only characters ``a`` to ``z``,
            ``A`` to ``Z``, ``0`` to ``9``, or ``_``, and must not start
            with ``0`` to ``9``. For example, ``foo_bar_17``.

            Field names matching the regular expression ``__.*__`` are
            reserved. Reserved field names are forbidden except in
            certain documented contexts. The map keys, represented as
            UTF-8, must not exceed 1,500 bytes and cannot be empty.

            Field paths may be used in other contexts to refer to
            structured fields defined here. For ``map_value``, the field
            path is represented by the simple or quoted field names of
            the containing fields, delimited by ``.``. For example, the
            structured field
            ``"foo" : { map_value: { "x&y" : { string_value: "hello" }}}``
            would be represented by the field path ``foo.x&y``.

            Within a field path, a quoted field name starts and ends
            with :literal:`\`` and may contain any character. Some
            characters, including :literal:`\``, must be escaped using a
            ``\``. For example, :literal:`\`x&y\`` represents ``x&y``
            and :literal:`\`bak\`tik\`` represents :literal:`bak`tik`.
        create_time (~.timestamp.Timestamp):
            Output only. The time at which the document was created.

            This value increases monotonically when a document is
            deleted then recreated. It can also be compared to values
            from other documents and the ``read_time`` of a query.
        update_time (~.timestamp.Timestamp):
            Output only. The time at which the document was last
            changed.

            This value is initially set to the ``create_time`` then
            increases monotonically with each change to the document. It
            can also be compared to values from other documents and the
            ``read_time`` of a query.
    """

    name = proto.Field(proto.STRING, number=1)

    fields = proto.MapField(proto.STRING, proto.MESSAGE, number=2, message="Value",)

    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)

    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp.Timestamp,)


class Value(proto.Message):
    r"""A message that can hold any of the supported value types.

    Attributes:
        null_value (~.struct.NullValue):
            A null value.
        boolean_value (bool):
            A boolean value.
        integer_value (int):
            An integer value.
        double_value (float):
            A double value.
        timestamp_value (~.timestamp.Timestamp):
            A timestamp value.
            Precise only to microseconds. When stored, any
            additional precision is rounded down.
        string_value (str):
            A string value.
            The string, represented as UTF-8, must not
            exceed 1 MiB - 89 bytes. Only the first 1,500
            bytes of the UTF-8 representation are considered
            by queries.
        bytes_value (bytes):
            A bytes value.
            Must not exceed 1 MiB - 89 bytes.
            Only the first 1,500 bytes are considered by
            queries.
        reference_value (str):
            A reference to a document. For example:
            ``projects/{project_id}/databases/{database_id}/documents/{document_path}``.
        geo_point_value (~.latlng.LatLng):
            A geo point value representing a point on the
            surface of Earth.
        array_value (~.document.ArrayValue):
            An array value.
            Cannot directly contain another array value,
            though can contain an map which contains another
            array.
        map_value (~.document.MapValue):
            A map value.
    """

    null_value = proto.Field(
        proto.ENUM, number=11, oneof="value_type", enum=struct.NullValue,
    )

    boolean_value = proto.Field(proto.BOOL, number=1, oneof="value_type")

    integer_value = proto.Field(proto.INT64, number=2, oneof="value_type")

    double_value = proto.Field(proto.DOUBLE, number=3, oneof="value_type")

    timestamp_value = proto.Field(
        proto.MESSAGE, number=10, oneof="value_type", message=timestamp.Timestamp,
    )

    string_value = proto.Field(proto.STRING, number=17, oneof="value_type")

    bytes_value = proto.Field(proto.BYTES, number=18, oneof="value_type")

    reference_value = proto.Field(proto.STRING, number=5, oneof="value_type")

    geo_point_value = proto.Field(
        proto.MESSAGE, number=8, oneof="value_type", message=latlng.LatLng,
    )

    array_value = proto.Field(
        proto.MESSAGE, number=9, oneof="value_type", message="ArrayValue",
    )

    map_value = proto.Field(
        proto.MESSAGE, number=6, oneof="value_type", message="MapValue",
    )


class ArrayValue(proto.Message):
    r"""An array value.

    Attributes:
        values (Sequence[~.document.Value]):
            Values in the array.
    """

    values = proto.RepeatedField(proto.MESSAGE, number=1, message="Value",)


class MapValue(proto.Message):
    r"""A map value.

    Attributes:
        fields (Sequence[~.document.MapValue.FieldsEntry]):
            The map's fields.

            The map keys represent field names. Field names matching the
            regular expression ``__.*__`` are reserved. Reserved field
            names are forbidden except in certain documented contexts.
            The map keys, represented as UTF-8, must not exceed 1,500
            bytes and cannot be empty.
    """

    fields = proto.MapField(proto.STRING, proto.MESSAGE, number=1, message="Value",)


__all__ = tuple(sorted(__protobuf__.manifest))
