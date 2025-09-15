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

import pandas as pd
import pyarrow as pa
import sqlglot
import sqlglot.expressions as sge

from bigframes import operations as ops
from bigframes.core.compile.constants import UNIT_TO_US_CONVERSION_FACTORS
import bigframes.core.compile.sqlglot.expressions.constants as constants
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler
import bigframes.dtypes as dtypes

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op


@register_unary_op(ops.abs_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Abs(this=expr.expr)


@register_unary_op(ops.arccosh_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr < sge.convert(1),
                true=constants._NAN,
            )
        ],
        default=sge.func("ACOSH", expr.expr),
    )


@register_unary_op(ops.arccos_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > sge.convert(1),
                true=constants._NAN,
            )
        ],
        default=sge.func("ACOS", expr.expr),
    )


@register_unary_op(ops.arcsin_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > sge.convert(1),
                true=constants._NAN,
            )
        ],
        default=sge.func("ASIN", expr.expr),
    )


@register_unary_op(ops.arcsinh_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ASINH", expr.expr)


@register_unary_op(ops.arctan_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ATAN", expr.expr)


@register_unary_op(ops.arctanh_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > sge.convert(1),
                true=constants._NAN,
            )
        ],
        default=sge.func("ATANH", expr.expr),
    )


@register_unary_op(ops.AsTypeOp, pass_op=True)
def _(expr: TypedExpr, op: ops.AsTypeOp) -> sge.Expression:
    # TODO: Support more types for casting, such as JSON, etc.
    return sge.Cast(this=expr.expr, to=op.to_type)


@register_unary_op(ops.ArrayToStringOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ArrayToStringOp) -> sge.Expression:
    return sge.ArrayToString(this=expr.expr, expression=f"'{op.delimiter}'")


@register_unary_op(ops.ArrayIndexOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ArrayIndexOp) -> sge.Expression:
    return sge.Bracket(
        this=expr.expr,
        expressions=[sge.Literal.number(op.index)],
        safe=True,
        offset=False,
    )


@register_unary_op(ops.ArraySliceOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ArraySliceOp) -> sge.Expression:
    slice_idx = sqlglot.to_identifier("slice_idx")

    conditions: typing.List[sge.Predicate] = [slice_idx >= op.start]

    if op.stop is not None:
        conditions.append(slice_idx < op.stop)

    # local name for each element in the array
    el = sqlglot.to_identifier("el")

    selected_elements = (
        sge.select(el)
        .from_(
            sge.Unnest(
                expressions=[expr.expr],
                alias=sge.TableAlias(columns=[el]),
                offset=slice_idx,
            )
        )
        .where(*conditions)
    )

    return sge.array(selected_elements)


@register_unary_op(ops.capitalize_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Initcap(this=expr.expr)


@register_unary_op(ops.ceil_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Ceil(this=expr.expr)


@register_unary_op(ops.cos_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("COS", expr.expr)


@register_unary_op(ops.cosh_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > sge.convert(709.78),
                true=constants._INF,
            )
        ],
        default=sge.func("COSH", expr.expr),
    )


@register_unary_op(ops.StrContainsOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrContainsOp) -> sge.Expression:
    return sge.Like(this=expr.expr, expression=sge.convert(f"%{op.pat}%"))


@register_unary_op(ops.StrContainsRegexOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrContainsRegexOp) -> sge.Expression:
    return sge.RegexpLike(this=expr.expr, expression=sge.convert(op.pat))


@register_unary_op(ops.StrExtractOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrExtractOp) -> sge.Expression:
    return sge.RegexpExtract(
        this=expr.expr, expression=sge.convert(op.pat), group=sge.convert(op.n)
    )


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
    return sge.Trim(this=expr.expr, expression=sge.convert(op.to_strip), side="LEFT")


@register_unary_op(ops.StrPadOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrPadOp) -> sge.Expression:
    pad_length = sge.func(
        "GREATEST", sge.Length(this=expr.expr), sge.convert(op.length)
    )
    if op.side == "left":
        return sge.func(
            "LPAD",
            expr.expr,
            pad_length,
            sge.convert(op.fillchar),
        )
    elif op.side == "right":
        return sge.func(
            "RPAD",
            expr.expr,
            pad_length,
            sge.convert(op.fillchar),
        )
    else:  # side == both
        lpad_amount = sge.Cast(
            this=sge.func(
                "SAFE_DIVIDE",
                sge.Sub(this=pad_length, expression=sge.Length(this=expr.expr)),
                sge.convert(2),
            ),
            to="INT64",
        ) + sge.Length(this=expr.expr)
        return sge.func(
            "RPAD",
            sge.func(
                "LPAD",
                expr.expr,
                lpad_amount,
                sge.convert(op.fillchar),
            ),
            pad_length,
            sge.convert(op.fillchar),
        )


@register_unary_op(ops.StrRepeatOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrRepeatOp) -> sge.Expression:
    return sge.Repeat(this=expr.expr, times=sge.convert(op.repeats))


@register_unary_op(ops.date_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Date(this=expr.expr)


@register_unary_op(ops.day_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="DAY"), expression=expr.expr)


@register_unary_op(ops.dayofweek_op)
def _(expr: TypedExpr) -> sge.Expression:
    # Adjust the 1-based day-of-week index (from SQL) to a 0-based index.
    return sge.Extract(
        this=sge.Identifier(this="DAYOFWEEK"), expression=expr.expr
    ) - sge.convert(1)


@register_unary_op(ops.dayofyear_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="DAYOFYEAR"), expression=expr.expr)


@register_unary_op(ops.EndsWithOp, pass_op=True)
def _(expr: TypedExpr, op: ops.EndsWithOp) -> sge.Expression:
    if not op.pat:
        return sge.false()

    def to_endswith(pat: str) -> sge.Expression:
        return sge.func("ENDS_WITH", expr.expr, sge.convert(pat))

    conditions = [to_endswith(pat) for pat in op.pat]
    return functools.reduce(lambda x, y: sge.Or(this=x, expression=y), conditions)


@register_unary_op(ops.exp_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr > constants._FLOAT64_EXP_BOUND,
                true=constants._INF,
            )
        ],
        default=sge.func("EXP", expr.expr),
    )


@register_unary_op(ops.expm1_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr > constants._FLOAT64_EXP_BOUND,
                true=constants._INF,
            )
        ],
        default=sge.func("EXP", expr.expr),
    ) - sge.convert(1)


@register_unary_op(ops.FloorDtOp, pass_op=True)
def _(expr: TypedExpr, op: ops.FloorDtOp) -> sge.Expression:
    # TODO: Remove this method when it is covered by ops.FloorOp
    return sge.TimestampTrunc(this=expr.expr, unit=sge.Identifier(this=op.freq))


@register_unary_op(ops.floor_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Floor(this=expr.expr)


@register_unary_op(ops.geo_area_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ST_AREA", expr.expr)


@register_unary_op(ops.geo_st_astext_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ST_ASTEXT", expr.expr)


@register_unary_op(ops.geo_st_boundary_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ST_BOUNDARY", expr.expr)


@register_unary_op(ops.GeoStBufferOp, pass_op=True)
def _(expr: TypedExpr, op: ops.GeoStBufferOp) -> sge.Expression:
    return sge.func(
        "ST_BUFFER",
        expr.expr,
        sge.convert(op.buffer_radius),
        sge.convert(op.num_seg_quarter_circle),
        sge.convert(op.use_spheroid),
    )


@register_unary_op(ops.geo_st_centroid_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ST_CENTROID", expr.expr)


@register_unary_op(ops.geo_st_convexhull_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ST_CONVEXHULL", expr.expr)


@register_unary_op(ops.geo_st_geogfromtext_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("SAFE.ST_GEOGFROMTEXT", expr.expr)


@register_unary_op(ops.geo_st_isclosed_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("ST_ISCLOSED", expr.expr)


@register_unary_op(ops.GeoStLengthOp, pass_op=True)
def _(expr: TypedExpr, op: ops.GeoStLengthOp) -> sge.Expression:
    return sge.func("ST_LENGTH", expr.expr)


@register_unary_op(ops.geo_x_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("SAFE.ST_X", expr.expr)


@register_unary_op(ops.geo_y_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("SAFE.ST_Y", expr.expr)


@register_unary_op(ops.hash_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("FARM_FINGERPRINT", expr.expr)


@register_unary_op(ops.hour_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="HOUR"), expression=expr.expr)


@register_unary_op(ops.invert_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.BitwiseNot(this=expr.expr)


@register_unary_op(ops.IsInOp, pass_op=True)
def _(expr: TypedExpr, op: ops.IsInOp) -> sge.Expression:
    values = []
    is_numeric_expr = dtypes.is_numeric(expr.dtype)
    for value in op.values:
        if value is None:
            continue
        dtype = dtypes.bigframes_type(type(value))
        if expr.dtype == dtype or is_numeric_expr and dtypes.is_numeric(dtype):
            values.append(sge.convert(value))

    if op.match_nulls:
        contains_nulls = any(_is_null(value) for value in op.values)
        if contains_nulls:
            return sge.Is(this=expr.expr, expression=sge.Null()) | sge.In(
                this=expr.expr, expressions=values
            )

    if len(values) == 0:
        return sge.convert(False)

    return sge.func(
        "COALESCE", sge.In(this=expr.expr, expressions=values), sge.convert(False)
    )


@register_unary_op(ops.isalnum_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.RegexpLike(this=expr.expr, expression=sge.convert(r"^(\p{N}|\p{L})+$"))


@register_unary_op(ops.isalpha_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.RegexpLike(this=expr.expr, expression=sge.convert(r"^\p{L}+$"))


@register_unary_op(ops.isdecimal_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.RegexpLike(this=expr.expr, expression=sge.convert(r"^\d+$"))


@register_unary_op(ops.isdigit_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.RegexpLike(this=expr.expr, expression=sge.convert(r"^\p{Nd}+$"))


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


@register_unary_op(ops.iso_day_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="DAYOFWEEK"), expression=expr.expr)


@register_unary_op(ops.iso_week_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="ISOWEEK"), expression=expr.expr)


@register_unary_op(ops.iso_year_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="ISOYEAR"), expression=expr.expr)


@register_unary_op(ops.isnull_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Is(this=expr.expr, expression=sge.Null())


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
    return sge.Length(this=expr.expr)


@register_unary_op(ops.ln_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr < sge.convert(0),
                true=constants._NAN,
            )
        ],
        default=sge.Ln(this=expr.expr),
    )


@register_unary_op(ops.log10_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr < sge.convert(0),
                true=constants._NAN,
            )
        ],
        default=sge.Log(this=expr.expr, expression=sge.convert(10)),
    )


@register_unary_op(ops.log1p_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr < sge.convert(-1),
                true=constants._NAN,
            )
        ],
        default=sge.Ln(this=sge.convert(1) + expr.expr),
    )


@register_unary_op(ops.lower_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Lower(this=expr.expr)


@register_unary_op(ops.MapOp, pass_op=True)
def _(expr: TypedExpr, op: ops.MapOp) -> sge.Expression:
    return sge.Case(
        this=expr.expr,
        ifs=[
            sge.If(this=sge.convert(key), true=sge.convert(value))
            for key, value in op.mappings
        ],
    )


@register_unary_op(ops.minute_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="MINUTE"), expression=expr.expr)


@register_unary_op(ops.month_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="MONTH"), expression=expr.expr)


@register_unary_op(ops.neg_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Neg(this=expr.expr)


@register_unary_op(ops.normalize_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.TimestampTrunc(this=expr.expr, unit=sge.Identifier(this="DAY"))


@register_unary_op(ops.notnull_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Not(this=sge.Is(this=expr.expr, expression=sge.Null()))


@register_unary_op(ops.obj_fetch_metadata_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("OBJ.FETCH_METADATA", expr.expr)


@register_unary_op(ops.ObjGetAccessUrl)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("OBJ.GET_ACCESS_URL", expr.expr)


@register_unary_op(ops.pos_op)
def _(expr: TypedExpr) -> sge.Expression:
    return expr.expr


@register_unary_op(ops.quarter_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="QUARTER"), expression=expr.expr)


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


@register_unary_op(ops.second_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="SECOND"), expression=expr.expr)


@register_unary_op(ops.StrRstripOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrRstripOp) -> sge.Expression:
    return sge.Trim(this=expr.expr, expression=sge.convert(op.to_strip), side="RIGHT")


@register_unary_op(ops.sqrt_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=expr.expr < sge.convert(0),
                true=constants._NAN,
            )
        ],
        default=sge.Sqrt(this=expr.expr),
    )


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
    return sge.Trim(this=sge.convert(op.to_strip), expression=expr.expr)


@register_unary_op(ops.sin_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("SIN", expr.expr)


@register_unary_op(ops.sinh_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.func("ABS", expr.expr) > constants._FLOAT64_EXP_BOUND,
                true=sge.func("SIGN", expr.expr) * constants._INF,
            )
        ],
        default=sge.func("SINH", expr.expr),
    )


@register_unary_op(ops.StringSplitOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StringSplitOp) -> sge.Expression:
    return sge.Split(this=expr.expr, expression=sge.convert(op.pat))


@register_unary_op(ops.StrGetOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrGetOp) -> sge.Expression:
    return sge.Substring(
        this=expr.expr,
        start=sge.convert(op.i + 1),
        length=sge.convert(1),
    )


@register_unary_op(ops.StrSliceOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrSliceOp) -> sge.Expression:
    start = op.start + 1 if op.start is not None else None
    if op.end is None:
        length = None
    elif op.start is None:
        length = op.end
    else:
        length = op.end - op.start
    return sge.Substring(
        this=expr.expr,
        start=sge.convert(start) if start is not None else None,
        length=sge.convert(length) if length is not None else None,
    )


@register_unary_op(ops.StrftimeOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StrftimeOp) -> sge.Expression:
    return sge.func("FORMAT_TIMESTAMP", sge.convert(op.date_format), expr.expr)


@register_unary_op(ops.StructFieldOp, pass_op=True)
def _(expr: TypedExpr, op: ops.StructFieldOp) -> sge.Expression:
    if isinstance(op.name_or_index, str):
        name = op.name_or_index
    else:
        pa_type = typing.cast(pd.ArrowDtype, expr.dtype)
        pa_struct_type = typing.cast(pa.StructType, pa_type.pyarrow_dtype)
        name = pa_struct_type.field(op.name_or_index).name

    return sge.Column(
        this=sge.to_identifier(name, quoted=True),
        catalog=expr.expr,
    )


@register_unary_op(ops.tan_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TAN", expr.expr)


@register_unary_op(ops.tanh_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TANH", expr.expr)


@register_unary_op(ops.time_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TIME", expr.expr)


@register_unary_op(ops.timedelta_floor_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Floor(this=expr.expr)


@register_unary_op(ops.ToDatetimeOp)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Cast(this=sge.func("TIMESTAMP_SECONDS", expr.expr), to="DATETIME")


@register_unary_op(ops.ToTimestampOp)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TIMESTAMP_SECONDS", expr.expr)


@register_unary_op(ops.ToTimedeltaOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ToTimedeltaOp) -> sge.Expression:
    value = expr.expr
    factor = UNIT_TO_US_CONVERSION_FACTORS[op.unit]
    if factor != 1:
        value = sge.Mul(this=value, expression=sge.convert(factor))
    return value


@register_unary_op(ops.UnixMicros)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("UNIX_MICROS", expr.expr)


@register_unary_op(ops.UnixMillis)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("UNIX_MILLIS", expr.expr)


@register_unary_op(ops.UnixSeconds, pass_op=True)
def _(expr: TypedExpr, op: ops.UnixSeconds) -> sge.Expression:
    return sge.func("UNIX_SECONDS", expr.expr)


@register_unary_op(ops.JSONExtract, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONExtract) -> sge.Expression:
    return sge.func("JSON_EXTRACT", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONExtractArray, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONExtractArray) -> sge.Expression:
    return sge.func("JSON_EXTRACT_ARRAY", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONExtractStringArray, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONExtractStringArray) -> sge.Expression:
    return sge.func("JSON_EXTRACT_STRING_ARRAY", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONQuery, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONQuery) -> sge.Expression:
    return sge.func("JSON_QUERY", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONQueryArray, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONQueryArray) -> sge.Expression:
    return sge.func("JSON_QUERY_ARRAY", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONValue, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONValue) -> sge.Expression:
    return sge.func("JSON_VALUE", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.JSONValueArray, pass_op=True)
def _(expr: TypedExpr, op: ops.JSONValueArray) -> sge.Expression:
    return sge.func("JSON_VALUE_ARRAY", expr.expr, sge.convert(op.json_path))


@register_unary_op(ops.ParseJSON)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("PARSE_JSON", expr.expr)


@register_unary_op(ops.ToJSONString)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("TO_JSON_STRING", expr.expr)


@register_unary_op(ops.upper_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Upper(this=expr.expr)


@register_unary_op(ops.year_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Extract(this=sge.Identifier(this="YEAR"), expression=expr.expr)


@register_unary_op(ops.ZfillOp, pass_op=True)
def _(expr: TypedExpr, op: ops.ZfillOp) -> sge.Expression:
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.EQ(
                    this=sge.Substring(
                        this=expr.expr, start=sge.convert(1), length=sge.convert(1)
                    ),
                    expression=sge.convert("-"),
                ),
                true=sge.Concat(
                    expressions=[
                        sge.convert("-"),
                        sge.func(
                            "LPAD",
                            sge.Substring(this=expr.expr, start=sge.convert(1)),
                            sge.convert(op.width - 1),
                            sge.convert("0"),
                        ),
                    ]
                ),
            )
        ],
        default=sge.func("LPAD", expr.expr, sge.convert(op.width), sge.convert("0")),
    )


# Helpers
def _is_null(value) -> bool:
    # float NaN/inf should be treated as distinct from 'true' null values
    return typing.cast(bool, pd.isna(value)) and not isinstance(value, float)
