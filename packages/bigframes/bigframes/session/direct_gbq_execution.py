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

from typing import Literal, Optional, Tuple

from google.cloud import bigquery
import google.cloud.bigquery.job as bq_job
import google.cloud.bigquery.table as bq_table

from bigframes.core import compile, nodes
import bigframes.core.compile.ibis_compiler.ibis_compiler as ibis_compiler
import bigframes.core.compile.sqlglot.compiler as sqlglot_compiler
import bigframes.core.events
from bigframes.session import executor, semi_executor
import bigframes.session._io.bigquery as bq_io


# used only in testing right now, BigQueryCachingExecutor is the fully featured engine
# simplified, doesnt not do large >10 gb result queries, error handling, respect global config
# or record metrics. Also avoids caching, and most pre-compile rewrites, to better serve as a
# reference for validating more complex executors.
class DirectGbqExecutor(semi_executor.SemiExecutor):
    def __init__(
        self,
        bqclient: bigquery.Client,
        compiler: Literal["ibis", "sqlglot"] = "ibis",
        *,
        publisher: bigframes.core.events.Publisher,
    ):
        self.bqclient = bqclient
        self._compile_fn = (
            ibis_compiler.compile_sql
            if compiler == "ibis"
            else sqlglot_compiler.compile_sql
        )
        self._publisher = publisher

    def execute(
        self,
        plan: nodes.BigFrameNode,
        ordered: bool,
        peek: Optional[int] = None,
    ) -> executor.ExecuteResult:
        """Just execute whatever plan as is, without further caching or decomposition."""
        # TODO(swast): plumb through the api_name of the user-facing api that
        # caused this query.

        compiled = self._compile_fn(
            compile.CompileRequest(plan, sort_rows=ordered, peek_count=peek)
        )

        iterator, query_job = self._run_execute_query(
            sql=compiled.sql,
            session=plan.session,
        )

        # just immediately downlaod everything for simplicity
        return executor.LocalExecuteResult(
            data=iterator.to_arrow(),
            bf_schema=plan.schema,
            execution_metadata=executor.ExecutionMetadata.from_iterator_and_job(
                iterator, query_job
            ),
        )

    def _run_execute_query(
        self,
        sql: str,
        job_config: Optional[bq_job.QueryJobConfig] = None,
        session=None,
    ) -> Tuple[bq_table.RowIterator, Optional[bigquery.QueryJob]]:
        """
        Starts BigQuery query job and waits for results.
        """
        return bq_io.start_query_with_client(
            self.bqclient,
            sql,
            job_config=job_config or bq_job.QueryJobConfig(),
            project=None,
            location=None,
            timeout=None,
            metrics=None,
            query_with_job=False,
            publisher=self._publisher,
            session=session,
        )
