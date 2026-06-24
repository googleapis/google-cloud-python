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

import bigframes.dtypes as dtypes
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
from bigframes.core import (
    agg_expressions,
    expression,
    identifiers,
    nodes,
)


def rewrite_substrait_aggregations(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
    """
    Rewrites AggregateNodes for Substrait compatibility:
    1. Pre-projects casts (like bool->float) and size literals, ensuring aggregate arguments
       are direct references.
    2. Post-projects casts to enforce correct Python output schema/types.
    """
    if not isinstance(node, nodes.AggregateNode):
        return node

    child = node.child
    child_ids = list(child.ids)

    # Collect size aggregations
    size_aggs = [
        (i, agg)
        for i, (agg, _) in enumerate(node.aggregations)
        if isinstance(agg.op, (agg_ops.SizeOp, agg_ops.SizeUnaryOp))
    ]

    # Collect cast aggregations (bool->float for mean/stddev/var, bool->int for sum)
    cast_aggs: list[tuple[int, identifiers.ColumnId, dtypes.Dtype]] = []
    for agg_idx, (agg, _) in enumerate(node.aggregations):
        if hasattr(agg, "column_references"):
            for col_id in agg.column_references:
                idx = child_ids.index(col_id)
                col_dtype = child.schema.items[idx].dtype
                is_bool = col_dtype == dtypes.BOOL_DTYPE
                if isinstance(
                    agg.op, (agg_ops.StdOp, agg_ops.VarOp, agg_ops.PopVarOp)
                ) or (isinstance(agg.op, agg_ops.MeanOp) and is_bool):
                    cast_aggs.append((agg_idx, col_id, dtypes.FLOAT_DTYPE))
                elif isinstance(agg.op, agg_ops.SumOp) and is_bool:
                    cast_aggs.append((agg_idx, col_id, dtypes.INT_DTYPE))

    # If we need pre-projection (casts or size constants)
    if size_aggs or cast_aggs:
        assignments = []

        cast_agg_to_col_id = {}
        for agg_idx, col_id, target_dtype in cast_aggs:
            new_id = identifiers.ColumnId(f"bf_cast_{col_id.name}_{agg_idx}")
            cast_expr = ops.AsTypeOp(to_type=target_dtype).as_expr(
                expression.deref(col_id.name)
            )
            assignments.append((cast_expr, new_id))
            cast_agg_to_col_id[(agg_idx, col_id)] = new_id

        size_agg_to_col_id = {}
        for size_idx, (agg_idx, _) in enumerate(size_aggs):
            new_id = identifiers.ColumnId(f"bf_size_const_{agg_idx}")
            const_expr = expression.const(size_idx + 1)
            assignments.append((const_expr, new_id))
            size_agg_to_col_id[agg_idx] = new_id

        # Wrap child in ProjectionNode
        pre_project = nodes.ProjectionNode(
            child,
            assignments=tuple(assignments),
        )
        child = pre_project

        # Rewrite aggregations to use the projected columns
        rewritten_aggs = []
        for agg_idx, (agg, out_col_id) in enumerate(node.aggregations):
            rewritten_agg: agg_expressions.Aggregation
            if isinstance(agg.op, (agg_ops.SizeOp, agg_ops.SizeUnaryOp)):
                new_col_id = size_agg_to_col_id[agg_idx]
                rewritten_agg = agg_expressions.UnaryAggregation(
                    agg_ops.SizeUnaryOp(), expression.deref(new_col_id.name)
                )
            elif hasattr(agg, "column_references"):
                new_exprs = []
                for col_id in agg.column_references:
                    if (agg_idx, col_id) in cast_agg_to_col_id:
                        new_exprs.append(
                            expression.deref(cast_agg_to_col_id[(agg_idx, col_id)].name)
                        )
                    else:
                        new_exprs.append(expression.deref(col_id.name))

                rewritten_agg = agg.replace_args(*new_exprs)
            else:
                rewritten_agg = agg

            rewritten_aggs.append((rewritten_agg, out_col_id))

        node = dataclasses.replace(
            node,
            child=child,
            aggregations=tuple(rewritten_aggs),
        )

    # Post-projection to enforce output schema types:
    group_ids = [deref.id for deref in node.by_column_ids]
    agg_ids = [out_id for _, out_id in node.aggregations]
    output_ids = group_ids + agg_ids

    expected_types = [item.dtype for item in node.schema.items]

    assignments = []
    selection_pairs = []
    for idx, (out_id, out_dtype) in enumerate(zip(output_ids, expected_types)):
        cast_id = identifiers.ColumnId(f"bf_out_cast_{out_id.name}")
        cast_expr = ops.AsTypeOp(to_type=out_dtype).as_expr(
            expression.deref(out_id.name)
        )
        assignments.append((cast_expr, cast_id))

        selection_pairs.append(
            (nodes.AliasedRef(expression.deref(cast_id.name), out_id), out_id)
        )

    post_project = nodes.ProjectionNode(
        node,
        assignments=tuple(assignments),
    )
    post_selection = nodes.SelectionNode(
        post_project,
        input_output_pairs=tuple(ref for ref, _ in selection_pairs),
    )

    return post_selection


def rewrite_substrait_windows(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
    """
    Rewrites WindowOpNode for Substrait compatibility:
    1. Pre-projects casts (like bool->float) and size literals, ensuring aggregate arguments
       are direct references.
    2. Post-projects casts to enforce correct Python output schema/types for window columns.
    """
    if not isinstance(node, nodes.WindowOpNode):
        return node

    child = node.child
    child_ids = list(child.ids)

    # Collect size and cast requirements for the window agg expressions
    size_aggs = []
    cast_aggs: list[tuple[int, identifiers.ColumnId, dtypes.Dtype]] = []

    for agg_idx, col_def in enumerate(node.agg_exprs):
        agg = col_def.expression
        assert isinstance(agg, agg_expressions.Aggregation)
        if isinstance(agg.op, (agg_ops.SizeOp, agg_ops.SizeUnaryOp)):
            size_aggs.append((agg_idx, agg))
        elif hasattr(agg, "column_references"):
            for col_id in agg.column_references:
                idx = child_ids.index(col_id)
                col_dtype = child.schema.items[idx].dtype
                is_bool = col_dtype == dtypes.BOOL_DTYPE
                if isinstance(
                    agg.op, (agg_ops.StdOp, agg_ops.VarOp, agg_ops.PopVarOp)
                ) or (isinstance(agg.op, agg_ops.MeanOp) and is_bool):
                    cast_aggs.append((agg_idx, col_id, dtypes.FLOAT_DTYPE))
                elif isinstance(agg.op, agg_ops.SumOp) and is_bool:
                    cast_aggs.append((agg_idx, col_id, dtypes.INT_DTYPE))

    # If we need pre-projection (casts or size constants)
    if size_aggs or cast_aggs:
        assignments = []

        cast_agg_to_col_id = {}
        for agg_idx, col_id, target_dtype in cast_aggs:
            new_id = identifiers.ColumnId(f"bf_window_cast_{col_id.name}_{agg_idx}")
            cast_expr = ops.AsTypeOp(to_type=target_dtype).as_expr(
                expression.deref(col_id.name)
            )
            assignments.append((cast_expr, new_id))
            cast_agg_to_col_id[(agg_idx, col_id)] = new_id

        size_agg_to_col_id = {}
        for size_idx, (agg_idx, _) in enumerate(size_aggs):
            new_id = identifiers.ColumnId(f"bf_window_size_const_{agg_idx}")
            const_expr = expression.const(size_idx + 1)
            assignments.append((const_expr, new_id))
            size_agg_to_col_id[agg_idx] = new_id

        # Wrap child in ProjectionNode
        pre_project = nodes.ProjectionNode(
            child,
            assignments=tuple(assignments),
        )
        child = pre_project

        # Rewrite window expressions to use the projected columns
        rewritten_agg_exprs = []
        for agg_idx, col_def in enumerate(node.agg_exprs):
            agg = col_def.expression
            assert isinstance(agg, agg_expressions.Aggregation)
            out_col_id = col_def.id
            rewritten_agg: agg_expressions.Aggregation

            if isinstance(agg.op, (agg_ops.SizeOp, agg_ops.SizeUnaryOp)):
                new_col_id = size_agg_to_col_id[agg_idx]
                rewritten_agg = agg_expressions.UnaryAggregation(
                    agg_ops.SizeUnaryOp(), expression.deref(new_col_id.name)
                )
            elif hasattr(agg, "column_references"):
                new_exprs = []
                for col_id in agg.column_references:
                    if (agg_idx, col_id) in cast_agg_to_col_id:
                        new_exprs.append(
                            expression.deref(cast_agg_to_col_id[(agg_idx, col_id)].name)
                        )
                    else:
                        new_exprs.append(expression.deref(col_id.name))

                rewritten_agg = agg.replace_args(*new_exprs)
            else:
                rewritten_agg = agg

            rewritten_agg_exprs.append(nodes.ColumnDef(rewritten_agg, out_col_id))

        node = dataclasses.replace(
            node,
            child=child,
            agg_exprs=tuple(rewritten_agg_exprs),
        )

    # Post-projection to enforce output schema types for newly introduced window columns:
    child_output_ids = (
        list(node.child.ids)
        if not isinstance(child, nodes.ProjectionNode)
        else list(child.child.ids)
    )

    assignments = []
    selection_pairs = []

    for child_id in child_output_ids:
        selection_pairs.append((nodes.AliasedRef.identity(child_id), child_id))

    for col_def, field in zip(node.agg_exprs, node.added_fields):
        out_id = col_def.id
        out_dtype = field.dtype

        cast_id = identifiers.ColumnId(f"bf_window_out_cast_{out_id.name}")
        cast_expr = ops.AsTypeOp(to_type=out_dtype).as_expr(
            expression.deref(out_id.name)
        )
        assignments.append((cast_expr, cast_id))

        selection_pairs.append(
            (nodes.AliasedRef(expression.deref(cast_id.name), out_id), out_id)
        )

    post_project = nodes.ProjectionNode(
        node,
        assignments=tuple(assignments),
    )
    post_selection = nodes.SelectionNode(
        post_project,
        input_output_pairs=tuple(ref for ref, _ in selection_pairs),
    )

    return post_selection
