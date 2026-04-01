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

import dataclasses
from typing import Mapping, Optional
import weakref

from bigframes.core import bq_data, local_data, nodes

SourceIdMapping = Mapping[str, str]


@dataclasses.dataclass(frozen=True)
class UploadedLocalData:
    bq_source: bq_data.BigqueryDataSource
    source_mapping: SourceIdMapping


class ExecutionCache:
    def __init__(self):
        # effectively two separate caches that don't interact
        self._cached_executions: weakref.WeakKeyDictionary[
            nodes.BigFrameNode, bq_data.BigqueryDataSource
        ] = weakref.WeakKeyDictionary()
        # This upload cache is entirely independent of the plan cache.
        self._uploaded_local_data: weakref.WeakKeyDictionary[
            local_data.ManagedArrowTable,
            UploadedLocalData,
        ] = weakref.WeakKeyDictionary()

    def subsitute_cached_subplans(self, root: nodes.BigFrameNode) -> nodes.BigFrameNode:
        def replace_if_cached(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
            if node not in self._cached_executions:
                return node
            # Assumption: GBQ cached table uses field name as bq column name
            scan_list = nodes.ScanList(
                tuple(nodes.ScanItem(field.id, field.id.sql) for field in node.fields)
            )
            bq_data = self._cached_executions[node]
            cached_replacement = nodes.CachedTableNode(
                source=bq_data,
                scan_list=scan_list,
                table_session=node.session,
                original_node=node,
            )
            assert node.schema == cached_replacement.schema
            return cached_replacement

        return nodes.top_down(root, replace_if_cached)

    def cache_results_table(
        self,
        original_root: nodes.BigFrameNode,
        data: bq_data.BigqueryDataSource,
    ):
        self._cached_executions[original_root] = data

    ## Local data upload caching
    def cache_remote_replacement(
        self,
        local_data: local_data.ManagedArrowTable,
        bq_data: bq_data.BigqueryDataSource,
    ):
        # bq table has one extra column for offsets, those are implicit for local data
        assert len(local_data.schema.items) + 1 == len(bq_data.table.physical_schema)
        mapping = {
            local_data.schema.items[i].column: bq_data.table.physical_schema[i].name
            for i in range(len(local_data.schema))
        }
        self._uploaded_local_data[local_data] = UploadedLocalData(bq_data, mapping)

    def get_uploaded_local_data(
        self, local_data: local_data.ManagedArrowTable
    ) -> Optional[UploadedLocalData]:
        return self._uploaded_local_data.get(local_data)
