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
    package="google.cloud.automl.v1beta1",
    manifest={"TypeCode", "DataType", "StructType",},
)


class TypeCode(proto.Enum):
    r"""``TypeCode`` is used as a part of
    [DataType][google.cloud.automl.v1beta1.DataType].
    """
    TYPE_CODE_UNSPECIFIED = 0
    FLOAT64 = 3
    TIMESTAMP = 4
    STRING = 6
    ARRAY = 8
    STRUCT = 9
    CATEGORY = 10


class DataType(proto.Message):
    r"""Indicated the type of data that can be stored in a structured
    data entity (e.g. a table).

    Attributes:
        list_element_type (google.cloud.automl_v1beta1.types.DataType):
            If
            [type_code][google.cloud.automl.v1beta1.DataType.type_code]
            == [ARRAY][google.cloud.automl.v1beta1.TypeCode.ARRAY], then
            ``list_element_type`` is the type of the elements.
        struct_type (google.cloud.automl_v1beta1.types.StructType):
            If
            [type_code][google.cloud.automl.v1beta1.DataType.type_code]
            == [STRUCT][google.cloud.automl.v1beta1.TypeCode.STRUCT],
            then ``struct_type`` provides type information for the
            struct's fields.
        time_format (str):
            If
            [type_code][google.cloud.automl.v1beta1.DataType.type_code]
            ==
            [TIMESTAMP][google.cloud.automl.v1beta1.TypeCode.TIMESTAMP]
            then ``time_format`` provides the format in which that time
            field is expressed. The time_format must either be one of:

            -  ``UNIX_SECONDS``
            -  ``UNIX_MILLISECONDS``
            -  ``UNIX_MICROSECONDS``
            -  ``UNIX_NANOSECONDS`` (for respectively number of seconds,
               milliseconds, microseconds and nanoseconds since start of
               the Unix epoch); or be written in ``strftime`` syntax. If
               time_format is not set, then the default format as
               described on the type_code is used.
        type_code (google.cloud.automl_v1beta1.types.TypeCode):
            Required. The
            [TypeCode][google.cloud.automl.v1beta1.TypeCode] for this
            type.
        nullable (bool):
            If true, this DataType can also be ``NULL``. In .CSV files
            ``NULL`` value is expressed as an empty string.
    """

    list_element_type = proto.Field(
        proto.MESSAGE, number=2, oneof="details", message="DataType",
    )
    struct_type = proto.Field(
        proto.MESSAGE, number=3, oneof="details", message="StructType",
    )
    time_format = proto.Field(proto.STRING, number=5, oneof="details",)
    type_code = proto.Field(proto.ENUM, number=1, enum="TypeCode",)
    nullable = proto.Field(proto.BOOL, number=4,)


class StructType(proto.Message):
    r"""``StructType`` defines the DataType-s of a
    [STRUCT][google.cloud.automl.v1beta1.TypeCode.STRUCT] type.

    Attributes:
        fields (Sequence[google.cloud.automl_v1beta1.types.StructType.FieldsEntry]):
            Unordered map of struct field names to their
            data types. Fields cannot be added or removed
            via Update. Their names and data types are still
            mutable.
    """

    fields = proto.MapField(proto.STRING, proto.MESSAGE, number=1, message="DataType",)


__all__ = tuple(sorted(__protobuf__.manifest))
