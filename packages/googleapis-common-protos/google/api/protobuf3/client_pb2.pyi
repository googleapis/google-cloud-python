from google.api import launch_stage_pb2 as _launch_stage_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

ADS: ClientLibraryOrganization
API_VERSION_FIELD_NUMBER: ClassVar[int]
CLIENT_LIBRARY_DESTINATION_UNSPECIFIED: ClientLibraryDestination
CLIENT_LIBRARY_ORGANIZATION_UNSPECIFIED: ClientLibraryOrganization
CLOUD: ClientLibraryOrganization
DEFAULT_HOST_FIELD_NUMBER: ClassVar[int]
DESCRIPTOR: _descriptor.FileDescriptor
GENERATIVE_AI: ClientLibraryOrganization
GEO: ClientLibraryOrganization
GITHUB: ClientLibraryDestination
METHOD_SIGNATURE_FIELD_NUMBER: ClassVar[int]
OAUTH_SCOPES_FIELD_NUMBER: ClassVar[int]
PACKAGE_MANAGER: ClientLibraryDestination
PHOTOS: ClientLibraryOrganization
SHOPPING: ClientLibraryOrganization
STREET_VIEW: ClientLibraryOrganization
api_version: _descriptor.FieldDescriptor
default_host: _descriptor.FieldDescriptor
method_signature: _descriptor.FieldDescriptor
oauth_scopes: _descriptor.FieldDescriptor

class ClientLibrarySettings(_message.Message):
    __slots__ = ["cpp_settings", "dotnet_settings", "go_settings", "java_settings", "launch_stage", "node_settings", "php_settings", "python_settings", "rest_numeric_enums", "ruby_settings", "version"]
    CPP_SETTINGS_FIELD_NUMBER: ClassVar[int]
    DOTNET_SETTINGS_FIELD_NUMBER: ClassVar[int]
    GO_SETTINGS_FIELD_NUMBER: ClassVar[int]
    JAVA_SETTINGS_FIELD_NUMBER: ClassVar[int]
    LAUNCH_STAGE_FIELD_NUMBER: ClassVar[int]
    NODE_SETTINGS_FIELD_NUMBER: ClassVar[int]
    PHP_SETTINGS_FIELD_NUMBER: ClassVar[int]
    PYTHON_SETTINGS_FIELD_NUMBER: ClassVar[int]
    REST_NUMERIC_ENUMS_FIELD_NUMBER: ClassVar[int]
    RUBY_SETTINGS_FIELD_NUMBER: ClassVar[int]
    VERSION_FIELD_NUMBER: ClassVar[int]
    cpp_settings: CppSettings
    dotnet_settings: DotnetSettings
    go_settings: GoSettings
    java_settings: JavaSettings
    launch_stage: _launch_stage_pb2.LaunchStage
    node_settings: NodeSettings
    php_settings: PhpSettings
    python_settings: PythonSettings
    rest_numeric_enums: bool
    ruby_settings: RubySettings
    version: str
    def __init__(self, version: Optional[str] = ..., launch_stage: Optional[Union[_launch_stage_pb2.LaunchStage, str]] = ..., rest_numeric_enums: bool = ..., java_settings: Optional[Union[JavaSettings, Mapping]] = ..., cpp_settings: Optional[Union[CppSettings, Mapping]] = ..., php_settings: Optional[Union[PhpSettings, Mapping]] = ..., python_settings: Optional[Union[PythonSettings, Mapping]] = ..., node_settings: Optional[Union[NodeSettings, Mapping]] = ..., dotnet_settings: Optional[Union[DotnetSettings, Mapping]] = ..., ruby_settings: Optional[Union[RubySettings, Mapping]] = ..., go_settings: Optional[Union[GoSettings, Mapping]] = ...) -> None: ...

class CommonLanguageSettings(_message.Message):
    __slots__ = ["destinations", "reference_docs_uri", "selective_gapic_generation"]
    DESTINATIONS_FIELD_NUMBER: ClassVar[int]
    REFERENCE_DOCS_URI_FIELD_NUMBER: ClassVar[int]
    SELECTIVE_GAPIC_GENERATION_FIELD_NUMBER: ClassVar[int]
    destinations: _containers.RepeatedScalarFieldContainer[ClientLibraryDestination]
    reference_docs_uri: str
    selective_gapic_generation: SelectiveGapicGeneration
    def __init__(self, reference_docs_uri: Optional[str] = ..., destinations: Optional[Iterable[Union[ClientLibraryDestination, str]]] = ..., selective_gapic_generation: Optional[Union[SelectiveGapicGeneration, Mapping]] = ...) -> None: ...

class CppSettings(_message.Message):
    __slots__ = ["common"]
    COMMON_FIELD_NUMBER: ClassVar[int]
    common: CommonLanguageSettings
    def __init__(self, common: Optional[Union[CommonLanguageSettings, Mapping]] = ...) -> None: ...

class DotnetSettings(_message.Message):
    __slots__ = ["common", "forced_namespace_aliases", "handwritten_signatures", "ignored_resources", "renamed_resources", "renamed_services"]
    class RenamedResourcesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    class RenamedServicesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    COMMON_FIELD_NUMBER: ClassVar[int]
    FORCED_NAMESPACE_ALIASES_FIELD_NUMBER: ClassVar[int]
    HANDWRITTEN_SIGNATURES_FIELD_NUMBER: ClassVar[int]
    IGNORED_RESOURCES_FIELD_NUMBER: ClassVar[int]
    RENAMED_RESOURCES_FIELD_NUMBER: ClassVar[int]
    RENAMED_SERVICES_FIELD_NUMBER: ClassVar[int]
    common: CommonLanguageSettings
    forced_namespace_aliases: _containers.RepeatedScalarFieldContainer[str]
    handwritten_signatures: _containers.RepeatedScalarFieldContainer[str]
    ignored_resources: _containers.RepeatedScalarFieldContainer[str]
    renamed_resources: _containers.ScalarMap[str, str]
    renamed_services: _containers.ScalarMap[str, str]
    def __init__(self, common: Optional[Union[CommonLanguageSettings, Mapping]] = ..., renamed_services: Optional[Mapping[str, str]] = ..., renamed_resources: Optional[Mapping[str, str]] = ..., ignored_resources: Optional[Iterable[str]] = ..., forced_namespace_aliases: Optional[Iterable[str]] = ..., handwritten_signatures: Optional[Iterable[str]] = ...) -> None: ...

class GoSettings(_message.Message):
    __slots__ = ["common", "renamed_services"]
    class RenamedServicesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    COMMON_FIELD_NUMBER: ClassVar[int]
    RENAMED_SERVICES_FIELD_NUMBER: ClassVar[int]
    common: CommonLanguageSettings
    renamed_services: _containers.ScalarMap[str, str]
    def __init__(self, common: Optional[Union[CommonLanguageSettings, Mapping]] = ..., renamed_services: Optional[Mapping[str, str]] = ...) -> None: ...

class JavaSettings(_message.Message):
    __slots__ = ["common", "library_package", "service_class_names"]
    class ServiceClassNamesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    COMMON_FIELD_NUMBER: ClassVar[int]
    LIBRARY_PACKAGE_FIELD_NUMBER: ClassVar[int]
    SERVICE_CLASS_NAMES_FIELD_NUMBER: ClassVar[int]
    common: CommonLanguageSettings
    library_package: str
    service_class_names: _containers.ScalarMap[str, str]
    def __init__(self, library_package: Optional[str] = ..., service_class_names: Optional[Mapping[str, str]] = ..., common: Optional[Union[CommonLanguageSettings, Mapping]] = ...) -> None: ...

class MethodSettings(_message.Message):
    __slots__ = ["auto_populated_fields", "long_running", "selector"]
    class LongRunning(_message.Message):
        __slots__ = ["initial_poll_delay", "max_poll_delay", "poll_delay_multiplier", "total_poll_timeout"]
        INITIAL_POLL_DELAY_FIELD_NUMBER: ClassVar[int]
        MAX_POLL_DELAY_FIELD_NUMBER: ClassVar[int]
        POLL_DELAY_MULTIPLIER_FIELD_NUMBER: ClassVar[int]
        TOTAL_POLL_TIMEOUT_FIELD_NUMBER: ClassVar[int]
        initial_poll_delay: _duration_pb2.Duration
        max_poll_delay: _duration_pb2.Duration
        poll_delay_multiplier: float
        total_poll_timeout: _duration_pb2.Duration
        def __init__(self, initial_poll_delay: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., poll_delay_multiplier: Optional[float] = ..., max_poll_delay: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., total_poll_timeout: Optional[Union[_duration_pb2.Duration, Mapping]] = ...) -> None: ...
    AUTO_POPULATED_FIELDS_FIELD_NUMBER: ClassVar[int]
    LONG_RUNNING_FIELD_NUMBER: ClassVar[int]
    SELECTOR_FIELD_NUMBER: ClassVar[int]
    auto_populated_fields: _containers.RepeatedScalarFieldContainer[str]
    long_running: MethodSettings.LongRunning
    selector: str
    def __init__(self, selector: Optional[str] = ..., long_running: Optional[Union[MethodSettings.LongRunning, Mapping]] = ..., auto_populated_fields: Optional[Iterable[str]] = ...) -> None: ...

class NodeSettings(_message.Message):
    __slots__ = ["common"]
    COMMON_FIELD_NUMBER: ClassVar[int]
    common: CommonLanguageSettings
    def __init__(self, common: Optional[Union[CommonLanguageSettings, Mapping]] = ...) -> None: ...

class PhpSettings(_message.Message):
    __slots__ = ["common"]
    COMMON_FIELD_NUMBER: ClassVar[int]
    common: CommonLanguageSettings
    def __init__(self, common: Optional[Union[CommonLanguageSettings, Mapping]] = ...) -> None: ...

class Publishing(_message.Message):
    __slots__ = ["api_short_name", "codeowner_github_teams", "doc_tag_prefix", "documentation_uri", "github_label", "library_settings", "method_settings", "new_issue_uri", "organization", "proto_reference_documentation_uri", "rest_reference_documentation_uri"]
    API_SHORT_NAME_FIELD_NUMBER: ClassVar[int]
    CODEOWNER_GITHUB_TEAMS_FIELD_NUMBER: ClassVar[int]
    DOCUMENTATION_URI_FIELD_NUMBER: ClassVar[int]
    DOC_TAG_PREFIX_FIELD_NUMBER: ClassVar[int]
    GITHUB_LABEL_FIELD_NUMBER: ClassVar[int]
    LIBRARY_SETTINGS_FIELD_NUMBER: ClassVar[int]
    METHOD_SETTINGS_FIELD_NUMBER: ClassVar[int]
    NEW_ISSUE_URI_FIELD_NUMBER: ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: ClassVar[int]
    PROTO_REFERENCE_DOCUMENTATION_URI_FIELD_NUMBER: ClassVar[int]
    REST_REFERENCE_DOCUMENTATION_URI_FIELD_NUMBER: ClassVar[int]
    api_short_name: str
    codeowner_github_teams: _containers.RepeatedScalarFieldContainer[str]
    doc_tag_prefix: str
    documentation_uri: str
    github_label: str
    library_settings: _containers.RepeatedCompositeFieldContainer[ClientLibrarySettings]
    method_settings: _containers.RepeatedCompositeFieldContainer[MethodSettings]
    new_issue_uri: str
    organization: ClientLibraryOrganization
    proto_reference_documentation_uri: str
    rest_reference_documentation_uri: str
    def __init__(self, method_settings: Optional[Iterable[Union[MethodSettings, Mapping]]] = ..., new_issue_uri: Optional[str] = ..., documentation_uri: Optional[str] = ..., api_short_name: Optional[str] = ..., github_label: Optional[str] = ..., codeowner_github_teams: Optional[Iterable[str]] = ..., doc_tag_prefix: Optional[str] = ..., organization: Optional[Union[ClientLibraryOrganization, str]] = ..., library_settings: Optional[Iterable[Union[ClientLibrarySettings, Mapping]]] = ..., proto_reference_documentation_uri: Optional[str] = ..., rest_reference_documentation_uri: Optional[str] = ...) -> None: ...

class PythonSettings(_message.Message):
    __slots__ = ["common", "experimental_features"]
    class ExperimentalFeatures(_message.Message):
        __slots__ = ["protobuf_pythonic_types_enabled", "rest_async_io_enabled", "unversioned_package_disabled"]
        PROTOBUF_PYTHONIC_TYPES_ENABLED_FIELD_NUMBER: ClassVar[int]
        REST_ASYNC_IO_ENABLED_FIELD_NUMBER: ClassVar[int]
        UNVERSIONED_PACKAGE_DISABLED_FIELD_NUMBER: ClassVar[int]
        protobuf_pythonic_types_enabled: bool
        rest_async_io_enabled: bool
        unversioned_package_disabled: bool
        def __init__(self, rest_async_io_enabled: bool = ..., protobuf_pythonic_types_enabled: bool = ..., unversioned_package_disabled: bool = ...) -> None: ...
    COMMON_FIELD_NUMBER: ClassVar[int]
    EXPERIMENTAL_FEATURES_FIELD_NUMBER: ClassVar[int]
    common: CommonLanguageSettings
    experimental_features: PythonSettings.ExperimentalFeatures
    def __init__(self, common: Optional[Union[CommonLanguageSettings, Mapping]] = ..., experimental_features: Optional[Union[PythonSettings.ExperimentalFeatures, Mapping]] = ...) -> None: ...

class RubySettings(_message.Message):
    __slots__ = ["common"]
    COMMON_FIELD_NUMBER: ClassVar[int]
    common: CommonLanguageSettings
    def __init__(self, common: Optional[Union[CommonLanguageSettings, Mapping]] = ...) -> None: ...

class SelectiveGapicGeneration(_message.Message):
    __slots__ = ["generate_omitted_as_internal", "methods"]
    GENERATE_OMITTED_AS_INTERNAL_FIELD_NUMBER: ClassVar[int]
    METHODS_FIELD_NUMBER: ClassVar[int]
    generate_omitted_as_internal: bool
    methods: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, methods: Optional[Iterable[str]] = ..., generate_omitted_as_internal: bool = ...) -> None: ...

class ClientLibraryOrganization(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ClientLibraryDestination(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
