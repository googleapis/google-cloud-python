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
import itertools
from typing import Optional, Sequence, Union

from bigframes.core import (
    agg_expressions,
    expression,
    guid,
    identifiers,
    nodes,
    ordering,
    sql_nodes,
)
import bigframes.core.rewrite


def _limit(select: sql_nodes.SqlSelectNode, limit: int) -> sql_nodes.SqlSelectNode:
    new_limit = limit if select.limit is None else min([select.limit, limit])
    return dataclasses.replace(select, limit=new_limit)


def _try_sort(
    select: sql_nodes.SqlSelectNode, sort_by: Sequence[ordering.OrderingExpression]
) -> Optional[sql_nodes.SqlSelectNode]:
    new_order_exprs = []
    for sort_expr in sort_by:
        new_expr = _try_bind(
            sort_expr.scalar_expression, select.get_id_mapping(), analytic_allowed=False
        )
        if new_expr is None:
            return None
        new_order_exprs.append(
            dataclasses.replace(sort_expr, scalar_expression=new_expr)
        )
    return dataclasses.replace(select, sorting=tuple(new_order_exprs))


def _sort(
    node: nodes.BigFrameNode, sort_by: Sequence[ordering.OrderingExpression]
) -> sql_nodes.SqlSelectNode:
    if isinstance(node, sql_nodes.SqlSelectNode):
        merged = _try_sort(node, sort_by)
        if merged:
            return merged
    result = _try_sort(_create_noop_select(node), sort_by)
    assert result is not None
    return result


def _try_bind(
    expr: expression.Expression,
    bindings: dict[identifiers.ColumnId, expression.Expression],
    analytic_allowed: bool = False,  # means block binding to an analytic even if original is scalar
) -> Optional[expression.Expression]:
    if not expr.is_scalar_expr or not analytic_allowed:
        for ref in expr.column_references:
            if ref in bindings and not bindings[ref].is_scalar_expr:
                return None
    return expr.bind_refs(bindings)


def _try_add_cdefs(
    select: sql_nodes.SqlSelectNode, cdefs: Sequence[nodes.ColumnDef]
) -> Optional[sql_nodes.SqlSelectNode]:
    # TODO: add up complexity measure while inlining refs
    new_defs = []
    for cdef in cdefs:
        cdef_expr = cdef.expression
        merged_expr = _try_bind(
            cdef_expr, select.get_id_mapping(), analytic_allowed=True
        )
        if merged_expr is None:
            return None
        new_defs.append(nodes.ColumnDef(merged_expr, cdef.id))

    return dataclasses.replace(select, selections=(*select.selections, *new_defs))


def _add_cdefs(
    node: nodes.BigFrameNode, cdefs: Sequence[nodes.ColumnDef]
) -> sql_nodes.SqlSelectNode:
    if isinstance(node, sql_nodes.SqlSelectNode):
        merged = _try_add_cdefs(node, cdefs)
        if merged:
            return merged
    # Otherwise, wrap the child in a SELECT and add the columns
    result = _try_add_cdefs(_create_noop_select(node), cdefs)
    assert result is not None
    return result


def _try_add_filter(
    select: sql_nodes.SqlSelectNode, predicates: Sequence[expression.Expression]
) -> Optional[sql_nodes.SqlSelectNode]:
    # Filter implicitly happens first, so merging it into ths select will modify non-scalar col expressions
    if not all(cdef.expression.is_scalar_expr for cdef in select.selections):
        return None
    if not all(
        sort_expr.scalar_expression.is_scalar_expr for sort_expr in select.sorting
    ):
        return None
    # Constraint: filters can only be merged if they are scalar expression after binding
    new_predicates = []
    # bind variables, merge predicates
    for predicate in predicates:
        merged_pred = _try_bind(predicate, select.get_id_mapping())
        if not merged_pred:
            return None
        new_predicates.append(merged_pred)
    return dataclasses.replace(select, predicates=(*select.predicates, *new_predicates))


def _add_filter(
    node: nodes.BigFrameNode, predicates: Sequence[expression.Expression]
) -> sql_nodes.SqlSelectNode:
    if isinstance(node, sql_nodes.SqlSelectNode):
        result = _try_add_filter(node, predicates)
        if result:
            return result
    new_node = _try_add_filter(_create_noop_select(node), predicates)
    assert new_node is not None
    return new_node


def _create_noop_select(node: nodes.BigFrameNode) -> sql_nodes.SqlSelectNode:
    return sql_nodes.SqlSelectNode(
        node,
        selections=tuple(
            nodes.ColumnDef(expression.ResolvedDerefOp.from_field(field), field.id)
            for field in node.fields
        ),
    )


def _try_remap_select_cols(
    select: sql_nodes.SqlSelectNode, cols: Sequence[nodes.AliasedRef]
):
    new_defs = []
    for aliased_ref in cols:
        new_defs.append(
            nodes.ColumnDef(select.get_id_mapping()[aliased_ref.ref.id], aliased_ref.id)
        )

    return dataclasses.replace(select, selections=tuple(new_defs))


def _remap_select_cols(node: nodes.BigFrameNode, cols: Sequence[nodes.AliasedRef]):
    if isinstance(node, sql_nodes.SqlSelectNode):
        result = _try_remap_select_cols(node, cols)
        if result:
            return result
    new_node = _try_remap_select_cols(_create_noop_select(node), cols)
    assert new_node is not None
    return new_node


def _get_added_cdefs(node: Union[nodes.ProjectionNode, nodes.WindowOpNode]):
    # TODO: InNode
    if isinstance(node, nodes.ProjectionNode):
        return tuple(nodes.ColumnDef(expr, id) for expr, id in node.assignments)
    if isinstance(node, nodes.WindowOpNode):
        new_cdefs = []
        for cdef in node.agg_exprs:
            assert isinstance(cdef.expression, agg_expressions.Aggregation)
            window_expr = agg_expressions.WindowExpression(
                cdef.expression, node.window_spec
            )
            # TODO: we probably should do this as another step
            rewritten_window_expr = bigframes.core.rewrite.simplify_complex_windows(
                window_expr
            )
            new_cdefs.append(nodes.ColumnDef(rewritten_window_expr, cdef.id))
        return tuple(new_cdefs)
    else:
        raise ValueError(f"Unexpected node type: {type(node)}")


def _as_sql_node(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
    # case one, can be converted to select
    if isinstance(node, nodes.ReadTableNode):
        leaf = sql_nodes.SqlDataSource(source=node.source)
        mappings = [
            nodes.AliasedRef(expression.deref(scan_item.source_id), scan_item.id)
            for scan_item in node.scan_list.items
        ]
        return _remap_select_cols(leaf, mappings)
    elif isinstance(node, (nodes.ProjectionNode, nodes.WindowOpNode)):
        cdefs = _get_added_cdefs(node)
        return _add_cdefs(node.child, cdefs)
    elif isinstance(node, (nodes.SelectionNode)):
        return _remap_select_cols(node.child, node.input_output_pairs)
    elif isinstance(node, nodes.FilterNode):
        return _add_filter(node.child, [node.predicate])
    elif isinstance(node, nodes.ResultNode):
        result = node.child
        if node.order_by is not None:
            result = _sort(result, node.order_by.all_ordering_columns)
        result = _remap_select_cols(
            result,
            [
                nodes.AliasedRef(ref, identifiers.ColumnId(name))
                for ref, name in node.output_cols
            ],
        )
        if node.limit is not None:
            result = _limit(result, node.limit)  # type: ignore
        return result
    else:
        return node


# In the future, we will have sql nodes for each of these node types.
_LOGICAL_NODE_TYPES_TO_WRAP = (
    nodes.ReadLocalNode,
    nodes.ExplodeNode,
    nodes.InNode,
    nodes.AggregateNode,
    nodes.FromRangeNode,
    nodes.ConcatNode,
    sql_nodes.SqlSelectNode,
)


def _insert_cte_markers(root: nodes.BigFrameNode) -> nodes.BigFrameNode:
    # important not to wrap nodes that are already wrapped
    wrapped_nodes = set(
        node.child for node in root.unique_nodes() if isinstance(node, nodes.CteNode)
    )
    # don't wrap child nodes of ConcatNode
    union_child_nodes = set(
        itertools.chain.from_iterable(
            node.child_nodes
            for node in root.unique_nodes()
            if isinstance(node, nodes.ConcatNode)
        )
    )

    def maybe_insert_cte_marker(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
        if node == root:
            return node
        if (
            isinstance(node, _LOGICAL_NODE_TYPES_TO_WRAP)
            and node not in wrapped_nodes
            and node not in union_child_nodes
        ):
            wrapped_nodes.add(node)
            return nodes.CteNode(node)
        return node

    return root.top_down(maybe_insert_cte_marker)


def _extract_ctes_to_with_expr(
    root: nodes.BigFrameNode, uid_gen: guid.SequentialUIDGenerator
) -> nodes.BigFrameNode:
    topological_ctes = list(
        filter(
            lambda n: isinstance(n, nodes.CteNode),
            root.iter_nodes_topo(),
        )
    )
    cte_names = tuple(
        next(uid_gen.get_uid_stream("bfcte_")) for _ in range(len(topological_ctes))
    )

    if len(topological_ctes) == 0:
        return root

    mapping = {
        cte_node: sql_nodes.SqlCteRefNode(cte_name, tuple(cte_node.fields))
        for cte_node, cte_name in zip(topological_ctes, cte_names)
    }

    # Replace all CTEs with CTE references and wrap the new root in a WITH clause
    return sql_nodes.SqlWithCtesNode(
        root.top_down(lambda x: mapping.get(x, x)),
        cte_names,
        tuple(
            cte_node.child.top_down(lambda x: mapping.get(x, x)) for cte_node in topological_ctes  # type: ignore
        ),
    )


def as_sql_nodes(
    root: nodes.BigFrameNode, uid_gen: guid.SequentialUIDGenerator
) -> nodes.BigFrameNode:
    root = nodes.bottom_up(root, _as_sql_node)
    # Insert CTE markers to indicate where we want to split the query.
    root = _insert_cte_markers(root)
    root = _extract_ctes_to_with_expr(root, uid_gen)
    return root
