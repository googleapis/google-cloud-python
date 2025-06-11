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

import pytest

import bigframes
from bigframes.core import identifiers, local_data, nodes
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


def test_engines_read_local(
    fake_session: bigframes.Session,
    managed_data_source: local_data.ManagedArrowTable,
    engine,
):
    scan_list = nodes.ScanList.from_items(
        nodes.ScanItem(identifiers.ColumnId(item.column), item.dtype, item.column)
        for item in managed_data_source.schema.items
    )
    local_node = nodes.ReadLocalNode(
        managed_data_source, scan_list, fake_session, offsets_col=None
    )
    assert_equivalence_execution(local_node, REFERENCE_ENGINE, engine)


def test_engines_read_local_w_offsets(
    fake_session: bigframes.Session,
    managed_data_source: local_data.ManagedArrowTable,
    engine,
):
    scan_list = nodes.ScanList.from_items(
        nodes.ScanItem(identifiers.ColumnId(item.column), item.dtype, item.column)
        for item in managed_data_source.schema.items
    )
    local_node = nodes.ReadLocalNode(
        managed_data_source,
        scan_list,
        fake_session,
        offsets_col=identifiers.ColumnId("offsets"),
    )
    assert_equivalence_execution(local_node, REFERENCE_ENGINE, engine)


def test_engines_read_local_w_col_subset(
    fake_session: bigframes.Session,
    managed_data_source: local_data.ManagedArrowTable,
    engine,
):
    scan_list = nodes.ScanList.from_items(
        nodes.ScanItem(identifiers.ColumnId(item.column), item.dtype, item.column)
        for item in managed_data_source.schema.items[::-2]
    )
    local_node = nodes.ReadLocalNode(
        managed_data_source, scan_list, fake_session, offsets_col=None
    )
    assert_equivalence_execution(local_node, REFERENCE_ENGINE, engine)


def test_engines_read_local_w_zero_row_source(
    fake_session: bigframes.Session,
    zero_row_source: local_data.ManagedArrowTable,
    engine,
):
    scan_list = nodes.ScanList.from_items(
        nodes.ScanItem(identifiers.ColumnId(item.column), item.dtype, item.column)
        for item in zero_row_source.schema.items
    )
    local_node = nodes.ReadLocalNode(
        zero_row_source, scan_list, fake_session, offsets_col=None
    )
    assert_equivalence_execution(local_node, REFERENCE_ENGINE, engine)


def test_engines_read_local_w_nested_source(
    fake_session: bigframes.Session,
    nested_data_source: local_data.ManagedArrowTable,
    engine,
):
    scan_list = nodes.ScanList.from_items(
        nodes.ScanItem(identifiers.ColumnId(item.column), item.dtype, item.column)
        for item in nested_data_source.schema.items
    )
    local_node = nodes.ReadLocalNode(
        nested_data_source, scan_list, fake_session, offsets_col=None
    )
    assert_equivalence_execution(local_node, REFERENCE_ENGINE, engine)


def test_engines_read_local_w_repeated_source(
    fake_session: bigframes.Session,
    repeated_data_source: local_data.ManagedArrowTable,
    engine,
):
    scan_list = nodes.ScanList.from_items(
        nodes.ScanItem(identifiers.ColumnId(item.column), item.dtype, item.column)
        for item in repeated_data_source.schema.items
    )
    local_node = nodes.ReadLocalNode(
        repeated_data_source, scan_list, fake_session, offsets_col=None
    )
    assert_equivalence_execution(local_node, REFERENCE_ENGINE, engine)
