# Copyright (c) 2021 The sqlalchemy-bigquery Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pytest
import sqlalchemy.exc

from conftest import setup_table
from conftest import sqlalchemy_1_4_or_higher


def test_constraints_are_ignored(faux_conn, metadata):
    sqlalchemy.Table(
        "ref", metadata, sqlalchemy.Column("id", sqlalchemy.Integer),
    )
    sqlalchemy.Table(
        "some_table",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column(
            "ref_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("ref.id")
        ),
        sqlalchemy.UniqueConstraint("id", "ref_id", name="uix_1"),
    )
    metadata.create_all(faux_conn.engine)
    assert " ".join(faux_conn.test_data["execute"][-1][0].strip().split()) == (
        "CREATE TABLE `some_table`" " ( `id` INT64 NOT NULL, `ref_id` INT64 )"
    )


def test_compile_column(faux_conn):
    table = setup_table(faux_conn, "t", sqlalchemy.Column("c", sqlalchemy.Integer))
    assert table.c.c.compile(faux_conn).string == "`c`"


def test_cant_compile_unnamed_column(faux_conn, metadata):
    with pytest.raises(
        sqlalchemy.exc.CompileError,
        match="Cannot compile Column object until its 'name' is assigned.",
    ):
        sqlalchemy.Column(sqlalchemy.Integer).compile(faux_conn)


@sqlalchemy_1_4_or_higher
def test_no_alias_for_known_tables(faux_conn, metadata):
    # See: https://github.com/googleapis/python-bigquery-sqlalchemy/issues/353
    table = setup_table(
        faux_conn,
        "table1",
        metadata,
        sqlalchemy.Column("foo", sqlalchemy.Integer),
        sqlalchemy.Column("bar", sqlalchemy.ARRAY(sqlalchemy.Integer)),
    )
    F = sqlalchemy.func
    q = sqlalchemy.select(table.c.foo).where(F.unnest(table.c.bar).column_valued() == 1)

    expected_sql = (
        "SELECT `table1`.`foo` \n"
        "FROM `table1`, unnest(`table1`.`bar`) AS `anon_1` \n"
        "WHERE `anon_1` = %(param_1:INT64)s"
    )
    found_sql = q.compile(faux_conn).string
    assert found_sql == expected_sql


@sqlalchemy_1_4_or_higher
def test_no_alias_for_known_tables_cte(faux_conn, metadata):
    # See: https://github.com/googleapis/python-bigquery-sqlalchemy/issues/368
    table = setup_table(
        faux_conn,
        "table1",
        metadata,
        sqlalchemy.Column("foo", sqlalchemy.Integer),
        sqlalchemy.Column("bars", sqlalchemy.ARRAY(sqlalchemy.Integer)),
    )
    F = sqlalchemy.func

    # Set up initiali query
    q = sqlalchemy.select(table.c.foo, F.unnest(table.c.bars).column_valued("bar"))

    expected_initial_sql = (
        "SELECT `table1`.`foo`, `bar` \n"
        "FROM `table1`, unnest(`table1`.`bars`) AS `bar`"
    )
    found_initial_sql = q.compile(faux_conn).string
    assert found_initial_sql == expected_initial_sql

    q = q.cte("cte")
    q = sqlalchemy.select(*q.columns)

    expected_cte_sql = (
        "WITH `cte` AS \n"
        "(SELECT `table1`.`foo` AS `foo`, `bar` \n"
        "FROM `table1`, unnest(`table1`.`bars`) AS `bar`)\n"
        " SELECT `cte`.`foo`, `cte`.`bar` \n"
        "FROM `cte`"
    )
    found_cte_sql = q.compile(faux_conn).string
    assert found_cte_sql == expected_cte_sql
