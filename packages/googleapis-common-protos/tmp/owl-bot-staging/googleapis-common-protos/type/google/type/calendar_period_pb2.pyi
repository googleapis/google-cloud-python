from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

CALENDAR_PERIOD_UNSPECIFIED: CalendarPeriod
DAY: CalendarPeriod
DESCRIPTOR: _descriptor.FileDescriptor
FORTNIGHT: CalendarPeriod
HALF: CalendarPeriod
MONTH: CalendarPeriod
QUARTER: CalendarPeriod
WEEK: CalendarPeriod
YEAR: CalendarPeriod

class CalendarPeriod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
