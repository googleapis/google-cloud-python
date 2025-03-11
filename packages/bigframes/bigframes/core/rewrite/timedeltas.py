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
from bigframes.operations import aggregations as aggs


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

    if isinstance(root, nodes.WindowOpNode):
        return nodes.WindowOpNode(
            root.child,
            _rewrite_aggregation(root.expression, root.schema),
            root.window_spec,
            root.output_name,
            root.never_skip_nulls,
            root.skip_reproject_unsafe,
        )

    if isinstance(root, nodes.AggregateNode):
        updated_aggregations = tuple(
            (_rewrite_aggregation(agg, root.child.schema), col_id)
            for agg, col_id in root.aggregations
        )
        return nodes.AggregateNode(
            root.child,
            updated_aggregations,
            root.by_column_ids,
            root.order_by,
            root.dropna,
        )

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
    if expr.dtype == dtypes.TIMEDELTA_DTYPE:
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

    if isinstance(expr.op, ops.ToTimedeltaOp):
        return _rewrite_to_timedelta_op(expr.op, inputs[0])

    return _TypedExpr.create_op_expr(expr.op, *inputs)


def _rewrite_sub_op(left: _TypedExpr, right: _TypedExpr) -> _TypedExpr:
    if dtypes.is_datetime_like(left.dtype) and dtypes.is_datetime_like(right.dtype):
        return _TypedExpr.create_op_expr(ops.timestamp_diff_op, left, right)

    if dtypes.is_datetime_like(left.dtype) and right.dtype == dtypes.TIMEDELTA_DTYPE:
        return _TypedExpr.create_op_expr(ops.timestamp_sub_op, left, right)

    if left.dtype == dtypes.DATE_DTYPE and right.dtype == dtypes.DATE_DTYPE:
        return _TypedExpr.create_op_expr(ops.date_diff_op, left, right)

    if left.dtype == dtypes.DATE_DTYPE and right.dtype == dtypes.TIMEDELTA_DTYPE:
        return _TypedExpr.create_op_expr(ops.date_sub_op, left, right)

    return _TypedExpr.create_op_expr(ops.sub_op, left, right)


def _rewrite_add_op(left: _TypedExpr, right: _TypedExpr) -> _TypedExpr:
    if dtypes.is_datetime_like(left.dtype) and right.dtype == dtypes.TIMEDELTA_DTYPE:
        return _TypedExpr.create_op_expr(ops.timestamp_add_op, left, right)

    if left.dtype == dtypes.TIMEDELTA_DTYPE and dtypes.is_datetime_like(right.dtype):
        # Re-arrange operands such that timestamp is always on the left and timedelta is
        # always on the right.
        return _TypedExpr.create_op_expr(ops.timestamp_add_op, right, left)

    if left.dtype == dtypes.DATE_DTYPE and right.dtype == dtypes.TIMEDELTA_DTYPE:
        return _TypedExpr.create_op_expr(ops.date_add_op, left, right)

    if left.dtype == dtypes.TIMEDELTA_DTYPE and right.dtype == dtypes.DATE_DTYPE:
        # Re-arrange operands such that date is always on the left and timedelta is
        # always on the right.
        return _TypedExpr.create_op_expr(ops.date_add_op, right, left)

    return _TypedExpr.create_op_expr(ops.add_op, left, right)


def _rewrite_mul_op(left: _TypedExpr, right: _TypedExpr) -> _TypedExpr:
    result = _TypedExpr.create_op_expr(ops.mul_op, left, right)

    if left.dtype == dtypes.TIMEDELTA_DTYPE and dtypes.is_numeric(right.dtype):
        return _TypedExpr.create_op_expr(ops.timedelta_floor_op, result)
    if dtypes.is_numeric(left.dtype) and right.dtype == dtypes.TIMEDELTA_DTYPE:
        return _TypedExpr.create_op_expr(ops.timedelta_floor_op, result)

    return result


def _rewrite_div_op(left: _TypedExpr, right: _TypedExpr) -> _TypedExpr:
    result = _TypedExpr.create_op_expr(ops.div_op, left, right)

    if left.dtype == dtypes.TIMEDELTA_DTYPE and dtypes.is_numeric(right.dtype):
        return _TypedExpr.create_op_expr(ops.timedelta_floor_op, result)

    return result


def _rewrite_floordiv_op(left: _TypedExpr, right: _TypedExpr) -> _TypedExpr:
    result = _TypedExpr.create_op_expr(ops.floordiv_op, left, right)

    if left.dtype == dtypes.TIMEDELTA_DTYPE and dtypes.is_numeric(right.dtype):
        return _TypedExpr.create_op_expr(ops.timedelta_floor_op, result)

    return result


def _rewrite_to_timedelta_op(op: ops.ToTimedeltaOp, arg: _TypedExpr):
    if arg.dtype == dtypes.TIMEDELTA_DTYPE:
        # Do nothing for values that are already timedeltas
        return arg

    return _TypedExpr.create_op_expr(op, arg)


@functools.cache
def _rewrite_aggregation(
    aggregation: ex.Aggregation, schema: schema.ArraySchema
) -> ex.Aggregation:
    if not isinstance(aggregation, ex.UnaryAggregation):
        return aggregation

    if isinstance(aggregation.arg, ex.DerefOp):
        input_type = schema.get_type(aggregation.arg.id.sql)
    else:
        input_type = aggregation.arg.dtype

    if isinstance(aggregation.op, aggs.DiffOp):
        if dtypes.is_datetime_like(input_type):
            return ex.UnaryAggregation(
                aggs.TimeSeriesDiffOp(aggregation.op.periods), aggregation.arg
            )
        elif input_type == dtypes.DATE_DTYPE:
            return ex.UnaryAggregation(
                aggs.DateSeriesDiffOp(aggregation.op.periods), aggregation.arg
            )

    if isinstance(aggregation.op, aggs.StdOp) and input_type == dtypes.TIMEDELTA_DTYPE:
        return ex.UnaryAggregation(
            aggs.StdOp(should_floor_result=True), aggregation.arg
        )

    if isinstance(aggregation.op, aggs.MeanOp) and input_type == dtypes.TIMEDELTA_DTYPE:
        return ex.UnaryAggregation(
            aggs.MeanOp(should_floor_result=True), aggregation.arg
        )

    if (
        isinstance(aggregation.op, aggs.QuantileOp)
        and input_type == dtypes.TIMEDELTA_DTYPE
    ):
        return ex.UnaryAggregation(
            aggs.QuantileOp(q=aggregation.op.q, should_floor_result=True),
            aggregation.arg,
        )

    return aggregation
