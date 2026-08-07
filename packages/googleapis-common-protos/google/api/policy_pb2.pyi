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
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor
FIELD_POLICY_FIELD_NUMBER: _ClassVar[int]
METHOD_POLICY_FIELD_NUMBER: _ClassVar[int]
field_policy: _descriptor.FieldDescriptor
method_policy: _descriptor.FieldDescriptor

class FieldPolicy(_message.Message):
    __slots__ = ["resource_permission", "resource_type", "selector"]
    RESOURCE_PERMISSION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    resource_permission: str
    resource_type: str
    selector: str
    def __init__(
        self,
        selector: _Optional[str] = ...,
        resource_permission: _Optional[str] = ...,
        resource_type: _Optional[str] = ...,
    ) -> None: ...

class MethodPolicy(_message.Message):
    __slots__ = ["request_policies", "selector"]
    REQUEST_POLICIES_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    request_policies: _containers.RepeatedCompositeFieldContainer[FieldPolicy]
    selector: str
    def __init__(
        self,
        selector: _Optional[str] = ...,
        request_policies: _Optional[_Iterable[_Union[FieldPolicy, _Mapping]]] = ...,
    ) -> None: ...
