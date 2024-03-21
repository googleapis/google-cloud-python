# Copyright 2023 Google LLC
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

import datetime as dt
from typing import Optional

import bigframes_vendored.pandas.core.arrays.datetimelike as vendored_pandas_datetimelike
import bigframes_vendored.pandas.core.indexes.accessor as vendordt

from bigframes.core import log_adapter
import bigframes.operations as ops
import bigframes.operations.base
import bigframes.series as series


@log_adapter.class_logger
class DatetimeMethods(
    bigframes.operations.base.SeriesMethods,
    vendordt.DatetimeProperties,
    vendored_pandas_datetimelike.DatelikeOps,
):
    __doc__ = vendordt.DatetimeProperties.__doc__

    # Date accessors
    @property
    def day(self) -> series.Series:
        return self._apply_unary_op(ops.day_op)

    @property
    def dayofweek(self) -> series.Series:
        return self._apply_unary_op(ops.dayofweek_op)

    @property
    def date(self) -> series.Series:
        return self._apply_unary_op(ops.date_op)

    @property
    def quarter(self) -> series.Series:
        return self._apply_unary_op(ops.quarter_op)

    @property
    def year(self) -> series.Series:
        return self._apply_unary_op(ops.year_op)

    @property
    def month(self) -> series.Series:
        return self._apply_unary_op(ops.month_op)

    # Time accessors
    @property
    def hour(self) -> series.Series:
        return self._apply_unary_op(ops.hour_op)

    @property
    def minute(self) -> series.Series:
        return self._apply_unary_op(ops.minute_op)

    @property
    def second(self) -> series.Series:
        return self._apply_unary_op(ops.second_op)

    @property
    def time(self) -> series.Series:
        return self._apply_unary_op(ops.time_op)

    @property
    def tz(self) -> Optional[dt.timezone]:
        # Assumption: pyarrow dtype
        tz_string = self._dtype.pyarrow_dtype.tz
        if tz_string == "UTC":
            return dt.timezone.utc
        elif tz_string is None:
            return None
        else:
            raise ValueError(f"Unexpected timezone {tz_string}")

    @property
    def unit(self) -> str:
        # Assumption: pyarrow dtype
        return self._dtype.pyarrow_dtype.unit

    def strftime(self, date_format: str) -> series.Series:
        return self._apply_unary_op(ops.StrftimeOp(date_format=date_format))

    def normalize(self) -> series.Series:
        return self._apply_unary_op(ops.normalize_op)

    def floor(self, freq: str) -> series.Series:
        return self._apply_unary_op(ops.FloorDtOp(freq=freq))
