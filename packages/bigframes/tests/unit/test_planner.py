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
from __future__ import annotations

import unittest.mock as mock

import google.cloud.bigquery
import pandas as pd

import bigframes.core as core
import bigframes.core.expression as ex
import bigframes.core.identifiers as ids
import bigframes.core.schema
import bigframes.operations as ops
import bigframes.session.planner as planner

TABLE_REF = google.cloud.bigquery.TableReference.from_string("project.dataset.table")
SCHEMA = (
    google.cloud.bigquery.SchemaField("col_a", "INTEGER"),
    google.cloud.bigquery.SchemaField("col_b", "INTEGER"),
)
TABLE = google.cloud.bigquery.Table(
    table_ref=TABLE_REF,
    schema=SCHEMA,
)
FAKE_SESSION = mock.create_autospec(bigframes.Session, instance=True)
type(FAKE_SESSION)._strictly_ordered = mock.PropertyMock(return_value=True)
LEAF: core.ArrayValue = core.ArrayValue.from_table(
    session=FAKE_SESSION,
    table=TABLE,
    schema=bigframes.core.schema.ArraySchema.from_bq_table(TABLE),
)


def test_session_aware_caching_project_filter():
    """
    Test that if a node is filtered by a column, the node is cached pre-filter and clustered by the filter column.
    """
    session_objects = [LEAF, LEAF.create_constant(4, pd.Int64Dtype())[0]]
    target, _ = LEAF.create_constant(4, pd.Int64Dtype())
    target = target.filter(ops.gt_op.as_expr("col_a", ex.const(3)))
    result, cluster_cols = planner.session_aware_cache_plan(
        target.node, [obj.node for obj in session_objects]
    )
    assert result == LEAF.node
    assert cluster_cols == [ids.ColumnId("col_a")]


def test_session_aware_caching_project_multi_filter():
    """
    Test that if a node is filtered by multiple columns, all of them are in the cluster cols
    """
    obj1 = LEAF
    obj2, _ = LEAF.create_constant(4, pd.Int64Dtype())
    session_objects = [obj1, obj2]
    predicate_1a = ops.gt_op.as_expr("col_a", ex.const(3))
    predicate_1b = ops.lt_op.as_expr("col_a", ex.const(55))
    predicate_1 = ops.and_op.as_expr(predicate_1a, predicate_1b)
    predicate_3 = ops.eq_op.as_expr("col_b", ex.const(1))
    target = (
        LEAF.filter(predicate_1)
        .create_constant(4, pd.Int64Dtype())[0]
        .filter(predicate_3)
    )
    result, cluster_cols = planner.session_aware_cache_plan(
        target.node, [obj.node for obj in session_objects]
    )
    assert result == LEAF.node
    assert cluster_cols == [ids.ColumnId("col_a"), ids.ColumnId("col_b")]


def test_session_aware_caching_unusable_filter():
    """
    Test that if a node is filtered by multiple columns in the same comparison, the node is cached pre-filter and not clustered by either column.

    Most filters with multiple column references cannot be used for scan pruning, as they cannot be converted to fixed value ranges.
    """
    session_objects = [LEAF, LEAF.create_constant(4, pd.Int64Dtype())[0]]
    target = LEAF.create_constant(4, pd.Int64Dtype())[0].filter(
        ops.gt_op.as_expr("col_a", "col_b")
    )
    result, cluster_cols = planner.session_aware_cache_plan(
        target.node, [obj.node for obj in session_objects]
    )
    assert result == LEAF.node
    assert cluster_cols == []


def test_session_aware_caching_fork_after_window_op():
    """
    Test that caching happens only after an windowed operation, but before filtering, projecting.

    Windowing is expensive, so caching should always compute the window function, in order to avoid later recomputation.
    """
    leaf_with_offsets = LEAF.promote_offsets()[0]
    other = leaf_with_offsets.create_constant(5, pd.Int64Dtype())[0]
    target = leaf_with_offsets.create_constant(4, pd.Int64Dtype())[0].filter(
        ops.eq_op.as_expr("col_a", ops.add_op.as_expr(ex.const(4), ex.const(3)))
    )
    result, cluster_cols = planner.session_aware_cache_plan(
        target.node,
        [
            other.node,
        ],
    )
    assert result == leaf_with_offsets.node
    assert cluster_cols == [ids.ColumnId("col_a")]
