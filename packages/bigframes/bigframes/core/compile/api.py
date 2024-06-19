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

from typing import Mapping, Tuple, TYPE_CHECKING

import bigframes.core.compile.compiler as compiler

if TYPE_CHECKING:
    import bigframes.core.nodes
    import bigframes.core.ordering
    import bigframes.core.schema


def compile_peek(node: bigframes.core.nodes.BigFrameNode, n_rows: int) -> str:
    """Compile node into sql that selects N arbitrary rows, may not execute deterministically."""
    return compiler.compile_unordered_ir(node).peek_sql(n_rows)


def compile_unordered(
    node: bigframes.core.nodes.BigFrameNode, *, col_id_overrides: Mapping[str, str] = {}
) -> str:
    """Compile node into sql where rows are unsorted, and no ordering information is preserved."""
    return compiler.compile_unordered_ir(node).to_sql(col_id_overrides=col_id_overrides)


def compile_ordered(
    node: bigframes.core.nodes.BigFrameNode, *, col_id_overrides: Mapping[str, str] = {}
) -> str:
    """Compile node into sql where rows are sorted with ORDER BY."""
    return compiler.compile_ordered_ir(node).to_sql(
        col_id_overrides=col_id_overrides, ordered=True
    )


def compile_raw(
    node: bigframes.core.nodes.BigFrameNode,
) -> Tuple[str, bigframes.core.ordering.ExpressionOrdering]:
    """Compile node into sql that exposes all columns, including hidden ordering-only columns."""
    ir = compiler.compile_ordered_ir(node)
    sql = ir.raw_sql()
    ordering_info = ir._ordering
    return sql, ordering_info


def test_only_try_evaluate(node: bigframes.core.nodes.BigFrameNode):
    """Use only for unit testing paths - not fully featured. Will throw exception if fails."""
    ibis = compiler.compile_ordered_ir(node)._to_ibis_expr(ordering_mode="unordered")
    return ibis.pandas.connect({}).execute(ibis)


def test_only_ibis_inferred_schema(node: bigframes.core.nodes.BigFrameNode):
    """Use only for testing paths to ensure ibis inferred schema does not diverge from bigframes inferred schema."""
    import bigframes.core.schema

    compiled = compiler.compile_unordered_ir(node)
    items = tuple(
        bigframes.core.schema.SchemaItem(id, compiled.get_column_type(id))
        for id in compiled.column_ids
    )
    return bigframes.core.schema.ArraySchema(items)
