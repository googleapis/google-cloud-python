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
from __future__ import annotations

import pyarrow
import pytest

from bigframes import dtypes
from bigframes.core import identifiers, local_data, nodes
from bigframes.session import local_scan_executor
from bigframes.testing import mocks


@pytest.fixture
def object_under_test():
    return local_scan_executor.LocalScanExecutor()


def create_read_local_node(arrow_table: pyarrow.Table):
    session = mocks.create_bigquery_session()
    local_data_source = local_data.ManagedArrowTable.from_pyarrow(arrow_table)
    return nodes.ReadLocalNode(
        local_data_source=local_data_source,
        session=session,
        scan_list=nodes.ScanList(
            items=tuple(
                nodes.ScanItem(
                    id=identifiers.ColumnId(column_name),
                    dtype=dtypes.arrow_dtype_to_bigframes_dtype(
                        arrow_table.field(column_name).type
                    ),
                    source_id=column_name,
                )
                for column_name in arrow_table.column_names
            ),
        ),
    )


@pytest.mark.parametrize(
    ("start", "stop", "expected_rows"),
    (
        # No-op slices.
        (None, None, 10),
        (0, None, 10),
        (None, 10, 10),
        # Slices equivalent to limits.
        (None, 7, 7),
        (0, 3, 3),
    ),
)
def test_local_scan_executor_with_slice(start, stop, expected_rows, object_under_test):
    pyarrow_table = pyarrow.Table.from_pydict(
        {
            "rowindex": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "letters": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
        }
    )
    assert pyarrow_table.num_rows == 10

    local_node = create_read_local_node(pyarrow_table)
    plan = nodes.SliceNode(
        child=local_node,
        start=start,
        stop=stop,
    )

    result = object_under_test.execute(plan, ordered=True)
    result_table = pyarrow.Table.from_batches(result.arrow_batches)
    assert result_table.num_rows == expected_rows


@pytest.mark.parametrize(
    ("start", "stop", "step"),
    (
        (-1, None, 1),
        (None, -1, 1),
        (None, None, 2),
        (None, None, -1),
        (4, None, 6),
        (1, 9, 8),
    ),
)
def test_local_scan_executor_with_slice_unsupported_inputs(
    start, stop, step, object_under_test
):
    local_node = create_read_local_node(pyarrow.Table.from_pydict({"col": [1, 2, 3]}))
    plan = nodes.SliceNode(
        child=local_node,
        start=start,
        stop=stop,
        step=step,
    )
    assert object_under_test.execute(plan, ordered=True) is None
