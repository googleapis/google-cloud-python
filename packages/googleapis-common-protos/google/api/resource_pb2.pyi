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
from typing import Iterable as _Iterable
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor
RESOURCE_DEFINITION_FIELD_NUMBER: _ClassVar[int]
RESOURCE_FIELD_NUMBER: _ClassVar[int]
RESOURCE_REFERENCE_FIELD_NUMBER: _ClassVar[int]
resource: _descriptor.FieldDescriptor
resource_definition: _descriptor.FieldDescriptor
resource_reference: _descriptor.FieldDescriptor

class ResourceDescriptor(_message.Message):
    __slots__ = [
        "history",
        "name_field",
        "pattern",
        "plural",
        "singular",
        "style",
        "type",
    ]
    class History(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    class Style(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    DECLARATIVE_FRIENDLY: ResourceDescriptor.Style
    FUTURE_MULTI_PATTERN: ResourceDescriptor.History
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    HISTORY_UNSPECIFIED: ResourceDescriptor.History
    NAME_FIELD_FIELD_NUMBER: _ClassVar[int]
    ORIGINALLY_SINGLE_PATTERN: ResourceDescriptor.History
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    PLURAL_FIELD_NUMBER: _ClassVar[int]
    SINGULAR_FIELD_NUMBER: _ClassVar[int]
    STYLE_FIELD_NUMBER: _ClassVar[int]
    STYLE_UNSPECIFIED: ResourceDescriptor.Style
    TYPE_FIELD_NUMBER: _ClassVar[int]
    history: ResourceDescriptor.History
    name_field: str
    pattern: _containers.RepeatedScalarFieldContainer[str]
    plural: str
    singular: str
    style: _containers.RepeatedScalarFieldContainer[ResourceDescriptor.Style]
    type: str
    def __init__(
        self,
        type: _Optional[str] = ...,
        pattern: _Optional[_Iterable[str]] = ...,
        name_field: _Optional[str] = ...,
        history: _Optional[_Union[ResourceDescriptor.History, str]] = ...,
        plural: _Optional[str] = ...,
        singular: _Optional[str] = ...,
        style: _Optional[_Iterable[_Union[ResourceDescriptor.Style, str]]] = ...,
    ) -> None: ...

class ResourceReference(_message.Message):
    __slots__ = ["child_type", "type"]
    CHILD_TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    child_type: str
    type: str
    def __init__(
        self, type: _Optional[str] = ..., child_type: _Optional[str] = ...
    ) -> None: ...
