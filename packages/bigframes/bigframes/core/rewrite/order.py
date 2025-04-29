# Copyright 2024 Google LLC
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
from typing import Mapping, Tuple

from bigframes.core import expression, identifiers
import bigframes.core.nodes
import bigframes.core.ordering
import bigframes.core.window_spec
from bigframes.operations import aggregations as agg_ops


def defer_order(
    root: bigframes.core.nodes.ResultNode, output_hidden_row_keys: bool
) -> bigframes.core.nodes.ResultNode:
    new_child, order = _pull_up_order(root.child, order_root=True)
    order_by = (
        order.with_ordering_columns(root.order_by.all_ordering_columns)
        if root.order_by
        else order
    )
    if output_hidden_row_keys:
        output_names = tuple((expression.DerefOp(id), id.sql) for id in new_child.ids)
    else:
        output_names = root.output_cols
    return dataclasses.replace(
        root, output_cols=output_names, child=new_child, order_by=order_by
    )


def bake_order(
    node: bigframes.core.nodes.BigFrameNode,
) -> bigframes.core.nodes.BigFrameNode:
    node, _ = _pull_up_order(node, order_root=False)
    return node


# Makes ordering explicit in window definitions
def _pull_up_order(
    root: bigframes.core.nodes.BigFrameNode,
    *,
    order_root: bool = True,
) -> Tuple[bigframes.core.nodes.BigFrameNode, bigframes.core.ordering.RowOrdering]:
    """
    Pull the ordering up, putting full order definition into window ops.

    May create extra colums, which must be removed by callers if they want to preserve original schema.

    Requires the following nodes to be removed/rewritten: SliceNode

    """

    @functools.cache
    def pull_up_order_inner(
        node: bigframes.core.nodes.BigFrameNode,
    ) -> Tuple[bigframes.core.nodes.BigFrameNode, bigframes.core.ordering.RowOrdering]:
        """Pull filter nodes out of a tree section."""
        if isinstance(node, bigframes.core.nodes.ReversedNode):
            child_result, child_order = pull_up_order_inner(node.child)
            return child_result, child_order.with_reverse()
        elif isinstance(node, bigframes.core.nodes.OrderByNode):
            if node.is_total_order:
                new_node = remove_order(node.child)
            else:
                new_node, child_order = pull_up_order_inner(node.child)

            new_by = []
            ids: list[identifiers.ColumnId] = []
            for part in node.by:
                if not isinstance(
                    part.scalar_expression, bigframes.core.expression.DerefOp
                ):
                    id = identifiers.ColumnId.unique()
                    new_node = bigframes.core.nodes.ProjectionNode(
                        new_node, ((part.scalar_expression, id),)
                    )
                    new_part = bigframes.core.ordering.OrderingExpression(
                        bigframes.core.expression.DerefOp(id),
                        part.direction,
                        part.na_last,
                    )
                    new_by.append(new_part)
                    ids.append(id)
                else:
                    new_by.append(part)
                    ids.append(part.scalar_expression.id)

            if node.is_total_order:
                new_order: bigframes.core.ordering.RowOrdering = (
                    bigframes.core.ordering.TotalOrdering(
                        ordering_value_columns=tuple(new_by),
                        total_ordering_columns=frozenset(
                            map(lambda x: bigframes.core.expression.DerefOp(x), ids)
                        ),
                    )
                )
            else:
                assert child_order
                new_order = child_order.with_ordering_columns(new_by)
            return new_node, new_order
        elif isinstance(node, bigframes.core.nodes.ProjectionNode):
            child_result, child_order = pull_up_order_inner(node.child)
            return node.replace_child(child_result), child_order
        elif isinstance(node, bigframes.core.nodes.JoinNode):
            if node.propogate_order:
                return pull_order_join(node)
            else:
                return (
                    dataclasses.replace(
                        node,
                        left_child=remove_order_strict(node.left_child),
                        right_child=remove_order_strict(node.right_child),
                    ),
                    bigframes.core.ordering.RowOrdering(),
                )
        elif isinstance(node, bigframes.core.nodes.ConcatNode):
            return pull_order_concat(node)
        elif isinstance(node, bigframes.core.nodes.FromRangeNode):
            new_start = remove_order_strict(node.start)
            new_end = remove_order_strict(node.end)

            new_node = dataclasses.replace(node, start=new_start, end=new_end)
            return node, bigframes.core.ordering.TotalOrdering.from_primary_key(
                [node.output_id]
            )
        elif isinstance(node, bigframes.core.nodes.ReadLocalNode):
            if node.offsets_col is None:
                offsets_id = identifiers.ColumnId.unique()
                new_root = dataclasses.replace(node, offsets_col=offsets_id)
                return new_root, bigframes.core.ordering.TotalOrdering.from_offset_col(
                    offsets_id
                )
            else:
                return node, bigframes.core.ordering.TotalOrdering.from_offset_col(
                    node.offsets_col
                )
        elif isinstance(node, bigframes.core.nodes.ReadTableNode):
            if node.source.ordering is not None:
                return node.with_order_cols()
            else:
                # No defined ordering
                return node, bigframes.core.ordering.RowOrdering()
        elif isinstance(node, bigframes.core.nodes.PromoteOffsetsNode):
            child_result, child_order = pull_up_order_inner(node.child)
            if child_order.is_total_ordering and child_order.is_sequential:
                # special case, we can just project the ordering
                order_expression = child_order.total_order_col
                assert order_expression is not None
                order_expression.scalar_expression
                new_node = bigframes.core.nodes.ProjectionNode(
                    child_result, ((order_expression.scalar_expression, node.col_id),)
                )
                return new_node, bigframes.core.ordering.TotalOrdering.from_offset_col(
                    node.col_id
                )
            else:
                # Otherwise we need to generate offsets
                agg = bigframes.core.expression.NullaryAggregation(
                    agg_ops.RowNumberOp()
                )
                window_spec = bigframes.core.window_spec.unbound(
                    ordering=tuple(child_order.all_ordering_columns)
                )
                new_offsets_node = bigframes.core.nodes.WindowOpNode(
                    child_result, agg, window_spec, node.col_id
                )
                return (
                    new_offsets_node,
                    bigframes.core.ordering.TotalOrdering.from_offset_col(node.col_id),
                )
        elif isinstance(node, bigframes.core.nodes.FilterNode):
            child_result, child_order = pull_up_order_inner(node.child)
            return node.replace_child(child_result), child_order.with_non_sequential()
        elif isinstance(node, bigframes.core.nodes.InNode):
            child_result, child_order = pull_up_order_inner(node.left_child)
            subquery_result = remove_order_strict(node.right_child)
            return (
                dataclasses.replace(
                    node, left_child=child_result, right_child=subquery_result
                ),
                child_order,
            )
        elif isinstance(node, bigframes.core.nodes.SelectionNode):
            child_result, child_order = pull_up_order_inner(node.child)
            selected_ids = set(ref.id for ref, _ in node.input_output_pairs)
            unselected_order_cols = tuple(
                col for col in child_order.referenced_columns if col not in selected_ids
            )
            # Create unique ids just to be safe
            new_selections = {
                col: identifiers.ColumnId.unique() for col in unselected_order_cols
            }
            all_selections = node.input_output_pairs + tuple(
                bigframes.core.nodes.AliasedRef(bigframes.core.expression.DerefOp(k), v)
                for k, v in new_selections.items()
            )
            new_select_node = dataclasses.replace(
                node, child=child_result, input_output_pairs=all_selections
            )
            new_order = child_order.remap_column_refs(new_select_node.get_id_mapping())
            return new_select_node, new_order
        elif isinstance(node, bigframes.core.nodes.AggregateNode):
            if node.has_ordered_ops:
                child_result, child_order = pull_up_order_inner(node.child)
                new_order_by = child_order.with_ordering_columns(node.order_by)
                new_order = bigframes.core.ordering.TotalOrdering.from_primary_key(
                    [ref.id for ref in node.by_column_ids]
                )
                return (
                    dataclasses.replace(
                        node,
                        child=child_result,
                        order_by=tuple(new_order_by.all_ordering_columns),
                    ),
                    new_order,
                )
            else:
                child_result = remove_order(node.child)
                return node.replace_child(
                    child_result
                ), bigframes.core.ordering.TotalOrdering.from_primary_key(
                    [ref.id for ref in node.by_column_ids]
                )
        elif isinstance(node, bigframes.core.nodes.WindowOpNode):
            child_result, child_order = pull_up_order_inner(node.child)
            if node.inherits_order:
                new_window_order = (
                    *node.window_spec.ordering,
                    *child_order.all_ordering_columns,
                )
                new_window_spec = dataclasses.replace(
                    node.window_spec, ordering=new_window_order
                )
            else:
                new_window_spec = node.window_spec
            return (
                dataclasses.replace(
                    node, child=child_result, window_spec=new_window_spec
                ),
                child_order,
            )
        elif isinstance(node, bigframes.core.nodes.RandomSampleNode):
            child_result, child_order = pull_up_order_inner(node.child)
            return node.replace_child(child_result), child_order.with_non_sequential()
        elif isinstance(node, bigframes.core.nodes.ExplodeNode):
            child_result, child_order = pull_up_order_inner(node.child)
            if node.offsets_col is None:
                offsets_id = identifiers.ColumnId.unique()
                new_explode: bigframes.core.nodes.BigFrameNode = dataclasses.replace(
                    node, child=child_result, offsets_col=offsets_id
                )
            else:
                offsets_id = node.offsets_col
                new_explode = node.replace_child(child_result)
            inner_order = bigframes.core.ordering.TotalOrdering.from_offset_col(
                offsets_id
            )
            return new_explode, child_order.join(inner_order)
        raise ValueError(f"Unexpected node: {node}")

    def pull_order_concat(
        node: bigframes.core.nodes.ConcatNode,
    ) -> Tuple[
        bigframes.core.nodes.BigFrameNode, bigframes.core.ordering.TotalOrdering
    ]:
        new_sources = []
        for i, source in enumerate(node.child_nodes):
            new_source, order = pull_up_order_inner(source)
            offsets_id = identifiers.ColumnId.unique()
            table_id = identifiers.ColumnId.unique()
            if order.is_total_ordering and order.integer_encoding.is_encoded:
                order_expression = order.total_order_col
                assert order_expression is not None
                new_source = bigframes.core.nodes.ProjectionNode(
                    new_source, ((order_expression.scalar_expression, offsets_id),)
                )
            else:
                agg = bigframes.core.expression.NullaryAggregation(
                    agg_ops.RowNumberOp()
                )
                window_spec = bigframes.core.window_spec.unbound(
                    ordering=tuple(order.all_ordering_columns)
                )
                new_source = bigframes.core.nodes.WindowOpNode(
                    new_source, agg, window_spec, offsets_id
                )
            new_source = bigframes.core.nodes.ProjectionNode(
                new_source, ((bigframes.core.expression.const(i), table_id),)
            )
            selection = tuple(
                (
                    bigframes.core.nodes.AliasedRef.identity(id)
                    for id in (*source.ids, table_id, offsets_id)
                )
            )
            new_source = bigframes.core.nodes.SelectionNode(new_source, selection)
            new_sources.append(new_source)

        union_offsets_id = identifiers.ColumnId.unique()
        union_table_id = identifiers.ColumnId.unique()
        new_ids = (*node.output_ids, union_table_id, union_offsets_id)
        new_node = dataclasses.replace(
            node, children=tuple(new_sources), output_ids=new_ids
        )
        new_ordering = bigframes.core.ordering.TotalOrdering.from_primary_key(
            (union_table_id, union_offsets_id)
        )
        return new_node, new_ordering

    def pull_order_join(
        node: bigframes.core.nodes.JoinNode,
    ) -> Tuple[bigframes.core.nodes.BigFrameNode, bigframes.core.ordering.RowOrdering]:
        left_child, left_order = pull_up_order_inner(node.left_child)
        # as tree is a dag, and pull_up_order_inner is memoized, self-joins can create conflicts in new columns
        right_child, right_order = pull_up_order_inner(node.right_child)
        conflicts = set(left_child.ids) & set(right_child.ids)
        if conflicts:
            right_child, mapping = rename_cols(right_child, conflicts)
            right_order = right_order.remap_column_refs(
                mapping, allow_partial_bindings=True
            )

        if node.type in ("right", "outer"):
            # right side is nullable
            left_indicator = identifiers.ColumnId.unique()
            left_child = bigframes.core.nodes.ProjectionNode(
                left_child, ((bigframes.core.expression.const(True), left_indicator),)
            )
            left_order = left_order.with_ordering_columns(
                [bigframes.core.ordering.descending_over(left_indicator)]
            )
        if node.type in ("left", "outer"):
            # right side is nullable
            right_indicator = identifiers.ColumnId.unique()
            right_child = bigframes.core.nodes.ProjectionNode(
                right_child, ((bigframes.core.expression.const(True), right_indicator),)
            )
            right_order = right_order.with_ordering_columns(
                [bigframes.core.ordering.descending_over(right_indicator)]
            )

        new_join = dataclasses.replace(
            node, left_child=left_child, right_child=right_child
        )
        new_order = (
            left_order.join(right_order)
            if (node.type != "right")
            else right_order.join(left_order)
        )
        return new_join, new_order

    @functools.cache
    def remove_order(
        node: bigframes.core.nodes.BigFrameNode,
    ) -> bigframes.core.nodes.BigFrameNode:
        if isinstance(
            node, (bigframes.core.nodes.OrderByNode, bigframes.core.nodes.ReversedNode)
        ):
            return remove_order(node.child)
        elif isinstance(
            node,
            (
                bigframes.core.nodes.WindowOpNode,
                bigframes.core.nodes.PromoteOffsetsNode,
            ),
        ):
            if isinstance(node, bigframes.core.nodes.PromoteOffsetsNode):
                node = rewrite_promote_offsets(node)
            if node.inherits_order:
                child_result, child_order = pull_up_order_inner(node.child)
                new_window_order = (
                    *node.window_spec.ordering,
                    *child_order.all_ordering_columns,
                )
                new_window_spec = dataclasses.replace(
                    node.window_spec, ordering=new_window_order
                )
                return dataclasses.replace(
                    node, child=child_result, window_spec=new_window_spec
                )
        elif isinstance(node, bigframes.core.nodes.AggregateNode):
            if node.has_ordered_ops:
                child_result, child_order = pull_up_order_inner(node.child)
                new_order_by = child_order.with_ordering_columns(node.order_by)
                return dataclasses.replace(
                    node,
                    child=child_result,
                    order_by=tuple(new_order_by.all_ordering_columns),
                )

        return node.transform_children(remove_order)

    def remove_order_strict(
        node: bigframes.core.nodes.BigFrameNode,
    ) -> bigframes.core.nodes.BigFrameNode:
        result = remove_order(node)
        if result.ids != node.ids:
            return bigframes.core.nodes.SelectionNode(
                result,
                tuple(bigframes.core.nodes.AliasedRef.identity(id) for id in node.ids),
            )
        return result

    return (
        pull_up_order_inner(root)
        if order_root
        else (remove_order(root), bigframes.core.ordering.RowOrdering())
    )


def rewrite_promote_offsets(
    node: bigframes.core.nodes.PromoteOffsetsNode,
) -> bigframes.core.nodes.WindowOpNode:
    agg = bigframes.core.expression.NullaryAggregation(agg_ops.RowNumberOp())
    window_spec = bigframes.core.window_spec.unbound()
    return bigframes.core.nodes.WindowOpNode(node.child, agg, window_spec, node.col_id)


def rename_cols(
    node: bigframes.core.nodes.BigFrameNode, cols: set[identifiers.ColumnId]
) -> Tuple[
    bigframes.core.nodes.BigFrameNode,
    Mapping[identifiers.ColumnId, identifiers.ColumnId],
]:
    mappings = dict((id, identifiers.ColumnId.unique()) for id in cols)

    result_node = bigframes.core.nodes.SelectionNode(
        node,
        tuple(
            bigframes.core.nodes.AliasedRef.identity(id).remap_vars(mappings)
            for id in node.ids
        ),
    )

    return result_node, dict(mappings)
