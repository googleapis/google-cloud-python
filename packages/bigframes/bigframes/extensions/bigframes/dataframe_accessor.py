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

from typing import TypeVar, cast

import bigframes.dataframe
import bigframes.extensions.core.dataframe_accessor as core_accessor
import bigframes.series
from bigframes.core.logging import log_adapter

T = TypeVar("T", bound="bigframes.dataframe.DataFrame")
S = TypeVar("S", bound="bigframes.series.Series")


@log_adapter.class_logger
class BigframesAIAccessor(core_accessor.AIAccessor[T, S]):
    """
    BigFrames DataFrame accessor for BigQuery AI functions.
    """

    def __init__(self, bf_obj: T):
        super().__init__(bf_obj)

    def _bf_from_dataframe(
        self, session: bigframes.session.Session | None
    ) -> bigframes.dataframe.DataFrame:
        return self._obj

    def _to_dataframe(self, bf_df: bigframes.dataframe.DataFrame) -> T:
        return cast(T, bf_df)

    def _to_series(self, bf_series: bigframes.series.Series) -> S:
        return cast(S, bf_series)


@log_adapter.class_logger
class BigframesBigQueryDataFrameAccessor(core_accessor.BigQueryDataFrameAccessor[T, S]):
    """
    BigFrames DataFrame accessor for BigQuery DataFrames functionality.
    """

    def __init__(self, bf_obj: T):
        super().__init__(bf_obj)

    @property
    def ai(self) -> BigframesAIAccessor:
        return BigframesAIAccessor(self._obj)

    def _bf_from_dataframe(
        self, session: bigframes.session.Session | None
    ) -> bigframes.dataframe.DataFrame:
        return self._obj

    def _to_dataframe(self, bf_df: bigframes.dataframe.DataFrame) -> T:
        return cast(T, bf_df)

    def _to_series(self, bf_series: bigframes.series.Series) -> S:
        return cast(S, bf_series)
