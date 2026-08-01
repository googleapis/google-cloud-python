from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthProvider(_message.Message):
    __slots__ = ["audiences", "authorization_url", "id", "issuer", "jwks_uri", "jwt_locations"]
    AUDIENCES_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_URL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    JWKS_URI_FIELD_NUMBER: _ClassVar[int]
    JWT_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    audiences: str
    authorization_url: str
    id: str
    issuer: str
    jwks_uri: str
    jwt_locations: _containers.RepeatedCompositeFieldContainer[JwtLocation]
    def __init__(self, id: _Optional[str] = ..., issuer: _Optional[str] = ..., jwks_uri: _Optional[str] = ..., audiences: _Optional[str] = ..., authorization_url: _Optional[str] = ..., jwt_locations: _Optional[_Iterable[_Union[JwtLocation, _Mapping]]] = ...) -> None: ...

class AuthRequirement(_message.Message):
    __slots__ = ["audiences", "provider_id"]
    AUDIENCES_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ID_FIELD_NUMBER: _ClassVar[int]
    audiences: str
    provider_id: str
    def __init__(self, provider_id: _Optional[str] = ..., audiences: _Optional[str] = ...) -> None: ...

class Authentication(_message.Message):
    __slots__ = ["providers", "rules"]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    providers: _containers.RepeatedCompositeFieldContainer[AuthProvider]
    rules: _containers.RepeatedCompositeFieldContainer[AuthenticationRule]
    def __init__(self, rules: _Optional[_Iterable[_Union[AuthenticationRule, _Mapping]]] = ..., providers: _Optional[_Iterable[_Union[AuthProvider, _Mapping]]] = ...) -> None: ...

class AuthenticationRule(_message.Message):
    __slots__ = ["allow_without_credential", "oauth", "requirements", "selector"]
    ALLOW_WITHOUT_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    OAUTH_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    allow_without_credential: bool
    oauth: OAuthRequirements
    requirements: _containers.RepeatedCompositeFieldContainer[AuthRequirement]
    selector: str
    def __init__(self, selector: _Optional[str] = ..., oauth: _Optional[_Union[OAuthRequirements, _Mapping]] = ..., allow_without_credential: bool = ..., requirements: _Optional[_Iterable[_Union[AuthRequirement, _Mapping]]] = ...) -> None: ...

class JwtLocation(_message.Message):
    __slots__ = ["cookie", "header", "query", "value_prefix"]
    COOKIE_FIELD_NUMBER: _ClassVar[int]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    VALUE_PREFIX_FIELD_NUMBER: _ClassVar[int]
    cookie: str
    header: str
    query: str
    value_prefix: str
    def __init__(self, header: _Optional[str] = ..., query: _Optional[str] = ..., cookie: _Optional[str] = ..., value_prefix: _Optional[str] = ...) -> None: ...

class OAuthRequirements(_message.Message):
    __slots__ = ["canonical_scopes"]
    CANONICAL_SCOPES_FIELD_NUMBER: _ClassVar[int]
    canonical_scopes: str
    def __init__(self, canonical_scopes: _Optional[str] = ...) -> None: ...
