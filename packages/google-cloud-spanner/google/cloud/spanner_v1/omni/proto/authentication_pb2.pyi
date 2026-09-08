from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class PasswordAuthenticationProtocol(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PASSWORD_AUTHENTICATION_PROTOCOL_UNSPECIFIED: _ClassVar[
        PasswordAuthenticationProtocol
    ]
    PASSWORD_AUTHENTICATION_PROTOCOL_OPAQUE: _ClassVar[PasswordAuthenticationProtocol]

PASSWORD_AUTHENTICATION_PROTOCOL_UNSPECIFIED: PasswordAuthenticationProtocol
PASSWORD_AUTHENTICATION_PROTOCOL_OPAQUE: PasswordAuthenticationProtocol

class HashParameters(_message.Message):
    __slots__ = ("argon2_id_parameters",)
    class Argon2IdParameters(_message.Message):
        __slots__ = ("iteration_count", "memory_usage", "parallelism", "hash_size")
        ITERATION_COUNT_FIELD_NUMBER: _ClassVar[int]
        MEMORY_USAGE_FIELD_NUMBER: _ClassVar[int]
        PARALLELISM_FIELD_NUMBER: _ClassVar[int]
        HASH_SIZE_FIELD_NUMBER: _ClassVar[int]
        iteration_count: int
        memory_usage: int
        parallelism: int
        hash_size: int
        def __init__(
            self,
            iteration_count: _Optional[int] = ...,
            memory_usage: _Optional[int] = ...,
            parallelism: _Optional[int] = ...,
            hash_size: _Optional[int] = ...,
        ) -> None: ...

    ARGON2_ID_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    argon2_id_parameters: HashParameters.Argon2IdParameters
    def __init__(
        self,
        argon2_id_parameters: _Optional[
            _Union[HashParameters.Argon2IdParameters, _Mapping]
        ] = ...,
    ) -> None: ...

class PasswordAuthenticationHandshakeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PasswordAuthenticationHandshakeResponse(_message.Message):
    __slots__ = ("password_authentication_protocol", "hash_parameters")
    PASSWORD_AUTHENTICATION_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    HASH_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    password_authentication_protocol: PasswordAuthenticationProtocol
    hash_parameters: HashParameters
    def __init__(
        self,
        password_authentication_protocol: _Optional[
            _Union[PasswordAuthenticationProtocol, str]
        ] = ...,
        hash_parameters: _Optional[_Union[HashParameters, _Mapping]] = ...,
    ) -> None: ...
