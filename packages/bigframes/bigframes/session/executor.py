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
from typing import Callable, Iterator, Literal, Mapping, Optional, Sequence, Union

from google.cloud import bigquery
import pandas as pd
import pyarrow

import bigframes.core
import bigframes.core.schema
import bigframes.session._io.pandas as io_pandas


@dataclasses.dataclass(frozen=True)
class ExecuteResult:
    arrow_batches: Callable[[], Iterator[pyarrow.RecordBatch]]
    schema: bigframes.core.schema.ArraySchema
    query_job: Optional[bigquery.QueryJob] = None
    total_bytes: Optional[int] = None
    total_rows: Optional[int] = None

    def to_arrow_table(self) -> pyarrow.Table:
        # Need to provide schema if no result rows, as arrow can't infer
        # If ther are rows, it is safest to infer schema from batches.
        # Any discrepencies between predicted schema and actual schema will produce errors.
        batches = iter(self.arrow_batches())
        peek_it = itertools.islice(batches, 0, 1)
        peek_value = list(peek_it)
        # TODO: Enforce our internal schema on the table for consistency
        if len(peek_value) > 0:
            return pyarrow.Table.from_batches(
                itertools.chain(peek_value, batches),  # reconstruct
            )
        else:
            return self.schema.to_pyarrow().empty_table()

    def to_pandas(self) -> pd.DataFrame:
        return io_pandas.arrow_to_pandas(self.to_arrow_table(), self.schema)

    def to_pandas_batches(self) -> Iterator[pd.DataFrame]:
        yield from map(
            functools.partial(io_pandas.arrow_to_pandas, schema=self.schema),
            self.arrow_batches(),
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

    def execute(
        self,
        array_value: bigframes.core.ArrayValue,
        *,
        ordered: bool = True,
        use_explicit_destination: Optional[bool] = False,
        page_size: Optional[int] = None,
        max_results: Optional[int] = None,
    ) -> ExecuteResult:
        """
        Execute the ArrayValue, storing the result to a temporary session-owned table.
        """
        raise NotImplementedError("execute not implemented for this executor")

    def export_gbq(
        self,
        array_value: bigframes.core.ArrayValue,
        destination: bigquery.TableReference,
        if_exists: Literal["fail", "replace", "append"] = "fail",
        cluster_cols: Sequence[str] = [],
    ) -> bigquery.QueryJob:
        """
        Export the ArrayValue to an existing BigQuery table.
        """
        raise NotImplementedError("export_gbq not implemented for this executor")

    def export_gcs(
        self,
        array_value: bigframes.core.ArrayValue,
        uri: str,
        format: Literal["json", "csv", "parquet"],
        export_options: Mapping[str, Union[bool, str]],
    ) -> bigquery.QueryJob:
        """
        Export the ArrayValue to gcs.
        """
        raise NotImplementedError("export_gcs not implemented for this executor")

    def dry_run(
        self, array_value: bigframes.core.ArrayValue, ordered: bool = True
    ) -> bigquery.QueryJob:
        """
        Dry run executing the ArrayValue.

        Does not actually execute the data but will get stats and indicate any invalid query errors.
        """
        raise NotImplementedError("dry_run not implemented for this executor")

    def peek(
        self,
        array_value: bigframes.core.ArrayValue,
        n_rows: int,
        use_explicit_destination: Optional[bool] = False,
    ) -> ExecuteResult:
        """
        A 'peek' efficiently accesses a small number of rows in the dataframe.
        """
        raise NotImplementedError("peek not implemented for this executor")

    # TODO: Remove this and replace with efficient slice operator that can use execute()
    def head(
        self, array_value: bigframes.core.ArrayValue, n_rows: int
    ) -> ExecuteResult:
        """
        Preview the first n rows of the dataframe. This is less efficient than the unordered peek preview op.
        """
        raise NotImplementedError("head not implemented for this executor")

    def cached(
        self,
        array_value: bigframes.core.ArrayValue,
        *,
        force: bool = False,
        use_session: bool = False,
        cluster_cols: Sequence[str] = (),
    ) -> None:
        raise NotImplementedError("cached not implemented for this executor")
