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

from unittest import mock

import ibis
from ibis.expr.types import Column, Table

from bigframes import core


def test_constructor_from_ibis_table_adds_all_columns(
    session, scalars_ibis_table: Table
):
    actual = core.ArrayValue(session=session, table=scalars_ibis_table)
    assert actual._table is scalars_ibis_table
    assert len(actual._columns) == len(scalars_ibis_table.columns)


def test_builder_doesnt_change_original(session):
    mock_table = mock.create_autospec(Table)
    mock_column = mock.create_autospec(Column)
    original = core.ArrayValue(session=session, table=mock_table, columns=[mock_column])
    assert original._table is mock_table
    assert len(original._columns) == 1
    assert original._columns[0] is mock_column

    # Create a new expression from a builder.
    builder = original.builder()
    new_table = mock.create_autospec(Table)
    assert new_table is not mock_table
    builder.table = new_table
    new_column = mock.create_autospec(Column)
    assert new_column is not mock_column
    builder.columns.append(new_column)
    actual = builder.build()

    # Expected values are present.
    assert actual._table is new_table
    assert len(actual._columns) == 2
    assert actual._columns[0] is mock_column
    assert actual._columns[1] is new_column
    # Don't modify the original.
    assert original._table is mock_table
    assert len(original._columns) == 1
    assert original._columns[0] is mock_column


def test_projection_doesnt_change_original(session):
    mock_table = mock.create_autospec(Table)
    mock_column = mock.create_autospec(Column)
    original = core.ArrayValue(session=session, table=mock_table, columns=[mock_column])
    assert original._table is mock_table
    assert len(original._columns) == 1
    assert original._columns[0] is mock_column

    # Create a new expression from a projection.
    new_column_1 = mock.create_autospec(Column)
    new_column_2 = mock.create_autospec(Column)
    assert new_column_1 is not mock_column
    assert new_column_2 is not mock_column
    actual = original.projection([new_column_1, mock_column, new_column_2])

    # Expected values are present.
    assert actual._table is mock_table
    assert len(actual._columns) == 3
    assert actual._columns[0] is new_column_1
    assert actual._columns[1] is mock_column
    assert actual._columns[2] is new_column_2
    # Don't modify the original.
    assert original._table is mock_table
    assert len(original._columns) == 1
    assert original._columns[0] is mock_column


def test_to_ibis_expr_with_projection(session, scalars_ibis_table: Table):
    expr = core.ArrayValue(session=session, table=scalars_ibis_table).projection(
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
