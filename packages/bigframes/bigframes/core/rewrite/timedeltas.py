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

import dataclasses
import functools
import typing

from bigframes import dtypes
from bigframes import operations as ops
from bigframes.core import expression as ex
from bigframes.core import nodes, schema, utils


@dataclasses.dataclass
class _TypedExpr:
    expr: ex.Expression
    dtype: dtypes.Dtype

    @classmethod
    def create_op_expr(
        cls, op: typing.Union[ops.ScalarOp, ops.RowOp], *inputs: _TypedExpr
    ) -> _TypedExpr:
        expr = op.as_expr(*tuple(x.expr for x in inputs))  # type: ignore
        dtype = op.output_type(*tuple(x.dtype for x in inputs))
        return cls(expr, dtype)


def rewrite_timedelta_expressions(root: nodes.BigFrameNode) -> nodes.BigFrameNode:
    """
    Rewrites expressions to properly handle timedelta values, because this type does not exist
    in the SQL world.
    """
    if isinstance(root, nodes.ProjectionNode):
        updated_assignments = tuple(
            (_rewrite_expressions(expr, root.schema).expr, column_id)
            for expr, column_id in root.assignments
        )
        return nodes.ProjectionNode(root.child, updated_assignments)

    if isinstance(root, nodes.FilterNode):
        return nodes.FilterNode(
            root.child, _rewrite_expressions(root.predicate, root.schema).expr
        )

    if isinstance(root, nodes.OrderByNode):
        by = tuple(_rewrite_ordering_expr(x, root.schema) for x in root.by)
        return nodes.OrderByNode(root.child, by)

    return root


def _rewrite_ordering_expr(
    expr: nodes.OrderingExpression, schema: schema.ArraySchema
) -> nodes.OrderingExpression:
    by = _rewrite_expressions(expr.scalar_expression, schema).expr
    return nodes.OrderingExpression(by, expr.direction, expr.na_last)


@functools.cache
def _rewrite_expressions(expr: ex.Expression, schema: schema.ArraySchema) -> _TypedExpr:
    if isinstance(expr, ex.DerefOp):
        return _TypedExpr(expr, schema.get_type(expr.id.sql))

    if isinstance(expr, ex.ScalarConstantExpression):
        return _rewrite_scalar_constant_expr(expr)

    if isinstance(expr, ex.OpExpression):
        updated_inputs = tuple(
            map(lambda x: _rewrite_expressions(x, schema), expr.inputs)
        )
        return _rewrite_op_expr(expr, updated_inputs)

    raise AssertionError(f"Unexpected expression type: {type(expr)}")


def _rewrite_scalar_constant_expr(expr: ex.ScalarConstantExpression) -> _TypedExpr:
    if expr.dtype is dtypes.TIMEDELTA_DTYPE:
        int_repr = utils.timedelta_to_micros(expr.value)  # type: ignore
        return _TypedExpr(ex.const(int_repr, expr.dtype), expr.dtype)

    return _TypedExpr(expr, expr.dtype)


def _rewrite_op_expr(
    expr: ex.OpExpression, inputs: typing.Tuple[_TypedExpr, ...]
) -> _TypedExpr:
    if isinstance(expr.op, ops.SubOp):
        return _rewrite_sub_op(inputs[0], inputs[1])

    if isinstance(expr.op, ops.AddOp):
        return _rewrite_add_op(inputs[0], inputs[1])

    if isinstance(expr.op, ops.MulOp):
        return _rewrite_mul_op(inputs[0], inputs[1])

    if isinstance(expr.op, ops.DivOp):
        return _rewrite_div_op(inputs[0], inputs[1])

    if isinstance(expr.op, ops.FloorDivOp):
        # We need to re-write floor div because for numerics: int // float => float
        # but for timedeltas: int(timedelta) // float => int(timedelta)
        return _rewrite_floordiv_op(inputs[0], inputs[1])

    return _TypedExpr.create_op_expr(expr.op, *inputs)


def _rewrite_sub_op(left: _TypedExpr, right: _TypedExpr) -> _TypedExpr:
    if dtypes.is_datetime_like(left.dtype) and dtypes.is_datetime_like(right.dtype):
        return _TypedExpr.create_op_expr(ops.timestamp_diff_op, left, right)

    if dtypes.is_datetime_like(left.dtype) and right.dtype is dtypes.TIMEDELTA_DTYPE:
        return _TypedExpr.create_op_expr(ops.timestamp_sub_op, left, right)

    return _TypedExpr.create_op_expr(ops.sub_op, left, right)


def _rewrite_add_op(left: _TypedExpr, right: _TypedExpr) -> _TypedExpr:
    if dtypes.is_datetime_like(left.dtype) and right.dtype is dtypes.TIMEDELTA_DTYPE:
        return _TypedExpr.create_op_expr(ops.timestamp_add_op, left, right)

    if left.dtype is dtypes.TIMEDELTA_DTYPE and dtypes.is_datetime_like(right.dtype):
        # Re-arrange operands such that timestamp is always on the left and timedelta is
        # always on the right.
        return _TypedExpr.create_op_expr(ops.timestamp_add_op, right, left)

    return _TypedExpr.create_op_expr(ops.add_op, left, right)


def _rewrite_mul_op(left: _TypedExpr, right: _TypedExpr) -> _TypedExpr:
    result = _TypedExpr.create_op_expr(ops.mul_op, left, right)

    if left.dtype is dtypes.TIMEDELTA_DTYPE and dtypes.is_numeric(right.dtype):
        return _TypedExpr.create_op_expr(ops.ToTimedeltaOp("us"), result)
    if dtypes.is_numeric(left.dtype) and right.dtype is dtypes.TIMEDELTA_DTYPE:
        return _TypedExpr.create_op_expr(ops.ToTimedeltaOp("us"), result)

    return result


def _rewrite_div_op(left: _TypedExpr, right: _TypedExpr) -> _TypedExpr:
    result = _TypedExpr.create_op_expr(ops.div_op, left, right)

    if left.dtype is dtypes.TIMEDELTA_DTYPE and dtypes.is_numeric(right.dtype):
        return _TypedExpr.create_op_expr(ops.ToTimedeltaOp("us"), result)

    return result


def _rewrite_floordiv_op(left: _TypedExpr, right: _TypedExpr) -> _TypedExpr:
    result = _TypedExpr.create_op_expr(ops.floordiv_op, left, right)

    if left.dtype is dtypes.TIMEDELTA_DTYPE and dtypes.is_numeric(right.dtype):
        return _TypedExpr.create_op_expr(ops.ToTimedeltaOp("us"), result)

    return result
