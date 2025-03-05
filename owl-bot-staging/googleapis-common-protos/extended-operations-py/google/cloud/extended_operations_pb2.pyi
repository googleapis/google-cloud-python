from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class OperationResponseMapping(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNDEFINED: _ClassVar[OperationResponseMapping]
    NAME: _ClassVar[OperationResponseMapping]
    STATUS: _ClassVar[OperationResponseMapping]
    ERROR_CODE: _ClassVar[OperationResponseMapping]
    ERROR_MESSAGE: _ClassVar[OperationResponseMapping]
UNDEFINED: OperationResponseMapping
NAME: OperationResponseMapping
STATUS: OperationResponseMapping
ERROR_CODE: OperationResponseMapping
ERROR_MESSAGE: OperationResponseMapping
OPERATION_FIELD_FIELD_NUMBER: _ClassVar[int]
operation_field: _descriptor.FieldDescriptor
OPERATION_REQUEST_FIELD_FIELD_NUMBER: _ClassVar[int]
operation_request_field: _descriptor.FieldDescriptor
OPERATION_RESPONSE_FIELD_FIELD_NUMBER: _ClassVar[int]
operation_response_field: _descriptor.FieldDescriptor
OPERATION_SERVICE_FIELD_NUMBER: _ClassVar[int]
operation_service: _descriptor.FieldDescriptor
OPERATION_POLLING_METHOD_FIELD_NUMBER: _ClassVar[int]
operation_polling_method: _descriptor.FieldDescriptor
