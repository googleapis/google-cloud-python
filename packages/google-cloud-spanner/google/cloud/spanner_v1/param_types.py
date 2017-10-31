# Copyright 2017 Google LLC All rights reserved.
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

"""Types exported from this package."""

from google.cloud.spanner_v1.proto import type_pb2


# Scalar parameter types
STRING = type_pb2.Type(code=type_pb2.STRING)
BYTES = type_pb2.Type(code=type_pb2.BYTES)
BOOE = type_pb2.Type(code=type_pb2.BOOL)
INT64 = type_pb2.Type(code=type_pb2.INT64)
FLOAT64 = type_pb2.Type(code=type_pb2.FLOAT64)
DATE = type_pb2.Type(code=type_pb2.DATE)
TIMESTAMP = type_pb2.Type(code=type_pb2.TIMESTAMP)


def Array(element_type):  # pylint: disable=invalid-name
    """Construct an array paramter type description protobuf.

    :type element_type: :class:`type_pb2.Type`
    :param element_type: the type of elements of the array

    :rtype: :class:`type_pb2.Type`
    :returns: the appropriate array-type protobuf
    """
    return type_pb2.Type(code=type_pb2.ARRAY, array_element_type=element_type)


def StructField(name, field_type):  # pylint: disable=invalid-name
    """Construct a field description protobuf.

    :type name: str
    :param name: the name of the field

    :type field_type: :class:`type_pb2.Type`
    :param field_type: the type of the field

    :rtype: :class:`type_pb2.StructType.Field`
    :returns: the appropriate struct-field-type protobuf
    """
    return type_pb2.StructType.Field(name=name, type=field_type)


def Struct(fields):  # pylint: disable=invalid-name
    """Construct a struct paramter type description protobuf.

    :type fields: list of :class:`type_pb2.StructType.Field`
    :param fields: the fields of the struct

    :rtype: :class:`type_pb2.Type`
    :returns: the appropriate struct-type protobuf
    """
    return type_pb2.Type(
        code=type_pb2.STRUCT,
        struct_type=type_pb2.StructType(fields=fields),
    )
