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

import dataclasses
from typing import Union
import weakref

import pandas
import polars

import bigframes
import bigframes.core.blocks
import bigframes.core.compile.polars
import bigframes.dataframe
import bigframes.session.execution_spec
import bigframes.session.executor
import bigframes.session.metrics


# Does not support to_sql, dry_run, peek, cached
@dataclasses.dataclass
class TestExecutor(bigframes.session.executor.Executor):
    compiler = bigframes.core.compile.polars.PolarsCompiler()

    def execute(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: bigframes.session.execution_spec.ExecutionSpec,
    ):
        """
        Execute the ArrayValue, storing the result to a temporary session-owned table.
        """
        if execution_spec.destination_spec is not None:
            raise ValueError(
                f"TestExecutor does not support destination spec: {execution_spec.destination_spec}"
            )
        lazy_frame: polars.LazyFrame = self.compiler.compile(array_value.node)
        if execution_spec.peek is not None:
            lazy_frame = lazy_frame.limit(execution_spec.peek)
        pa_table = lazy_frame.collect().to_arrow()
        # Currently, pyarrow types might not quite be exactly the ones in the bigframes schema.
        # Nullability may be different, and might use large versions of list, string datatypes.
        return bigframes.session.executor.ExecuteResult(
            _arrow_batches=pa_table.to_batches(),
            schema=array_value.schema,
            total_bytes=pa_table.nbytes,
            total_rows=pa_table.num_rows,
        )

    def cached(
        self,
        array_value: bigframes.core.ArrayValue,
        *,
        config,
    ) -> None:
        return


class TestSession(bigframes.session.Session):
    def __init__(self):
        self._location = None  # type: ignore
        self._bq_kms_key_name = None  # type: ignore
        self._clients_provider = None  # type: ignore
        self._bq_connection = None  # type: ignore
        self._skip_bq_connection_check = True
        self._session_id: str = "test_session"
        self._objects: list[
            weakref.ReferenceType[
                Union[
                    bigframes.core.indexes.Index,
                    bigframes.series.Series,
                    bigframes.dataframe.DataFrame,
                ]
            ]
        ] = []
        self._strictly_ordered: bool = True
        self._allow_ambiguity = False  # type: ignore
        self._default_index_type = bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64
        self._metrics = bigframes.session.metrics.ExecutionMetrics()
        self._function_session = None  # type: ignore
        self._temp_storage_manager = None  # type: ignore
        self._executor = TestExecutor()
        self._loader = None  # type: ignore

    def read_pandas(self, pandas_dataframe, write_engine="default"):
        original_input = pandas_dataframe

        # override read_pandas to always keep data local-only
        if isinstance(pandas_dataframe, (pandas.Series, pandas.Index)):
            pandas_dataframe = pandas_dataframe.to_frame()

        local_block = bigframes.core.blocks.Block.from_local(pandas_dataframe, self)
        bf_df = bigframes.dataframe.DataFrame(local_block)

        if isinstance(original_input, pandas.Series):
            series = bf_df[bf_df.columns[0]]
            series.name = original_input.name
            return series

        if isinstance(original_input, pandas.Index):
            return bf_df.index

        return bf_df

    @property
    def bqclient(self):
        # prevents logger from trying to call bq upon any errors
        return None
