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

import ibis
from ibis.expr.types import Table

from bigframes import core

ORDERING = core.ExpressionOrdering(
    [
        core.OrderingColumnReference("int64_col"),
        core.OrderingColumnReference("string_col"),
    ],
    total_ordering_columns=frozenset(["int64_col", "string_col"]),
)


def test_constructor_from_ibis_table_adds_all_columns(
    session, scalars_ibis_table: Table
):
    columns = tuple(scalars_ibis_table[key] for key in scalars_ibis_table.columns)
    actual = core.ArrayValue(
        session=session, table=scalars_ibis_table, columns=columns, ordering=ORDERING
    )
    assert actual._table is scalars_ibis_table
    assert len(actual._columns) == len(scalars_ibis_table.columns)


def test_to_ibis_expr_with_projection(session, scalars_ibis_table: Table):
    columns = tuple(scalars_ibis_table[key] for key in scalars_ibis_table.columns)
    expr = core.ArrayValue(
        session=session, table=scalars_ibis_table, columns=columns, ordering=ORDERING
    ).projection(
        [
            scalars_ibis_table["int64_col"],
            ibis.literal(123456789).name("literals"),
            scalars_ibis_table["string_col"],
        ]
    )
    actual = expr.to_ibis_expr()
    assert len(actual.columns) == 3
    assert actual.columns[0] == "int64_col"
    assert actual.columns[1] == "literals"
    assert actual.columns[2] == "string_col"
