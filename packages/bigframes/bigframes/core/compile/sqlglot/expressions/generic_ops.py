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

import bigframes_vendored.sqlglot as sg
import bigframes_vendored.sqlglot.expressions as sge

from bigframes import dtypes
from bigframes import operations as ops
from bigframes.core.compile.sqlglot import sqlglot_ir, sqlglot_types
from bigframes.core.compile.sqlglot.expressions.typed_expr import TypedExpr
import bigframes.core.compile.sqlglot.scalar_compiler as scalar_compiler

register_unary_op = scalar_compiler.scalar_op_compiler.register_unary_op
register_binary_op = scalar_compiler.scalar_op_compiler.register_binary_op
register_nary_op = scalar_compiler.scalar_op_compiler.register_nary_op
register_ternary_op = scalar_compiler.scalar_op_compiler.register_ternary_op


@register_unary_op(ops.AsTypeOp, pass_op=True)
def _(expr: TypedExpr, op: ops.AsTypeOp) -> sge.Expression:
    from_type = expr.dtype
    to_type = op.to_type
    sg_to_type = sqlglot_types.from_bigframes_dtype(to_type)
    sg_expr = expr.expr

    if to_type == dtypes.JSON_DTYPE:
        return _cast_to_json(expr, op)

    if from_type == dtypes.JSON_DTYPE:
        return _cast_from_json(expr, op)

    if to_type == dtypes.INT_DTYPE:
        result = _cast_to_int(expr, op)
        if result is not None:
            return result

    if to_type == dtypes.FLOAT_DTYPE and from_type == dtypes.BOOL_DTYPE:
        sg_expr = _cast(sg_expr, "INT64", op.safe)
        return _cast(sg_expr, sg_to_type, op.safe)

    if to_type == dtypes.BOOL_DTYPE:
        if from_type == dtypes.BOOL_DTYPE:
            return sg_expr
        else:
            return sge.NEQ(this=sg_expr, expression=sge.convert(0))

    if to_type == dtypes.STRING_DTYPE:
        sg_expr = _cast(sg_expr, sg_to_type, op.safe)
        if from_type == dtypes.BOOL_DTYPE:
            sg_expr = sge.func("INITCAP", sg_expr)
        return sg_expr

    if dtypes.is_time_like(to_type) and from_type == dtypes.INT_DTYPE:
        sg_expr = sge.func("TIMESTAMP_MICROS", sg_expr)
        return _cast(sg_expr, sg_to_type, op.safe)

    return _cast(sg_expr, sg_to_type, op.safe)


@register_unary_op(ops.hash_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.func("FARM_FINGERPRINT", expr.expr)


@register_unary_op(ops.invert_op)
def _(expr: TypedExpr) -> sge.Expression:
    if expr.dtype == dtypes.BOOL_DTYPE:
        return sge.Not(this=sge.paren(expr.expr))
    return sge.BitwiseNot(this=sge.paren(expr.expr))


@register_nary_op(ops.SqlScalarOp, pass_op=True)
def _(*operands: TypedExpr, op: ops.SqlScalarOp) -> sge.Expression:
    return sg.parse_one(
        op.sql_template.format(
            *[operand.expr.sql(dialect="bigquery") for operand in operands]
        ),
        dialect="bigquery",
    )


@register_unary_op(ops.isnull_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Is(this=expr.expr, expression=sge.Null())


@register_unary_op(ops.MapOp, pass_op=True)
def _(expr: TypedExpr, op: ops.MapOp) -> sge.Expression:
    if len(op.mappings) == 0:
        return expr.expr

    mappings = [
        (
            sqlglot_ir._literal(key, dtypes.is_compatible(key, expr.dtype)),
            sqlglot_ir._literal(value, dtypes.is_compatible(value, expr.dtype)),
        )
        for key, value in op.mappings
    ]
    return sge.Case(
        ifs=[
            sge.If(
                this=sge.EQ(this=expr.expr, expression=key)
                if not sqlglot_ir._is_null_literal(key)
                else sge.Is(this=expr.expr, expression=sge.Null()),
                true=value,
            )
            for key, value in mappings
        ],
        default=expr.expr,
    )


@register_unary_op(ops.notnull_op)
def _(expr: TypedExpr) -> sge.Expression:
    return sge.Not(this=sge.Is(this=expr.expr, expression=sge.Null()))


@register_ternary_op(ops.where_op)
def _(
    original: TypedExpr, condition: TypedExpr, replacement: TypedExpr
) -> sge.Expression:
    return sge.If(this=condition.expr, true=original.expr, false=replacement.expr)


@register_ternary_op(ops.clip_op)
def _(
    original: TypedExpr,
    lower: TypedExpr,
    upper: TypedExpr,
) -> sge.Expression:
    return sge.Greatest(
        this=sge.Least(this=original.expr, expressions=[upper.expr]),
        expressions=[lower.expr],
    )


@register_binary_op(ops.fillna_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    return sge.Coalesce(this=left.expr, expressions=[right.expr])


@register_unary_op(ops.RemoteFunctionOp, pass_op=True)
def _(expr: TypedExpr, op: ops.RemoteFunctionOp) -> sge.Expression:
    routine_ref = op.function_def.routine_ref
    # Quote project, dataset, and routine IDs to avoid keyword clashes.
    func_name = (
        f"`{routine_ref.project}`.`{routine_ref.dataset_id}`.`{routine_ref.routine_id}`"
    )
    func = sge.func(func_name, expr.expr)

    if not op.apply_on_null:
        return sge.If(
            this=sge.Is(this=expr.expr, expression=sge.Null()),
            true=expr.expr,
            false=func,
        )

    return func


@register_binary_op(ops.BinaryRemoteFunctionOp, pass_op=True)
def _(
    left: TypedExpr, right: TypedExpr, op: ops.BinaryRemoteFunctionOp
) -> sge.Expression:
    routine_ref = op.function_def.routine_ref
    # Quote project, dataset, and routine IDs to avoid keyword clashes.
    func_name = (
        f"`{routine_ref.project}`.`{routine_ref.dataset_id}`.`{routine_ref.routine_id}`"
    )

    return sge.func(func_name, left.expr, right.expr)


@register_nary_op(ops.case_when_op)
def _(*cases_and_outputs: TypedExpr) -> sge.Expression:
    # Need to upcast BOOL to INT if any output is numeric
    result_values = cases_and_outputs[1::2]
    do_upcast_bool = any(
        dtypes.is_numeric(t.dtype, include_bool=False) for t in result_values
    )
    if do_upcast_bool:
        result_values = tuple(
            TypedExpr(
                sge.Cast(this=val.expr, to="INT64"),
                dtypes.INT_DTYPE,
            )
            if val.dtype == dtypes.BOOL_DTYPE
            else val
            for val in result_values
        )

    return sge.Case(
        ifs=[
            sge.If(this=predicate.expr, true=output.expr)
            for predicate, output in zip(cases_and_outputs[::2], result_values)
        ],
    )


@register_binary_op(ops.coalesce_op)
def _(left: TypedExpr, right: TypedExpr) -> sge.Expression:
    if left.expr == right.expr:
        return left.expr
    return sge.Coalesce(this=left.expr, expressions=[right.expr])


@register_nary_op(ops.RowKey)
def _(*values: TypedExpr) -> sge.Expression:
    # All inputs into hash must be non-null or resulting hash will be null
    str_values = [_convert_to_nonnull_string_sqlglot(value) for value in values]

    full_row_hash_p1 = sge.func("FARM_FINGERPRINT", sge.Concat(expressions=str_values))

    # By modifying value slightly, we get another hash uncorrelated with the first
    full_row_hash_p2 = sge.func(
        "FARM_FINGERPRINT", sge.Concat(expressions=[*str_values, sge.convert("_")])
    )

    # Used to disambiguate between identical rows (which will have identical hash)
    random_hash_p3 = sge.func("RAND")

    return sge.Concat(
        expressions=[
            sge.Cast(this=full_row_hash_p1, to="STRING"),
            sge.Cast(this=full_row_hash_p2, to="STRING"),
            sge.Cast(this=random_hash_p3, to="STRING"),
        ]
    )


# Helper functions
def _cast_to_json(expr: TypedExpr, op: ops.AsTypeOp) -> sge.Expression:
    from_type = expr.dtype
    sg_expr = expr.expr

    if from_type == dtypes.STRING_DTYPE:
        func_name = "PARSE_JSON_IN_SAFE" if op.safe else "PARSE_JSON"
        return sge.func(func_name, sg_expr)
    if from_type in (dtypes.INT_DTYPE, dtypes.BOOL_DTYPE, dtypes.FLOAT_DTYPE):
        sg_expr = sge.Cast(this=sg_expr, to="STRING")
        return sge.func("PARSE_JSON", sg_expr)
    raise TypeError(f"Cannot cast from {from_type} to {dtypes.JSON_DTYPE}")


def _cast_from_json(expr: TypedExpr, op: ops.AsTypeOp) -> sge.Expression:
    to_type = op.to_type
    sg_expr = expr.expr
    func_name = ""
    if to_type == dtypes.INT_DTYPE:
        func_name = "INT64"
    elif to_type == dtypes.FLOAT_DTYPE:
        func_name = "FLOAT64"
    elif to_type == dtypes.BOOL_DTYPE:
        func_name = "BOOL"
    elif to_type == dtypes.STRING_DTYPE:
        func_name = "STRING"
    if func_name:
        func_name = "SAFE." + func_name if op.safe else func_name
        return sge.func(func_name, sg_expr)
    raise TypeError(f"Cannot cast from {dtypes.JSON_DTYPE} to {to_type}")


def _cast_to_int(expr: TypedExpr, op: ops.AsTypeOp) -> sge.Expression | None:
    from_type = expr.dtype
    sg_expr = expr.expr
    # Cannot cast DATETIME to INT directly so need to convert to TIMESTAMP first.
    if from_type == dtypes.DATETIME_DTYPE:
        sg_expr = _cast(sg_expr, "TIMESTAMP", op.safe)
        return sge.func("UNIX_MICROS", sg_expr)
    if from_type == dtypes.TIMESTAMP_DTYPE:
        return sge.func("UNIX_MICROS", sg_expr)
    if from_type == dtypes.TIME_DTYPE:
        return sge.func(
            "TIME_DIFF",
            _cast(sg_expr, "TIME", op.safe),
            sge.convert("00:00:00"),
            "MICROSECOND",
        )
    if from_type == dtypes.NUMERIC_DTYPE or from_type == dtypes.FLOAT_DTYPE:
        sg_expr = sge.func("TRUNC", sg_expr)
        return _cast(sg_expr, "INT64", op.safe)
    return None


def _cast(expr: sge.Expression, to: str, safe: bool):
    if safe:
        return sge.TryCast(this=expr, to=to)
    else:
        return sge.Cast(this=expr, to=to)


def _convert_to_nonnull_string_sqlglot(expr: TypedExpr) -> sge.Expression:
    col_type = expr.dtype
    sg_expr = expr.expr

    if col_type == dtypes.STRING_DTYPE:
        result = sg_expr
    elif (
        dtypes.is_numeric(col_type)
        or dtypes.is_time_or_date_like(col_type)
        or col_type == dtypes.BYTES_DTYPE
    ):
        result = sge.Cast(this=sg_expr, to="STRING")
    elif col_type == dtypes.GEO_DTYPE:
        result = sge.func("ST_ASTEXT", sg_expr)
    else:
        # TO_JSON_STRING works with all data types, but isn't the most efficient
        # Needed for JSON, STRUCT and ARRAY datatypes
        result = sge.func("TO_JSON_STRING", sg_expr)

    # Escape backslashes and use backslash as delineator
    escaped = sge.func(
        "REPLACE",
        sge.func("COALESCE", result, sge.convert("")),
        sge.convert("\\"),
        sge.convert("\\\\"),
    )
    return sge.Concat(expressions=[sge.convert("\\"), escaped])
