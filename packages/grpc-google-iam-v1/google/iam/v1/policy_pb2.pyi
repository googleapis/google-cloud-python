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
from google.type import expr_pb2 as _expr_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class AuditConfig(_message.Message):
    __slots__ = ["audit_log_configs", "service"]
    AUDIT_LOG_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    audit_log_configs: _containers.RepeatedCompositeFieldContainer[AuditLogConfig]
    service: str
    def __init__(
        self,
        service: _Optional[str] = ...,
        audit_log_configs: _Optional[_Iterable[_Union[AuditLogConfig, _Mapping]]] = ...,
    ) -> None: ...

class AuditConfigDelta(_message.Message):
    __slots__ = ["action", "exempted_member", "log_type", "service"]
    class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    ACTION_FIELD_NUMBER: _ClassVar[int]
    ACTION_UNSPECIFIED: AuditConfigDelta.Action
    ADD: AuditConfigDelta.Action
    EXEMPTED_MEMBER_FIELD_NUMBER: _ClassVar[int]
    LOG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REMOVE: AuditConfigDelta.Action
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    action: AuditConfigDelta.Action
    exempted_member: str
    log_type: str
    service: str
    def __init__(
        self,
        action: _Optional[_Union[AuditConfigDelta.Action, str]] = ...,
        service: _Optional[str] = ...,
        exempted_member: _Optional[str] = ...,
        log_type: _Optional[str] = ...,
    ) -> None: ...

class AuditLogConfig(_message.Message):
    __slots__ = ["exempted_members", "log_type"]
    class LogType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    ADMIN_READ: AuditLogConfig.LogType
    DATA_READ: AuditLogConfig.LogType
    DATA_WRITE: AuditLogConfig.LogType
    EXEMPTED_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    LOG_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOG_TYPE_UNSPECIFIED: AuditLogConfig.LogType
    exempted_members: _containers.RepeatedScalarFieldContainer[str]
    log_type: AuditLogConfig.LogType
    def __init__(
        self,
        log_type: _Optional[_Union[AuditLogConfig.LogType, str]] = ...,
        exempted_members: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class Binding(_message.Message):
    __slots__ = ["condition", "members", "role"]
    CONDITION_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    condition: _expr_pb2.Expr
    members: _containers.RepeatedScalarFieldContainer[str]
    role: str
    def __init__(
        self,
        role: _Optional[str] = ...,
        members: _Optional[_Iterable[str]] = ...,
        condition: _Optional[_Union[_expr_pb2.Expr, _Mapping]] = ...,
    ) -> None: ...

class BindingDelta(_message.Message):
    __slots__ = ["action", "condition", "member", "role"]
    class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    ACTION_FIELD_NUMBER: _ClassVar[int]
    ACTION_UNSPECIFIED: BindingDelta.Action
    ADD: BindingDelta.Action
    CONDITION_FIELD_NUMBER: _ClassVar[int]
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    REMOVE: BindingDelta.Action
    ROLE_FIELD_NUMBER: _ClassVar[int]
    action: BindingDelta.Action
    condition: _expr_pb2.Expr
    member: str
    role: str
    def __init__(
        self,
        action: _Optional[_Union[BindingDelta.Action, str]] = ...,
        role: _Optional[str] = ...,
        member: _Optional[str] = ...,
        condition: _Optional[_Union[_expr_pb2.Expr, _Mapping]] = ...,
    ) -> None: ...

class Policy(_message.Message):
    __slots__ = ["audit_configs", "bindings", "etag", "version"]
    AUDIT_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    BINDINGS_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    audit_configs: _containers.RepeatedCompositeFieldContainer[AuditConfig]
    bindings: _containers.RepeatedCompositeFieldContainer[Binding]
    etag: bytes
    version: int
    def __init__(
        self,
        version: _Optional[int] = ...,
        bindings: _Optional[_Iterable[_Union[Binding, _Mapping]]] = ...,
        audit_configs: _Optional[_Iterable[_Union[AuditConfig, _Mapping]]] = ...,
        etag: _Optional[bytes] = ...,
    ) -> None: ...

class PolicyDelta(_message.Message):
    __slots__ = ["audit_config_deltas", "binding_deltas"]
    AUDIT_CONFIG_DELTAS_FIELD_NUMBER: _ClassVar[int]
    BINDING_DELTAS_FIELD_NUMBER: _ClassVar[int]
    audit_config_deltas: _containers.RepeatedCompositeFieldContainer[AuditConfigDelta]
    binding_deltas: _containers.RepeatedCompositeFieldContainer[BindingDelta]
    def __init__(
        self,
        binding_deltas: _Optional[_Iterable[_Union[BindingDelta, _Mapping]]] = ...,
        audit_config_deltas: _Optional[
            _Iterable[_Union[AuditConfigDelta, _Mapping]]
        ] = ...,
    ) -> None: ...
