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

import operator

import numpy
import packaging.version
import pandas
from pandas._libs.lib import is_integer


pandas_release = packaging.version.parse(pandas.__version__).release


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


@import_default("pandas.core.arraylike")
class OpsMixin:
    def _cmp_method(self, other, op):  # pragma: NO COVER
        return NotImplemented

    def __eq__(self, other):
        return self._cmp_method(other, operator.eq)

    def __ne__(self, other):
        return self._cmp_method(other, operator.ne)

    def __lt__(self, other):
        return self._cmp_method(other, operator.lt)

    def __le__(self, other):
        return self._cmp_method(other, operator.le)

    def __gt__(self, other):
        return self._cmp_method(other, operator.gt)

    def __ge__(self, other):
        return self._cmp_method(other, operator.ge)

    __add__ = __radd__ = __sub__ = lambda self, other: NotImplemented


@import_default("pandas.core.arrays._mixins", pandas_release < (1, 3))
class NDArrayBackedExtensionArray(pandas.core.arrays.base.ExtensionArray):

    ndim = 1

    def __init__(self, values, dtype):
        assert isinstance(values, numpy.ndarray)
        assert values.ndim == 1
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
        self._ndarray[index] = value

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

    @classmethod
    def _concat_same_type(cls, to_concat, axis=0):
        dtypes = {str(x.dtype) for x in to_concat}
        if len(dtypes) != 1:
            raise ValueError("to_concat must have the same dtype (tz)", dtypes)

        new_values = [x._ndarray for x in to_concat]
        new_values = numpy.concatenate(new_values, axis=axis)
        return to_concat[0]._from_backing_data(new_values)  # type: ignore[arg-type]
