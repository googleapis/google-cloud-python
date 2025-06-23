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

from typing import Any, Iterator, Optional

from google.cloud import bigquery_storage_v1
import pyarrow as pa

from bigframes.core import bigframe_node, nodes, pyarrow_utils, rewrite
from bigframes.session import executor, semi_executor


class ReadApiSemiExecutor(semi_executor.SemiExecutor):
    """
    Executes plans reducible to a bq table scan by directly reading the table with the read api.
    """

    def __init__(
        self, bqstoragereadclient: bigquery_storage_v1.BigQueryReadClient, project: str
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

        if limit is not None:
            if peek is None or limit < peek:
                peek = limit

        import google.cloud.bigquery_storage_v1.types as bq_storage_types
        from google.protobuf import timestamp_pb2

        bq_table = node.source.table.get_table_ref()
        read_options: dict[str, Any] = {
            "selected_fields": [item.source_id for item in node.scan_list.items]
        }
        if node.source.sql_predicate:
            read_options["row_restriction"] = node.source.sql_predicate
        read_options = bq_storage_types.ReadSession.TableReadOptions(**read_options)

        table_mod_options = {}
        if node.source.at_time:
            snapshot_time = timestamp_pb2.Timestamp()
            snapshot_time.FromDatetime(node.source.at_time)
            table_mod_options["snapshot_time"] = snapshot_time = snapshot_time
        table_mods = bq_storage_types.ReadSession.TableModifiers(**table_mod_options)

        requested_session = bq_storage_types.stream.ReadSession(
            table=bq_table.to_bqstorage(),
            data_format=bq_storage_types.DataFormat.ARROW,
            read_options=read_options,
            table_modifiers=table_mods,
        )
        # Single stream to maintain ordering
        request = bq_storage_types.CreateReadSessionRequest(
            parent=f"projects/{self.project}",
            read_session=requested_session,
            max_stream_count=1,
        )
        session = self.bqstoragereadclient.create_read_session(
            request=request, retry=None
        )

        if not session.streams:
            batches: Iterator[pa.RecordBatch] = iter([])
        else:
            reader = self.bqstoragereadclient.read_rows(
                session.streams[0].name, retry=None
            )
            rowstream = reader.rows()

            def process_page(page):
                pa_batch = page.to_arrow()
                pa_batch = pa_batch.select(
                    [item.source_id for item in node.scan_list.items]
                )
                return pa.RecordBatch.from_arrays(
                    pa_batch.columns, names=[id.sql for id in node.ids]
                )

            batches = map(process_page, rowstream.pages)

        if peek:
            batches = pyarrow_utils.truncate_pyarrow_iterable(batches, max_results=peek)

        rows = node.source.n_rows
        if peek and rows:
            rows = min(peek, rows)

        return executor.ExecuteResult(
            _arrow_batches=batches,
            schema=plan.schema,
            query_job=None,
            total_bytes=None,
            total_rows=rows,
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
