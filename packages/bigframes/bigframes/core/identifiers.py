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
import functools
import itertools
from typing import Generator

import bigframes.core.guid


def standard_id_strings(prefix: str = "col_") -> Generator[str, None, None]:
    i = 0
    while True:
        yield f"{prefix}{i}"
        i = i + 1


# Used for expression trees
@functools.total_ordering
@dataclasses.dataclass(frozen=True)
class ColumnId:
    """Local id without plan-wide id."""

    name: str

    @property
    def sql(self) -> str:
        """Returns the unescaped SQL name."""
        return self.name

    @property
    def local_normalized(self) -> ColumnId:
        """For use in compiler only. Normalizes to ColumnId referring to sql name."""
        return self  # == ColumnId(name=self.sql)

    def __lt__(self, other: ColumnId) -> bool:
        return self.sql < other.sql

    @classmethod
    def unique(cls) -> ColumnId:
        return ColumnId(name=bigframes.core.guid.generate_guid())


@dataclasses.dataclass(frozen=True)
class SerialColumnId(ColumnId):
    """Id that is assigned a unique serial within the tree."""

    name: str
    id: int

    @property
    def sql(self) -> str:
        """Returns the unescaped SQL name."""
        return f"{self.name}_{self.id}"

    @property
    def local_normalized(self) -> ColumnId:
        """For use in compiler only. Normalizes to ColumnId referring to sql name."""
        return ColumnId(name=self.sql)


# TODO: Create serial ids locally, so can preserve name info
def anonymous_serial_ids() -> Generator[ColumnId, None, None]:
    for i in itertools.count():
        yield SerialColumnId("uid", i)
