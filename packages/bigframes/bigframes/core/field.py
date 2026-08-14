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

from __future__ import annotations

import dataclasses

from bigframes import dtypes
from bigframes.core import identifiers


@dataclasses.dataclass(frozen=True)
class Field:
    id: identifiers.ColumnId
    dtype: dtypes.Dtype
    # Best effort, nullable=True if not certain
    nullable: bool = True

    def with_nullable(self) -> Field:
        return Field(self.id, self.dtype, nullable=True)

    def with_nonnull(self) -> Field:
        return Field(self.id, self.dtype, nullable=False)

    def with_id(self, id: identifiers.ColumnId) -> Field:
        return Field(id, self.dtype, nullable=self.nullable)
