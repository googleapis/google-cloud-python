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

import math
import typing

import ibis

import bigframes.core.compile.compiled as compiled
import bigframes.core.expression as ex
from bigframes.core.ordering import (
    ascending_over,
    reencode_order_string,
    StringEncoding,
    TotalOrdering,
)

ORDER_ID_COLUMN = "bigframes_ordering_id"


def concat_unordered(
    items: typing.Sequence[compiled.UnorderedIR],
    output_ids: typing.Sequence[str],
) -> compiled.UnorderedIR:
    """Append together multiple ArrayValue objects."""
    if len(items) == 1:
        return items[0]
    tables = []
    for expr in items:
        table = expr._to_ibis_expr()
        table = table.select(
            [table[col].name(id) for id, col in zip(output_ids, table.columns)]
        )
        tables.append(table)
    combined_table = ibis.union(*tables)
    return compiled.UnorderedIR(
        combined_table,
        columns=[combined_table[col] for col in combined_table.columns],
    )


def concat_ordered(
    items: typing.Sequence[compiled.OrderedIR],
    output_ids: typing.Sequence[str],
) -> compiled.OrderedIR:
    """Append together multiple ArrayValue objects."""
    if len(items) == 1:
        return items[0]

    tables = []
    prefix_base = 10
    prefix_size = math.ceil(math.log(len(items), prefix_base))
    # Must normalize all ids to the same encoding size
    max_encoding_size = max(
        *[expression._ordering.string_encoding.length for expression in items],
    )
    for i, expr in enumerate(items):
        ordering_prefix = str(i).zfill(prefix_size)
        renames = {
            old_id: new_id for old_id, new_id in zip(expr.column_ids, output_ids)
        }
        table = expr._to_ibis_expr(
            ordering_mode="string_encoded",
            order_col_name=ORDER_ID_COLUMN,
        )
        table = table.select(
            [
                table[col].name(renames[col])
                if col != ORDER_ID_COLUMN
                else (
                    ordering_prefix
                    + reencode_order_string(table[ORDER_ID_COLUMN], max_encoding_size)
                ).name(ORDER_ID_COLUMN)
                for col in table.columns
            ]
        )
        tables.append(table)
    combined_table = ibis.union(*tables)
    ordering = TotalOrdering(
        ordering_value_columns=tuple([ascending_over(ORDER_ID_COLUMN)]),
        total_ordering_columns=frozenset([ex.deref(ORDER_ID_COLUMN)]),
        string_encoding=StringEncoding(True, prefix_size + max_encoding_size),
    )
    return compiled.OrderedIR(
        combined_table,
        columns=[
            combined_table[col]
            for col in combined_table.columns
            if col != ORDER_ID_COLUMN
        ],
        hidden_ordering_columns=[combined_table[ORDER_ID_COLUMN]],
        ordering=ordering,
    )
