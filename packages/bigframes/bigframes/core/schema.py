# Copyright 2024 Google LLC
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

from dataclasses import dataclass
import functools
import typing

import bigframes.core.guid
import bigframes.dtypes

ColumnIdentifierType = str


@dataclass(frozen=True)
class SchemaItem:
    column: ColumnIdentifierType
    dtype: bigframes.dtypes.Dtype


@dataclass(frozen=True)
class ArraySchema:
    items: typing.Tuple[SchemaItem, ...]

    @property
    def names(self) -> typing.Tuple[str, ...]:
        return tuple(item.column for item in self.items)

    @property
    def dtypes(self) -> typing.Tuple[bigframes.dtypes.Dtype, ...]:
        return tuple(item.dtype for item in self.items)

    @functools.cached_property
    def _mapping(self) -> typing.Dict[ColumnIdentifierType, bigframes.dtypes.Dtype]:
        return {item.column: item.dtype for item in self.items}

    def drop(self, columns: typing.Iterable[str]) -> ArraySchema:
        return ArraySchema(
            tuple(item for item in self.items if item.column not in columns)
        )

    def append(self, item: SchemaItem):
        return ArraySchema(tuple([*self.items, item]))

    def prepend(self, item: SchemaItem):
        return ArraySchema(tuple([item, *self.items]))

    def update_dtype(
        self, id: ColumnIdentifierType, dtype: bigframes.dtypes.Dtype
    ) -> ArraySchema:
        return ArraySchema(
            tuple(
                SchemaItem(id, dtype) if item.column == id else item
                for item in self.items
            )
        )

    def get_type(self, id: ColumnIdentifierType):
        return self._mapping[id]
