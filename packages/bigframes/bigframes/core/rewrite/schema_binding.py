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
import typing

from bigframes.core import bigframe_node
from bigframes.core import expression as ex
from bigframes.core import nodes, ordering


def bind_schema_to_tree(
    node: bigframe_node.BigFrameNode,
) -> bigframe_node.BigFrameNode:
    return nodes.bottom_up(node, bind_schema_to_node)


def bind_schema_to_node(
    node: bigframe_node.BigFrameNode,
) -> bigframe_node.BigFrameNode:
    if isinstance(node, nodes.ProjectionNode):
        bound_assignments = tuple(
            (ex.bind_schema_fields(expr, node.child.field_by_id), id)
            for expr, id in node.assignments
        )
        return dataclasses.replace(node, assignments=bound_assignments)

    if isinstance(node, nodes.FilterNode):
        bound_predicate = ex.bind_schema_fields(node.predicate, node.child.field_by_id)
        return dataclasses.replace(node, predicate=bound_predicate)

    if isinstance(node, nodes.OrderByNode):
        bound_bys = []
        for by in node.by:
            bound_by = dataclasses.replace(
                by,
                scalar_expression=ex.bind_schema_fields(
                    by.scalar_expression, node.child.field_by_id
                ),
            )
            bound_bys.append(bound_by)

        return dataclasses.replace(node, by=tuple(bound_bys))

    if isinstance(node, nodes.JoinNode):
        conditions = tuple(
            (
                ex.ResolvedDerefOp.from_field(node.left_child.field_by_id[left.id]),
                ex.ResolvedDerefOp.from_field(node.right_child.field_by_id[right.id]),
            )
            for left, right in node.conditions
        )
        return dataclasses.replace(
            node,
            conditions=conditions,
        )
    if isinstance(node, nodes.InNode):
        return dataclasses.replace(
            node,
            left_col=ex.ResolvedDerefOp.from_field(
                node.left_child.field_by_id[node.left_col.id]
            ),
            right_col=ex.ResolvedDerefOp.from_field(
                node.right_child.field_by_id[node.right_col.id]
            ),
        )

    if isinstance(node, nodes.AggregateNode):
        aggregations = []
        for aggregation, id in node.aggregations:
            aggregations.append(
                (_bind_schema_to_aggregation_expr(aggregation, node.child), id)
            )

        return dataclasses.replace(
            node,
            aggregations=tuple(aggregations),
        )

    if isinstance(node, nodes.WindowOpNode):
        window_spec = dataclasses.replace(
            node.window_spec,
            grouping_keys=tuple(
                typing.cast(
                    ex.DerefOp, ex.bind_schema_fields(expr, node.child.field_by_id)
                )
                for expr in node.window_spec.grouping_keys
            ),
            ordering=tuple(
                ordering.OrderingExpression(
                    scalar_expression=ex.bind_schema_fields(
                        expr.scalar_expression, node.child.field_by_id
                    ),
                    direction=expr.direction,
                    na_last=expr.na_last,
                )
                for expr in node.window_spec.ordering
            ),
        )
        return dataclasses.replace(
            node,
            expression=_bind_schema_to_aggregation_expr(node.expression, node.child),
            window_spec=window_spec,
        )

    return node


def _bind_schema_to_aggregation_expr(
    aggregation: ex.Aggregation,
    child: bigframe_node.BigFrameNode,
) -> ex.Aggregation:
    assert isinstance(
        aggregation, ex.Aggregation
    ), f"Expected Aggregation, got {type(aggregation)}"

    if isinstance(aggregation, ex.UnaryAggregation):
        return typing.cast(
            ex.Aggregation,
            dataclasses.replace(
                aggregation,
                arg=typing.cast(
                    ex.RefOrConstant,
                    ex.bind_schema_fields(aggregation.arg, child.field_by_id),
                ),
            ),
        )
    elif isinstance(aggregation, ex.BinaryAggregation):
        return typing.cast(
            ex.Aggregation,
            dataclasses.replace(
                aggregation,
                left=typing.cast(
                    ex.RefOrConstant,
                    ex.bind_schema_fields(aggregation.left, child.field_by_id),
                ),
                right=typing.cast(
                    ex.RefOrConstant,
                    ex.bind_schema_fields(aggregation.right, child.field_by_id),
                ),
            ),
        )
    else:
        return aggregation
