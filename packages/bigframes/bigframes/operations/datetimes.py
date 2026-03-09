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
from typing import Generic, Literal, Optional, TypeVar

import bigframes_vendored.pandas.core.arrays.datetimelike as vendored_pandas_datetimelike
import bigframes_vendored.pandas.core.indexes.accessor as vendordt
import pandas

from bigframes import dataframe, dtypes, series
from bigframes._tools import docs
import bigframes.core.col
import bigframes.core.indexes.base as indices
from bigframes.core.logging import log_adapter
import bigframes.operations as ops

_ONE_DAY = pandas.Timedelta("1D")
_ONE_SECOND = pandas.Timedelta("1s")
_ONE_MICRO = pandas.Timedelta("1us")
_SUPPORTED_FREQS = ("Y", "Q", "M", "W", "D", "h", "min", "s", "ms", "us")


T = TypeVar("T", series.Series, indices.Index, bigframes.core.col.Expression)


# Simpler base class for datetime properties, excludes isocalendar, unit, tz
class DatetimeSimpleMethods(Generic[T]):
    def __init__(self, data: T):
        self._data: T = data

    # Date accessors
    @property
    def day(self) -> T:
        return self._data._apply_unary_op(ops.day_op)

    @property
    def dayofweek(self) -> T:
        return self._data._apply_unary_op(ops.dayofweek_op)

    @property
    def day_of_week(self) -> T:
        return self.dayofweek

    @property
    def weekday(self) -> T:
        return self.dayofweek

    @property
    def dayofyear(self) -> T:
        return self._data._apply_unary_op(ops.dayofyear_op)

    @property
    def day_of_year(self) -> T:
        return self.dayofyear

    @property
    def date(self) -> T:
        return self._data._apply_unary_op(ops.date_op)

    @property
    def quarter(self) -> T:
        return self._data._apply_unary_op(ops.quarter_op)

    @property
    def year(self) -> T:
        return self._data._apply_unary_op(ops.year_op)

    @property
    def month(self) -> T:
        return self._data._apply_unary_op(ops.month_op)

    # Time accessors
    @property
    def hour(self) -> T:
        return self._data._apply_unary_op(ops.hour_op)

    @property
    def minute(self) -> T:
        return self._data._apply_unary_op(ops.minute_op)

    @property
    def second(self) -> T:
        return self._data._apply_unary_op(ops.second_op)

    @property
    def time(self) -> T:
        return self._data._apply_unary_op(ops.time_op)

    # Timedelta accessors
    @property
    def days(self) -> T:
        self._check_dtype(dtypes.TIMEDELTA_DTYPE)

        return self._data._apply_binary_op(_ONE_DAY, ops.floordiv_op)

    @property
    def seconds(self) -> T:
        self._check_dtype(dtypes.TIMEDELTA_DTYPE)

        return self._data._apply_binary_op(_ONE_DAY, ops.mod_op) // _ONE_SECOND  # type: ignore

    @property
    def microseconds(self) -> T:
        self._check_dtype(dtypes.TIMEDELTA_DTYPE)

        return self._data._apply_binary_op(_ONE_SECOND, ops.mod_op) // _ONE_MICRO  # type: ignore

    def total_seconds(self) -> T:
        self._check_dtype(dtypes.TIMEDELTA_DTYPE)

        return self._data._apply_binary_op(_ONE_SECOND, ops.div_op)

    def _check_dtype(self, target_dtype: dtypes.Dtype):
        if isinstance(self._data, (indices.Index, series.Series)):
            if self._data.dtype != target_dtype:
                raise TypeError(
                    f"Expect dtype: {target_dtype}, but got {self._data.dtype}"
                )
        return

    def tz_localize(self, tz: Literal["UTC"] | None) -> T:
        if tz == "UTC":
            return self._data._apply_unary_op(ops.ToTimestampOp())

        if tz is None:
            return self._data._apply_unary_op(ops.ToDatetimeOp())

        raise ValueError(f"Unsupported timezone {tz}")

    def day_name(self) -> T:
        return self.strftime("%A")

    def strftime(self, date_format: str) -> T:
        return self._data._apply_unary_op(ops.StrftimeOp(date_format=date_format))

    def normalize(self) -> T:
        return self._data._apply_unary_op(ops.normalize_op)

    def floor(self, freq: str) -> T:
        if freq not in _SUPPORTED_FREQS:
            raise ValueError(f"freq must be one of {_SUPPORTED_FREQS}")
        return self._data._apply_unary_op(ops.FloorDtOp(freq=freq))  # type: ignore


# this is the version used by series.dt, and the one that shows up in reference docs
@log_adapter.class_logger
@docs.inherit_docs(vendordt.DatetimeProperties)
@docs.inherit_docs(vendored_pandas_datetimelike.DatelikeOps)
class DatetimeMethods(DatetimeSimpleMethods[bigframes.series.Series]):
    def __init__(self, data: series.Series):
        super().__init__(data)

    @property
    def tz(self) -> Optional[dt.timezone]:
        # Assumption: pyarrow dtype
        tz_string = self._data._dtype.pyarrow_dtype.tz
        if tz_string == "UTC":
            return dt.timezone.utc
        elif tz_string is None:
            return None
        else:
            raise ValueError(f"Unexpected timezone {tz_string}")

    @property
    def unit(self) -> str:
        # Assumption: pyarrow dtype
        return self._data._dtype.pyarrow_dtype.unit

    def isocalendar(self) -> dataframe.DataFrame:
        iso_ops = [ops.iso_year_op, ops.iso_week_op, ops.iso_day_op]
        labels = pandas.Index(["year", "week", "day"])
        block = self._data._block.project_exprs(
            [op.as_expr(self._data._value_column) for op in iso_ops], labels, drop=True
        )
        return dataframe.DataFrame(block)
