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

import pytest

from bigframes.core import array_value, expression, identifiers, nodes
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


def test_engines_select_identity(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    selection = tuple(
        nodes.AliasedRef(expression.deref(col), identifiers.ColumnId(col))
        for col in scalars_array_value.column_ids
    )
    node = nodes.SelectionNode(scalars_array_value.node, selection)
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)


def test_engines_select_rename(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    selection = tuple(
        nodes.AliasedRef(expression.deref(col), identifiers.ColumnId(f"renamed_{col}"))
        for col in scalars_array_value.column_ids
    )
    node = nodes.SelectionNode(scalars_array_value.node, selection)
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)


def test_engines_select_reorder_rename_drop(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    selection = tuple(
        nodes.AliasedRef(expression.deref(col), identifiers.ColumnId(f"renamed_{col}"))
        for col in scalars_array_value.column_ids[::-2]
    )
    node = nodes.SelectionNode(scalars_array_value.node, selection)
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)
