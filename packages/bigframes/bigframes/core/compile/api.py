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

from typing import Mapping, Sequence, Tuple, TYPE_CHECKING

import google.cloud.bigquery as bigquery

import bigframes.core.compile.compiler as compiler
import bigframes.core.rewrite as rewrites

if TYPE_CHECKING:
    import bigframes.core.nodes
    import bigframes.core.ordering
    import bigframes.core.schema

_STRICT_COMPILER = compiler.Compiler(strict=True)


class SQLCompiler:
    def __init__(self, strict: bool = True):
        self._compiler = compiler.Compiler(strict=strict)

    def compile_peek(self, node: bigframes.core.nodes.BigFrameNode, n_rows: int) -> str:
        """Compile node into sql that selects N arbitrary rows, may not execute deterministically."""
        return self._compiler.compile_unordered_ir(node).peek_sql(n_rows)

    def compile_unordered(
        self,
        node: bigframes.core.nodes.BigFrameNode,
        *,
        col_id_overrides: Mapping[str, str] = {},
    ) -> str:
        """Compile node into sql where rows are unsorted, and no ordering information is preserved."""
        # TODO: Enable limit pullup, but only if not being used to write to clustered table.
        return self._compiler.compile_unordered_ir(node).to_sql(
            col_id_overrides=col_id_overrides
        )

    def compile_ordered(
        self,
        node: bigframes.core.nodes.BigFrameNode,
        *,
        col_id_overrides: Mapping[str, str] = {},
    ) -> str:
        """Compile node into sql where rows are sorted with ORDER BY."""
        # If we are ordering the query anyways, compiling the slice as a limit is probably a good idea.
        new_node, limit = rewrites.pullup_limit_from_slice(node)
        return self._compiler.compile_ordered_ir(new_node).to_sql(
            col_id_overrides=col_id_overrides, ordered=True, limit=limit
        )

    def compile_raw(
        self,
        node: bigframes.core.nodes.BigFrameNode,
    ) -> Tuple[
        str, Sequence[bigquery.SchemaField], bigframes.core.ordering.RowOrdering
    ]:
        """Compile node into sql that exposes all columns, including hidden ordering-only columns."""
        ir = self._compiler.compile_ordered_ir(node)
        sql, schema = ir.raw_sql_and_schema()
        return sql, schema, ir._ordering


def test_only_try_evaluate(node: bigframes.core.nodes.BigFrameNode):
    """Use only for unit testing paths - not fully featured. Will throw exception if fails."""
    ibis = _STRICT_COMPILER.compile_ordered_ir(node)._to_ibis_expr(
        ordering_mode="unordered"
    )
    return ibis.pandas.connect({}).execute(ibis)


def test_only_ibis_inferred_schema(node: bigframes.core.nodes.BigFrameNode):
    """Use only for testing paths to ensure ibis inferred schema does not diverge from bigframes inferred schema."""
    import bigframes.core.schema

    compiled = _STRICT_COMPILER.compile_unordered_ir(node)
    items = tuple(
        bigframes.core.schema.SchemaItem(id, compiled.get_column_type(id))
        for id in compiled.column_ids
    )
    return bigframes.core.schema.ArraySchema(items)
