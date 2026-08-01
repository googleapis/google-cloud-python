from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

ANDROID: OsType
BASIC: DeviceManagementLevel
COMPLETE: DeviceManagementLevel
DESCRIPTOR: _descriptor.FileDescriptor
DESKTOP_CHROME_OS: OsType
DESKTOP_LINUX: OsType
DESKTOP_MAC: OsType
DESKTOP_WINDOWS: OsType
ENCRYPTED: DeviceEncryptionStatus
ENCRYPTION_UNSPECIFIED: DeviceEncryptionStatus
ENCRYPTION_UNSUPPORTED: DeviceEncryptionStatus
IOS: OsType
MANAGEMENT_UNSPECIFIED: DeviceManagementLevel
NONE: DeviceManagementLevel
OS_UNSPECIFIED: OsType
UNENCRYPTED: DeviceEncryptionStatus

class DeviceEncryptionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class OsType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DeviceManagementLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
