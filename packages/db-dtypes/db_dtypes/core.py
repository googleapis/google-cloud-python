# Copyright 2021 Google LLC
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

from typing import Any, Optional, Sequence

import numpy
import pandas
from pandas._libs import NaT
import pandas.compat.numpy.function
import pandas.core.algorithms
import pandas.core.arrays
import pandas.core.dtypes.base
from pandas.core.dtypes.common import is_dtype_equal, is_list_like, pandas_dtype
import pandas.core.dtypes.dtypes
import pandas.core.dtypes.generic
import pandas.core.nanops

from db_dtypes import pandas_backports


pandas_release = pandas_backports.pandas_release


class BaseDatetimeDtype(pandas.core.dtypes.base.ExtensionDtype):
    na_value = NaT
    kind = "o"
    names = None

    @classmethod
    def construct_from_string(cls, name):
        if name != cls.name:
            raise TypeError()

        return cls()


class BaseDatetimeArray(
    pandas_backports.OpsMixin, pandas_backports.NDArrayBackedExtensionArray
):
    def __init__(self, values, dtype=None, copy: bool = False):
        if not (
            isinstance(values, numpy.ndarray) and values.dtype == numpy.dtype("<M8[ns]")
        ):
            values = self.__ndarray(values)
        elif copy:
            values = values.copy()

        super().__init__(values=values, dtype=values.dtype)

    @classmethod
    def __ndarray(cls, scalars):
        return numpy.array(
            [None if scalar is None else cls._datetime(scalar) for scalar in scalars],
            "M8[ns]",
        )

    @classmethod
    def _from_sequence(cls, scalars, *, dtype=None, copy=False):
        if dtype is not None:
            assert dtype.__class__ is cls.dtype.__class__
        return cls(cls.__ndarray(scalars))

    _from_sequence_of_strings = _from_sequence

    def astype(self, dtype, copy=True):
        dtype = pandas_dtype(dtype)
        if is_dtype_equal(dtype, self.dtype):
            if not copy:
                return self
            else:
                return self.copy()

        return super().astype(dtype, copy=copy)

    def _cmp_method(self, other, op):
        oshape = getattr(other, "shape", None)
        if oshape != self.shape and oshape != (1,) and self.shape != (1,):
            raise TypeError(
                "Can't compare arrays with different shapes", self.shape, oshape
            )

        if type(other) != type(self):
            return NotImplemented
        return op(self._ndarray, other._ndarray)

    def __setitem__(self, key, value):
        if is_list_like(value):
            _datetime = self._datetime
            value = [_datetime(v) for v in value]
        elif not pandas.isna(value):
            value = self._datetime(value)
        return super().__setitem__(key, value)

    def _from_factorized(self, unique, original):
        return self.__class__(unique)

    def isna(self):
        return pandas.isna(self._ndarray)

    def _validate_scalar(self, value):
        if pandas.isna(value):
            return None

        if not isinstance(value, self.dtype.type):
            raise ValueError(value)

        return value

    def take(
        self,
        indices: Sequence[int],
        *,
        allow_fill: bool = False,
        fill_value: Any = None,
    ):
        indices = numpy.asarray(indices, dtype=numpy.intp)
        data = self._ndarray
        if allow_fill:
            fill_value = self._validate_scalar(fill_value)
            fill_value = (
                numpy.datetime64()
                if fill_value is None
                else numpy.datetime64(self._datetime(fill_value))
            )
            if (indices < -1).any():
                raise ValueError(
                    "take called with negative indexes other than -1,"
                    " when a fill value is provided."
                )
        out = data.take(indices)
        if allow_fill:
            out[indices == -1] = fill_value

        return self.__class__(out)

    # TODO: provide implementations of dropna, fillna, unique,
    # factorize, argsort, searchsoeted for better performance over
    # abstract implementations.

    def any(
        self,
        *,
        axis: Optional[int] = None,
        out=None,
        keepdims: bool = False,
        skipna: bool = True,
    ):
        pandas.compat.numpy.function.validate_any(
            (), {"out": out, "keepdims": keepdims}
        )
        result = pandas.core.nanops.nanany(self._ndarray, axis=axis, skipna=skipna)
        return result

    def all(
        self,
        *,
        axis: Optional[int] = None,
        out=None,
        keepdims: bool = False,
        skipna: bool = True,
    ):
        pandas.compat.numpy.function.validate_all(
            (), {"out": out, "keepdims": keepdims}
        )
        result = pandas.core.nanops.nanall(self._ndarray, axis=axis, skipna=skipna)
        return result

    def min(self, *, axis: Optional[int] = None, skipna: bool = True, **kwargs):
        pandas.compat.numpy.function.validate_min((), kwargs)
        result = pandas.core.nanops.nanmin(
            values=self._ndarray, axis=axis, mask=self.isna(), skipna=skipna
        )
        return self._box_func(result)

    def max(self, *, axis: Optional[int] = None, skipna: bool = True, **kwargs):
        pandas.compat.numpy.function.validate_max((), kwargs)
        result = pandas.core.nanops.nanmax(
            values=self._ndarray, axis=axis, mask=self.isna(), skipna=skipna
        )
        return self._box_func(result)

    if pandas_release >= (1, 2):

        def median(
            self,
            *,
            axis: Optional[int] = None,
            out=None,
            overwrite_input: bool = False,
            keepdims: bool = False,
            skipna: bool = True,
        ):
            pandas.compat.numpy.function.validate_median(
                (),
                {"out": out, "overwrite_input": overwrite_input, "keepdims": keepdims},
            )
            result = pandas.core.nanops.nanmedian(
                self._ndarray, axis=axis, skipna=skipna
            )
            return self._box_func(result)
