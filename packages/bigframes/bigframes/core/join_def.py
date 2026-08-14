# Copyright 2023 Google LLC
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
from __future__ import annotations

import dataclasses
import enum
from typing import Literal, NamedTuple


class JoinSide(enum.Enum):
    LEFT = 0
    RIGHT = 1

    def inverse(self) -> JoinSide:
        if self == JoinSide.LEFT:
            return JoinSide.RIGHT
        return JoinSide.LEFT


JoinType = Literal["inner", "outer", "left", "right", "cross"]


class JoinCondition(NamedTuple):
    left_id: str
    right_id: str


@dataclasses.dataclass(frozen=True)
class JoinColumnMapping:
    source_table: JoinSide
    source_id: str
    destination_id: str


@dataclasses.dataclass(frozen=True)
class CoalescedColumnMapping:
    """Special column mapping used only by implicit joiner only"""

    left_source_id: str
    right_source_id: str
    destination_id: str
