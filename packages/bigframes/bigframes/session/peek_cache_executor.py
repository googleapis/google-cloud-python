# Copyright 2026 Google LLC
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

import asyncio
import dataclasses
from typing import Optional

import google.cloud.bigquery as bigquery

import bigframes.core
import bigframes.core.events
from bigframes.core import local_data
from bigframes.session import execution_spec as ex_spec
from bigframes.session import executor
from bigframes.session._async import run_sync


class PeekCacheExecutor(executor.Executor):
    """
    Decorator executor that implements a peek cache.

    If the execution spec requests a peek and the peek cache is enabled,
    it attempts to rewrite the plan to use cached subplans and execute it
    locally using the Polars executor.

    Otherwise, it delegates execution to the target executor and caches
    the result.
    """

    def __init__(
        self,
        target: executor.Executor,
        publisher: bigframes.core.events.Publisher,
    ):
        self._target = target
        self._publisher = publisher

        from bigframes.session.peek_cache import PeekCache

        self._peek_cache = PeekCache()

        self._polars_executor = None
        try:
            from bigframes.session.polars_executor import PolarsExecutor

            self._polars_executor = PolarsExecutor()
        except ImportError:
            # Polars is not installed, so the peek cache shortcut cannot be used.
            pass

    def to_sql(
        self,
        array_value: bigframes.core.ArrayValue,
        offset_column: Optional[str] = None,
        ordered: bool = False,
        enable_cache: bool = True,
    ) -> str:
        return self._target.to_sql(
            array_value,
            offset_column=offset_column,
            ordered=ordered,
            enable_cache=enable_cache,
        )

    def dry_run(
        self, array_value: bigframes.core.ArrayValue, ordered: bool = True
    ) -> bigquery.QueryJob:
        return self._target.dry_run(array_value, ordered=ordered)

    def cached(
        self,
        array_value: bigframes.core.ArrayValue,
        *,
        config: executor.CacheConfig,
    ) -> None:
        return self._target.cached(array_value, config=config)

    def execute(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: ex_spec.ExecutionSpec,
    ) -> executor.ExecuteResult:
        from bigframes.session.productionize import _state as prod_state

        if prod_state.active:
            return self._target.execute(array_value, execution_spec)

        execution_spec = execution_spec.with_compute_options(bigframes.options.compute)

        enable_peek_cache = (
            execution_spec.bigquery_config.enable_peek_cache
            if execution_spec.bigquery_config
            else False
        )

        if not enable_peek_cache or self._polars_executor is None:
            return self._target.execute(array_value, execution_spec)

        return run_sync(self._execute_async(array_value, execution_spec))

    async def _execute_async(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: ex_spec.ExecutionSpec,
    ) -> executor.ExecuteResult:
        await self._publisher.publish_async(bigframes.core.events.ExecutionStarted())

        from bigframes.session.peek_cache import substitute_peek_cached_subplans

        # 1. Attempt to rewrite the plan using cached subplans from the peek cache.
        rewritten_node = substitute_peek_cached_subplans(
            array_value.node,
            self._peek_cache,
            min_rows_required=execution_spec.peek,
        )
        if rewritten_node != array_value.node:
            # The plan was rewritten! Try to execute the rewritten plan using only the Polars executor.
            assert self._polars_executor is not None
            maybe_result = await self._polars_executor.execute(
                rewritten_node, execution_spec
            )
            if maybe_result is not None:
                num_rows = maybe_result.batches().approx_total_rows
                # If it's a full execution (peek is None), the result is complete because we only substituted complete entries.
                # If it's a peek execution, we must ensure we got enough rows.
                is_sufficient = execution_spec.peek is None or (
                    num_rows is not None and num_rows >= execution_spec.peek
                )
                if is_sufficient:
                    await self._publisher.publish_async(
                        bigframes.core.events.EventEnvelope(
                            event=bigframes.core.events.ExecutionFinished(
                                result=maybe_result,
                            ),
                            cell_execution_count=execution_spec.cell_execution_count,
                        )
                    )
                    return maybe_result

        # 2. If the shortcut wasn't used or failed, run the query on the target executor.
        if execution_spec.peek is not None:
            sample_size = (
                execution_spec.bigquery_config.peek_cache_size
                if execution_spec.bigquery_config
                else 10000
            )
            actual_sample_size = max(execution_spec.peek, sample_size)
            cache_execution_spec = dataclasses.replace(
                execution_spec, peek=actual_sample_size
            )
        else:
            cache_execution_spec = execution_spec

        bq_result = await asyncio.to_thread(
            self._target.execute,
            array_value,
            cache_execution_spec,
        )

        # 3. Cache the result if appropriate.
        if execution_spec.peek is not None:
            # For peek executions, we always download and cache the sample.
            arrow_table = await asyncio.to_thread(bq_result.batches().to_arrow_table)
            is_complete = arrow_table.num_rows < actual_sample_size
            managed_table = local_data.ManagedArrowTable.from_pyarrow(
                arrow_table, bq_result.schema
            )
            self._peek_cache.put(
                array_value.node, managed_table, is_complete=is_complete
            )

            sliced_table = arrow_table.slice(0, execution_spec.peek)
            result: executor.ExecuteResult = executor.LocalExecuteResult(
                sliced_table,
                bq_result.schema,
                execution_metadata=bq_result.execution_metadata,
            )
        else:
            # For full executions, we only cache if the target executor returned a local result.
            if isinstance(bq_result, executor.LocalExecuteResult):
                peek_cache_size = (
                    execution_spec.bigquery_config.peek_cache_size
                    if execution_spec.bigquery_config
                    else 10000
                )
                if bq_result._data.data.num_rows > peek_cache_size:
                    sliced_data = bq_result._data.data.slice(0, peek_cache_size)
                    managed_table = local_data.ManagedArrowTable.from_pyarrow(
                        sliced_data, bq_result.schema
                    )
                    is_complete = False
                else:
                    managed_table = bq_result._data
                    is_complete = True
                self._peek_cache.put(
                    array_value.node, managed_table, is_complete=is_complete
                )
            result = bq_result

        await self._publisher.publish_async(
            bigframes.core.events.EventEnvelope(
                event=bigframes.core.events.ExecutionFinished(result=result),
                cell_execution_count=execution_spec.cell_execution_count,
            )
        )
        return result
