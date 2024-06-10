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

import pytest

import bigframes.core.compile.googlesql as sql


@pytest.mark.parametrize(
    ("table_id", "dataset_id", "project_id", "expected"),
    [
        pytest.param("a", None, None, "`a`"),
        pytest.param("a", "b", None, "`b`.`a`"),
        pytest.param("a", "b", "c", "`c`.`b`.`a`"),
        pytest.param("a", None, "c", None, marks=pytest.mark.xfail(raises=ValueError)),
    ],
)
def test_table_expression(table_id, dataset_id, project_id, expected):
    expr = sql.TableExpression(
        table_id=table_id, dataset_id=dataset_id, project_id=project_id
    )
    assert expr.sql() == expected


@pytest.mark.parametrize(
    ("table_name", "alias", "expected"),
    [
        pytest.param(None, None, None, marks=pytest.mark.xfail(raises=ValueError)),
        pytest.param("a", None, "`a`"),
        pytest.param("a", "aa", "`a` AS `aa`"),
    ],
)
def test_from_item_w_table_name(table_name, alias, expected):
    expr = sql.FromItem(
        table_name=None
        if table_name is None
        else sql.TableExpression(table_id=table_name),
        as_alias=None
        if alias is None
        else sql.AsAlias(sql.AliasExpression(alias=alias)),
    )
    assert expr.sql() == expected


def test_from_item_w_query_expr():
    from_clause = sql.FromClause(
        sql.FromItem(table_name=sql.TableExpression(table_id="table_a"))
    )
    select = sql.Select(
        select_list=[sql.SelectAll(sql.StarExpression())],
        from_clause_list=[from_clause],
    )
    query_expr = sql.QueryExpr(select=select)
    expected = "SELECT\n*\nFROM\n`table_a`"

    # A QueryExpr object
    expr = sql.FromItem(query_expr=query_expr)
    assert expr.sql() == f"({expected})"

    # A str object
    expr = sql.FromItem(query_expr=expected)
    assert expr.sql() == f"({expected})"


def test_from_item_w_cte():
    expr = sql.FromItem(cte_name=sql.CTEExpression("test"))
    assert expr.sql() == "`test`"


@pytest.mark.parametrize(
    ("col_name", "alias", "expected"),
    [
        pytest.param("a", None, "`a`"),
        pytest.param("a", "aa", "`a` AS `aa`"),
    ],
)
def test_select_expression(col_name, alias, expected):
    expr = sql.SelectExpression(
        expression=sql.ColumnExpression(col_name),
        alias=None if alias is None else sql.AliasExpression(alias=alias),
    )
    assert expr.sql() == expected


def test_select():
    select_1 = sql.SelectExpression(expression=sql.ColumnExpression("a"))
    select_2 = sql.SelectExpression(
        expression=sql.ColumnExpression("b"), alias=sql.AliasExpression(alias="bb")
    )
    from_1 = sql.FromItem(table_name=sql.TableExpression(table_id="table_a"))
    from_2 = sql.FromItem(
        query_expr="SELECT * FROM project.table_b",
        as_alias=sql.AsAlias(sql.AliasExpression(alias="table_b")),
    )
    expr = sql.Select(
        select_list=[select_1, select_2],
        from_clause_list=[sql.FromClause(from_1), sql.FromClause(from_2)],
    )
    expected = "SELECT\n`a`,\n`b` AS `bb`\nFROM\n`table_a`,\n(SELECT * FROM project.table_b) AS `table_b`"

    assert expr.sql() == expected


def test_query_expr_w_cte():
    # Test a simple SELECT query.
    from_clause1 = sql.FromClause(
        sql.FromItem(table_name=sql.TableExpression(table_id="table_a"))
    )
    select1 = sql.Select(
        select_list=[sql.SelectAll(sql.StarExpression())],
        from_clause_list=[from_clause1],
    )
    query1 = sql.QueryExpr(select=select1)
    query1_sql = "SELECT\n*\nFROM\n`table_a`"
    assert query1.sql() == query1_sql

    # Test a query with CTE statements.
    cte1 = sql.NonRecursiveCTE(cte_name=sql.CTEExpression("a"), query_expr=query1)
    cte2 = sql.NonRecursiveCTE(cte_name=sql.CTEExpression("b"), query_expr=query1)

    cte1_sql = f"`a` AS (\n{query1_sql}\n)"
    cte2_sql = f"`b` AS (\n{query1_sql}\n)"
    assert cte1.sql() == cte1_sql
    assert cte2.sql() == cte2_sql

    with_cte_list = [cte1, cte2]
    select2 = sql.Select(
        select_list=[
            sql.SelectExpression(
                sql.ColumnExpression(parent=cte1.cte_name, name="column_x")
            ),
            sql.SelectAll(sql.StarExpression(parent=cte2.cte_name)),
        ],
        from_clause_list=[
            sql.FromClause(sql.FromItem(cte_name=cte1.cte_name)),
            sql.FromClause(sql.FromItem(cte_name=cte2.cte_name)),
        ],
    )
    select2_sql = "SELECT\n`a`.`column_x`,\n`b`.*\nFROM\n`a`,\n`b`"
    assert select2.sql() == select2_sql

    query2 = sql.QueryExpr(select=select2, with_cte_list=with_cte_list)
    query2_sql = f"WITH {cte1_sql},\n{cte2_sql}\n{select2_sql}"
    assert query2.sql() == query2_sql
