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

from __future__ import annotations

import functools
import typing

import bigframes_vendored.sqlglot.expressions as sge

from bigframes import dtypes
from bigframes import operations as ops
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op
register_binary_op = scalar_compiler.scalar_op_compiler.register_binary_op


@register_unary_op(ops.capitalize_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Initcap(this=expr.expr, expression=sge.convert(""))


@register_unary_op(ops.StrContainsOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrContainsOp) -> sge.Expression:
    return sge.Like(this=expr.expr, expression=sge.convert(f"%{op.pat}%"))


@register_unary_op(ops.StrContainsRegexOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrContainsRegexOp) -> sge.Expression:
    return sge.RegexpLike(this=expr.expr, expression=sge.convert(op.pat))


@register_unary_op(ops.StrExtractOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrExtractOp) -> sge.Expression:
    # Cannot use BigQuery's REGEXP_EXTRACT function, which only allows one
    # capturing group.
    pat_expr = sge.convert(op.pat)
    if op.n == 0:
        pat_expr = sge.func("CONCAT", sge.convert(".*?("), pat_expr, sge.convert(").*"))
        n = 1
    else:
        pat_expr = sge.func("CONCAT", sge.convert(".*?"), pat_expr, sge.convert(".*"))
        n = op.n

    rex_replace = sge.func("REGEXP_REPLACE", expr.expr, pat_expr, sge.convert(f"\\{n}"))
    rex_contains = sge.func("REGEXP_CONTAINS", expr.expr, sge.convert(op.pat))
    return sge.If(this=rex_contains, true=rex_replace, false=sge.null())


@register_unary_op(ops.StrFindOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrFindOp) -> sge.Expression:
    # INSTR is 1-based, so we need to adjust the start position.
    start = sge.convert(op.start + 1) if op.start is not None else sge.convert(1)
    if op.end is not None:
        # BigQuery's INSTR doesn't support `end`, so we need to use SUBSTR.
        return sge.func(
            "INSTR",
            sge.Substring(
                this=expr.expr,
                start=start,
                length=sge.convert(op.end - (op.start or 0)),
            ),
            sge.convert(op.substr),
        ) - sge.convert(1)
    else:
        return sge.func(
            "INSTR",
            expr.expr,
            sge.convert(op.substr),
            start,
        ) - sge.convert(1)


@register_unary_op(ops.StrLstripOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrLstripOp) -> sge.Expression:
    return sge.func("LTRIM", expr.expr, sge.convert(op.to_strip))


@register_unary_op(ops.StrRstripOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrRstripOp) -> sge.Expression:
    return sge.func("RTRIM", expr.expr, sge.convert(op.to_strip))


@register_unary_op(ops.StrPadOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrPadOp) -> sge.Expression:
    expr_length = sge.Length(this=expr.expr)
    fillchar = sge.convert(op.fillchar)
    pad_length = sge.func("GREATEST", expr_length, sge.convert(op.length))

    if op.side == "left":
        return sge.func("LPAD", expr.expr, pad_length, fillchar)
    elif op.side == "right":
        return sge.func("RPAD", expr.expr, pad_length, fillchar)
    else:  # side == both
        lpad_amount = (
            sge.Cast(
                this=sge.Floor(
                    this=sge.func(
                        "SAFE_DIVIDE",
                        sge.Sub(this=pad_length, expression=expr_length),
                        sge.convert(2),
                    )
                ),
                to="INT64",
            )
            + expr_length
        )
        return sge.func(
            "RPAD",
            sge.func("LPAD", expr.expr, lpad_amount, fillchar),
            pad_length,
            fillchar,
        )


@register_unary_op(ops.StrRepeatOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrRepeatOp) -> sge.Expression:
    return sge.Repeat(this=expr.expr, times=sge.convert(op.repeats))


@register_unary_op(ops.EndsWithOp, pass_op=True)
def _(expr: TypedExpr, op: ops.EndsWithOp) -> sge.Expression:
    if not op.pat:
        return sge.false()

    def to_endswith(pat: str) -> sge.Expression:
        return sge.func("ENDS_WITH", expr.expr, sge.convert(pat))

    conditions = [to_endswith(pat) for pat in op.pat]
    return functools.reduce(lambda x, y: sge.Or(this=x, expression=y), conditions)


@register_unary_op(ops.isalnum_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.RegexpLike(this=expr.expr, expression=sge.convert(r"^(\p{N}|\p{L})+$"))


@register_unary_op(ops.isalpha_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.RegexpLike(this=expr.expr, expression=sge.convert(r"^\p{L}+$"))


@register_unary_op(ops.isdecimal_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.RegexpLike(this=expr.expr, expression=sge.convert(r"^(\p{Nd})+$"))


@register_unary_op(ops.isdigit_op)
def _(expr: TypedExpr) -> sge.Expression:
    regexp_pattern = (
        r"^[\p{Nd}\x{00B9}\x{00B2}\x{00B3}\x{2070}\x{2074}-\x{2079}\x{2080}-\x{2089}]+$"
    )
    return sge.RegexpLike(this=expr.expr, expression=sge.convert(regexp_pattern))


@register_unary_op(ops.islower_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.And(
        this=sge.EQ(
            this=sge.Lower(this=expr.expr),
            expression=expr.expr,
        ),
        expression=sge.NEQ(
            this=sge.Upper(this=expr.expr),
            expression=expr.expr,
        ),
    )


@register_unary_op(ops.isnumeric_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.RegexpLike(this=expr.expr, expression=sge.convert(r"^\pN+$"))


@register_unary_op(ops.isspace_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.RegexpLike(this=expr.expr, expression=sge.convert(r"^\s+$"))


@register_unary_op(ops.isupper_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.And(
        this=sge.EQ(
            this=sge.Upper(this=expr.expr),
            expression=expr.expr,
        ),
        expression=sge.NEQ(
            this=sge.Lower(this=expr.expr),
            expression=expr.expr,
        ),
    )


@register_unary_op(ops.len_op)
def _(expr: TypedExpr) -> sge.Expression:
    if dtypes.is_array_like(expr.dtype):
        return sge.func("ARRAY_LENGTH", expr.expr)

    return sge.Length(this=expr.expr)


@register_unary_op(ops.lower_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Lower(this=expr.expr)


@register_unary_op(ops.ReplaceStrOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ReplaceStrOp) -> sge.Expression:
    return sge.func("REPLACE", expr.expr, sge.convert(op.pat), sge.convert(op.repl))


@register_unary_op(ops.RegexReplaceStrOp, pass_op=True)
def _(expr: TypedExpr, op: ops.RegexReplaceStrOp) -> sge.Expression:
    return sge.func(
        "REGEXP_REPLACE", expr.expr, sge.convert(op.pat), sge.convert(op.repl)
    )


@register_unary_op(ops.reverse_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("REVERSE", expr.expr)


@register_unary_op(ops.StartsWithOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StartsWithOp) -> sge.Expression:
    if not op.pat:
        return sge.false()

    def to_startswith(pat: str) -> sge.Expression:
        return sge.func("STARTS_WITH", expr.expr, sge.convert(pat))

    conditions = [to_startswith(pat) for pat in op.pat]
    return functools.reduce(lambda x, y: sge.Or(this=x, expression=y), conditions)


@register_unary_op(ops.StrStripOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrStripOp) -> sge.Expression:
    return sge.Trim(this=expr.expr, expression=sge.convert(op.to_strip))


@register_unary_op(ops.StringSplitOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StringSplitOp) -> sge.Expression:
    return sge.Split(this=expr.expr, expression=sge.convert(op.pat))


@register_unary_op(ops.StrGetOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrGetOp) -> sge.Expression:
    return string_index(expr, op.i)


@register_unary_op(ops.StrSliceOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrSliceOp) -> sge.Expression:
    return string_slice(expr, op.start, op.end)


@register_unary_op(ops.upper_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Upper(this=expr.expr)


@register_binary_op(ops.strconcat_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    return sge.Concat(expressions=[left.expr, right.expr])


@register_unary_op(ops.ZfillOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ZfillOp) -> sge.Expression:
    length_expr = sge.Greatest(
        expressions=[sge.Length(this=expr.expr), sge.convert(op.width)]
    )
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func(
                    "STARTS_WITH",
                    expr.expr,
                    sge.convert("-"),
                ),
                true=sge.Concat(
                    expressions=[
                        sge.convert("-"),
                        sge.func(
                            "LPAD",
                            sge.Substring(this=expr.expr, start=sge.convert(2)),
                            length_expr - 1,
                            sge.convert("0"),
                        ),
                    ]
                ),
            )
        ],
        default=sge.func("LPAD", expr.expr, length_expr, sge.convert("0")),
    )


def string_index(expr: TypedExpr, index: int) -> sge.Expression:
    sub_str = sge.Substring(
        this=expr.expr,
        start=sge.convert(index + 1),
        length=sge.convert(1),
    )
    return sge.If(
        this=sge.NEQ(this=sub_str, expression=sge.convert("")),
        true=sub_str,
        false=sge.Null(),
    )


def string_slice(
    expr: TypedExpr, op_start: typing.Optional[int], op_end: typing.Optional[int]
) -> sge.Expression:
    column_length = sge.Length(this=expr.expr)
    if op_start is None:
        start = 0
    else:
        start = op_start

    start_expr = sge.convert(start) if start < 0 else sge.convert(start + 1)
    length_expr: typing.Optional[sge.Expression]
    if op_end is None:
        length_expr = None
    elif op_end < 0:
        if start < 0:
            start_expr = sge.Greatest(
                expressions=[
                    sge.convert(1),
                    column_length + sge.convert(start + 1),
                ]
            )
            length_expr = sge.Greatest(
                expressions=[
                    sge.convert(0),
                    column_length + sge.convert(op_end),
                ]
            ) - sge.Greatest(
                expressions=[
                    sge.convert(0),
                    column_length + sge.convert(start),
                ]
            )
        else:
            length_expr = sge.Greatest(
                expressions=[
                    sge.convert(0),
                    column_length + sge.convert(op_end - start),
                ]
            )
    else:  # op.end >= 0
        if start < 0:
            start_expr = sge.Greatest(
                expressions=[
                    sge.convert(1),
                    column_length + sge.convert(start + 1),
                ]
            )
            length_expr = sge.convert(op_end) - sge.Greatest(
                expressions=[
                    sge.convert(0),
                    column_length + sge.convert(start),
                ]
            )
        else:
            length_expr = sge.convert(op_end - start)

    return sge.Substring(
        this=expr.expr,
        start=start_expr,
        length=length_expr,
    )
