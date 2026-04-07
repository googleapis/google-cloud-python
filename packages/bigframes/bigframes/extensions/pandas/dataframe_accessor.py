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

from typing import TypeVar, cast

import pandas
import pandas.api.extensions

import bigframes.core.global_session as bf_session
import bigframes.dataframe
import bigframes.pandas as bpd
from bigframes.core.logging import log_adapter
from bigframes.extensions.core.dataframe_accessor import (
    AIAccessor,
    BigQueryDataFrameAccessor,
)

T = TypeVar("T", bound="pandas.DataFrame")
S = TypeVar("S", bound="pandas.Series")


@log_adapter.class_logger
class PandasAIAccessor(AIAccessor[T, S]):
    """
    Pandas DataFrame accessor for BigQuery AI functions.
    """

    def __init__(self, pandas_obj: T):
        super().__init__(pandas_obj)

    def _bf_from_dataframe(
        self, session: bigframes.session.Session | None
    ) -> bigframes.dataframe.DataFrame:
        if session is None:
            session = bf_session.get_global_session()

        return cast(bpd.DataFrame, session.read_pandas(self._obj))

    def _to_dataframe(self, bf_df: bigframes.dataframe.DataFrame) -> T:
        return cast(T, bf_df.to_pandas(ordered=True))

    def _to_series(self, bf_series: bigframes.series.Series) -> S:
        return cast(S, bf_series.to_pandas(ordered=True))


@pandas.api.extensions.register_dataframe_accessor("bigquery")
@log_adapter.class_logger
class PandasBigQueryDataFrameAccessor(BigQueryDataFrameAccessor[T, S]):
    """
    Pandas DataFrame accessor for BigQuery DataFrames functionality.

    This accessor is registered under the ``bigquery`` namespace on pandas DataFrame objects.
    """

    def __init__(self, pandas_obj: T):
        super().__init__(pandas_obj)

    @property
    def ai(self) -> PandasAIAccessor:
        return PandasAIAccessor(self._obj)

    def _bf_from_dataframe(self, session) -> bigframes.dataframe.DataFrame:
        if session is None:
            session = bf_session.get_global_session()

        return cast(bpd.DataFrame, session.read_pandas(self._obj))

    def _to_dataframe(self, bf_df: bigframes.dataframe.DataFrame) -> T:
        return cast(T, bf_df.to_pandas(ordered=True))

    def _to_series(self, bf_series: bigframes.series.Series) -> S:
        return cast(S, bf_series.to_pandas(ordered=True))
