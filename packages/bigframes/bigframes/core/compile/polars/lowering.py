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

from bigframes import dtypes
from bigframes.core import bigframe_node, expression
from bigframes.core.rewrite import op_lowering
from bigframes.operations import numeric_ops
import bigframes.operations as ops

# TODO: Would be more precise to actually have separate op set for polars ops (where they diverge from the original ops)


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


POLARS_LOWERING_RULES = (LowerFloorDivRule(),)


def lower_ops_to_polars(root: bigframe_node.BigFrameNode) -> bigframe_node.BigFrameNode:
    return op_lowering.lower_ops(root, rules=POLARS_LOWERING_RULES)
