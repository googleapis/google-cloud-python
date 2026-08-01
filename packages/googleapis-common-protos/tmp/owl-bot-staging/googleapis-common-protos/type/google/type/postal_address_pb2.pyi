from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PostalAddress(_message.Message):
    __slots__ = ["address_lines", "administrative_area", "language_code", "locality", "organization", "postal_code", "recipients", "region_code", "revision", "sorting_code", "sublocality"]
    ADDRESS_LINES_FIELD_NUMBER: _ClassVar[int]
    ADMINISTRATIVE_AREA_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    LOCALITY_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTS_FIELD_NUMBER: _ClassVar[int]
    REGION_CODE_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    SORTING_CODE_FIELD_NUMBER: _ClassVar[int]
    SUBLOCALITY_FIELD_NUMBER: _ClassVar[int]
    address_lines: _containers.RepeatedScalarFieldContainer[str]
    administrative_area: str
    language_code: str
    locality: str
    organization: str
    postal_code: str
    recipients: _containers.RepeatedScalarFieldContainer[str]
    region_code: str
    revision: int
    sorting_code: str
    sublocality: str
    def __init__(self, revision: _Optional[int] = ..., region_code: _Optional[str] = ..., language_code: _Optional[str] = ..., postal_code: _Optional[str] = ..., sorting_code: _Optional[str] = ..., administrative_area: _Optional[str] = ..., locality: _Optional[str] = ..., sublocality: _Optional[str] = ..., address_lines: _Optional[_Iterable[str]] = ..., recipients: _Optional[_Iterable[str]] = ..., organization: _Optional[str] = ...) -> None: ...
