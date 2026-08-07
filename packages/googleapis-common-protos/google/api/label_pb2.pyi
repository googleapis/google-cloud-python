# Copyright 2025 Google LLC
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

from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class LabelDescriptor(_message.Message):
    __slots__ = ["description", "key", "value_type"]
    class ValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    BOOL: LabelDescriptor.ValueType
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    INT64: LabelDescriptor.ValueType
    KEY_FIELD_NUMBER: _ClassVar[int]
    STRING: LabelDescriptor.ValueType
    VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    description: str
    key: str
    value_type: LabelDescriptor.ValueType
    def __init__(
        self,
        key: _Optional[str] = ...,
        value_type: _Optional[_Union[LabelDescriptor.ValueType, str]] = ...,
        description: _Optional[str] = ...,
    ) -> None: ...
