# Copyright 2021 Google LLC
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

"""Custom data types for spanner."""

import json
import types

from google.protobuf.message import Message
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper


class JsonObject(dict):
    """
    Provides functionality of JSON data type in Cloud Spanner
    API, mimicking simple `dict()` behaviour and making
    all the necessary conversions under the hood.
    """

    def __init__(self, *args, **kwargs):
        self._is_null = (args, kwargs) == ((), {}) or args == (None,)
        self._is_array = len(args) and isinstance(args[0], (list, tuple))
        self._is_scalar_value = len(args) == 1 and not isinstance(args[0], (list, dict))

        # if the JSON object is represented with an array,
        # the value is contained separately
        if self._is_array:
            self._array_value = args[0]
            return

        # If it's a scalar value, set _simple_value and return early
        if self._is_scalar_value:
            self._simple_value = args[0]
            return

        if len(args) and isinstance(args[0], JsonObject):
            self._is_array = args[0]._is_array
            self._is_scalar_value = args[0]._is_scalar_value
            if self._is_array:
                self._array_value = args[0]._array_value
            elif self._is_scalar_value:
                self._simple_value = args[0]._simple_value

        if not self._is_null:
            super(JsonObject, self).__init__(*args, **kwargs)

    def __repr__(self):
        if self._is_array:
            return str(self._array_value)

        if self._is_scalar_value:
            return str(self._simple_value)

        return super(JsonObject, self).__repr__()

    @classmethod
    def from_str(cls, str_repr):
        """Initiate an object from its `str` representation.

        Args:
            str_repr (str): JSON text representation.

        Returns:
            JsonObject: JSON object.
        """
        if str_repr == "null":
            return cls()

        return cls(json.loads(str_repr))

    def serialize(self):
        """Return the object text representation.

        Returns:
            str: JSON object text representation.
        """
        if self._is_null:
            return None

        if self._is_scalar_value:
            return json.dumps(self._simple_value)

        if self._is_array:
            return json.dumps(self._array_value, sort_keys=True, separators=(",", ":"))

        return json.dumps(self, sort_keys=True, separators=(",", ":"))


def _proto_message(bytes_val, proto_message_object):
    """Helper for :func:`get_proto_message`.
    parses serialized protocol buffer bytes data into proto message.

    Args:
        bytes_val (bytes): bytes object.
        proto_message_object (Message): Message object for parsing

    Returns:
        Message: parses serialized protocol buffer data into this message.

    Raises:
        ValueError: if the input proto_message_object is not of type Message
    """
    if isinstance(bytes_val, types.NoneType):
        return None

    if not isinstance(bytes_val, bytes):
        raise ValueError("Expected input bytes_val to be a string")

    proto_message = proto_message_object.__deepcopy__()
    proto_message.ParseFromString(bytes_val)
    return proto_message


def _proto_enum(int_val, proto_enum_object):
    """Helper for :func:`get_proto_enum`.
    parses int value into string containing the name of an enum value.

    Args:
        int_val (int): integer value.
        proto_enum_object (EnumTypeWrapper): Enum object.

    Returns:
        str: string containing the name of an enum value.

    Raises:
        ValueError: if the input proto_enum_object is not of type EnumTypeWrapper
    """
    if isinstance(int_val, types.NoneType):
        return None

    if not isinstance(int_val, int):
        raise ValueError("Expected input int_val to be a integer")

    return proto_enum_object.Name(int_val)


def get_proto_message(bytes_string, proto_message_object):
    """parses serialized protocol buffer bytes' data or its list into proto message or list of proto message.

    Args:
        bytes_string (bytes or list[bytes]): bytes object.
        proto_message_object (Message): Message object for parsing

    Returns:
        Message or list[Message]: parses serialized protocol buffer data into this message.

    Raises:
        ValueError: if the input proto_message_object is not of type Message
    """
    if isinstance(bytes_string, types.NoneType):
        return None

    if not isinstance(proto_message_object, Message):
        raise ValueError("Input proto_message_object should be of type Message")

    if not isinstance(bytes_string, (bytes, list)):
        raise ValueError(
            "Expected input bytes_string to be a string or list of strings"
        )

    if isinstance(bytes_string, list):
        return [_proto_message(item, proto_message_object) for item in bytes_string]

    return _proto_message(bytes_string, proto_message_object)


def get_proto_enum(int_value, proto_enum_object):
    """parses int or list of int values into enum or list of enum values.

    Args:
        int_value (int or list[int]): list of integer value.
        proto_enum_object (EnumTypeWrapper): Enum object.

    Returns:
        str or list[str]: list of strings containing the name of enum value.

    Raises:
        ValueError: if the input int_list is not of type list
    """
    if isinstance(int_value, types.NoneType):
        return None

    if not isinstance(proto_enum_object, EnumTypeWrapper):
        raise ValueError("Input proto_enum_object should be of type EnumTypeWrapper")

    if not isinstance(int_value, (int, list)):
        raise ValueError("Expected input int_value to be a integer or list of integers")

    if isinstance(int_value, list):
        return [_proto_enum(item, proto_enum_object) for item in int_value]

    return _proto_enum(int_value, proto_enum_object)
