# Copyright 2026 Google LLC
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

import bigframes.functions.udf_def as udf_def
import bigframes.operations as ops
from bigframes.core import bigframe_node, expression
from bigframes.core.rewrite import op_lowering


@dataclasses.dataclass
class LowerRemoteFunctionRule(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return ops.RemoteFunctionOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, ops.RemoteFunctionOp)
        func_def = expr.op.function_def
        devirtualized_expr = ops.RemoteFunctionOp(
            func_def.with_devirtualize(),
            apply_on_null=expr.op.apply_on_null,
        ).as_expr(*expr.children)
        if isinstance(func_def.signature.output, udf_def.VirtualListTypeV1):
            return func_def.signature.output.out_expr(devirtualized_expr)
        else:
            return devirtualized_expr


@dataclasses.dataclass
class LowerBinaryRemoteFunctionRule(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return ops.BinaryRemoteFunctionOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, ops.BinaryRemoteFunctionOp)
        func_def = expr.op.function_def
        devirtualized_expr = ops.BinaryRemoteFunctionOp(
            func_def.with_devirtualize(),
        ).as_expr(*expr.children)
        if isinstance(func_def.signature.output, udf_def.VirtualListTypeV1):
            return func_def.signature.output.out_expr(devirtualized_expr)
        else:
            return devirtualized_expr


@dataclasses.dataclass
class LowerNaryRemoteFunctionRule(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return ops.NaryRemoteFunctionOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, ops.NaryRemoteFunctionOp)
        func_def = expr.op.function_def
        devirtualized_expr = ops.NaryRemoteFunctionOp(
            func_def.with_devirtualize(),
        ).as_expr(*expr.children)
        if isinstance(func_def.signature.output, udf_def.VirtualListTypeV1):
            return func_def.signature.output.out_expr(devirtualized_expr)
        else:
            return devirtualized_expr


UDF_LOWERING_RULES = (
    LowerRemoteFunctionRule(),
    LowerBinaryRemoteFunctionRule(),
    LowerNaryRemoteFunctionRule(),
)


def lower_udfs(root: bigframe_node.BigFrameNode) -> bigframe_node.BigFrameNode:
    return op_lowering.lower_ops(root, rules=UDF_LOWERING_RULES)
