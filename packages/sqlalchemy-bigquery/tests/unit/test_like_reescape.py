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

import sqlalchemy
import sqlalchemy.sql.operators
import sqlalchemy.sql.schema

import sqlalchemy_bigquery.base


def _check(raw, escaped, escape=None, autoescape=True):
    col = sqlalchemy.sql.schema.Column()
    op = col.contains(raw, escape=escape, autoescape=autoescape)
    orig_modifiers = op.modifiers.copy()
    orig_right = op.right
    orig_right_value = op.right.value

    o2 = sqlalchemy_bigquery.base.BigQueryCompiler._maybe_reescape(op)
    assert o2.left.__dict__ == op.left.__dict__
    assert not o2.modifiers.get("escape")
    assert o2.right.value == escaped

    # Original AST must not be mutated in-place.
    assert op.modifiers == orig_modifiers
    assert op.modifiers is not o2.modifiers
    assert op.right is orig_right
    assert op.right.value == orig_right_value
    if escape != "\\" and autoescape:
        assert o2.right is not op.right


def test_like_autoescape_reescape():
    _check("ab%cd", "ab\\%cd")
    _check("ab%c_d", "ab\\%c\\_d")
    _check("ab%cd", "ab%cd", autoescape=False)
    _check("ab%c_d", "ab\\%c\\_d", escape="\\")
    _check("ab/%c/_/d", "ab/\\%c/\\_/d")
    _check(r"ab\%cd", r"ab\\\%cd")
    _check(r"ab\_cd", r"ab\\\_cd")
    _check(r"ab\cd", r"ab\\cd")
    _check(r"ab\/%cd", r"ab\\/\%cd")
    _check(r"ab\\cd", r"ab\\\\cd")
    _check(r"ab\%cd", r"ab\\\%cd", escape="^")
    _check(r"ab^%cd", r"ab^\%cd", escape="^")


def test_like_reescape_non_string_right():
    col = sqlalchemy.sql.schema.Column("c", sqlalchemy.String)
    other_col = sqlalchemy.sql.schema.Column("other", sqlalchemy.String)

    op_col = col.contains(other_col, escape="/")
    o2_col = sqlalchemy_bigquery.base.BigQueryCompiler._maybe_reescape(op_col)
    assert not o2_col.modifiers.get("escape")
    assert op_col.modifiers.get("escape") == "/"
    assert o2_col.right is other_col

    param = sqlalchemy.bindparam("p")
    op_param = col.contains(param, escape="/")
    o2_param = sqlalchemy_bigquery.base.BigQueryCompiler._maybe_reescape(op_param)
    assert not o2_param.modifiers.get("escape")
    assert op_param.modifiers.get("escape") == "/"
    assert o2_param.right is op_param.right
    assert o2_param.right.value is None


def test_like_autoescape_repeated_compile_idempotent():
    dialect = sqlalchemy_bigquery.BigQueryDialect()
    col = sqlalchemy.sql.schema.Column("c", sqlalchemy.String)

    for method in (
        "contains",
        "startswith",
        "endswith",
    ):
        expr = getattr(col, method)(r"ab\%c_d\e", autoescape=True)
        orig_modifiers = expr.modifiers.copy()
        orig_value = expr.right.value

        compiled1 = expr.compile(dialect=dialect)
        compiled2 = expr.compile(dialect=dialect)

        assert compiled1.string == compiled2.string
        assert "ESCAPE" not in compiled1.string
        assert compiled1.params == compiled2.params
        assert list(compiled1.params.values()) == [r"ab\\\%c\_d\\e"]
        assert expr.modifiers == orig_modifiers
        assert expr.right.value == orig_value

        neg_expr = ~expr
        neg_compiled1 = neg_expr.compile(dialect=dialect)
        neg_compiled2 = neg_expr.compile(dialect=dialect)
        assert neg_compiled1.string == neg_compiled2.string
        assert "ESCAPE" not in neg_compiled1.string
        assert neg_compiled1.params == neg_compiled2.params
        assert list(neg_compiled1.params.values()) == [r"ab\\\%c\_d\\e"]
