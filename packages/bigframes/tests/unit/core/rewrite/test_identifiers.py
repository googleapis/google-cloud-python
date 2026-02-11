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
import typing

from bigframes.core import bq_data
import bigframes.core as core
import bigframes.core.agg_expressions as agg_ex
import bigframes.core.expression as ex
import bigframes.core.identifiers as identifiers
import bigframes.core.nodes as nodes
import bigframes.core.rewrite.identifiers as id_rewrite
import bigframes.operations.aggregations as agg_ops


def test_remap_variables_single_node(leaf):
    node = leaf
    id_generator = (identifiers.ColumnId(f"id_{i}") for i in range(100))
    new_node, mapping = id_rewrite.remap_variables(node, id_generator)
    assert new_node is not node
    assert len(mapping) == 2
    assert set(mapping.keys()) == {f.id for f in node.fields}
    assert set(mapping.values()) == {
        identifiers.ColumnId("id_0"),
        identifiers.ColumnId("id_1"),
    }


def test_remap_variables_projection(leaf):
    node = nodes.ProjectionNode(
        leaf,
        (
            (
                core.expression.DerefOp(leaf.fields[0].id),
                identifiers.ColumnId("new_col"),
            ),
        ),
    )
    id_generator = (identifiers.ColumnId(f"id_{i}") for i in range(100))
    new_node, mapping = id_rewrite.remap_variables(node, id_generator)
    assert new_node is not node
    assert len(mapping) == 3
    assert set(mapping.keys()) == {f.id for f in node.fields}
    assert set(mapping.values()) == {identifiers.ColumnId(f"id_{i}") for i in range(3)}


def test_remap_variables_aggregate(leaf):
    # Aggregation: sum(col_a) AS sum_a
    # Group by nothing
    agg_op = agg_ex.UnaryAggregation(
        op=agg_ops.sum_op,
        arg=ex.DerefOp(leaf.fields[0].id),
    )
    node = nodes.AggregateNode(
        child=leaf,
        aggregations=((agg_op, identifiers.ColumnId("sum_a")),),
        by_column_ids=(),
    )

    id_generator = (identifiers.ColumnId(f"id_{i}") for i in range(100))
    _, mapping = id_rewrite.remap_variables(node, id_generator)

    # leaf has 2 columns: col_a, col_b
    # AggregateNode defines 1 column: sum_a
    # Output of AggregateNode should only be sum_a
    assert len(mapping) == 1
    assert identifiers.ColumnId("sum_a") in mapping


def test_remap_variables_aggregate_with_grouping(leaf):
    # Aggregation: sum(col_b) AS sum_b
    # Group by col_a
    agg_op = agg_ex.UnaryAggregation(
        op=agg_ops.sum_op,
        arg=ex.DerefOp(leaf.fields[1].id),
    )
    node = nodes.AggregateNode(
        child=leaf,
        aggregations=((agg_op, identifiers.ColumnId("sum_b")),),
        by_column_ids=(ex.DerefOp(leaf.fields[0].id),),
    )

    id_generator = (identifiers.ColumnId(f"id_{i}") for i in range(100))
    _, mapping = id_rewrite.remap_variables(node, id_generator)

    # Output should have 2 columns: col_a (grouping) and sum_b (agg)
    assert len(mapping) == 2
    assert leaf.fields[0].id in mapping
    assert identifiers.ColumnId("sum_b") in mapping


def test_remap_variables_nested_join_stability(leaf, fake_session, table):
    # Create two more distinct leaf nodes
    leaf2_uncached = core.ArrayValue.from_table(
        session=fake_session,
        table=bq_data.GbqNativeTable.from_table(table),
    ).node
    leaf2 = leaf2_uncached.remap_vars(
        {
            field.id: identifiers.ColumnId(f"leaf2_{field.id.name}")
            for field in leaf2_uncached.fields
        }
    )
    leaf3_uncached = core.ArrayValue.from_table(
        session=fake_session,
        table=bq_data.GbqNativeTable.from_table(table),
    ).node
    leaf3 = leaf3_uncached.remap_vars(
        {
            field.id: identifiers.ColumnId(f"leaf3_{field.id.name}")
            for field in leaf3_uncached.fields
        }
    )

    # Create a nested join: (leaf JOIN leaf2) JOIN leaf3
    inner_join = nodes.JoinNode(
        left_child=leaf,
        right_child=leaf2,
        conditions=(
            (
                core.expression.DerefOp(leaf.fields[0].id),
                core.expression.DerefOp(leaf2.fields[0].id),
            ),
        ),
        type="inner",
        propogate_order=False,
    )
    outer_join = nodes.JoinNode(
        left_child=inner_join,
        right_child=leaf3,
        conditions=(
            (
                core.expression.DerefOp(inner_join.fields[0].id),
                core.expression.DerefOp(leaf3.fields[0].id),
            ),
        ),
        type="inner",
        propogate_order=False,
    )

    # Run remap_variables twice and assert stability
    id_generator1 = (identifiers.ColumnId(f"id_{i}") for i in range(100))
    new_node1, mapping1 = id_rewrite.remap_variables(outer_join, id_generator1)

    id_generator2 = (identifiers.ColumnId(f"id_{i}") for i in range(100))
    new_node2, mapping2 = id_rewrite.remap_variables(outer_join, id_generator2)

    assert new_node1 == new_node2
    assert mapping1 == mapping2


def test_remap_variables_concat_self_stability(leaf):
    # Create a concat node with the same child twice
    node = nodes.ConcatNode(
        children=(leaf, leaf),
        output_ids=(
            identifiers.ColumnId("concat_a"),
            identifiers.ColumnId("concat_b"),
        ),
    )

    # Run remap_variables twice and assert stability
    id_generator1 = (identifiers.ColumnId(f"id_{i}") for i in range(100))
    new_node1, mapping1 = id_rewrite.remap_variables(node, id_generator1)

    id_generator2 = (identifiers.ColumnId(f"id_{i}") for i in range(100))
    new_node2, mapping2 = id_rewrite.remap_variables(node, id_generator2)

    assert new_node1 == new_node2
    assert mapping1 == mapping2


def test_remap_variables_in_node_converts_dag_to_tree(leaf, leaf_too):
    # Create an InNode with the same child twice, should create a tree from a DAG
    right = nodes.SelectionNode(
        leaf_too, (nodes.AliasedRef.identity(identifiers.ColumnId("col_a")),)
    )
    node = nodes.InNode(
        left_child=leaf,
        right_child=right,
        left_col=ex.DerefOp(identifiers.ColumnId("col_a")),
        indicator_col=identifiers.ColumnId("indicator"),
    )

    id_generator = (identifiers.ColumnId(f"id_{i}") for i in range(100))
    new_node, _ = id_rewrite.remap_variables(node, id_generator)
    new_node = typing.cast(nodes.InNode, new_node)

    left_col_id = new_node.left_col.id.name
    new_node.validate_tree()
    assert left_col_id.startswith("id_")
