from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class DeviceEncryptionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENCRYPTION_UNSPECIFIED: _ClassVar[DeviceEncryptionStatus]
    ENCRYPTION_UNSUPPORTED: _ClassVar[DeviceEncryptionStatus]
    UNENCRYPTED: _ClassVar[DeviceEncryptionStatus]
    ENCRYPTED: _ClassVar[DeviceEncryptionStatus]

class OsType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OS_UNSPECIFIED: _ClassVar[OsType]
    DESKTOP_MAC: _ClassVar[OsType]
    DESKTOP_WINDOWS: _ClassVar[OsType]
    DESKTOP_LINUX: _ClassVar[OsType]
    DESKTOP_CHROME_OS: _ClassVar[OsType]
    ANDROID: _ClassVar[OsType]
    IOS: _ClassVar[OsType]

class DeviceManagementLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MANAGEMENT_UNSPECIFIED: _ClassVar[DeviceManagementLevel]
    NONE: _ClassVar[DeviceManagementLevel]
    BASIC: _ClassVar[DeviceManagementLevel]
    COMPLETE: _ClassVar[DeviceManagementLevel]

ENCRYPTION_UNSPECIFIED: DeviceEncryptionStatus
ENCRYPTION_UNSUPPORTED: DeviceEncryptionStatus
UNENCRYPTED: DeviceEncryptionStatus
ENCRYPTED: DeviceEncryptionStatus
OS_UNSPECIFIED: OsType
DESKTOP_MAC: OsType
DESKTOP_WINDOWS: OsType
DESKTOP_LINUX: OsType
DESKTOP_CHROME_OS: OsType
ANDROID: OsType
IOS: OsType
MANAGEMENT_UNSPECIFIED: DeviceManagementLevel
NONE: DeviceManagementLevel
BASIC: DeviceManagementLevel
COMPLETE: DeviceManagementLevel
