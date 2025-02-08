from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class CalendarPeriod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CALENDAR_PERIOD_UNSPECIFIED: _ClassVar[CalendarPeriod]
    DAY: _ClassVar[CalendarPeriod]
    WEEK: _ClassVar[CalendarPeriod]
    FORTNIGHT: _ClassVar[CalendarPeriod]
    MONTH: _ClassVar[CalendarPeriod]
    QUARTER: _ClassVar[CalendarPeriod]
    HALF: _ClassVar[CalendarPeriod]
    YEAR: _ClassVar[CalendarPeriod]
CALENDAR_PERIOD_UNSPECIFIED: CalendarPeriod
DAY: CalendarPeriod
WEEK: CalendarPeriod
FORTNIGHT: CalendarPeriod
MONTH: CalendarPeriod
QUARTER: CalendarPeriod
HALF: CalendarPeriod
YEAR: CalendarPeriod
