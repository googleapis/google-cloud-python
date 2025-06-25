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

import abc
from typing import Sequence

from bigframes.core import bigframe_node, expression, nodes
import bigframes.operations as ops


class OpLoweringRule(abc.ABC):
    @property
    @abc.abstractmethod
    def op(self) -> type[ops.ScalarOp]:
        ...

    @abc.abstractmethod
    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        ...


def lower_ops(
    root: bigframe_node.BigFrameNode, rules: Sequence[OpLoweringRule]
) -> bigframe_node.BigFrameNode:
    rules_by_op = {rule.op: rule for rule in rules}

    def lower_expr(expr: expression.Expression):
        def lower_expr_step(expr: expression.Expression) -> expression.Expression:
            if isinstance(expr, expression.OpExpression):
                maybe_rule = rules_by_op.get(expr.op.__class__)
                if maybe_rule:
                    return maybe_rule.lower(expr)
            return expr

        return lower_expr_step(expr.transform_children(lower_expr_step))

    def lower_node(node: bigframe_node.BigFrameNode) -> bigframe_node.BigFrameNode:
        if isinstance(
            node, (nodes.ProjectionNode, nodes.FilterNode, nodes.OrderByNode)
        ):
            return node.transform_exprs(lower_expr)
        else:
            return node

    return root.bottom_up(lower_node)
