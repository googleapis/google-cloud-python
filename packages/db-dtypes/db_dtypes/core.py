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

from typing import Optional

import numpy
import pandas
import pandas.api.extensions
from pandas.api.types import is_dtype_equal, is_list_like, is_scalar, pandas_dtype

from db_dtypes import pandas_backports

pandas_release = pandas_backports.pandas_release


class BaseDatetimeDtype(pandas.api.extensions.ExtensionDtype):
    na_value = pandas.NaT
    kind = "O"
    names = None

    @classmethod
    def construct_from_string(cls, name: str):
        if not isinstance(name, str):
            raise TypeError(
                f"'construct_from_string' expects a string, got {type(name)}"
            )

        if name != cls.name:
            raise TypeError(f"Cannot construct a '{cls.__name__}' from 'another_type'")

        return cls()


class BaseDatetimeArray(
    pandas_backports.OpsMixin, pandas_backports.NDArrayBackedExtensionArray
):
    # scalar used to denote NA value inside our self._ndarray, e.g. -1 for
    # Categorical, iNaT for Period. Outside of object dtype, self.isna() should
    # be exactly locations in self._ndarray with _internal_fill_value. See:
    # https://github.com/pandas-dev/pandas/blob/main/pandas/core/arrays/_mixins.py
    _internal_fill_value = numpy.datetime64("NaT")

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
            [cls._datetime(scalar) for scalar in scalars],
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
        """Compare array values, for use in OpsMixin."""

        if is_scalar(other) and (
            pandas.isna(other) or isinstance(other, self.dtype.type)
        ):
            other = type(self)([other])

        if type(other) is not type(self):
            return NotImplemented

        oshape = getattr(other, "shape", None)
        if oshape != self.shape and oshape != (1,) and self.shape != (1,):
            raise TypeError(
                "Can't compare arrays with different shapes", self.shape, oshape
            )
        return op(self._ndarray, other._ndarray)

    def _from_factorized(self, unique, original):
        return self.__class__(unique)

    def isna(self):
        return pandas.isna(self._ndarray)

    def _validate_scalar(self, value):
        """
        Validate and convert a scalar value to datetime64[ns] for storage in
        backing NumPy array.
        """
        return self._datetime(value)

    def _validate_searchsorted_value(self, value):
        """
        Convert a value for use in searching for a value in the backing numpy array.

        TODO: With pandas 2.0, this may be unnecessary. https://github.com/pandas-dev/pandas/pull/45544#issuecomment-1052809232
        """
        return self._validate_setitem_value(value)

    def _validate_setitem_value(self, value):
        """
        Convert a value for use in setting a value in the backing numpy array.
        """
        if is_list_like(value):
            _datetime = self._datetime
            return [_datetime(v) for v in value]

        return self._datetime(value)

    def any(
        self,
        *,
        axis: Optional[int] = None,
        out=None,
        keepdims: bool = False,
        skipna: bool = True,
    ):
        pandas_backports.numpy_validate_any((), {"out": out, "keepdims": keepdims})
        result = pandas_backports.nanany(self._ndarray, axis=axis, skipna=skipna)
        return result

    def all(
        self,
        *,
        axis: Optional[int] = None,
        out=None,
        keepdims: bool = False,
        skipna: bool = True,
    ):
        pandas_backports.numpy_validate_all((), {"out": out, "keepdims": keepdims})
        result = pandas_backports.nanall(self._ndarray, axis=axis, skipna=skipna)
        return result

    def min(self, *, axis: Optional[int] = None, skipna: bool = True, **kwargs):
        pandas_backports.numpy_validate_min((), kwargs)
        result = pandas_backports.nanmin(
            values=self._ndarray, axis=axis, mask=self.isna(), skipna=skipna
        )
        if axis is None or self.ndim == 1:
            return self._box_func(result)
        return self._from_backing_data(result)

    def max(self, *, axis: Optional[int] = None, skipna: bool = True, **kwargs):
        pandas_backports.numpy_validate_max((), kwargs)
        result = pandas_backports.nanmax(
            values=self._ndarray, axis=axis, mask=self.isna(), skipna=skipna
        )
        if axis is None or self.ndim == 1:
            return self._box_func(result)
        return self._from_backing_data(result)

    def median(
        self,
        *,
        axis: Optional[int] = None,
        out=None,
        overwrite_input: bool = False,
        keepdims: bool = False,
        skipna: bool = True,
    ):
        if not hasattr(pandas_backports, "numpy_validate_median"):
            raise NotImplementedError("Need pandas 1.3 or later to calculate median.")

        pandas_backports.numpy_validate_median(
            (),
            {"out": out, "overwrite_input": overwrite_input, "keepdims": keepdims},
        )
        result = pandas_backports.nanmedian(self._ndarray, axis=axis, skipna=skipna)
        if axis is None or self.ndim == 1:
            return self._box_func(result)
        return self._from_backing_data(result)
