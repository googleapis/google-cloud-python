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
from typing import cast

from bigframes.core import expression, identifiers, nodes


def defer_selection(
    root: nodes.BigFrameNode,
) -> nodes.BigFrameNode:
    """
    Defers SelectionNode operations in the tree, pulling them up.

    In many cases, these nodes will be merged or eliminated entirely, simplifying the overall tree.
    """
    return nodes.bottom_up(
        root, functools.partial(pull_up_select, prefer_source_names=True)
    )


def pull_up_select(
    node: nodes.BigFrameNode, prefer_source_names: bool
) -> nodes.BigFrameNode:
    if isinstance(node, nodes.LeafNode):
        if prefer_source_names and isinstance(node, nodes.ReadTableNode):
            return pull_up_source_ids(node)
        else:
            return node
    if isinstance(node, nodes.JoinNode):
        return pull_up_selects_under_join(node)
    if isinstance(node, nodes.ConcatNode):
        return handle_selects_under_concat(node)
    if isinstance(node, nodes.UnaryNode):
        return pull_up_select_unary(node)
    # shouldn't hit this, but not worth crashing over
    return node


def pull_up_source_ids(node: nodes.ReadTableNode) -> nodes.BigFrameNode:
    if all(id.sql == source_id for id, source_id in node.scan_list.items):
        return node
    else:
        source_ids = sorted(
            set(scan_item.source_id for scan_item in node.scan_list.items)
        )
        new_scan_list = nodes.ScanList.from_items(
            [
                nodes.ScanItem(identifiers.ColumnId(source_id), source_id)
                for source_id in source_ids
            ]
        )
        new_source = dataclasses.replace(node, scan_list=new_scan_list)
        new_selection = nodes.SelectionNode(
            new_source,
            tuple(
                nodes.AliasedRef(
                    expression.DerefOp(identifiers.ColumnId(source_id)), id
                )
                for id, source_id in node.scan_list.items
            ),
        )
        return new_selection


def pull_up_select_unary(node: nodes.UnaryNode) -> nodes.BigFrameNode:
    child = node.child
    if not isinstance(child, nodes.SelectionNode):
        return node

    # Schema-preserving nodes
    if isinstance(
        node,
        (
            nodes.ReversedNode,
            nodes.OrderByNode,
            nodes.SliceNode,
            nodes.FilterNode,
            nodes.RandomSampleNode,
        ),
    ):
        pushed_down_node: nodes.BigFrameNode = node.remap_refs(
            {id: ref.id for ref, id in child.input_output_pairs}
        ).replace_child(child.child)
        pulled_up_select = cast(
            nodes.SelectionNode, child.replace_child(pushed_down_node)
        )
        return pulled_up_select
    elif isinstance(
        node,
        (
            nodes.SelectionNode,
            nodes.ResultNode,
        ),
    ):
        return node.remap_refs(
            {id: ref.id for ref, id in child.input_output_pairs}
        ).replace_child(child.child)
    elif isinstance(node, nodes.AggregateNode):
        pushed_down_agg = node.remap_refs(
            {id: ref.id for ref, id in child.input_output_pairs}
        ).replace_child(child.child)
        new_selection = tuple(
            nodes.AliasedRef.identity(id).remap_refs(
                {id: ref.id for ref, id in child.input_output_pairs}
            )
            for id in node.ids
        )
        return nodes.SelectionNode(pushed_down_agg, new_selection)
    elif isinstance(node, nodes.ExplodeNode):
        pushed_down_node = node.remap_refs(
            {id: ref.id for ref, id in child.input_output_pairs}
        ).replace_child(child.child)
        pulled_up_select = cast(
            nodes.SelectionNode, child.replace_child(pushed_down_node)
        )
        if node.offsets_col:
            pulled_up_select = dataclasses.replace(
                pulled_up_select,
                input_output_pairs=(
                    *pulled_up_select.input_output_pairs,
                    nodes.AliasedRef(
                        expression.DerefOp(node.offsets_col), node.offsets_col
                    ),
                ),
            )
        return pulled_up_select
    elif isinstance(node, nodes.AdditiveNode):
        pushed_down_node = node.replace_additive_base(child.child).remap_refs(
            {id: ref.id for ref, id in child.input_output_pairs}
        )
        new_selection = (
            *child.input_output_pairs,
            *(
                nodes.AliasedRef(expression.DerefOp(col.id), col.id)
                for col in node.added_fields
            ),
        )
        pulled_up_select = dataclasses.replace(
            child, child=pushed_down_node, input_output_pairs=new_selection
        )
        return pulled_up_select
    # shouldn't hit this, but not worth crashing over
    return node


def pull_up_selects_under_join(node: nodes.JoinNode) -> nodes.JoinNode:
    # Can in theory pull up selects here, but it is a bit dangerous, in particular or self-joins, when there are more transforms to do.
    # TODO: Safely pull up selects above join
    return node


def handle_selects_under_concat(node: nodes.ConcatNode) -> nodes.ConcatNode:
    new_children = []
    for child in node.child_nodes:
        # remove select if no-op
        if not isinstance(child, nodes.SelectionNode):
            new_children.append(child)
        else:
            inputs = (ref.id for ref in child.input_output_pairs)
            if inputs == tuple(child.child.ids):
                new_children.append(child.child)
            else:
                new_children.append(child)
    return dataclasses.replace(node, children=tuple(new_children))
