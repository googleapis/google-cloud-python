# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.protobuf import wrappers_pb2


class WrapperMarshal:
    """A marshal for converting the protobuf wrapper classes to Python.

    This class converts between ``google.protobuf.BoolValue``,
    ``google.protobuf.StringValue``, and their siblings to the appropriate
    Python equivalents.

    These are effectively similar to the protobuf primitives except
    that None becomes a possible value.
    """
    def to_python(self, value, *, absent: bool = None):
        if isinstance(value, self._proto_type):
            if absent:
                return None
            return value.value
        return value

    def to_proto(self, value):
        if isinstance(value, self._python_type):
            return self._proto_type(value=value)
        return value


class DoubleValueMarshal(WrapperMarshal):
    _proto_type = wrappers_pb2.DoubleValue
    _python_type = float


class FloatValueMarshal(WrapperMarshal):
    _proto_type = wrappers_pb2.FloatValue
    _python_type = float


class Int64ValueMarshal(WrapperMarshal):
    _proto_type = wrappers_pb2.Int64Value
    _python_type = int


class UInt64ValueMarshal(WrapperMarshal):
    _proto_type = wrappers_pb2.UInt64Value
    _python_type = int


class Int32ValueMarshal(WrapperMarshal):
    _proto_type = wrappers_pb2.Int32Value
    _python_type = int


class UInt32ValueMarshal(WrapperMarshal):
    _proto_type = wrappers_pb2.UInt32Value
    _python_type = int


class BoolValueMarshal(WrapperMarshal):
    _proto_type = wrappers_pb2.BoolValue
    _python_type = bool


class StringValueMarshal(WrapperMarshal):
    _proto_type = wrappers_pb2.StringValue
    _python_type = str


class BytesValueMarshal(WrapperMarshal):
    _proto_type = wrappers_pb2.BytesValue
    _python_type = bytes
