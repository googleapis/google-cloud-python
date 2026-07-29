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

import uuid
import warnings
from typing import Optional

import google.cloud.bigquery as bigquery
import google.cloud.exceptions

import bigframes.core
import bigframes.functions._function_session as bff_session
from bigframes import exceptions as bfe
from bigframes.session import (
    bq_caching_executor,
    execution_cache,
    execution_spec,
    executor,
    loader,
    temporary_storage,
)

_COMPILER_LABEL_KEY = "bigframes-compiler"


class DualCompilerProxyExecutor(executor.Executor):
    """
    Used to rollout new compiler implementation.
    """

    def __init__(
        self,
        bqclient: bigquery.Client,
        storage_manager: temporary_storage.TemporaryStorageManager,
        bqstoragereadclient: google.cloud.bigquery_storage_v1.BigQueryReadClient,
        loader: loader.GbqDataLoader,
        *,
        metrics: Optional[bigframes.session.metrics.ExecutionMetrics] = None,
        enable_polars_execution: bool = False,
        publisher: bigframes.core.events.Publisher,
        function_manager: bff_session.FunctionSession,
        labels: tuple[tuple[str, str], ...] = (),
    ):
        self._enable_polars_execution = enable_polars_execution
        shared_cache = execution_cache.ExecutionCache()
        self._ibis_executor = bq_caching_executor.BigQueryCachingExecutor(
            bqclient,
            storage_manager,
            bqstoragereadclient,
            loader,
            metrics=metrics,
            enable_polars_execution=self._enable_polars_execution,
            publisher=publisher,
            labels=labels,
            cache=shared_cache,
            compiler_name="ibis",
            function_manager=function_manager,
        )
        self._sqlglot_executor = bq_caching_executor.BigQueryCachingExecutor(
            bqclient,
            storage_manager,
            bqstoragereadclient,
            loader,
            metrics=metrics,
            enable_polars_execution=self._enable_polars_execution,
            publisher=publisher,
            labels=labels,
            cache=shared_cache,
            compiler_name="sqlglot",
            function_manager=function_manager,
        )

    def to_sql(
        self,
        array_value: bigframes.core.ArrayValue,
        offset_column: Optional[str] = None,
        ordered: bool = False,
        enable_cache: bool = True,
    ) -> str:
        """
        Convert an ArrayValue to a sql query that will yield its value.
        """
        compiler_option = bigframes.options.experiments.sql_compiler
        # Use ibis unless sqlglot explicitly selected, since we can't handle errors resulting
        # from use of the sql produced by this method.
        if compiler_option == "experimental":
            return self._sqlglot_executor.to_sql(
                array_value,
                offset_column=offset_column,
                ordered=ordered,
                enable_cache=enable_cache,
            )
        # stable or legacy use ibis
        # TODO(b/510408650): Use sqlglot by default.
        return self._ibis_executor.to_sql(
            array_value,
            offset_column=offset_column,
            ordered=ordered,
            enable_cache=enable_cache,
        )

    def execute(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: execution_spec.ExecutionSpec,
    ) -> executor.ExecuteResult:
        compiler_option = bigframes.options.experiments.sql_compiler
        if compiler_option == "legacy":
            return self._ibis_executor.execute(array_value, execution_spec)
        elif compiler_option == "experimental":
            return self._sqlglot_executor.execute(
                array_value,
                execution_spec.with_bq_labels({_COMPILER_LABEL_KEY: "sqlglot"}),
            )
        else:  # stable
            correlation_id = f"{uuid.uuid1().hex[:12]}"
            try:
                return self._sqlglot_executor.execute(
                    array_value,
                    execution_spec.with_bq_labels(
                        {_COMPILER_LABEL_KEY: f"sqlglot-{correlation_id}"}
                    ),
                )
            except Exception as e:
                msg = bfe.format_message(
                    f"Compiler ID {correlation_id}: Exception on sqlglot. "
                    f"Falling back to ibis. Details: {e}"
                )
                warnings.warn(msg, category=UserWarning)
                return self._ibis_executor.execute(
                    array_value,
                    execution_spec.with_bq_labels(
                        {_COMPILER_LABEL_KEY: f"ibis-{correlation_id}"}
                    ),
                )

    def dry_run(
        self, array_value: bigframes.core.ArrayValue, ordered: bool = True
    ) -> bigquery.QueryJob:
        """
        Dry run executing the ArrayValue.

        Does not actually execute the data but will get stats and indicate any invalid query errors.
        """
        # TODO(b/510408650): Use sqlglot for dry runs when sqlglot has been validated.
        return self._ibis_executor.dry_run(array_value, ordered=ordered)

    def cached(
        self,
        array_value: bigframes.core.ArrayValue,
        *,
        config: executor.CacheConfig,
    ) -> None:
        compiler_option = bigframes.options.experiments.sql_compiler
        if compiler_option == "legacy":
            return self._ibis_executor.cached(array_value, config=config)
        elif compiler_option == "experimental":
            return self._sqlglot_executor.cached(array_value, config=config)
        else:  # stable
            correlation_id = f"{uuid.uuid1().hex[:12]}"
            try:
                return self._sqlglot_executor.cached(array_value, config=config)
            except Exception as e:
                msg = bfe.format_message(
                    f"Compiler ID {correlation_id}: Exception on sqlglot. "
                    f"Falling back to ibis. Details: {e}"
                )
                warnings.warn(msg, category=UserWarning)
                return self._ibis_executor.cached(
                    array_value,
                    config=config,
                )
