from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor
ERROR_CODE: OperationResponseMapping
ERROR_MESSAGE: OperationResponseMapping
NAME: OperationResponseMapping
OPERATION_FIELD_FIELD_NUMBER: _ClassVar[int]
OPERATION_POLLING_METHOD_FIELD_NUMBER: _ClassVar[int]
OPERATION_REQUEST_FIELD_FIELD_NUMBER: _ClassVar[int]
OPERATION_RESPONSE_FIELD_FIELD_NUMBER: _ClassVar[int]
OPERATION_SERVICE_FIELD_NUMBER: _ClassVar[int]
STATUS: OperationResponseMapping
UNDEFINED: OperationResponseMapping
operation_field: _descriptor.FieldDescriptor
operation_polling_method: _descriptor.FieldDescriptor
operation_request_field: _descriptor.FieldDescriptor
operation_response_field: _descriptor.FieldDescriptor
operation_service: _descriptor.FieldDescriptor

class OperationResponseMapping(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
