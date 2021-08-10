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
