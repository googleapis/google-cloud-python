from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class LaunchStage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LAUNCH_STAGE_UNSPECIFIED: _ClassVar[LaunchStage]
    UNIMPLEMENTED: _ClassVar[LaunchStage]
    PRELAUNCH: _ClassVar[LaunchStage]
    EARLY_ACCESS: _ClassVar[LaunchStage]
    ALPHA: _ClassVar[LaunchStage]
    BETA: _ClassVar[LaunchStage]
    GA: _ClassVar[LaunchStage]
    DEPRECATED: _ClassVar[LaunchStage]
LAUNCH_STAGE_UNSPECIFIED: LaunchStage
UNIMPLEMENTED: LaunchStage
PRELAUNCH: LaunchStage
EARLY_ACCESS: LaunchStage
ALPHA: LaunchStage
BETA: LaunchStage
GA: LaunchStage
DEPRECATED: LaunchStage
