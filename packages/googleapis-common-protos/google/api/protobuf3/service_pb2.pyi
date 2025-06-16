from google.api import auth_pb2 as _auth_pb2
from google.api import backend_pb2 as _backend_pb2
from google.api import billing_pb2 as _billing_pb2
from google.api import client_pb2 as _client_pb2
from google.api import context_pb2 as _context_pb2
from google.api import control_pb2 as _control_pb2
from google.api import documentation_pb2 as _documentation_pb2
from google.api import endpoint_pb2 as _endpoint_pb2
from google.api import http_pb2 as _http_pb2
from google.api import log_pb2 as _log_pb2
from google.api import logging_pb2 as _logging_pb2
from google.api import metric_pb2 as _metric_pb2
from google.api import monitored_resource_pb2 as _monitored_resource_pb2
from google.api import monitoring_pb2 as _monitoring_pb2
from google.api import quota_pb2 as _quota_pb2
from google.api import source_info_pb2 as _source_info_pb2
from google.api import system_parameter_pb2 as _system_parameter_pb2
from google.api import usage_pb2 as _usage_pb2
from google.protobuf import api_pb2 as _api_pb2
from google.protobuf import type_pb2 as _type_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Service(_message.Message):
    __slots__ = ["apis", "authentication", "backend", "billing", "config_version", "context", "control", "documentation", "endpoints", "enums", "http", "id", "logging", "logs", "metrics", "monitored_resources", "monitoring", "name", "producer_project_id", "publishing", "quota", "source_info", "system_parameters", "title", "types", "usage"]
    APIS_FIELD_NUMBER: ClassVar[int]
    AUTHENTICATION_FIELD_NUMBER: ClassVar[int]
    BACKEND_FIELD_NUMBER: ClassVar[int]
    BILLING_FIELD_NUMBER: ClassVar[int]
    CONFIG_VERSION_FIELD_NUMBER: ClassVar[int]
    CONTEXT_FIELD_NUMBER: ClassVar[int]
    CONTROL_FIELD_NUMBER: ClassVar[int]
    DOCUMENTATION_FIELD_NUMBER: ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: ClassVar[int]
    ENUMS_FIELD_NUMBER: ClassVar[int]
    HTTP_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    LOGGING_FIELD_NUMBER: ClassVar[int]
    LOGS_FIELD_NUMBER: ClassVar[int]
    METRICS_FIELD_NUMBER: ClassVar[int]
    MONITORED_RESOURCES_FIELD_NUMBER: ClassVar[int]
    MONITORING_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    PRODUCER_PROJECT_ID_FIELD_NUMBER: ClassVar[int]
    PUBLISHING_FIELD_NUMBER: ClassVar[int]
    QUOTA_FIELD_NUMBER: ClassVar[int]
    SOURCE_INFO_FIELD_NUMBER: ClassVar[int]
    SYSTEM_PARAMETERS_FIELD_NUMBER: ClassVar[int]
    TITLE_FIELD_NUMBER: ClassVar[int]
    TYPES_FIELD_NUMBER: ClassVar[int]
    USAGE_FIELD_NUMBER: ClassVar[int]
    apis: _containers.RepeatedCompositeFieldContainer[_api_pb2.Api]
    authentication: _auth_pb2.Authentication
    backend: _backend_pb2.Backend
    billing: _billing_pb2.Billing
    config_version: _wrappers_pb2.UInt32Value
    context: _context_pb2.Context
    control: _control_pb2.Control
    documentation: _documentation_pb2.Documentation
    endpoints: _containers.RepeatedCompositeFieldContainer[_endpoint_pb2.Endpoint]
    enums: _containers.RepeatedCompositeFieldContainer[_type_pb2.Enum]
    http: _http_pb2.Http
    id: str
    logging: _logging_pb2.Logging
    logs: _containers.RepeatedCompositeFieldContainer[_log_pb2.LogDescriptor]
    metrics: _containers.RepeatedCompositeFieldContainer[_metric_pb2.MetricDescriptor]
    monitored_resources: _containers.RepeatedCompositeFieldContainer[_monitored_resource_pb2.MonitoredResourceDescriptor]
    monitoring: _monitoring_pb2.Monitoring
    name: str
    producer_project_id: str
    publishing: _client_pb2.Publishing
    quota: _quota_pb2.Quota
    source_info: _source_info_pb2.SourceInfo
    system_parameters: _system_parameter_pb2.SystemParameters
    title: str
    types: _containers.RepeatedCompositeFieldContainer[_type_pb2.Type]
    usage: _usage_pb2.Usage
    def __init__(self, name: Optional[str] = ..., title: Optional[str] = ..., producer_project_id: Optional[str] = ..., id: Optional[str] = ..., apis: Optional[Iterable[Union[_api_pb2.Api, Mapping]]] = ..., types: Optional[Iterable[Union[_type_pb2.Type, Mapping]]] = ..., enums: Optional[Iterable[Union[_type_pb2.Enum, Mapping]]] = ..., documentation: Optional[Union[_documentation_pb2.Documentation, Mapping]] = ..., backend: Optional[Union[_backend_pb2.Backend, Mapping]] = ..., http: Optional[Union[_http_pb2.Http, Mapping]] = ..., quota: Optional[Union[_quota_pb2.Quota, Mapping]] = ..., authentication: Optional[Union[_auth_pb2.Authentication, Mapping]] = ..., context: Optional[Union[_context_pb2.Context, Mapping]] = ..., usage: Optional[Union[_usage_pb2.Usage, Mapping]] = ..., endpoints: Optional[Iterable[Union[_endpoint_pb2.Endpoint, Mapping]]] = ..., control: Optional[Union[_control_pb2.Control, Mapping]] = ..., logs: Optional[Iterable[Union[_log_pb2.LogDescriptor, Mapping]]] = ..., metrics: Optional[Iterable[Union[_metric_pb2.MetricDescriptor, Mapping]]] = ..., monitored_resources: Optional[Iterable[Union[_monitored_resource_pb2.MonitoredResourceDescriptor, Mapping]]] = ..., billing: Optional[Union[_billing_pb2.Billing, Mapping]] = ..., logging: Optional[Union[_logging_pb2.Logging, Mapping]] = ..., monitoring: Optional[Union[_monitoring_pb2.Monitoring, Mapping]] = ..., system_parameters: Optional[Union[_system_parameter_pb2.SystemParameters, Mapping]] = ..., source_info: Optional[Union[_source_info_pb2.SourceInfo, Mapping]] = ..., publishing: Optional[Union[_client_pb2.Publishing, Mapping]] = ..., config_version: Optional[Union[_wrappers_pb2.UInt32Value, Mapping]] = ...) -> None: ...
