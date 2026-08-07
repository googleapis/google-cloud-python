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

from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import message as _message
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class AttributeContext(_message.Message):
    __slots__ = [
        "api",
        "destination",
        "extensions",
        "origin",
        "request",
        "resource",
        "response",
        "source",
    ]
    class Api(_message.Message):
        __slots__ = ["operation", "protocol", "service", "version"]
        OPERATION_FIELD_NUMBER: _ClassVar[int]
        PROTOCOL_FIELD_NUMBER: _ClassVar[int]
        SERVICE_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        operation: str
        protocol: str
        service: str
        version: str
        def __init__(
            self,
            service: _Optional[str] = ...,
            operation: _Optional[str] = ...,
            protocol: _Optional[str] = ...,
            version: _Optional[str] = ...,
        ) -> None: ...

    class Auth(_message.Message):
        __slots__ = ["access_levels", "audiences", "claims", "presenter", "principal"]
        ACCESS_LEVELS_FIELD_NUMBER: _ClassVar[int]
        AUDIENCES_FIELD_NUMBER: _ClassVar[int]
        CLAIMS_FIELD_NUMBER: _ClassVar[int]
        PRESENTER_FIELD_NUMBER: _ClassVar[int]
        PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
        access_levels: _containers.RepeatedScalarFieldContainer[str]
        audiences: _containers.RepeatedScalarFieldContainer[str]
        claims: _struct_pb2.Struct
        presenter: str
        principal: str
        def __init__(
            self,
            principal: _Optional[str] = ...,
            audiences: _Optional[_Iterable[str]] = ...,
            presenter: _Optional[str] = ...,
            claims: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
            access_levels: _Optional[_Iterable[str]] = ...,
        ) -> None: ...

    class Peer(_message.Message):
        __slots__ = ["ip", "labels", "port", "principal", "region_code"]
        class LabelsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[str] = ...
            ) -> None: ...

        IP_FIELD_NUMBER: _ClassVar[int]
        LABELS_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
        REGION_CODE_FIELD_NUMBER: _ClassVar[int]
        ip: str
        labels: _containers.ScalarMap[str, str]
        port: int
        principal: str
        region_code: str
        def __init__(
            self,
            ip: _Optional[str] = ...,
            port: _Optional[int] = ...,
            labels: _Optional[_Mapping[str, str]] = ...,
            principal: _Optional[str] = ...,
            region_code: _Optional[str] = ...,
        ) -> None: ...

    class Request(_message.Message):
        __slots__ = [
            "auth",
            "headers",
            "host",
            "id",
            "method",
            "origin",
            "path",
            "protocol",
            "query",
            "reason",
            "scheme",
            "size",
            "time",
        ]
        class HeadersEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[str] = ...
            ) -> None: ...

        AUTH_FIELD_NUMBER: _ClassVar[int]
        HEADERS_FIELD_NUMBER: _ClassVar[int]
        HOST_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        METHOD_FIELD_NUMBER: _ClassVar[int]
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        PATH_FIELD_NUMBER: _ClassVar[int]
        PROTOCOL_FIELD_NUMBER: _ClassVar[int]
        QUERY_FIELD_NUMBER: _ClassVar[int]
        REASON_FIELD_NUMBER: _ClassVar[int]
        SCHEME_FIELD_NUMBER: _ClassVar[int]
        SIZE_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        auth: AttributeContext.Auth
        headers: _containers.ScalarMap[str, str]
        host: str
        id: str
        method: str
        origin: str
        path: str
        protocol: str
        query: str
        reason: str
        scheme: str
        size: int
        time: _timestamp_pb2.Timestamp
        def __init__(
            self,
            id: _Optional[str] = ...,
            method: _Optional[str] = ...,
            headers: _Optional[_Mapping[str, str]] = ...,
            path: _Optional[str] = ...,
            host: _Optional[str] = ...,
            scheme: _Optional[str] = ...,
            query: _Optional[str] = ...,
            time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            size: _Optional[int] = ...,
            protocol: _Optional[str] = ...,
            reason: _Optional[str] = ...,
            auth: _Optional[_Union[AttributeContext.Auth, _Mapping]] = ...,
            origin: _Optional[str] = ...,
        ) -> None: ...

    class Resource(_message.Message):
        __slots__ = [
            "annotations",
            "create_time",
            "delete_time",
            "display_name",
            "etag",
            "labels",
            "location",
            "name",
            "service",
            "type",
            "uid",
            "update_time",
        ]
        class AnnotationsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[str] = ...
            ) -> None: ...

        class LabelsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[str] = ...
            ) -> None: ...

        ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
        CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
        DELETE_TIME_FIELD_NUMBER: _ClassVar[int]
        DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
        ETAG_FIELD_NUMBER: _ClassVar[int]
        LABELS_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        SERVICE_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        UID_FIELD_NUMBER: _ClassVar[int]
        UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
        annotations: _containers.ScalarMap[str, str]
        create_time: _timestamp_pb2.Timestamp
        delete_time: _timestamp_pb2.Timestamp
        display_name: str
        etag: str
        labels: _containers.ScalarMap[str, str]
        location: str
        name: str
        service: str
        type: str
        uid: str
        update_time: _timestamp_pb2.Timestamp
        def __init__(
            self,
            service: _Optional[str] = ...,
            name: _Optional[str] = ...,
            type: _Optional[str] = ...,
            labels: _Optional[_Mapping[str, str]] = ...,
            uid: _Optional[str] = ...,
            annotations: _Optional[_Mapping[str, str]] = ...,
            display_name: _Optional[str] = ...,
            create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            delete_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            etag: _Optional[str] = ...,
            location: _Optional[str] = ...,
        ) -> None: ...

    class Response(_message.Message):
        __slots__ = ["backend_latency", "code", "headers", "size", "time"]
        class HeadersEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[str] = ...
            ) -> None: ...

        BACKEND_LATENCY_FIELD_NUMBER: _ClassVar[int]
        CODE_FIELD_NUMBER: _ClassVar[int]
        HEADERS_FIELD_NUMBER: _ClassVar[int]
        SIZE_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        backend_latency: _duration_pb2.Duration
        code: int
        headers: _containers.ScalarMap[str, str]
        size: int
        time: _timestamp_pb2.Timestamp
        def __init__(
            self,
            code: _Optional[int] = ...,
            size: _Optional[int] = ...,
            headers: _Optional[_Mapping[str, str]] = ...,
            time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
            backend_latency: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        ) -> None: ...

    API_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    api: AttributeContext.Api
    destination: AttributeContext.Peer
    extensions: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    origin: AttributeContext.Peer
    request: AttributeContext.Request
    resource: AttributeContext.Resource
    response: AttributeContext.Response
    source: AttributeContext.Peer
    def __init__(
        self,
        origin: _Optional[_Union[AttributeContext.Peer, _Mapping]] = ...,
        source: _Optional[_Union[AttributeContext.Peer, _Mapping]] = ...,
        destination: _Optional[_Union[AttributeContext.Peer, _Mapping]] = ...,
        request: _Optional[_Union[AttributeContext.Request, _Mapping]] = ...,
        response: _Optional[_Union[AttributeContext.Response, _Mapping]] = ...,
        resource: _Optional[_Union[AttributeContext.Resource, _Mapping]] = ...,
        api: _Optional[_Union[AttributeContext.Api, _Mapping]] = ...,
        extensions: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...,
    ) -> None: ...
