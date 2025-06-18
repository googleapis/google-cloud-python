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
import typing

from bigframes.core import identifiers, nodes


def column_pruning(
    root: nodes.BigFrameNode,
) -> nodes.BigFrameNode:
    return nodes.top_down(root, prune_columns)


def to_fixed(max_iterations: int = 100):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            previous_result = None
            current_result = func(*args, **kwargs)
            attempts = 1

            while attempts < max_iterations:
                if current_result == previous_result:
                    return current_result
                previous_result = current_result
                current_result = func(current_result)
                attempts += 1

            return current_result

        return wrapper

    return decorator


@to_fixed(max_iterations=100)
def prune_columns(node: nodes.BigFrameNode):
    if isinstance(node, nodes.SelectionNode):
        result = prune_selection_child(node)
    elif isinstance(node, nodes.ResultNode):
        result = node.replace_child(
            prune_node(
                node.child, node.consumed_ids or frozenset(list(node.child.ids)[0:1])
            )
        )
    elif isinstance(node, nodes.AggregateNode):
        result = node.replace_child(
            prune_node(
                node.child, node.consumed_ids or frozenset(list(node.child.ids)[0:1])
            )
        )
    elif isinstance(node, nodes.InNode):
        result = dataclasses.replace(
            node,
            right_child=prune_node(node.right_child, frozenset([node.right_col.id])),
        )
    else:
        result = node
    return result


def prune_selection_child(
    selection: nodes.SelectionNode,
) -> nodes.BigFrameNode:
    child = selection.child

    # Important to check this first
    if list(selection.ids) == list(child.ids):
        if (ref.ref.id == ref.id for ref in selection.input_output_pairs):
            # selection is no-op so just remove it entirely
            return child

    if isinstance(child, nodes.SelectionNode):
        return selection.remap_refs(
            {id: ref.id for ref, id in child.input_output_pairs}
        ).replace_child(child.child)
    elif isinstance(child, nodes.AdditiveNode):
        if not set(field.id for field in child.added_fields) & selection.consumed_ids:
            return selection.replace_child(child.additive_base)
        needed_ids = selection.consumed_ids | child.referenced_ids
        if isinstance(child, nodes.ProjectionNode):
            # Projection expressions are independent, so can be individually removed from the node
            child = dataclasses.replace(
                child,
                assignments=tuple(
                    (ex, id) for (ex, id) in child.assignments if id in needed_ids
                ),
            )
        return selection.replace_child(
            child.replace_additive_base(prune_node(child.additive_base, needed_ids))
        )
    elif isinstance(child, nodes.ConcatNode):
        indices = [
            list(child.ids).index(ref.id) for ref, _ in selection.input_output_pairs
        ]
        if len(indices) == 0:
            # pushing zero-column selection into concat messes up emitter for now, which doesn't like zero columns
            return selection
        new_children = []
        for concat_node in child.child_nodes:
            cc_ids = tuple(concat_node.ids)
            sub_selection = tuple(nodes.AliasedRef.identity(cc_ids[i]) for i in indices)
            new_children.append(nodes.SelectionNode(concat_node, sub_selection))
        return nodes.ConcatNode(
            children=tuple(new_children), output_ids=tuple(selection.ids)
        )
    # Nodes that pass through input columns
    elif isinstance(
        child,
        (
            nodes.RandomSampleNode,
            nodes.ReversedNode,
            nodes.OrderByNode,
            nodes.FilterNode,
            nodes.SliceNode,
            nodes.JoinNode,
            nodes.ExplodeNode,
        ),
    ):
        ids = selection.consumed_ids | child.referenced_ids
        return selection.replace_child(
            child.transform_children(lambda x: prune_node(x, ids))
        )
    elif isinstance(child, nodes.AggregateNode):
        return selection.replace_child(prune_aggregate(child, selection.consumed_ids))
    elif isinstance(child, nodes.LeafNode):
        return selection.replace_child(prune_leaf(child, selection.consumed_ids))
    return selection


def prune_node(
    node: nodes.BigFrameNode,
    ids: typing.AbstractSet[identifiers.ColumnId],
):
    # This clause is important, ensures idempotency, so can reach fixed point
    if not (set(node.ids) - ids):
        return node
    else:
        return nodes.SelectionNode(
            node,
            tuple(nodes.AliasedRef.identity(id) for id in node.ids if id in ids),
        )


def prune_aggregate(
    node: nodes.AggregateNode,
    used_cols: typing.AbstractSet[identifiers.ColumnId],
) -> nodes.AggregateNode:
    pruned_aggs = (
        tuple(agg for agg in node.aggregations if agg[1] in used_cols)
        or node.aggregations[0:1]
    )
    return dataclasses.replace(node, aggregations=pruned_aggs)


@functools.singledispatch
def prune_leaf(
    node: nodes.BigFrameNode,
    used_cols: typing.AbstractSet[identifiers.ColumnId],
):
    ...


@prune_leaf.register
def prune_readlocal(
    node: nodes.ReadLocalNode,
    selection: typing.AbstractSet[identifiers.ColumnId],
) -> nodes.ReadLocalNode:
    new_scan_list = node.scan_list.filter_cols(selection)
    return dataclasses.replace(
        node,
        scan_list=new_scan_list,
        offsets_col=node.offsets_col if (node.offsets_col in selection) else None,
    )


@prune_leaf.register
def prune_readtable(
    node: nodes.ReadTableNode,
    selection: typing.AbstractSet[identifiers.ColumnId],
) -> nodes.ReadTableNode:
    new_scan_list = node.scan_list.filter_cols(selection)
    return dataclasses.replace(node, scan_list=new_scan_list)
