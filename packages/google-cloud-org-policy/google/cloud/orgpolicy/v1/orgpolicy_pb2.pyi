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
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class Policy(_message.Message):
    __slots__ = [
        "boolean_policy",
        "constraint",
        "etag",
        "list_policy",
        "restore_default",
        "update_time",
        "version",
    ]
    class BooleanPolicy(_message.Message):
        __slots__ = ["enforced"]
        ENFORCED_FIELD_NUMBER: _ClassVar[int]
        enforced: bool
        def __init__(self, enforced: bool = ...) -> None: ...

    class ListPolicy(_message.Message):
        __slots__ = [
            "all_values",
            "allowed_values",
            "denied_values",
            "inherit_from_parent",
            "suggested_value",
        ]
        class AllValues(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []

        ALLOW: Policy.ListPolicy.AllValues
        ALLOWED_VALUES_FIELD_NUMBER: _ClassVar[int]
        ALL_VALUES_FIELD_NUMBER: _ClassVar[int]
        ALL_VALUES_UNSPECIFIED: Policy.ListPolicy.AllValues
        DENIED_VALUES_FIELD_NUMBER: _ClassVar[int]
        DENY: Policy.ListPolicy.AllValues
        INHERIT_FROM_PARENT_FIELD_NUMBER: _ClassVar[int]
        SUGGESTED_VALUE_FIELD_NUMBER: _ClassVar[int]
        all_values: Policy.ListPolicy.AllValues
        allowed_values: _containers.RepeatedScalarFieldContainer[str]
        denied_values: _containers.RepeatedScalarFieldContainer[str]
        inherit_from_parent: bool
        suggested_value: str
        def __init__(
            self,
            allowed_values: _Optional[_Iterable[str]] = ...,
            denied_values: _Optional[_Iterable[str]] = ...,
            all_values: _Optional[_Union[Policy.ListPolicy.AllValues, str]] = ...,
            suggested_value: _Optional[str] = ...,
            inherit_from_parent: bool = ...,
        ) -> None: ...

    class RestoreDefault(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...

    BOOLEAN_POLICY_FIELD_NUMBER: _ClassVar[int]
    CONSTRAINT_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    LIST_POLICY_FIELD_NUMBER: _ClassVar[int]
    RESTORE_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    boolean_policy: Policy.BooleanPolicy
    constraint: str
    etag: bytes
    list_policy: Policy.ListPolicy
    restore_default: Policy.RestoreDefault
    update_time: _timestamp_pb2.Timestamp
    version: int
    def __init__(
        self,
        version: _Optional[int] = ...,
        constraint: _Optional[str] = ...,
        etag: _Optional[bytes] = ...,
        update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        list_policy: _Optional[_Union[Policy.ListPolicy, _Mapping]] = ...,
        boolean_policy: _Optional[_Union[Policy.BooleanPolicy, _Mapping]] = ...,
        restore_default: _Optional[_Union[Policy.RestoreDefault, _Mapping]] = ...,
    ) -> None: ...
