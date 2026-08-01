from google.api import resource_pb2 as _resource_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServicePerimeter(_message.Message):
    __slots__ = ["create_time", "description", "name", "perimeter_type", "spec", "status", "title", "update_time", "use_explicit_dry_run_spec"]
    class PerimeterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PERIMETER_TYPE_BRIDGE: ServicePerimeter.PerimeterType
    PERIMETER_TYPE_FIELD_NUMBER: _ClassVar[int]
    PERIMETER_TYPE_REGULAR: ServicePerimeter.PerimeterType
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    USE_EXPLICIT_DRY_RUN_SPEC_FIELD_NUMBER: _ClassVar[int]
    create_time: _timestamp_pb2.Timestamp
    description: str
    name: str
    perimeter_type: ServicePerimeter.PerimeterType
    spec: ServicePerimeterConfig
    status: ServicePerimeterConfig
    title: str
    update_time: _timestamp_pb2.Timestamp
    use_explicit_dry_run_spec: bool
    def __init__(self, name: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., perimeter_type: _Optional[_Union[ServicePerimeter.PerimeterType, str]] = ..., status: _Optional[_Union[ServicePerimeterConfig, _Mapping]] = ..., spec: _Optional[_Union[ServicePerimeterConfig, _Mapping]] = ..., use_explicit_dry_run_spec: bool = ...) -> None: ...

class ServicePerimeterConfig(_message.Message):
    __slots__ = ["access_levels", "egress_policies", "ingress_policies", "resources", "restricted_services", "vpc_accessible_services"]
    class IdentityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class ApiOperation(_message.Message):
        __slots__ = ["method_selectors", "service_name"]
        METHOD_SELECTORS_FIELD_NUMBER: _ClassVar[int]
        SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
        method_selectors: _containers.RepeatedCompositeFieldContainer[ServicePerimeterConfig.MethodSelector]
        service_name: str
        def __init__(self, service_name: _Optional[str] = ..., method_selectors: _Optional[_Iterable[_Union[ServicePerimeterConfig.MethodSelector, _Mapping]]] = ...) -> None: ...
    class EgressFrom(_message.Message):
        __slots__ = ["identities", "identity_type"]
        IDENTITIES_FIELD_NUMBER: _ClassVar[int]
        IDENTITY_TYPE_FIELD_NUMBER: _ClassVar[int]
        identities: _containers.RepeatedScalarFieldContainer[str]
        identity_type: ServicePerimeterConfig.IdentityType
        def __init__(self, identities: _Optional[_Iterable[str]] = ..., identity_type: _Optional[_Union[ServicePerimeterConfig.IdentityType, str]] = ...) -> None: ...
    class EgressPolicy(_message.Message):
        __slots__ = ["egress_from", "egress_to"]
        EGRESS_FROM_FIELD_NUMBER: _ClassVar[int]
        EGRESS_TO_FIELD_NUMBER: _ClassVar[int]
        egress_from: ServicePerimeterConfig.EgressFrom
        egress_to: ServicePerimeterConfig.EgressTo
        def __init__(self, egress_from: _Optional[_Union[ServicePerimeterConfig.EgressFrom, _Mapping]] = ..., egress_to: _Optional[_Union[ServicePerimeterConfig.EgressTo, _Mapping]] = ...) -> None: ...
    class EgressTo(_message.Message):
        __slots__ = ["external_resources", "operations", "resources"]
        EXTERNAL_RESOURCES_FIELD_NUMBER: _ClassVar[int]
        OPERATIONS_FIELD_NUMBER: _ClassVar[int]
        RESOURCES_FIELD_NUMBER: _ClassVar[int]
        external_resources: _containers.RepeatedScalarFieldContainer[str]
        operations: _containers.RepeatedCompositeFieldContainer[ServicePerimeterConfig.ApiOperation]
        resources: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, resources: _Optional[_Iterable[str]] = ..., operations: _Optional[_Iterable[_Union[ServicePerimeterConfig.ApiOperation, _Mapping]]] = ..., external_resources: _Optional[_Iterable[str]] = ...) -> None: ...
    class IngressFrom(_message.Message):
        __slots__ = ["identities", "identity_type", "sources"]
        IDENTITIES_FIELD_NUMBER: _ClassVar[int]
        IDENTITY_TYPE_FIELD_NUMBER: _ClassVar[int]
        SOURCES_FIELD_NUMBER: _ClassVar[int]
        identities: _containers.RepeatedScalarFieldContainer[str]
        identity_type: ServicePerimeterConfig.IdentityType
        sources: _containers.RepeatedCompositeFieldContainer[ServicePerimeterConfig.IngressSource]
        def __init__(self, sources: _Optional[_Iterable[_Union[ServicePerimeterConfig.IngressSource, _Mapping]]] = ..., identities: _Optional[_Iterable[str]] = ..., identity_type: _Optional[_Union[ServicePerimeterConfig.IdentityType, str]] = ...) -> None: ...
    class IngressPolicy(_message.Message):
        __slots__ = ["ingress_from", "ingress_to"]
        INGRESS_FROM_FIELD_NUMBER: _ClassVar[int]
        INGRESS_TO_FIELD_NUMBER: _ClassVar[int]
        ingress_from: ServicePerimeterConfig.IngressFrom
        ingress_to: ServicePerimeterConfig.IngressTo
        def __init__(self, ingress_from: _Optional[_Union[ServicePerimeterConfig.IngressFrom, _Mapping]] = ..., ingress_to: _Optional[_Union[ServicePerimeterConfig.IngressTo, _Mapping]] = ...) -> None: ...
    class IngressSource(_message.Message):
        __slots__ = ["access_level", "resource"]
        ACCESS_LEVEL_FIELD_NUMBER: _ClassVar[int]
        RESOURCE_FIELD_NUMBER: _ClassVar[int]
        access_level: str
        resource: str
        def __init__(self, access_level: _Optional[str] = ..., resource: _Optional[str] = ...) -> None: ...
    class IngressTo(_message.Message):
        __slots__ = ["operations", "resources"]
        OPERATIONS_FIELD_NUMBER: _ClassVar[int]
        RESOURCES_FIELD_NUMBER: _ClassVar[int]
        operations: _containers.RepeatedCompositeFieldContainer[ServicePerimeterConfig.ApiOperation]
        resources: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, operations: _Optional[_Iterable[_Union[ServicePerimeterConfig.ApiOperation, _Mapping]]] = ..., resources: _Optional[_Iterable[str]] = ...) -> None: ...
    class MethodSelector(_message.Message):
        __slots__ = ["method", "permission"]
        METHOD_FIELD_NUMBER: _ClassVar[int]
        PERMISSION_FIELD_NUMBER: _ClassVar[int]
        method: str
        permission: str
        def __init__(self, method: _Optional[str] = ..., permission: _Optional[str] = ...) -> None: ...
    class VpcAccessibleServices(_message.Message):
        __slots__ = ["allowed_services", "enable_restriction"]
        ALLOWED_SERVICES_FIELD_NUMBER: _ClassVar[int]
        ENABLE_RESTRICTION_FIELD_NUMBER: _ClassVar[int]
        allowed_services: _containers.RepeatedScalarFieldContainer[str]
        enable_restriction: bool
        def __init__(self, enable_restriction: bool = ..., allowed_services: _Optional[_Iterable[str]] = ...) -> None: ...
    ACCESS_LEVELS_FIELD_NUMBER: _ClassVar[int]
    ANY_IDENTITY: ServicePerimeterConfig.IdentityType
    ANY_SERVICE_ACCOUNT: ServicePerimeterConfig.IdentityType
    ANY_USER_ACCOUNT: ServicePerimeterConfig.IdentityType
    EGRESS_POLICIES_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_TYPE_UNSPECIFIED: ServicePerimeterConfig.IdentityType
    INGRESS_POLICIES_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    RESTRICTED_SERVICES_FIELD_NUMBER: _ClassVar[int]
    VPC_ACCESSIBLE_SERVICES_FIELD_NUMBER: _ClassVar[int]
    access_levels: _containers.RepeatedScalarFieldContainer[str]
    egress_policies: _containers.RepeatedCompositeFieldContainer[ServicePerimeterConfig.EgressPolicy]
    ingress_policies: _containers.RepeatedCompositeFieldContainer[ServicePerimeterConfig.IngressPolicy]
    resources: _containers.RepeatedScalarFieldContainer[str]
    restricted_services: _containers.RepeatedScalarFieldContainer[str]
    vpc_accessible_services: ServicePerimeterConfig.VpcAccessibleServices
    def __init__(self, resources: _Optional[_Iterable[str]] = ..., access_levels: _Optional[_Iterable[str]] = ..., restricted_services: _Optional[_Iterable[str]] = ..., vpc_accessible_services: _Optional[_Union[ServicePerimeterConfig.VpcAccessibleServices, _Mapping]] = ..., ingress_policies: _Optional[_Iterable[_Union[ServicePerimeterConfig.IngressPolicy, _Mapping]]] = ..., egress_policies: _Optional[_Iterable[_Union[ServicePerimeterConfig.EgressPolicy, _Mapping]]] = ...) -> None: ...
