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

from functools import singledispatch

from bigframes.core import expression as ex
from bigframes.core import nodes, ordering


@singledispatch
def find_order_direction(
    root: nodes.BigFrameNode, column_id: str
) -> ordering.OrderingDirection | None:
    """Returns the order of the given column with tree traversal. If the column cannot be found,
    or the ordering information is not available, return None.
    """
    return None


@find_order_direction.register
def _(root: nodes.OrderByNode, column_id: str):
    if len(root.by) == 0:
        # This is a no-op
        return find_order_direction(root.child, column_id)

    # Make sure the window key is the prefix of sorting keys.
    order_expr = root.by[0]
    scalar_expr = order_expr.scalar_expression
    if isinstance(scalar_expr, ex.DerefOp) and scalar_expr.id.name == column_id:
        return order_expr.direction

    return None


@find_order_direction.register
def _(root: nodes.ReversedNode, column_id: str):
    direction = find_order_direction(root.child, column_id)

    if direction is None:
        return None
    return direction.reverse()


@find_order_direction.register
def _(root: nodes.SelectionNode, column_id: str):
    for alias_ref in root.input_output_pairs:
        if alias_ref.id.name == column_id:
            return find_order_direction(root.child, alias_ref.ref.id.name)


@find_order_direction.register
def _(root: nodes.FilterNode, column_id: str):
    return find_order_direction(root.child, column_id)


@find_order_direction.register
def _(root: nodes.InNode, column_id: str):
    return find_order_direction(root.left_child, column_id)


@find_order_direction.register
def _(root: nodes.WindowOpNode, column_id: str):
    return find_order_direction(root.child, column_id)


@find_order_direction.register
def _(root: nodes.ProjectionNode, column_id: str):
    for expr, ref in root.assignments:
        if ref.name == column_id and isinstance(expr, ex.DerefOp):
            # This source column is renamed.
            return find_order_direction(root.child, expr.id.name)

    return find_order_direction(root.child, column_id)
