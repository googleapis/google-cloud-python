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


__protobuf__ = proto.module(
    package="google.spanner.v1", manifest={"TypeCode", "Type", "StructType",},
)


class TypeCode(proto.Enum):
    r"""``TypeCode`` is used as part of [Type][google.spanner.v1.Type] to
    indicate the type of a Cloud Spanner value.

    Each legal value of a type can be encoded to or decoded from a JSON
    value, using the encodings described below. All Cloud Spanner values
    can be ``null``, regardless of type; ``null``\ s are always encoded
    as a JSON ``null``.
    """
    TYPE_CODE_UNSPECIFIED = 0
    BOOL = 1
    INT64 = 2
    FLOAT64 = 3
    TIMESTAMP = 4
    DATE = 5
    STRING = 6
    BYTES = 7
    ARRAY = 8
    STRUCT = 9
    NUMERIC = 10


class Type(proto.Message):
    r"""``Type`` indicates the type of a Cloud Spanner value, as might be
    stored in a table cell or returned from an SQL query.

    Attributes:
        code (~.gs_type.TypeCode):
            Required. The [TypeCode][google.spanner.v1.TypeCode] for
            this type.
        array_element_type (~.gs_type.Type):
            If [code][google.spanner.v1.Type.code] ==
            [ARRAY][google.spanner.v1.TypeCode.ARRAY], then
            ``array_element_type`` is the type of the array elements.
        struct_type (~.gs_type.StructType):
            If [code][google.spanner.v1.Type.code] ==
            [STRUCT][google.spanner.v1.TypeCode.STRUCT], then
            ``struct_type`` provides type information for the struct's
            fields.
    """

    code = proto.Field(proto.ENUM, number=1, enum="TypeCode",)

    array_element_type = proto.Field(proto.MESSAGE, number=2, message="Type",)

    struct_type = proto.Field(proto.MESSAGE, number=3, message="StructType",)


class StructType(proto.Message):
    r"""``StructType`` defines the fields of a
    [STRUCT][google.spanner.v1.TypeCode.STRUCT] type.

    Attributes:
        fields (Sequence[~.gs_type.StructType.Field]):
            The list of fields that make up this struct. Order is
            significant, because values of this struct type are
            represented as lists, where the order of field values
            matches the order of fields in the
            [StructType][google.spanner.v1.StructType]. In turn, the
            order of fields matches the order of columns in a read
            request, or the order of fields in the ``SELECT`` clause of
            a query.
    """

    class Field(proto.Message):
        r"""Message representing a single field of a struct.

        Attributes:
            name (str):
                The name of the field. For reads, this is the column name.
                For SQL queries, it is the column alias (e.g., ``"Word"`` in
                the query ``"SELECT 'hello' AS Word"``), or the column name
                (e.g., ``"ColName"`` in the query
                ``"SELECT ColName FROM Table"``). Some columns might have an
                empty name (e.g., `"SELECT UPPER(ColName)"`). Note that a
                query result can contain multiple fields with the same name.
            type_ (~.gs_type.Type):
                The type of the field.
        """

        name = proto.Field(proto.STRING, number=1)

        type_ = proto.Field(proto.MESSAGE, number=2, message="Type",)

    fields = proto.RepeatedField(proto.MESSAGE, number=1, message=Field,)


__all__ = tuple(sorted(__protobuf__.manifest))
