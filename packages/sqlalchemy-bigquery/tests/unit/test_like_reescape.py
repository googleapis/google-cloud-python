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

"""SQLAlchemy and BigQuery escape % and _ differently in like expressions.

We need to correct for the autoescape option in various string
functions.
"""

import pytest
import sqlalchemy
import sqlalchemy.exc
import sqlalchemy.sql.schema

import sqlalchemy_bigquery.base


@pytest.mark.parametrize(
    "raw,escape,expected",
    [
        ("ab%cd", None, "ab%cd"),
        (r"ab\%cd", "\\", r"ab\%cd"),
        ("ab/%cd", "/", r"ab\%cd"),
    ],
)
def test_like_reescape_autoescape_off(raw, escape, expected):
    col = sqlalchemy.sql.schema.Column()
    op = col.contains(raw, escape=escape, autoescape=False)
    orig_modifiers = op.modifiers.copy()
    orig_right_value = op.right.value

    o2 = sqlalchemy_bigquery.base.BigQueryCompiler._maybe_reescape(op)

    assert o2.left.__dict__ == op.left.__dict__
    assert not o2.modifiers.get("escape")
    assert o2.right.value == expected
    assert op.modifiers == orig_modifiers
    assert op.right.value == orig_right_value


@pytest.mark.parametrize(
    "raw,escape,expected",
    [
        ("ab%cd", None, r"ab\%cd"),
        ("ab%c_d", None, r"ab\%c\_d"),
        ("ab%c_d", "\\", r"ab\%c\_d"),
        ("ab/%c/_/d", None, r"ab/\%c/\_/d"),
        (r"ab\%cd", None, r"ab\\\%cd"),
        (r"ab\_cd", None, r"ab\\\_cd"),
        (r"ab\cd", None, r"ab\\cd"),
        (r"ab\/%cd", None, r"ab\\/\%cd"),
        (r"ab\\cd", None, r"ab\\\\cd"),
        (r"ab\%cd", "^", r"ab\\\%cd"),
        (r"ab^%cd", "^", r"ab^\%cd"),
    ],
)
def test_like_reescape_autoescape_on(raw, escape, expected):
    col = sqlalchemy.sql.schema.Column()
    op = col.contains(raw, escape=escape, autoescape=True)
    orig_modifiers = op.modifiers.copy()
    orig_right_value = op.right.value

    o2 = sqlalchemy_bigquery.base.BigQueryCompiler._maybe_reescape(op)

    assert o2.left.__dict__ == op.left.__dict__
    assert not o2.modifiers.get("escape")
    assert o2.right.value == expected
    assert op.modifiers == orig_modifiers
    assert op.right.value == orig_right_value


@pytest.mark.parametrize(
    "build_expr",
    [
        lambda col, other: col.contains(other, escape="/"),
        lambda col, other: col.startswith(
            sqlalchemy.func.replace(other, "%", "/%"), escape="/"
        ),
        lambda col, other: col.startswith(
            sqlalchemy.literal("50/%") + other, escape="/"
        ),
        lambda col, other: col.contains(sqlalchemy.bindparam("q"), escape="/"),
        lambda col, other: col.contains(sqlalchemy.bindparam("q", "a/%"), escape="/"),
        lambda col, other: col.contains(
            sqlalchemy.bindparam("q", unique=True), escape="/"
        ),
    ],
    ids=[
        "column",
        "func_expression",
        "binary_expression",
        "unbound_bindparam",
        "named_bindparam_with_default",
        "unique_bindparam_without_string",
    ],
)
def test_like_reescape_non_literal_custom_escape_raises(build_expr):
    dialect = sqlalchemy_bigquery.BigQueryDialect()
    col = sqlalchemy.sql.schema.Column("c", sqlalchemy.String)
    other_col = sqlalchemy.sql.schema.Column("other", sqlalchemy.String)
    expr = build_expr(col, other_col)
    orig_modifiers = expr.modifiers.copy()

    with pytest.raises(
        sqlalchemy.exc.CompileError,
        match="BigQuery only supports a custom escape character for literal strings",
    ):
        expr.compile(dialect=dialect)

    assert expr.modifiers == orig_modifiers


def test_like_custom_escape_literal_string_compiles():
    dialect = sqlalchemy_bigquery.BigQueryDialect()
    col = sqlalchemy.sql.schema.Column("c", sqlalchemy.String)
    expr = col.contains(sqlalchemy.literal("50/%"), escape="/")

    compiled = expr.compile(dialect=dialect)

    assert "ESCAPE" not in compiled.string
    assert list(compiled.params.values()) == [r"50\%"]


def test_like_backslash_escape_bindparam_compiles():
    dialect = sqlalchemy_bigquery.BigQueryDialect()
    col = sqlalchemy.sql.schema.Column("c", sqlalchemy.String)
    expr = col.contains(sqlalchemy.bindparam("q"), escape="\\")

    compiled = expr.compile(dialect=dialect)

    assert "ESCAPE" not in compiled.string
    assert compiled.params == {"q": None}


@pytest.mark.parametrize(
    "build_expr",
    [
        lambda col: col.contains(r"ab\%c_d\e", autoescape=True),
        lambda col: col.startswith(r"ab\%c_d\e", autoescape=True),
        lambda col: col.endswith(r"ab\%c_d\e", autoescape=True),
        lambda col: ~col.contains(r"ab\%c_d\e", autoescape=True),
        lambda col: ~col.startswith(r"ab\%c_d\e", autoescape=True),
        lambda col: ~col.endswith(r"ab\%c_d\e", autoescape=True),
    ],
    ids=[
        "contains",
        "startswith",
        "endswith",
        "not_contains",
        "not_startswith",
        "not_endswith",
    ],
)
def test_like_autoescape_repeated_compile_idempotent(build_expr):
    dialect = sqlalchemy_bigquery.BigQueryDialect()
    col = sqlalchemy.sql.schema.Column("c", sqlalchemy.String)
    expr = build_expr(col)

    compiled1 = expr.compile(dialect=dialect)
    compiled2 = expr.compile(dialect=dialect)

    assert compiled1.string == compiled2.string
    assert "ESCAPE" not in compiled1.string
    assert compiled1.params == compiled2.params
    assert list(compiled1.params.values()) == [r"ab\\\%c\_d\\e"]
