# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Pandas Data Types for SQL systems (BigQuery, Spanner)
"""

import datetime
import re
from typing import Union

import numpy
import packaging.version
import pandas
import pandas.compat.numpy.function
import pandas.core.algorithms
import pandas.core.arrays
import pandas.core.dtypes.base
import pandas.core.dtypes.dtypes
import pandas.core.dtypes.generic
import pandas.core.nanops
import pyarrow
import pyarrow.compute

from db_dtypes.version import __version__
from db_dtypes import core


date_dtype_name = "dbdate"
time_dtype_name = "dbtime"
_EPOCH = datetime.datetime(1970, 1, 1)
_NPEPOCH = numpy.datetime64(_EPOCH)

pandas_release = packaging.version.parse(pandas.__version__).release


@pandas.core.dtypes.dtypes.register_extension_dtype
class TimeDtype(core.BaseDatetimeDtype):
    """
    Extension dtype for time data.
    """

    name = time_dtype_name
    type = datetime.time

    def construct_array_type(self):
        return TimeArray

    @staticmethod
    def __from_arrow__(
        array: Union[pyarrow.Array, pyarrow.ChunkedArray]
    ) -> "TimeArray":
        """Convert to dbtime data from an Arrow array.

        See:
        https://pandas.pydata.org/pandas-docs/stable/development/extending.html#compatibility-with-apache-arrow
        """
        # We can't call combine_chunks on an empty array, so short-circuit the
        # rest of the function logic for this special case.
        if len(array) == 0:
            return TimeArray(numpy.array([], dtype="datetime64[ns]"))

        # We can't cast to timestamp("ns"), but time64("ns") has the same
        # memory layout: 64-bit integers representing the number of nanoseconds
        # since the datetime epoch (midnight 1970-01-01).
        array = pyarrow.compute.cast(array, pyarrow.time64("ns"))

        # ChunkedArray has no "view" method, so combine into an Array.
        if isinstance(array, pyarrow.ChunkedArray):
            array = array.combine_chunks()

        array = array.view(pyarrow.timestamp("ns"))
        np_array = array.to_numpy(zero_copy_only=False)
        return TimeArray(np_array)


class TimeArray(core.BaseDatetimeArray):
    """
    Pandas array type containing time data
    """

    # Data are stored as datetime64 values with a date of Jan 1, 1970

    dtype = TimeDtype()

    @classmethod
    def _datetime(
        cls,
        scalar,
        match_fn=re.compile(
            r"\s*(?P<hours>\d+)"
            r"(?::(?P<minutes>\d+)"
            r"(?::(?P<seconds>\d+)"
            r"(?:\.(?P<fraction>\d*))?)?)?\s*$"
        ).match,
    ):
        # Convert pyarrow values to datetime.time.
        if isinstance(scalar, (pyarrow.Time32Scalar, pyarrow.Time64Scalar)):
            scalar = (
                scalar.cast(pyarrow.time64("ns"))
                .cast(pyarrow.int64())
                .cast(pyarrow.timestamp("ns"))
                .as_py()
            )

        if scalar is None:
            return None
        elif isinstance(scalar, datetime.time):
            return datetime.datetime.combine(_EPOCH, scalar)
        elif isinstance(scalar, pandas.Timestamp):
            return scalar.to_datetime64()
        elif isinstance(scalar, str):
            # iso string
            parsed = match_fn(scalar)
            if not parsed:
                raise ValueError(f"Bad time string: {repr(scalar)}")

            hours = parsed.group("hours")
            minutes = parsed.group("minutes")
            seconds = parsed.group("seconds")
            fraction = parsed.group("fraction")
            microseconds = int(fraction.ljust(6, "0")[:6]) if fraction else 0
            return datetime.datetime(
                1970,
                1,
                1,
                int(hours),
                int(minutes) if minutes else 0,
                int(seconds) if seconds else 0,
                microseconds,
            )
        else:
            raise TypeError("Invalid value type", scalar)

    def _box_func(self, x):
        if pandas.isnull(x):
            return None

        try:
            return x.astype("<M8[us]").astype(datetime.datetime).time()
        except AttributeError:
            x = numpy.datetime64(x)
            return x.astype("<M8[us]").astype(datetime.datetime).time()

    __return_deltas = {"timedelta", "timedelta64", "timedelta64[ns]", "<m8", "<m8[ns]"}

    def astype(self, dtype, copy=True):
        deltas = self._ndarray - _NPEPOCH
        stype = str(dtype)
        if stype in self.__return_deltas:
            return deltas
        elif stype.startswith("timedelta64[") or stype.startswith("<m8["):
            return deltas.astype(dtype, copy=False)
        else:
            return super().astype(dtype, copy=copy)

    def __arrow_array__(self, type=None):
        """Convert to an Arrow array from dbtime data.

        See:
        https://pandas.pydata.org/pandas-docs/stable/development/extending.html#compatibility-with-apache-arrow
        """
        array = pyarrow.array(self._ndarray, type=pyarrow.timestamp("ns"))

        # ChunkedArray has no "view" method, so combine into an Array.
        array = (
            array.combine_chunks() if isinstance(array, pyarrow.ChunkedArray) else array
        )

        # We can't cast to time64("ns"), but timestamp("ns") has the same
        # memory layout: 64-bit integers representing the number of nanoseconds
        # since the datetime epoch (midnight 1970-01-01).
        array = array.view(pyarrow.time64("ns"))
        return pyarrow.compute.cast(
            array, type if type is not None else pyarrow.time64("ns"),
        )


@pandas.core.dtypes.dtypes.register_extension_dtype
class DateDtype(core.BaseDatetimeDtype):
    """
    Extension dtype for time data.
    """

    name = date_dtype_name
    type = datetime.date

    def construct_array_type(self):
        return DateArray

    @staticmethod
    def __from_arrow__(
        array: Union[pyarrow.Array, pyarrow.ChunkedArray]
    ) -> "DateArray":
        """Convert to dbdate data from an Arrow array.

        See:
        https://pandas.pydata.org/pandas-docs/stable/development/extending.html#compatibility-with-apache-arrow
        """
        array = pyarrow.compute.cast(array, pyarrow.timestamp("ns"))
        np_array = array.to_numpy()
        return DateArray(np_array)


class DateArray(core.BaseDatetimeArray):
    """
    Pandas array type containing date data
    """

    # Data are stored as datetime64 values with a date of Jan 1, 1970

    dtype = DateDtype()

    @staticmethod
    def _datetime(
        scalar,
        match_fn=re.compile(r"\s*(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)\s*$").match,
    ):
        # Convert pyarrow values to datetime.date.
        if isinstance(scalar, (pyarrow.Date32Scalar, pyarrow.Date64Scalar)):
            scalar = scalar.as_py()

        if scalar is None:
            return None
        elif isinstance(scalar, datetime.date):
            return datetime.datetime(scalar.year, scalar.month, scalar.day)
        elif isinstance(scalar, str):
            match = match_fn(scalar)
            if not match:
                raise ValueError(f"Bad date string: {repr(scalar)}")
            year = int(match.group("year"))
            month = int(match.group("month"))
            day = int(match.group("day"))
            return datetime.datetime(year, month, day)
        else:
            raise TypeError("Invalid value type", scalar)

    def _box_func(self, x):
        if pandas.isnull(x):
            return None
        try:
            return x.astype("<M8[us]").astype(datetime.datetime).date()
        except AttributeError:
            x = numpy.datetime64(x)
            return x.astype("<M8[us]").astype(datetime.datetime).date()

    def astype(self, dtype, copy=True):
        stype = str(dtype)
        if stype.startswith("datetime"):
            if stype == "datetime" or stype == "datetime64":
                dtype = self._ndarray.dtype
            return self._ndarray.astype(dtype, copy=copy)
        elif stype.startswith("<M8"):
            if stype == "<M8":
                dtype = self._ndarray.dtype
            return self._ndarray.astype(dtype, copy=copy)

        return super().astype(dtype, copy=copy)

    def __arrow_array__(self, type=None):
        """Convert to an Arrow array from dbdate data.

        See:
        https://pandas.pydata.org/pandas-docs/stable/development/extending.html#compatibility-with-apache-arrow
        """
        array = pyarrow.array(self._ndarray, type=pyarrow.timestamp("ns"))
        return pyarrow.compute.cast(
            array, type if type is not None else pyarrow.date32(),
        )

    def __add__(self, other):
        if isinstance(other, pandas.DateOffset):
            return self.astype("object") + other

        if isinstance(other, TimeArray):
            return (other._ndarray - _NPEPOCH) + self._ndarray

        return super().__add__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, pandas.DateOffset):
            return self.astype("object") - other

        if isinstance(other, self.__class__):
            return self._ndarray - other._ndarray

        return super().__sub__(other)


__all__ = [
    "__version__",
    "DateArray",
    "DateDtype",
    "TimeArray",
    "TimeDtype",
]
