# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

APRIL: Month
AUGUST: Month
DECEMBER: Month
DESCRIPTOR: _descriptor.FileDescriptor
FEBRUARY: Month
JANUARY: Month
JULY: Month
JUNE: Month
MARCH: Month
MAY: Month
MONTH_UNSPECIFIED: Month
NOVEMBER: Month
OCTOBER: Month
SEPTEMBER: Month

class Month(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
