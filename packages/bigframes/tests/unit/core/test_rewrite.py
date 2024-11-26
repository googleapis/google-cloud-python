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
import unittest.mock as mock

import google.cloud.bigquery

import bigframes.core as core
import bigframes.core.nodes as nodes
import bigframes.core.rewrite.slices
import bigframes.core.schema

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
LEAF = core.ArrayValue.from_table(
    session=FAKE_SESSION,
    table=TABLE,
    schema=bigframes.core.schema.ArraySchema.from_bq_table(TABLE),
).node


def test_rewrite_noop_slice():
    slice = nodes.SliceNode(LEAF, None, None)
    result = bigframes.core.rewrite.slices.rewrite_slice(slice)
    assert result == LEAF


def test_rewrite_reverse_slice():
    slice = nodes.SliceNode(LEAF, None, None, -1)
    result = bigframes.core.rewrite.slices.rewrite_slice(slice)
    assert result == nodes.ReversedNode(LEAF)


def test_rewrite_filter_slice():
    slice = nodes.SliceNode(LEAF, None, 2)
    result = bigframes.core.rewrite.slices.rewrite_slice(slice)
    assert list(result.fields) == list(LEAF.fields)
    assert isinstance(result.child, nodes.FilterNode)
