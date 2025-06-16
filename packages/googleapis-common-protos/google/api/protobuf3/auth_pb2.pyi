from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthProvider(_message.Message):
    __slots__ = ["audiences", "authorization_url", "id", "issuer", "jwks_uri", "jwt_locations"]
    AUDIENCES_FIELD_NUMBER: ClassVar[int]
    AUTHORIZATION_URL_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    ISSUER_FIELD_NUMBER: ClassVar[int]
    JWKS_URI_FIELD_NUMBER: ClassVar[int]
    JWT_LOCATIONS_FIELD_NUMBER: ClassVar[int]
    audiences: str
    authorization_url: str
    id: str
    issuer: str
    jwks_uri: str
    jwt_locations: _containers.RepeatedCompositeFieldContainer[JwtLocation]
    def __init__(self, id: Optional[str] = ..., issuer: Optional[str] = ..., jwks_uri: Optional[str] = ..., audiences: Optional[str] = ..., authorization_url: Optional[str] = ..., jwt_locations: Optional[Iterable[Union[JwtLocation, Mapping]]] = ...) -> None: ...

class AuthRequirement(_message.Message):
    __slots__ = ["audiences", "provider_id"]
    AUDIENCES_FIELD_NUMBER: ClassVar[int]
    PROVIDER_ID_FIELD_NUMBER: ClassVar[int]
    audiences: str
    provider_id: str
    def __init__(self, provider_id: Optional[str] = ..., audiences: Optional[str] = ...) -> None: ...

class Authentication(_message.Message):
    __slots__ = ["providers", "rules"]
    PROVIDERS_FIELD_NUMBER: ClassVar[int]
    RULES_FIELD_NUMBER: ClassVar[int]
    providers: _containers.RepeatedCompositeFieldContainer[AuthProvider]
    rules: _containers.RepeatedCompositeFieldContainer[AuthenticationRule]
    def __init__(self, rules: Optional[Iterable[Union[AuthenticationRule, Mapping]]] = ..., providers: Optional[Iterable[Union[AuthProvider, Mapping]]] = ...) -> None: ...

class AuthenticationRule(_message.Message):
    __slots__ = ["allow_without_credential", "oauth", "requirements", "selector"]
    ALLOW_WITHOUT_CREDENTIAL_FIELD_NUMBER: ClassVar[int]
    OAUTH_FIELD_NUMBER: ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: ClassVar[int]
    SELECTOR_FIELD_NUMBER: ClassVar[int]
    allow_without_credential: bool
    oauth: OAuthRequirements
    requirements: _containers.RepeatedCompositeFieldContainer[AuthRequirement]
    selector: str
    def __init__(self, selector: Optional[str] = ..., oauth: Optional[Union[OAuthRequirements, Mapping]] = ..., allow_without_credential: bool = ..., requirements: Optional[Iterable[Union[AuthRequirement, Mapping]]] = ...) -> None: ...

class JwtLocation(_message.Message):
    __slots__ = ["cookie", "header", "query", "value_prefix"]
    COOKIE_FIELD_NUMBER: ClassVar[int]
    HEADER_FIELD_NUMBER: ClassVar[int]
    QUERY_FIELD_NUMBER: ClassVar[int]
    VALUE_PREFIX_FIELD_NUMBER: ClassVar[int]
    cookie: str
    header: str
    query: str
    value_prefix: str
    def __init__(self, header: Optional[str] = ..., query: Optional[str] = ..., cookie: Optional[str] = ..., value_prefix: Optional[str] = ...) -> None: ...

class OAuthRequirements(_message.Message):
    __slots__ = ["canonical_scopes"]
    CANONICAL_SCOPES_FIELD_NUMBER: ClassVar[int]
    canonical_scopes: str
    def __init__(self, canonical_scopes: Optional[str] = ...) -> None: ...
