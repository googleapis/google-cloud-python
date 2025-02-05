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

import dataclasses
import functools
import typing

from bigframes import dtypes
from bigframes import operations as ops
from bigframes.core import expression as ex
from bigframes.core import nodes, schema


@dataclasses.dataclass
class _TypedExpr:
    expr: ex.Expression
    dtype: dtypes.Dtype


def rewrite_timedelta_ops(root: nodes.BigFrameNode) -> nodes.BigFrameNode:
    """
    Rewrites expressions to properly handle timedelta values, because this type does not exist
    in the SQL world.
    """
    if isinstance(root, nodes.ProjectionNode):
        updated_assignments = tuple(
            (_rewrite_expressions(expr, root.schema).expr, column_id)
            for expr, column_id in root.assignments
        )
        root = nodes.ProjectionNode(root.child, updated_assignments)

    # TODO(b/394354614): FilterByNode and OrderNode also contain expressions. Need to update them too.
    return root


@functools.cache
def _rewrite_expressions(expr: ex.Expression, schema: schema.ArraySchema) -> _TypedExpr:
    if isinstance(expr, ex.DerefOp):
        return _TypedExpr(expr, schema.get_type(expr.id.sql))

    if isinstance(expr, ex.ScalarConstantExpression):
        return _TypedExpr(expr, expr.dtype)

    if isinstance(expr, ex.OpExpression):
        updated_inputs = tuple(
            map(lambda x: _rewrite_expressions(x, schema), expr.inputs)
        )
        return _rewrite_op_expr(expr, updated_inputs)

    raise AssertionError(f"Unexpected expression type: {type(expr)}")


def _rewrite_op_expr(
    expr: ex.OpExpression, inputs: typing.Tuple[_TypedExpr, ...]
) -> _TypedExpr:
    if isinstance(expr.op, ops.SubOp):
        return _rewrite_sub_op(inputs[0], inputs[1])

    input_types = tuple(map(lambda x: x.dtype, inputs))
    return _TypedExpr(expr, expr.op.output_type(*input_types))


def _rewrite_sub_op(left: _TypedExpr, right: _TypedExpr) -> _TypedExpr:
    result_op: ops.BinaryOp = ops.sub_op
    if dtypes.is_datetime_like(left.dtype) and dtypes.is_datetime_like(right.dtype):
        result_op = ops.timestamp_diff_op

    return _TypedExpr(
        result_op.as_expr(left.expr, right.expr),
        result_op.output_type(left.dtype, right.dtype),
    )
