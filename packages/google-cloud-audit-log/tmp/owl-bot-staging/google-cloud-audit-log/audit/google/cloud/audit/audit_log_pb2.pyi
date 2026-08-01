from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.rpc.context import attribute_context_pb2 as _attribute_context_pb2
from google.rpc import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuditLog(_message.Message):
    __slots__ = ["authentication_info", "authorization_info", "metadata", "method_name", "num_response_items", "policy_violation_info", "request", "request_metadata", "resource_location", "resource_name", "resource_original_state", "response", "service_data", "service_name", "status"]
    AUTHENTICATION_INFO_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_INFO_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METHOD_NAME_FIELD_NUMBER: _ClassVar[int]
    NUM_RESPONSE_ITEMS_FIELD_NUMBER: _ClassVar[int]
    POLICY_VIOLATION_INFO_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    REQUEST_METADATA_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ORIGINAL_STATE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_DATA_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    authentication_info: AuthenticationInfo
    authorization_info: _containers.RepeatedCompositeFieldContainer[AuthorizationInfo]
    metadata: _struct_pb2.Struct
    method_name: str
    num_response_items: int
    policy_violation_info: PolicyViolationInfo
    request: _struct_pb2.Struct
    request_metadata: RequestMetadata
    resource_location: ResourceLocation
    resource_name: str
    resource_original_state: _struct_pb2.Struct
    response: _struct_pb2.Struct
    service_data: _any_pb2.Any
    service_name: str
    status: _status_pb2.Status
    def __init__(self, service_name: _Optional[str] = ..., method_name: _Optional[str] = ..., resource_name: _Optional[str] = ..., resource_location: _Optional[_Union[ResourceLocation, _Mapping]] = ..., resource_original_state: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., num_response_items: _Optional[int] = ..., status: _Optional[_Union[_status_pb2.Status, _Mapping]] = ..., authentication_info: _Optional[_Union[AuthenticationInfo, _Mapping]] = ..., authorization_info: _Optional[_Iterable[_Union[AuthorizationInfo, _Mapping]]] = ..., policy_violation_info: _Optional[_Union[PolicyViolationInfo, _Mapping]] = ..., request_metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., request: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., response: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., service_data: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class AuthenticationInfo(_message.Message):
    __slots__ = ["authority_selector", "principal_email", "principal_subject", "service_account_delegation_info", "service_account_key_name", "third_party_principal"]
    AUTHORITY_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_EMAIL_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_SUBJECT_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_DELEGATION_INFO_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_KEY_NAME_FIELD_NUMBER: _ClassVar[int]
    THIRD_PARTY_PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    authority_selector: str
    principal_email: str
    principal_subject: str
    service_account_delegation_info: _containers.RepeatedCompositeFieldContainer[ServiceAccountDelegationInfo]
    service_account_key_name: str
    third_party_principal: _struct_pb2.Struct
    def __init__(self, principal_email: _Optional[str] = ..., authority_selector: _Optional[str] = ..., third_party_principal: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., service_account_key_name: _Optional[str] = ..., service_account_delegation_info: _Optional[_Iterable[_Union[ServiceAccountDelegationInfo, _Mapping]]] = ..., principal_subject: _Optional[str] = ...) -> None: ...

class AuthorizationInfo(_message.Message):
    __slots__ = ["granted", "permission", "permission_type", "resource", "resource_attributes"]
    class PermissionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ADMIN_READ: AuthorizationInfo.PermissionType
    ADMIN_WRITE: AuthorizationInfo.PermissionType
    DATA_READ: AuthorizationInfo.PermissionType
    DATA_WRITE: AuthorizationInfo.PermissionType
    GRANTED_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_TYPE_UNSPECIFIED: AuthorizationInfo.PermissionType
    RESOURCE_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    granted: bool
    permission: str
    permission_type: AuthorizationInfo.PermissionType
    resource: str
    resource_attributes: _attribute_context_pb2.AttributeContext.Resource
    def __init__(self, resource: _Optional[str] = ..., permission: _Optional[str] = ..., granted: bool = ..., resource_attributes: _Optional[_Union[_attribute_context_pb2.AttributeContext.Resource, _Mapping]] = ..., permission_type: _Optional[_Union[AuthorizationInfo.PermissionType, str]] = ...) -> None: ...

class OrgPolicyViolationInfo(_message.Message):
    __slots__ = ["payload", "resource_tags", "resource_type", "violation_info"]
    class ResourceTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TAGS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    VIOLATION_INFO_FIELD_NUMBER: _ClassVar[int]
    payload: _struct_pb2.Struct
    resource_tags: _containers.ScalarMap[str, str]
    resource_type: str
    violation_info: _containers.RepeatedCompositeFieldContainer[ViolationInfo]
    def __init__(self, payload: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., resource_type: _Optional[str] = ..., resource_tags: _Optional[_Mapping[str, str]] = ..., violation_info: _Optional[_Iterable[_Union[ViolationInfo, _Mapping]]] = ...) -> None: ...

class PolicyViolationInfo(_message.Message):
    __slots__ = ["org_policy_violation_info"]
    ORG_POLICY_VIOLATION_INFO_FIELD_NUMBER: _ClassVar[int]
    org_policy_violation_info: OrgPolicyViolationInfo
    def __init__(self, org_policy_violation_info: _Optional[_Union[OrgPolicyViolationInfo, _Mapping]] = ...) -> None: ...

class RequestMetadata(_message.Message):
    __slots__ = ["caller_ip", "caller_network", "caller_supplied_user_agent", "destination_attributes", "request_attributes"]
    CALLER_IP_FIELD_NUMBER: _ClassVar[int]
    CALLER_NETWORK_FIELD_NUMBER: _ClassVar[int]
    CALLER_SUPPLIED_USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    caller_ip: str
    caller_network: str
    caller_supplied_user_agent: str
    destination_attributes: _attribute_context_pb2.AttributeContext.Peer
    request_attributes: _attribute_context_pb2.AttributeContext.Request
    def __init__(self, caller_ip: _Optional[str] = ..., caller_supplied_user_agent: _Optional[str] = ..., caller_network: _Optional[str] = ..., request_attributes: _Optional[_Union[_attribute_context_pb2.AttributeContext.Request, _Mapping]] = ..., destination_attributes: _Optional[_Union[_attribute_context_pb2.AttributeContext.Peer, _Mapping]] = ...) -> None: ...

class ResourceLocation(_message.Message):
    __slots__ = ["current_locations", "original_locations"]
    CURRENT_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    current_locations: _containers.RepeatedScalarFieldContainer[str]
    original_locations: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, current_locations: _Optional[_Iterable[str]] = ..., original_locations: _Optional[_Iterable[str]] = ...) -> None: ...

class ServiceAccountDelegationInfo(_message.Message):
    __slots__ = ["first_party_principal", "principal_subject", "third_party_principal"]
    class FirstPartyPrincipal(_message.Message):
        __slots__ = ["principal_email", "service_metadata"]
        PRINCIPAL_EMAIL_FIELD_NUMBER: _ClassVar[int]
        SERVICE_METADATA_FIELD_NUMBER: _ClassVar[int]
        principal_email: str
        service_metadata: _struct_pb2.Struct
        def __init__(self, principal_email: _Optional[str] = ..., service_metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    class ThirdPartyPrincipal(_message.Message):
        __slots__ = ["third_party_claims"]
        THIRD_PARTY_CLAIMS_FIELD_NUMBER: _ClassVar[int]
        third_party_claims: _struct_pb2.Struct
        def __init__(self, third_party_claims: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    FIRST_PARTY_PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_SUBJECT_FIELD_NUMBER: _ClassVar[int]
    THIRD_PARTY_PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    first_party_principal: ServiceAccountDelegationInfo.FirstPartyPrincipal
    principal_subject: str
    third_party_principal: ServiceAccountDelegationInfo.ThirdPartyPrincipal
    def __init__(self, principal_subject: _Optional[str] = ..., first_party_principal: _Optional[_Union[ServiceAccountDelegationInfo.FirstPartyPrincipal, _Mapping]] = ..., third_party_principal: _Optional[_Union[ServiceAccountDelegationInfo.ThirdPartyPrincipal, _Mapping]] = ...) -> None: ...

class ViolationInfo(_message.Message):
    __slots__ = ["checked_value", "constraint", "error_message", "policy_type"]
    class PolicyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BOOLEAN_CONSTRAINT: ViolationInfo.PolicyType
    CHECKED_VALUE_FIELD_NUMBER: _ClassVar[int]
    CONSTRAINT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CONSTRAINT: ViolationInfo.PolicyType
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LIST_CONSTRAINT: ViolationInfo.PolicyType
    POLICY_TYPE_FIELD_NUMBER: _ClassVar[int]
    POLICY_TYPE_UNSPECIFIED: ViolationInfo.PolicyType
    checked_value: str
    constraint: str
    error_message: str
    policy_type: ViolationInfo.PolicyType
    def __init__(self, constraint: _Optional[str] = ..., error_message: _Optional[str] = ..., checked_value: _Optional[str] = ..., policy_type: _Optional[_Union[ViolationInfo.PolicyType, str]] = ...) -> None: ...
