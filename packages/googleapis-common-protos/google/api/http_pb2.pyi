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

DESCRIPTOR: _descriptor.FileDescriptor

class CustomHttpPattern(_message.Message):
    __slots__ = ["kind", "path"]
    KIND_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    kind: str
    path: str
    def __init__(
        self, kind: _Optional[str] = ..., path: _Optional[str] = ...
    ) -> None: ...

class Http(_message.Message):
    __slots__ = ["fully_decode_reserved_expansion", "rules"]
    FULLY_DECODE_RESERVED_EXPANSION_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    fully_decode_reserved_expansion: bool
    rules: _containers.RepeatedCompositeFieldContainer[HttpRule]
    def __init__(
        self,
        rules: _Optional[_Iterable[_Union[HttpRule, _Mapping]]] = ...,
        fully_decode_reserved_expansion: bool = ...,
    ) -> None: ...

class HttpRule(_message.Message):
    __slots__ = [
        "additional_bindings",
        "body",
        "custom",
        "delete",
        "get",
        "patch",
        "post",
        "put",
        "response_body",
        "selector",
    ]
    ADDITIONAL_BINDINGS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    DELETE_FIELD_NUMBER: _ClassVar[int]
    GET_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    POST_FIELD_NUMBER: _ClassVar[int]
    PUT_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_BODY_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    additional_bindings: _containers.RepeatedCompositeFieldContainer[HttpRule]
    body: str
    custom: CustomHttpPattern
    delete: str
    get: str
    patch: str
    post: str
    put: str
    response_body: str
    selector: str
    def __init__(
        self,
        selector: _Optional[str] = ...,
        get: _Optional[str] = ...,
        put: _Optional[str] = ...,
        post: _Optional[str] = ...,
        delete: _Optional[str] = ...,
        patch: _Optional[str] = ...,
        custom: _Optional[_Union[CustomHttpPattern, _Mapping]] = ...,
        body: _Optional[str] = ...,
        response_body: _Optional[str] = ...,
        additional_bindings: _Optional[_Iterable[_Union[HttpRule, _Mapping]]] = ...,
    ) -> None: ...
