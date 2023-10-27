# Copyright 2023 Google LLC
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

import functools
import io
import typing

import pandas as pd

import bigframes.core.compile as compiled
import bigframes.core.compile.single_column
import bigframes.core.nodes as nodes

if typing.TYPE_CHECKING:
    import bigframes.core
    import bigframes.session


@functools.cache
def compile_node(node: nodes.BigFrameNode) -> compiled.CompiledArrayValue:
    """Compile node into CompileArrayValue. Caches result."""
    return _compile_node(node)


@functools.singledispatch
def _compile_node(node: nodes.BigFrameNode) -> compiled.CompiledArrayValue:
    """Defines transformation but isn't cached, always use compile_node instead"""
    raise ValueError(f"Can't compile unnrecognized node: {node}")


@_compile_node.register
def compile_join(node: nodes.JoinNode):
    compiled_left = compile_node(node.left_child)
    compiled_right = compile_node(node.right_child)
    return bigframes.core.compile.single_column.join_by_column(
        compiled_left,
        node.left_column_ids,
        compiled_right,
        node.right_column_ids,
        how=node.how,
        allow_row_identity_join=node.allow_row_identity_join,
    )


@_compile_node.register
def compile_select(node: nodes.SelectNode):
    return compile_node(node.child).select_columns(node.column_ids)


@_compile_node.register
def compile_drop(node: nodes.DropColumnsNode):
    return compile_node(node.child).drop_columns(node.columns)


@_compile_node.register
def compile_readlocal(node: nodes.ReadLocalNode):
    array_as_pd = pd.read_feather(io.BytesIO(node.feather_bytes))
    return compiled.CompiledArrayValue.mem_expr_from_pandas(array_as_pd)


@_compile_node.register
def compile_readgbq(node: nodes.ReadGbqNode):
    return compiled.CompiledArrayValue(
        node.table,
        node.columns,
        node.hidden_ordering_columns,
        node.ordering,
    )


@_compile_node.register
def compile_promote_offsets(node: nodes.PromoteOffsetsNode):
    return compile_node(node.child).promote_offsets(node.col_id)


@_compile_node.register
def compile_filter(node: nodes.FilterNode):
    return compile_node(node.child).filter(node.predicate_id, node.keep_null)


@_compile_node.register
def compile_orderby(node: nodes.OrderByNode):
    return compile_node(node.child).order_by(node.by, node.stable)


@_compile_node.register
def compile_reversed(node: nodes.ReversedNode):
    return compile_node(node.child).reversed()


@_compile_node.register
def compile_project_unary(node: nodes.ProjectUnaryOpNode):
    return compile_node(node.child).project_unary_op(
        node.input_id, node.op, node.output_id
    )


@_compile_node.register
def compile_project_binary(node: nodes.ProjectBinaryOpNode):
    return compile_node(node.child).project_binary_op(
        node.left_input_id, node.right_input_id, node.op, node.output_id
    )


@_compile_node.register
def compile_project_ternary(node: nodes.ProjectTernaryOpNode):
    return compile_node(node.child).project_ternary_op(
        node.input_id1, node.input_id2, node.input_id3, node.op, node.output_id
    )


@_compile_node.register
def compile_concat(node: nodes.ConcatNode):
    compiled_nodes = [compile_node(node) for node in node.children]
    return compiled_nodes[0].concat(compiled_nodes[1:])


@_compile_node.register
def compile_aggregate(node: nodes.AggregateNode):
    return compile_node(node.child).aggregate(
        node.aggregations, node.by_column_ids, node.dropna
    )


@_compile_node.register
def compile_corr(node: nodes.CorrNode):
    return compile_node(node.child).corr_aggregate(node.corr_aggregations)


@_compile_node.register
def compile_window(node: nodes.WindowOpNode):
    return compile_node(node.child).project_window_op(
        node.column_name,
        node.op,
        node.window_spec,
        node.output_name,
        never_skip_nulls=node.never_skip_nulls,
        skip_reproject_unsafe=node.skip_reproject_unsafe,
    )


@_compile_node.register
def compile_reproject(node: nodes.ReprojectOpNode):
    return compile_node(node.child)._reproject_to_table()


@_compile_node.register
def compile_unpivot(node: nodes.UnpivotNode):
    return compile_node(node.child).unpivot(
        node.row_labels,
        node.unpivot_columns,
        passthrough_columns=node.passthrough_columns,
        index_col_ids=node.index_col_ids,
        dtype=node.dtype,
        how=node.how,
    )


@_compile_node.register
def compile_assign(node: nodes.AssignNode):
    return compile_node(node.child).assign(node.source_id, node.destination_id)


@_compile_node.register
def compile_assign_constant(node: nodes.AssignConstantNode):
    return compile_node(node.child).assign_constant(
        node.destination_id, node.value, node.dtype
    )


@_compile_node.register
def compiler_random_sample(node: nodes.RandomSampleNode):
    return compile_node(node.child)._uniform_sampling(node.fraction)
