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
from typing import Dict, List, Sequence

import google.cloud.bigquery
import pyarrow

import bigframes.dtypes

ColumnIdentifierType = str


@dataclass(frozen=True)
class SchemaItem:
    column: ColumnIdentifierType
    dtype: bigframes.dtypes.Dtype


@dataclass(frozen=True)
class ArraySchema:
    items: Sequence[SchemaItem]

    def __iter__(self):
        yield from self.items

    @classmethod
    def from_bq_table(
        cls,
        table: google.cloud.bigquery.Table,
        column_type_overrides: typing.Optional[
            typing.Dict[str, bigframes.dtypes.Dtype]
        ] = None,
    ):
        return ArraySchema.from_bq_schema(
            table.schema, column_type_overrides=column_type_overrides
        )

    @classmethod
    def from_bq_schema(
        cls,
        schema: List[google.cloud.bigquery.SchemaField],
        column_type_overrides: typing.Optional[
            Dict[str, bigframes.dtypes.Dtype]
        ] = None,
    ):
        if column_type_overrides is None:
            column_type_overrides = {}
        items = tuple(
            SchemaItem(name, column_type_overrides.get(name, dtype))
            for name, dtype in bigframes.dtypes.bf_type_from_type_kind(schema).items()
        )
        return ArraySchema(items)

    @property
    def names(self) -> typing.Tuple[str, ...]:
        return tuple(item.column for item in self.items)

    @property
    def dtypes(self) -> typing.Tuple[bigframes.dtypes.Dtype, ...]:
        return tuple(item.dtype for item in self.items)

    @functools.cached_property
    def _mapping(self) -> typing.Dict[ColumnIdentifierType, bigframes.dtypes.Dtype]:
        return {item.column: item.dtype for item in self.items}

    def to_bigquery(
        self, overrides: dict[bigframes.dtypes.Dtype, str] = {}
    ) -> typing.Tuple[google.cloud.bigquery.SchemaField, ...]:
        return tuple(
            bigframes.dtypes.convert_to_schema_field(
                item.column, item.dtype, overrides=overrides
            )
            for item in self.items
        )

    def to_pyarrow(self) -> pyarrow.Schema:
        fields = []
        for item in self.items:
            pa_type = bigframes.dtypes.bigframes_dtype_to_arrow_dtype(item.dtype)
            fields.append(
                pyarrow.field(
                    item.column,
                    pa_type,
                    nullable=not pyarrow.types.is_list(pa_type),
                )
            )
        return pyarrow.schema(fields)

    def drop(self, columns: typing.Iterable[str]) -> ArraySchema:
        return ArraySchema(
            tuple(item for item in self.items if item.column not in columns)
        )

    def select(self, columns: typing.Iterable[str]) -> ArraySchema:
        return ArraySchema(
            tuple(SchemaItem(name, self.get_type(name)) for name in columns)
        )

    def rename(self, mapping: typing.Mapping[str, str]) -> ArraySchema:
        return ArraySchema(
            tuple(
                SchemaItem(mapping.get(item.column, item.column), item.dtype)
                for item in self.items
            )
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

    def __len__(self) -> int:
        return len(self.items)
