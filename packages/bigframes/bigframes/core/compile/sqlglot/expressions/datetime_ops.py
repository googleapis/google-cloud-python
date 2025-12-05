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

import sqlglot.expressions as sge

from bigframes import dtypes
from bigframes import operations as ops
from bigframes.core.compile.constants import UNIT_TO_US_CONVERSION_FACTORS
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op
register_binary_op = scalar_compiler.scalar_op_compiler.register_binary_op


def _calculate_resample_first(y: TypedExpr, origin: str) -> sge.Expression:
    if origin == "epoch":
        return sge.convert(0)
    elif origin == "start_day":
        return sge.func(
            "UNIX_MICROS",
            sge.Cast(
                this=sge.Cast(
                    this=y.expr, to=sge.DataType(this=sge.DataType.Type.DATE)
                ),
                to=sge.DataType(this=sge.DataType.Type.TIMESTAMPTZ),
            ),
        )
    elif origin == "start":
        return sge.func(
            "UNIX_MICROS",
            sge.Cast(this=y.expr, to=sge.DataType(this=sge.DataType.Type.TIMESTAMPTZ)),
        )
    else:
        raise ValueError(f"Origin {origin} not supported")


@register_binary_op(ops.DatetimeToIntegerLabelOp, pass_op=True)
def datetime_to_integer_label_op(
    x: TypedExpr, y: TypedExpr, op: ops.DatetimeToIntegerLabelOp
) -> sge.Expression:
    # Determine if the frequency is fixed by checking if 'op.freq.nanos' is defined.
    try:
        return _datetime_to_integer_label_fixed_frequency(x, y, op)
    except ValueError:
        return _datetime_to_integer_label_non_fixed_frequency(x, y, op)


def _datetime_to_integer_label_fixed_frequency(
    x: TypedExpr, y: TypedExpr, op: ops.DatetimeToIntegerLabelOp
) -> sge.Expression:
    """
    This function handles fixed frequency conversions where the unit can range
    from microseconds (us) to days.
    """
    us = op.freq.nanos / 1000
    x_int = sge.func(
        "UNIX_MICROS",
        sge.Cast(this=x.expr, to=sge.DataType(this=sge.DataType.Type.TIMESTAMPTZ)),
    )
    first = _calculate_resample_first(y, op.origin)  # type: ignore
    x_int_label = sge.Cast(
        this=sge.Floor(
            this=sge.func(
                "IEEE_DIVIDE",
                sge.Sub(this=x_int, expression=first),
                sge.convert(int(us)),
            )
        ),
        to=sge.DataType.build("INT64"),
    )
    return x_int_label


def _datetime_to_integer_label_non_fixed_frequency(
    x: TypedExpr, y: TypedExpr, op: ops.DatetimeToIntegerLabelOp
) -> sge.Expression:
    """
    This function handles non-fixed frequency conversions for units ranging
    from weeks to years.
    """
    rule_code = op.freq.rule_code
    n = op.freq.n
    if rule_code == "W-SUN":  # Weekly
        us = n * 7 * 24 * 60 * 60 * 1000000
        x_trunc = sge.TimestampTrunc(this=x.expr, unit=sge.Var(this="WEEK(MONDAY)"))
        y_trunc = sge.TimestampTrunc(this=y.expr, unit=sge.Var(this="WEEK(MONDAY)"))
        x_plus_6 = sge.Add(
            this=x_trunc,
            expression=sge.Interval(
                this=sge.convert(6), unit=sge.Identifier(this="DAY")
            ),
        )
        y_plus_6 = sge.Add(
            this=y_trunc,
            expression=sge.Interval(
                this=sge.convert(6), unit=sge.Identifier(this="DAY")
            ),
        )
        x_int = sge.func(
            "UNIX_MICROS",
            sge.Cast(
                this=x_plus_6, to=sge.DataType(this=sge.DataType.Type.TIMESTAMPTZ)
            ),
        )
        first = sge.func(
            "UNIX_MICROS",
            sge.Cast(
                this=y_plus_6, to=sge.DataType(this=sge.DataType.Type.TIMESTAMPTZ)
            ),
        )
        return sge.Case(
            ifs=[
                sge.If(
                    this=sge.EQ(this=x_int, expression=first),
                    true=sge.convert(0),
                )
            ],
            default=sge.Add(
                this=sge.Cast(
                    this=sge.Floor(
                        this=sge.func(
                            "IEEE_DIVIDE",
                            sge.Sub(
                                this=sge.Sub(this=x_int, expression=first),
                                expression=sge.convert(1),
                            ),
                            sge.convert(us),
                        )
                    ),
                    to=sge.DataType.build("INT64"),
                ),
                expression=sge.convert(1),
            ),
        )
    elif rule_code == "ME":  # Monthly
        x_int = sge.Paren(  # type: ignore
            this=sge.Add(
                this=sge.Mul(
                    this=sge.Extract(
                        this=sge.Identifier(this="YEAR"), expression=x.expr
                    ),
                    expression=sge.convert(12),
                ),
                expression=sge.Sub(
                    this=sge.Extract(
                        this=sge.Identifier(this="MONTH"), expression=x.expr
                    ),
                    expression=sge.convert(1),
                ),
            )
        )
        first = sge.Paren(  # type: ignore
            this=sge.Add(
                this=sge.Mul(
                    this=sge.Extract(
                        this=sge.Identifier(this="YEAR"), expression=y.expr
                    ),
                    expression=sge.convert(12),
                ),
                expression=sge.Sub(
                    this=sge.Extract(
                        this=sge.Identifier(this="MONTH"), expression=y.expr
                    ),
                    expression=sge.convert(1),
                ),
            )
        )
        return sge.Case(
            ifs=[
                sge.If(
                    this=sge.EQ(this=x_int, expression=first),
                    true=sge.convert(0),
                )
            ],
            default=sge.Add(
                this=sge.Cast(
                    this=sge.Floor(
                        this=sge.func(
                            "IEEE_DIVIDE",
                            sge.Sub(
                                this=sge.Sub(this=x_int, expression=first),
                                expression=sge.convert(1),
                            ),
                            sge.convert(n),
                        )
                    ),
                    to=sge.DataType.build("INT64"),
                ),
                expression=sge.convert(1),
            ),
        )
    elif rule_code == "QE-DEC":  # Quarterly
        x_int = sge.Paren(  # type: ignore
            this=sge.Add(
                this=sge.Mul(
                    this=sge.Extract(
                        this=sge.Identifier(this="YEAR"), expression=x.expr
                    ),
                    expression=sge.convert(4),
                ),
                expression=sge.Sub(
                    this=sge.Extract(
                        this=sge.Identifier(this="QUARTER"), expression=x.expr
                    ),
                    expression=sge.convert(1),
                ),
            )
        )
        first = sge.Paren(  # type: ignore
            this=sge.Add(
                this=sge.Mul(
                    this=sge.Extract(
                        this=sge.Identifier(this="YEAR"), expression=y.expr
                    ),
                    expression=sge.convert(4),
                ),
                expression=sge.Sub(
                    this=sge.Extract(
                        this=sge.Identifier(this="QUARTER"), expression=y.expr
                    ),
                    expression=sge.convert(1),
                ),
            )
        )
        return sge.Case(
            ifs=[
                sge.If(
                    this=sge.EQ(this=x_int, expression=first),
                    true=sge.convert(0),
                )
            ],
            default=sge.Add(
                this=sge.Cast(
                    this=sge.Floor(
                        this=sge.func(
                            "IEEE_DIVIDE",
                            sge.Sub(
                                this=sge.Sub(this=x_int, expression=first),
                                expression=sge.convert(1),
                            ),
                            sge.convert(n),
                        )
                    ),
                    to=sge.DataType.build("INT64"),
                ),
                expression=sge.convert(1),
            ),
        )
    elif rule_code == "YE-DEC":  # Yearly
        x_int = sge.Extract(this=sge.Identifier(this="YEAR"), expression=x.expr)
        first = sge.Extract(this=sge.Identifier(this="YEAR"), expression=y.expr)
        return sge.Case(
            ifs=[
                sge.If(
                    this=sge.EQ(this=x_int, expression=first),
                    true=sge.convert(0),
                )
            ],
            default=sge.Add(
                this=sge.Cast(
                    this=sge.Floor(
                        this=sge.func(
                            "IEEE_DIVIDE",
                            sge.Sub(
                                this=sge.Sub(this=x_int, expression=first),
                                expression=sge.convert(1),
                            ),
                            sge.convert(n),
                        )
                    ),
                    to=sge.DataType.build("INT64"),
                ),
                expression=sge.convert(1),
            ),
        )
    else:
        raise ValueError(rule_code)


@register_unary_op(ops.FloorDtOp, pass_op=True)
def _(expr: TypedExpr, op: ops.FloorDtOp) -> sge.Expression:
    pandas_to_bq_freq_map = {
        "Y": "YEAR",
        "Q": "QUARTER",
        "M": "MONTH",
        "W": "WEEK(MONDAY)",
        "D": "DAY",
        "h": "HOUR",
        "min": "MINUTE",
        "s": "SECOND",
        "ms": "MILLISECOND",
        "us": "MICROSECOND",
        "ns": "NANOSECOND",
    }
    if op.freq not in pandas_to_bq_freq_map.keys():
        raise NotImplementedError(
            f"Unsupported freq paramater: {op.freq}"
            + " Supported freq parameters are: "
            + ",".join(pandas_to_bq_freq_map.keys())
        )

    bq_freq = pandas_to_bq_freq_map[op.freq]
    return sge.TimestampTrunc(this=expr.expr, unit=sge.Identifier(this=bq_freq))


@register_unary_op(ops.hour_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="HOUR"), expression=expr.expr)


@register_unary_op(ops.minute_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="MINUTE"), expression=expr.expr)


@register_unary_op(ops.month_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="MONTH"), expression=expr.expr)


@register_unary_op(ops.normalize_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.TimestampTrunc(this=expr.expr, unit=sge.Identifier(this="DAY"))


@register_unary_op(ops.quarter_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="QUARTER"), expression=expr.expr)


@register_unary_op(ops.second_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="SECOND"), expression=expr.expr)


@register_unary_op(ops.StrftimeOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrftimeOp) -> sge.Expression:
    func_name = ""
    if expr.dtype == dtypes.DATE_DTYPE:
        func_name = "FORMAT_DATE"
    elif expr.dtype == dtypes.DATETIME_DTYPE:
        func_name = "FORMAT_DATETIME"
    elif expr.dtype == dtypes.TIME_DTYPE:
        func_name = "FORMAT_TIME"
    elif expr.dtype == dtypes.TIMESTAMP_DTYPE:
        func_name = "FORMAT_TIMESTAMP"

    return sge.func(func_name, sge.convert(op.date_format), expr.expr)


@register_unary_op(ops.time_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TIME", expr.expr)


@register_unary_op(ops.ToDatetimeOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ToDatetimeOp) -> sge.Expression:
    if op.format:
        result = expr.expr
        if expr.dtype != dtypes.STRING_DTYPE:
            result = sge.Cast(this=result, to="STRING")
        result = sge.func(
            "PARSE_TIMESTAMP", sge.convert(op.format), result, sge.convert("UTC")
        )
        return sge.Cast(this=result, to="DATETIME")

    if expr.dtype == dtypes.STRING_DTYPE:
        return sge.TryCast(this=expr.expr, to="DATETIME")

    value = expr.expr
    unit = op.unit or "ns"
    factor = UNIT_TO_US_CONVERSION_FACTORS[unit]
    if factor != 1:
        value = sge.Mul(this=value, expression=sge.convert(factor))
    value = sge.func("TRUNC", value)
    return sge.Cast(
        this=sge.func("TIMESTAMP_MICROS", sge.Cast(this=value, to="INT64")),
        to="DATETIME",
    )


@register_unary_op(ops.ToTimestampOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ToTimestampOp) -> sge.Expression:
    if op.format:
        result = expr.expr
        if expr.dtype != dtypes.STRING_DTYPE:
            result = sge.Cast(this=result, to="STRING")
        return sge.func(
            "PARSE_TIMESTAMP", sge.convert(op.format), expr.expr, sge.convert("UTC")
        )

    if expr.dtype == dtypes.STRING_DTYPE:
        return sge.func("TIMESTAMP", expr.expr)

    value = expr.expr
    unit = op.unit or "ns"
    factor = UNIT_TO_US_CONVERSION_FACTORS[unit]
    if factor != 1:
        value = sge.Mul(this=value, expression=sge.convert(factor))
    value = sge.func("TRUNC", value)
    return sge.Cast(
        this=sge.func("TIMESTAMP_MICROS", sge.Cast(this=value, to="INT64")),
        to="TIMESTAMP",
    )


@register_unary_op(ops.UnixMicros)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("UNIX_MICROS", expr.expr)


@register_unary_op(ops.UnixMillis)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("UNIX_MILLIS", expr.expr)


@register_unary_op(ops.UnixSeconds, pass_op=True)
def _(expr: TypedExpr, op: ops.UnixSeconds) -> sge.Expression:
    return sge.func("UNIX_SECONDS", expr.expr)


@register_unary_op(ops.year_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="YEAR"), expression=expr.expr)
