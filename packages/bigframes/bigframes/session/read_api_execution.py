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

from typing import Optional

from google.cloud import bigquery_storage_v1

from bigframes.core import bigframe_node, nodes, rewrite
from bigframes.session import executor, semi_executor


class ReadApiSemiExecutor(semi_executor.SemiExecutor):
    """
    Executes plans reducible to a bq table scan by directly reading the table with the read api.
    """

    def __init__(
        self,
        bqstoragereadclient: bigquery_storage_v1.BigQueryReadClient,
        project: str,
    ):
        self.bqstoragereadclient = bqstoragereadclient
        self.project = project

    def execute(
        self,
        plan: bigframe_node.BigFrameNode,
        ordered: bool,
        peek: Optional[int] = None,
    ) -> Optional[executor.ExecuteResult]:
        adapt_result = self._try_adapt_plan(plan, ordered)
        if not adapt_result:
            return None
        node, limit = adapt_result
        if node.explicitly_ordered and ordered:
            return None

        if not node.source.table.is_physically_stored:
            return None

        if limit is not None:
            if peek is None or limit < peek:
                peek = limit

        return executor.BQTableExecuteResult(
            data=node.source,
            project_id=self.project,
            storage_client=self.bqstoragereadclient,
            limit=peek,
            selected_fields=[
                (item.source_id, item.id.sql) for item in node.scan_list.items
            ],
        )

    def _try_adapt_plan(
        self,
        plan: bigframe_node.BigFrameNode,
        ordered: bool,
    ) -> Optional[tuple[nodes.ReadTableNode, Optional[int]]]:
        """
        Tries to simplify the plan to an equivalent single ReadTableNode and a limit. Otherwise, returns None.
        """
        plan, limit = rewrite.pull_out_limit(plan)
        # bake_order does not allow slice ops
        plan = plan.bottom_up(rewrite.rewrite_slice)
        if not ordered:
            # gets rid of order_by ops
            plan = rewrite.bake_order(plan)
        read_table_node = rewrite.try_reduce_to_table_scan(plan)
        if read_table_node is None:
            return None
        if (limit is not None) and (read_table_node.source.ordering is not None):
            # read api can only use physical ordering to limit, not a logical ordering
            return None
        return (read_table_node, limit)
