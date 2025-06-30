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

from bigframes import dtypes
from bigframes.core import bigframe_node, expression
from bigframes.core.rewrite import op_lowering
from bigframes.operations import comparison_ops, numeric_ops
import bigframes.operations as ops

# TODO: Would be more precise to actually have separate op set for polars ops (where they diverge from the original ops)


@dataclasses.dataclass
class CoerceArgsRule(op_lowering.OpLoweringRule):
    op_type: type[ops.BinaryOp]

    @property
    def op(self) -> type[ops.ScalarOp]:
        return self.op_type

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, self.op_type)
        larg, rarg = _coerce_comparables(expr.children[0], expr.children[1])
        return expr.op.as_expr(larg, rarg)


class LowerFloorDivRule(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return numeric_ops.FloorDivOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        dividend = expr.children[0]
        divisor = expr.children[1]
        using_floats = (dividend.output_type == dtypes.FLOAT_DTYPE) or (
            divisor.output_type == dtypes.FLOAT_DTYPE
        )
        inf_or_zero = (
            expression.const(float("INF")) if using_floats else expression.const(0)
        )
        zero_result = ops.mul_op.as_expr(inf_or_zero, dividend)
        divisor_is_zero = ops.eq_op.as_expr(divisor, expression.const(0))
        return ops.where_op.as_expr(zero_result, divisor_is_zero, expr)


def _coerce_comparables(expr1: expression.Expression, expr2: expression.Expression):

    target_type = dtypes.coerce_to_common(expr1.output_type, expr2.output_type)
    if expr1.output_type != target_type:
        expr1 = _lower_cast(ops.AsTypeOp(target_type), expr1)
    if expr2.output_type != target_type:
        expr2 = _lower_cast(ops.AsTypeOp(target_type), expr2)
    return expr1, expr2


# TODO: Need to handle bool->string cast to get capitalization correct
def _lower_cast(cast_op: ops.AsTypeOp, arg: expression.Expression):
    if arg.output_type == dtypes.BOOL_DTYPE and dtypes.is_numeric(cast_op.to_type):
        # bool -> decimal needs two-step cast
        new_arg = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(arg)
        return cast_op.as_expr(new_arg)
    return cast_op.as_expr(arg)


LOWER_COMPARISONS = tuple(
    CoerceArgsRule(op)
    for op in (
        comparison_ops.EqOp,
        comparison_ops.EqNullsMatchOp,
        comparison_ops.NeOp,
        comparison_ops.LtOp,
        comparison_ops.GtOp,
        comparison_ops.LeOp,
        comparison_ops.GeOp,
    )
)

POLARS_LOWERING_RULES = (
    *LOWER_COMPARISONS,
    LowerFloorDivRule(),
)


def lower_ops_to_polars(root: bigframe_node.BigFrameNode) -> bigframe_node.BigFrameNode:
    return op_lowering.lower_ops(root, rules=POLARS_LOWERING_RULES)
