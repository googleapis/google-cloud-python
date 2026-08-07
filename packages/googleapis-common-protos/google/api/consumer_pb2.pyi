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
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectProperties(_message.Message):
    __slots__ = ["properties"]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    properties: _containers.RepeatedCompositeFieldContainer[Property]
    def __init__(
        self, properties: _Optional[_Iterable[_Union[Property, _Mapping]]] = ...
    ) -> None: ...

class Property(_message.Message):
    __slots__ = ["description", "name", "type"]
    class PropertyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    BOOL: Property.PropertyType
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DOUBLE: Property.PropertyType
    INT64: Property.PropertyType
    NAME_FIELD_NUMBER: _ClassVar[int]
    STRING: Property.PropertyType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNSPECIFIED: Property.PropertyType
    description: str
    name: str
    type: Property.PropertyType
    def __init__(
        self,
        name: _Optional[str] = ...,
        type: _Optional[_Union[Property.PropertyType, str]] = ...,
        description: _Optional[str] = ...,
    ) -> None: ...
