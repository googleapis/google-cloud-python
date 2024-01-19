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
from typing import Literal, Mapping, NamedTuple, Tuple


class JoinSide(enum.Enum):
    LEFT = 0
    RIGHT = 1


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
class JoinDefinition:
    conditions: Tuple[JoinCondition, ...]
    mappings: Tuple[JoinColumnMapping, ...]
    type: JoinType

    def get_left_mapping(self) -> Mapping[str, str]:
        return {
            i.source_id: i.destination_id
            for i in self.mappings
            if i.source_table == JoinSide.LEFT
        }

    def get_right_mapping(self) -> Mapping[str, str]:
        return {
            i.source_id: i.destination_id
            for i in self.mappings
            if i.source_table == JoinSide.RIGHT
        }
