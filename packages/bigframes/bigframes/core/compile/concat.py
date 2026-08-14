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

import typing

import bigframes_vendored.ibis.expr.api as ibis_api

import bigframes.core.compile.compiled as compiled


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
    combined_table = ibis_api.union(*tables)
    return compiled.UnorderedIR(
        combined_table,
        columns=[combined_table[col] for col in combined_table.columns],
    )
