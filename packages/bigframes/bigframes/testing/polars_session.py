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
from typing import Optional, Union
import weakref

import pandas
import polars

import bigframes
import bigframes.core.blocks
import bigframes.core.compile.polars
import bigframes.dataframe
import bigframes.session.executor
import bigframes.session.metrics


# Does not support to_sql, export_gbq, export_gcs, dry_run, peek, head, get_row_count, cached
@dataclasses.dataclass
class TestExecutor(bigframes.session.executor.Executor):
    compiler = bigframes.core.compile.polars.PolarsCompiler()

    def peek(
        self,
        array_value: bigframes.core.ArrayValue,
        n_rows: int,
        use_explicit_destination: Optional[bool] = False,
    ):
        """
        A 'peek' efficiently accesses a small number of rows in the dataframe.
        """
        lazy_frame: polars.LazyFrame = self.compiler.compile(array_value.node)
        pa_table = lazy_frame.collect().limit(n_rows).to_arrow()
        # Currently, pyarrow types might not quite be exactly the ones in the bigframes schema.
        # Nullability may be different, and might use large versions of list, string datatypes.
        return bigframes.session.executor.ExecuteResult(
            _arrow_batches=pa_table.to_batches(),
            schema=array_value.schema,
            total_bytes=pa_table.nbytes,
            total_rows=pa_table.num_rows,
        )

    def execute(
        self,
        array_value: bigframes.core.ArrayValue,
        *,
        ordered: bool = True,
        use_explicit_destination: Optional[bool] = False,
        page_size: Optional[int] = None,
        max_results: Optional[int] = None,
    ):
        """
        Execute the ArrayValue, storing the result to a temporary session-owned table.
        """
        lazy_frame: polars.LazyFrame = self.compiler.compile(array_value.node)
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
        # override read_pandas to always keep data local-only
        if isinstance(pandas_dataframe, pandas.Series):
            pandas_dataframe = pandas_dataframe.to_frame()
        local_block = bigframes.core.blocks.Block.from_local(pandas_dataframe, self)
        return bigframes.dataframe.DataFrame(local_block)

    @property
    def bqclient(self):
        # prevents logger from trying to call bq upon any errors
        return None
