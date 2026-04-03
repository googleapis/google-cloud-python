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

import dataclasses
import weakref
from typing import TYPE_CHECKING, Union

import pandas

import bigframes
import bigframes.core.blocks
import bigframes.dataframe
import bigframes.session.execution_spec
import bigframes.session.executor
import bigframes.session.metrics

if TYPE_CHECKING:
    import bigframes.core


@dataclasses.dataclass
class SubstraitTestExecutor(bigframes.session.executor.Executor):
    def __init__(self):
        from bigframes.session.substrait_executor import DataFusionSubstraitConsumer, SubstraitExecutor
        self.executor = SubstraitExecutor(DataFusionSubstraitConsumer())

    def execute(
        self,
        array_value: bigframes.core.ArrayValue,
        execution_spec: bigframes.session.execution_spec.ExecutionSpec,
    ):
        if execution_spec.destination_spec is not None:
            raise ValueError(
                f"SubstraitTestExecutor does not support destination spec: {execution_spec.destination_spec}"
            )
        
        result = self.executor.execute(array_value.node, ordered=True, peek=execution_spec.peek)
        if result is None:
            raise NotImplementedError("SubstraitExecutor cannot execute this plan")
            
        return result

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
        self._session_id: str = "substrait_test_session"
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
        self._executor = SubstraitTestExecutor()
        self._loader = None  # type: ignore

    def read_pandas(self, pandas_dataframe, write_engine="default"):
        original_input = pandas_dataframe

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
        return None
