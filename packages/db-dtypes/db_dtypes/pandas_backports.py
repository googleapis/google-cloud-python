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

"""
Utilities to support older pandas versions.

These backported versions are simpler and, in some cases, less featureful than
the versions in the later versions of pandas.
"""

from typing import Any

import numpy
import packaging.version
import pandas
from pandas.api.types import is_integer
import pandas.compat.numpy.function
import pandas.core.nanops

pandas_release = packaging.version.parse(pandas.__version__).release

# Create aliases for private methods in case they move in a future version.
nanall = pandas.core.nanops.nanall
nanany = pandas.core.nanops.nanany
nanmax = pandas.core.nanops.nanmax
nanmin = pandas.core.nanops.nanmin
numpy_validate_all = pandas.compat.numpy.function.validate_all
numpy_validate_any = pandas.compat.numpy.function.validate_any
numpy_validate_max = pandas.compat.numpy.function.validate_max
numpy_validate_min = pandas.compat.numpy.function.validate_min

if pandas_release >= (1, 3):
    nanmedian = pandas.core.nanops.nanmedian
    numpy_validate_median = pandas.compat.numpy.function.validate_median


def import_default(module_name, force=False, default=None):
    """
    Provide an implementation for a class or function when it can't be imported

    or when force is True.

    This is used to replicate Pandas APIs that are missing or insufficient
    (thus the force option) in early pandas versions.
    """

    if default is None:
        return lambda func_or_class: import_default(module_name, force, func_or_class)

    if force:
        return default

    name = default.__name__
    try:
        module = __import__(module_name, {}, {}, [name])
    except ModuleNotFoundError:
        return default

    return getattr(module, name, default)


# pandas.core.arraylike.OpsMixin is private, but the related public API
# "ExtensionScalarOpsMixin" is not sufficient for adding dates to times.
# It results in unsupported operand type(s) for +: 'datetime.time' and
# 'datetime.date'
@import_default("pandas.core.arraylike")
class OpsMixin:
    def _cmp_method(self, other, op):  # pragma: NO COVER
        return NotImplemented


# TODO: use public API once pandas 1.5 / 2.x is released.
# See: https://github.com/pandas-dev/pandas/pull/45544
@import_default("pandas.core.arrays._mixins", pandas_release < (1, 3))
class NDArrayBackedExtensionArray(pandas.core.arrays.base.ExtensionArray):
    def __init__(self, values, dtype):
        assert isinstance(values, numpy.ndarray)
        self._ndarray = values
        self._dtype = dtype

    @classmethod
    def _from_backing_data(cls, data):
        return cls(data, data.dtype)

    def __getitem__(self, index):
        value = self._ndarray[index]
        if is_integer(index):
            return self._box_func(value)
        return self.__class__(value, self._dtype)

    def __setitem__(self, index, value):
        self._ndarray[index] = self._validate_setitem_value(value)

    def __len__(self):
        return len(self._ndarray)

    @property
    def shape(self):
        return self._ndarray.shape

    @property
    def ndim(self) -> int:
        return self._ndarray.ndim

    @property
    def size(self) -> int:
        return self._ndarray.size

    @property
    def nbytes(self) -> int:
        return self._ndarray.nbytes

    def copy(self):
        return self[:]

    def repeat(self, n):
        return self.__class__(self._ndarray.repeat(n), self._dtype)

    def take(
        self,
        indices,
        *,
        allow_fill: bool = False,
        fill_value: Any = None,
        axis: int = 0,
    ):
        from pandas.core.algorithms import take

        if allow_fill:
            fill_value = self._validate_scalar(fill_value)

        new_data = take(
            self._ndarray,
            indices,
            allow_fill=allow_fill,
            fill_value=fill_value,
            axis=axis,
        )
        return self._from_backing_data(new_data)

    @classmethod
    def _concat_same_type(cls, to_concat, axis=0):
        dtypes = {str(x.dtype) for x in to_concat}
        if len(dtypes) != 1:
            raise ValueError("to_concat must have the same dtype (tz)", dtypes)

        new_values = [x._ndarray for x in to_concat]
        new_values = numpy.concatenate(new_values, axis=axis)
        return to_concat[0]._from_backing_data(new_values)  # type: ignore[arg-type]
