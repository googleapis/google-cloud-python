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

import abc
import dataclasses
import functools
import itertools
from typing import Iterator, Literal, Optional, Sequence, Union

from google.cloud import bigquery, bigquery_storage_v1
import google.cloud.bigquery.table as bq_table
import pandas as pd
import pyarrow
import pyarrow as pa

import bigframes
import bigframes.core
from bigframes.core import bq_data, local_data, pyarrow_utils
import bigframes.core.schema
import bigframes.dtypes
import bigframes.session._io.pandas as io_pandas
import bigframes.session.execution_spec as ex_spec

_ROW_LIMIT_EXCEEDED_TEMPLATE = (
    "Execution has downloaded {result_rows} rows so far, which exceeds the "
    "limit of {maximum_result_rows}. You can adjust this limit by setting "
    "`bpd.options.compute.maximum_result_rows`."
)


class ResultsIterator(Iterator[pa.RecordBatch]):
    """
    Iterator for query results, with some extra metadata attached.
    """

    def __init__(
        self,
        batches: Iterator[pa.RecordBatch],
        schema: bigframes.core.schema.ArraySchema,
        total_rows: Optional[int] = 0,
        total_bytes: Optional[int] = 0,
    ):
        self._batches = batches
        self._schema = schema
        self._total_rows = total_rows
        self._total_bytes = total_bytes

    @property
    def approx_total_rows(self) -> Optional[int]:
        return self._total_rows

    @property
    def approx_total_bytes(self) -> Optional[int]:
        return self._total_bytes

    def __next__(self) -> pa.RecordBatch:
        return next(self._batches)

    @property
    def arrow_batches(self) -> Iterator[pyarrow.RecordBatch]:
        result_rows = 0

        for batch in self._batches:
            result_rows += batch.num_rows

            maximum_result_rows = bigframes.options.compute.maximum_result_rows
            if maximum_result_rows is not None and result_rows > maximum_result_rows:
                message = bigframes.exceptions.format_message(
                    _ROW_LIMIT_EXCEEDED_TEMPLATE.format(
                        result_rows=result_rows,
                        maximum_result_rows=maximum_result_rows,
                    )
                )
                raise bigframes.exceptions.MaximumResultRowsExceeded(message)

            yield batch

    def to_arrow_table(self) -> pyarrow.Table:
        # Need to provide schema if no result rows, as arrow can't infer
        # If ther are rows, it is safest to infer schema from batches.
        # Any discrepencies between predicted schema and actual schema will produce errors.
        batches = iter(self.arrow_batches)
        peek_it = itertools.islice(batches, 0, 1)
        peek_value = list(peek_it)
        # TODO: Enforce our internal schema on the table for consistency
        if len(peek_value) > 0:
            return pyarrow.Table.from_batches(
                itertools.chain(peek_value, batches),  # reconstruct
            )
        else:
            try:
                return self._schema.to_pyarrow().empty_table()
            except pa.ArrowNotImplementedError:
                # Bug with some pyarrow versions, empty_table only supports base storage types, not extension types.
                return self._schema.to_pyarrow(use_storage_types=True).empty_table()

    def to_pandas(self) -> pd.DataFrame:
        return io_pandas.arrow_to_pandas(self.to_arrow_table(), self._schema)

    def to_pandas_batches(
        self, page_size: Optional[int] = None, max_results: Optional[int] = None
    ) -> Iterator[pd.DataFrame]:
        assert (page_size is None) or (page_size > 0)
        assert (max_results is None) or (max_results > 0)
        batch_iter: Iterator[
            Union[pyarrow.Table, pyarrow.RecordBatch]
        ] = self.arrow_batches
        if max_results is not None:
            batch_iter = pyarrow_utils.truncate_pyarrow_iterable(
                batch_iter, max_results
            )

        if page_size is not None:
            batches_iter = pyarrow_utils.chunk_by_row_count(batch_iter, page_size)
            batch_iter = map(
                lambda batches: pyarrow.Table.from_batches(batches), batches_iter
            )

        yield from map(
            functools.partial(io_pandas.arrow_to_pandas, schema=self._schema),
            batch_iter,
        )

    def to_py_scalar(self):
        columns = list(self.to_arrow_table().to_pydict().values())
        if len(columns) != 1:
            raise ValueError(
                f"Expected single column result, got {len(columns)} columns."
            )
        column = columns[0]
        if len(column) != 1:
            raise ValueError(f"Expected single row result, got {len(column)} rows.")
        return column[0]


class ExecuteResult(abc.ABC):
    @property
    @abc.abstractmethod
    def execution_metadata(self) -> ExecutionMetadata:
        ...

    @property
    @abc.abstractmethod
    def schema(self) -> bigframes.core.schema.ArraySchema:
        ...

    @abc.abstractmethod
    def batches(self) -> ResultsIterator:
        ...

    @property
    def query_job(self) -> Optional[bigquery.QueryJob]:
        return self.execution_metadata.query_job

    @property
    def total_bytes_processed(self) -> Optional[int]:
        return self.execution_metadata.bytes_processed


@dataclasses.dataclass(frozen=True)
class ExecutionMetadata:
    query_job: Optional[bigquery.QueryJob] = None
    bytes_processed: Optional[int] = None

    @classmethod
    def from_iterator_and_job(
        cls, iterator: bq_table.RowIterator, job: Optional[bigquery.QueryJob]
    ) -> ExecutionMetadata:
        return cls(query_job=job, bytes_processed=iterator.total_bytes_processed)


class LocalExecuteResult(ExecuteResult):
    def __init__(
        self,
        data: pa.Table,
        bf_schema: bigframes.core.schema.ArraySchema,
        execution_metadata: ExecutionMetadata = ExecutionMetadata(),
    ):
        self._data = local_data.ManagedArrowTable.from_pyarrow(data, bf_schema)
        self._execution_metadata = execution_metadata

    @property
    def execution_metadata(self) -> ExecutionMetadata:
        return self._execution_metadata

    @property
    def schema(self) -> bigframes.core.schema.ArraySchema:
        return self._data.schema

    def batches(self) -> ResultsIterator:
        return ResultsIterator(
            iter(self._data.to_arrow()[1]),
            self.schema,
            self._data.metadata.row_count,
            self._data.metadata.total_bytes,
        )


class EmptyExecuteResult(ExecuteResult):
    def __init__(
        self,
        bf_schema: bigframes.core.schema.ArraySchema,
        execution_metadata: ExecutionMetadata = ExecutionMetadata(),
    ):
        self._schema = bf_schema
        self._execution_metadata = execution_metadata

    @property
    def execution_metadata(self) -> ExecutionMetadata:
        return self._execution_metadata

    @property
    def schema(self) -> bigframes.core.schema.ArraySchema:
        return self._schema

    def batches(self) -> ResultsIterator:
        return ResultsIterator(iter([]), self.schema, 0, 0)


class BQTableExecuteResult(ExecuteResult):
    def __init__(
        self,
        data: bq_data.BigqueryDataSource,
        storage_client: bigquery_storage_v1.BigQueryReadClient,
        project_id: str,
        *,
        execution_metadata: ExecutionMetadata = ExecutionMetadata(),
        limit: Optional[int] = None,
        selected_fields: Optional[Sequence[tuple[str, str]]] = None,
    ):
        self._data = data
        self._project_id = project_id
        self._execution_metadata = execution_metadata
        self._storage_client = storage_client
        self._limit = limit
        self._selected_fields = selected_fields or [
            (name, name) for name in data.schema.names
        ]

    @property
    def execution_metadata(self) -> ExecutionMetadata:
        return self._execution_metadata

    @property
    @functools.cache
    def schema(self) -> bigframes.core.schema.ArraySchema:
        source_ids = [selection[0] for selection in self._selected_fields]
        return self._data.schema.select(source_ids).rename(dict(self._selected_fields))

    def batches(self) -> ResultsIterator:
        read_batches = bq_data.get_arrow_batches(
            self._data,
            [x[0] for x in self._selected_fields],
            self._storage_client,
            self._project_id,
        )
        arrow_batches: Iterator[pa.RecordBatch] = map(
            functools.partial(
                pyarrow_utils.rename_batch, names=list(self.schema.names)
            ),
            read_batches.iter,
        )
        approx_bytes: Optional[int] = read_batches.approx_bytes
        approx_rows: Optional[int] = self._data.n_rows or read_batches.approx_rows

        if self._limit is not None:
            if approx_rows is not None:
                approx_rows = min(approx_rows, self._limit)
            arrow_batches = pyarrow_utils.truncate_pyarrow_iterable(
                arrow_batches, self._limit
            )

        if self._data.sql_predicate:
            approx_bytes = None
            approx_rows = None

        return ResultsIterator(arrow_batches, self.schema, approx_rows, approx_bytes)


@dataclasses.dataclass(frozen=True)
class HierarchicalKey:
    columns: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class CacheConfig(abc.ABC):
    optimize_for: Union[Literal["auto", "head"], HierarchicalKey] = "auto"
    if_cached: Literal["reuse-strict", "reuse-any", "replace"] = "reuse-any"


class Executor(abc.ABC):
    """
    Interface for an executor, which compiles and executes ArrayValue objects.
    """

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
        raise NotImplementedError("to_sql not implemented for this executor")

    @abc.abstractmethod
    def execute(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: ex_spec.ExecutionSpec,
    ) -> ExecuteResult:
        """
        Execute the ArrayValue.
        """
        ...

    def dry_run(
        self, array_value: bigframes.core.ArrayValue, ordered: bool = True
    ) -> bigquery.QueryJob:
        """
        Dry run executing the ArrayValue.

        Does not actually execute the data but will get stats and indicate any invalid query errors.
        """
        raise NotImplementedError("dry_run not implemented for this executor")

    def cached(
        self,
        array_value: bigframes.core.ArrayValue,
        *,
        config: CacheConfig,
    ) -> None:
        raise NotImplementedError("cached not implemented for this executor")
