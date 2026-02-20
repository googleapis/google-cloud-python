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

import bigframes_vendored.sqlglot.expressions as sge

from bigframes import dtypes
from bigframes import operations as ops
from bigframes.core.compile.constants import UNIT_TO_US_CONVERSION_FACTORS
from bigframes.core.compile.sqlglot import sqlglot_types
import bigframes.core.compile.sqlglot.expression_compiler as expression_compiler
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr

register_unary_op = expression_compiler.expression_compiler.register_unary_op
register_binary_op = expression_compiler.expression_compiler.register_binary_op


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


def _calculate_resample_first(y: TypedExpr, origin: str) -> sge.Expression:
    if origin == "epoch":
        return sge.convert(0)
    elif origin == "start_day":
        return sge.func(
            "UNIX_MICROS",
            sge.Cast(this=sge.Cast(this=y.expr, to="DATE"), to="TIMESTAMP"),
        )
    elif origin == "start":
        return sge.func("UNIX_MICROS", sge.Cast(this=y.expr, to="TIMESTAMP"))
    else:
        raise ValueError(f"Origin {origin} not supported")


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

    if expr.dtype in (dtypes.STRING_DTYPE, dtypes.TIMESTAMP_DTYPE):
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

    if expr.dtype in (dtypes.STRING_DTYPE, dtypes.DATETIME_DTYPE):
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


@register_binary_op(ops.IntegerLabelToDatetimeOp, pass_op=True)
def integer_label_to_datetime_op(
    x: TypedExpr, y: TypedExpr, op: ops.IntegerLabelToDatetimeOp
) -> sge.Expression:
    # Determine if the frequency is fixed by checking if 'op.freq.nanos' is defined.
    try:
        return _integer_label_to_datetime_op_fixed_frequency(x, y, op)

    except ValueError:
        # Non-fixed frequency conversions for units ranging from weeks to years.
        rule_code = op.freq.rule_code

        if rule_code == "W-SUN":
            return _integer_label_to_datetime_op_weekly_freq(x, y, op)

        if rule_code in ("ME", "M"):
            return _integer_label_to_datetime_op_monthly_freq(x, y, op)

        if rule_code in ("QE-DEC", "Q-DEC"):
            return _integer_label_to_datetime_op_quarterly_freq(x, y, op)

        if rule_code in ("YE-DEC", "A-DEC", "Y-DEC"):
            return _integer_label_to_datetime_op_yearly_freq(x, y, op)

        # If the rule_code is not recognized, raise an error here.
        raise ValueError(f"Unsupported frequency rule code: {rule_code}")


def _integer_label_to_datetime_op_fixed_frequency(
    x: TypedExpr, y: TypedExpr, op: ops.IntegerLabelToDatetimeOp
) -> sge.Expression:
    """
    This function handles fixed frequency conversions where the unit can range
    from microseconds (us) to days.
    """
    us = op.freq.nanos / 1000
    first = _calculate_resample_first(y, op.origin)  # type: ignore
    x_label = sge.Cast(
        this=sge.func(
            "TIMESTAMP_MICROS",
            sge.Cast(
                this=sge.Add(
                    this=sge.Mul(
                        this=sge.Cast(this=x.expr, to="BIGNUMERIC"),
                        expression=sge.convert(int(us)),
                    ),
                    expression=sge.Cast(this=first, to="BIGNUMERIC"),
                ),
                to="INT64",
            ),
        ),
        to=sqlglot_types.from_bigframes_dtype(y.dtype),
    )
    return x_label


def _integer_label_to_datetime_op_weekly_freq(
    x: TypedExpr, y: TypedExpr, op: ops.IntegerLabelToDatetimeOp
) -> sge.Expression:
    n = op.freq.n
    # Calculate microseconds for the weekly interval.
    us = n * 7 * 24 * 60 * 60 * 1000000
    first = sge.func(
        "UNIX_MICROS",
        sge.Add(
            this=sge.TimestampTrunc(
                this=sge.Cast(this=y.expr, to="TIMESTAMP"),
                unit=sge.Var(this="WEEK(MONDAY)"),
            ),
            expression=sge.Interval(
                this=sge.convert(6), unit=sge.Identifier(this="DAY")
            ),
        ),
    )
    return sge.Cast(
        this=sge.func(
            "TIMESTAMP_MICROS",
            sge.Cast(
                this=sge.Add(
                    this=sge.Mul(
                        this=sge.Cast(this=x.expr, to="BIGNUMERIC"),
                        expression=sge.convert(us),
                    ),
                    expression=sge.Cast(this=first, to="BIGNUMERIC"),
                ),
                to="INT64",
            ),
        ),
        to=sqlglot_types.from_bigframes_dtype(y.dtype),
    )


def _integer_label_to_datetime_op_monthly_freq(
    x: TypedExpr, y: TypedExpr, op: ops.IntegerLabelToDatetimeOp
) -> sge.Expression:
    n = op.freq.n
    one = sge.convert(1)
    twelve = sge.convert(12)
    first = sge.Sub(  # type: ignore
        this=sge.Add(
            this=sge.Mul(
                this=sge.Extract(this="YEAR", expression=y.expr),
                expression=twelve,
            ),
            expression=sge.Extract(this="MONTH", expression=y.expr),
        ),
        expression=one,
    )
    x_val = sge.Add(
        this=sge.Mul(this=x.expr, expression=sge.convert(n)), expression=first
    )
    year = sge.Cast(
        this=sge.Floor(this=sge.func("IEEE_DIVIDE", x_val, twelve)),
        to="INT64",
    )
    month = sge.Add(this=sge.Mod(this=x_val, expression=twelve), expression=one)

    next_year = sge.Case(
        ifs=[
            sge.If(
                this=sge.EQ(this=month, expression=twelve),
                true=sge.Add(this=year, expression=one),
            )
        ],
        default=year,
    )
    next_month = sge.Case(
        ifs=[sge.If(this=sge.EQ(this=month, expression=twelve), true=one)],
        default=sge.Add(this=month, expression=one),
    )
    next_month_date = sge.func(
        "TIMESTAMP",
        sge.Anonymous(
            this="DATETIME",
            expressions=[
                next_year,
                next_month,
                one,
                sge.convert(0),
                sge.convert(0),
                sge.convert(0),
            ],
        ),
    )
    x_label = sge.Sub(  # type: ignore
        this=next_month_date, expression=sge.Interval(this=one, unit="DAY")
    )
    return sge.Cast(this=x_label, to=sqlglot_types.from_bigframes_dtype(y.dtype))


def _integer_label_to_datetime_op_quarterly_freq(
    x: TypedExpr, y: TypedExpr, op: ops.IntegerLabelToDatetimeOp
) -> sge.Expression:
    n = op.freq.n
    one = sge.convert(1)
    three = sge.convert(3)
    four = sge.convert(4)
    twelve = sge.convert(12)
    first = sge.Sub(  # type: ignore
        this=sge.Add(
            this=sge.Mul(
                this=sge.Extract(this="YEAR", expression=y.expr),
                expression=four,
            ),
            expression=sge.Extract(this="QUARTER", expression=y.expr),
        ),
        expression=one,
    )
    x_val = sge.Add(
        this=sge.Mul(this=x.expr, expression=sge.convert(n)), expression=first
    )
    year = sge.Cast(
        this=sge.Floor(this=sge.func("IEEE_DIVIDE", x_val, four)),
        to="INT64",
    )
    month = sge.Mul(  # type: ignore
        this=sge.Paren(
            this=sge.Add(this=sge.Mod(this=x_val, expression=four), expression=one)
        ),
        expression=three,
    )

    next_year = sge.Case(
        ifs=[
            sge.If(
                this=sge.EQ(this=month, expression=twelve),
                true=sge.Add(this=year, expression=one),
            )
        ],
        default=year,
    )
    next_month = sge.Case(
        ifs=[sge.If(this=sge.EQ(this=month, expression=twelve), true=one)],
        default=sge.Add(this=month, expression=one),
    )
    next_month_date = sge.Anonymous(
        this="DATETIME",
        expressions=[
            next_year,
            next_month,
            one,
            sge.convert(0),
            sge.convert(0),
            sge.convert(0),
        ],
    )
    x_label = sge.Sub(  # type: ignore
        this=next_month_date, expression=sge.Interval(this=one, unit="DAY")
    )
    return sge.Cast(this=x_label, to=sqlglot_types.from_bigframes_dtype(y.dtype))


def _integer_label_to_datetime_op_yearly_freq(
    x: TypedExpr, y: TypedExpr, op: ops.IntegerLabelToDatetimeOp
) -> sge.Expression:
    n = op.freq.n
    one = sge.convert(1)
    first = sge.Extract(this="YEAR", expression=y.expr)
    x_val = sge.Add(
        this=sge.Mul(this=x.expr, expression=sge.convert(n)), expression=first
    )
    next_year = sge.Add(this=x_val, expression=one)  # type: ignore
    next_month_date = sge.func(
        "TIMESTAMP",
        sge.Anonymous(
            this="DATETIME",
            expressions=[
                next_year,
                one,
                one,
                sge.convert(0),
                sge.convert(0),
                sge.convert(0),
            ],
        ),
    )
    x_label = sge.Sub(  # type: ignore
        this=next_month_date, expression=sge.Interval(this=one, unit="DAY")
    )
    return sge.Cast(this=x_label, to=sqlglot_types.from_bigframes_dtype(y.dtype))
