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

import pyarrow as pa

from bigframes import dtypes
from bigframes.core import local_data, nodes
from bigframes.operations import aggregations


def fold_row_counts(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
    if not isinstance(node, nodes.AggregateNode):
        return node
    if len(node.by_column_ids) > 0:
        return node
    if node.child.row_count is None:
        return node
    for agg, _ in node.aggregations:
        if agg.op != aggregations.size_op:
            return node
    local_data_source = local_data.ManagedArrowTable.from_pyarrow(
        pa.table({"count": pa.array([node.child.row_count], type=pa.int64())})
    )
    scan_list = nodes.ScanList(
        tuple(
            nodes.ScanItem(out_id, dtypes.INT_DTYPE, "count")
            for _, out_id in node.aggregations
        )
    )
    return nodes.ReadLocalNode(
        local_data_source=local_data_source, scan_list=scan_list, session=node.session
    )
