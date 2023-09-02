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
import pandas

import bigframes.core as core

from . import resources


def test_arrayvalue_constructor_from_ibis_table_adds_all_columns():
    session = resources.create_pandas_session(
        {
            "test_table": pandas.DataFrame(
                {
                    "col1": [1, 2, 3],
                    "not_included": [True, False, True],
                    "col2": ["a", "b", "c"],
                    "col3": [0.1, 0.2, 0.3],
                }
            )
        }
    )
    ibis_table = session.ibis_client.table("test_table")
    columns = (ibis_table["col1"], ibis_table["col2"], ibis_table["col3"])
    ordering = core.ExpressionOrdering(
        [core.OrderingColumnReference("col1")],
        total_ordering_columns=frozenset(["col1"]),
    )
    actual = core.ArrayValue(
        session=session, table=ibis_table, columns=columns, ordering=ordering
    )
    assert actual.table is ibis_table
    assert len(actual.columns) == 3


def test_arrayvalue_to_ibis_expr_with_projection():
    value = resources.create_arrayvalue(
        pandas.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": ["a", "b", "c"],
                "col3": [0.1, 0.2, 0.3],
            }
        ),
        total_ordering_columns=["col1"],
    )
    expr = value.projection(
        [
            (value.table["col1"] + ibis.literal(-1)).name("int64_col"),
            ibis.literal(123456789).name("literals"),
            value.table["col2"].name("string_col"),
        ]
    )
    actual = expr.to_ibis_expr()
    assert len(actual.columns) == 3
    assert actual.columns[0] == "int64_col"
    assert actual.columns[1] == "literals"
    assert actual.columns[2] == "string_col"
