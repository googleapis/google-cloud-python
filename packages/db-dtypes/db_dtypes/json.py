# Copyright 2024 Google LLC
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

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pandas.arrays as arrays
import pandas.core.dtypes.common as common
import pandas.core.indexers as indexers
import pyarrow as pa
import pyarrow.compute


@pd.api.extensions.register_extension_dtype
class JSONDtype(pd.api.extensions.ExtensionDtype):
    """Extension dtype for BigQuery JSON data."""

    name = "dbjson"

    @property
    def na_value(self) -> pd.NA:
        """Default NA value to use for this type."""
        return pd.NA

    @property
    def type(self) -> type[str]:
        """
        Return the scalar type for the array elements.
        The standard JSON data types can be one of `dict`, `list`, `str`, `int`, `float`,
        `bool` and `None`. However, this method returns a `str` type to indicate its
        storage type, because the union of multiple types are not supported well in pandas.
        """
        return str

    @property
    def pyarrow_dtype(self):
        """Return the pyarrow data type used for storing data in the pyarrow array."""
        return pa.string()

    @property
    def _is_numeric(self) -> bool:
        return False

    @property
    def _is_boolean(self) -> bool:
        return False

    @classmethod
    def construct_array_type(cls):
        """Return the array type associated with this dtype."""
        return JSONArray


class JSONArray(arrays.ArrowExtensionArray):
    """Extension array that handles BigQuery JSON data, leveraging a string-based
    pyarrow array for storage. It enables seamless conversion to JSON objects when
    accessing individual elements."""

    _dtype = JSONDtype()

    def __init__(self, values, dtype=None, copy=False) -> None:
        self._dtype = JSONDtype()
        if isinstance(values, pa.Array):
            self._pa_array = pa.chunked_array([values])
        elif isinstance(values, pa.ChunkedArray):
            self._pa_array = values
        else:
            raise ValueError(f"Unsupported type '{type(values)}' for JSONArray")

    @classmethod
    def _box_pa(
        cls, value, pa_type: pa.DataType | None = None
    ) -> pa.Array | pa.ChunkedArray | pa.Scalar:
        """Box value into a pyarrow Array, ChunkedArray or Scalar."""
        assert pa_type is None or pa_type == cls._dtype.pyarrow_dtype

        if isinstance(value, pa.Scalar) or not (
            common.is_list_like(value) and not common.is_dict_like(value)
        ):
            return cls._box_pa_scalar(value)
        return cls._box_pa_array(value)

    @classmethod
    def _box_pa_scalar(cls, value) -> pa.Scalar:
        """Box value into a pyarrow Scalar."""
        if pd.isna(value):
            pa_scalar = pa.scalar(None, type=cls._dtype.pyarrow_dtype)
        else:
            value = JSONArray._serialize_json(value)
            pa_scalar = pa.scalar(
                value, type=cls._dtype.pyarrow_dtype, from_pandas=True
            )

        return pa_scalar

    @classmethod
    def _box_pa_array(cls, value, copy: bool = False) -> pa.Array | pa.ChunkedArray:
        """Box value into a pyarrow Array or ChunkedArray."""
        if isinstance(value, cls):
            pa_array = value._pa_array
        else:
            value = [JSONArray._serialize_json(x) for x in value]
            pa_array = pa.array(value, type=cls._dtype.pyarrow_dtype, from_pandas=True)
        return pa_array

    @classmethod
    def _from_sequence(cls, scalars, *, dtype=None, copy=False):
        """Construct a new ExtensionArray from a sequence of scalars."""
        pa_array = cls._box_pa(scalars)
        arr = cls(pa_array)
        return arr

    @staticmethod
    def _serialize_json(value):
        """A static method that converts a JSON value into a string representation."""
        if not common.is_list_like(value) and pd.isna(value):
            return value
        else:
            # `sort_keys=True` sorts dictionary keys before serialization, making
            # JSON comparisons deterministic.
            return json.dumps(value, sort_keys=True)

    @staticmethod
    def _deserialize_json(value):
        """A static method that converts a JSON string back into its original value."""
        if not pd.isna(value):
            return json.loads(value)
        else:
            return value

    @property
    def dtype(self) -> JSONDtype:
        """An instance of JSONDtype"""
        return self._dtype

    def _cmp_method(self, other, op):
        if op.__name__ == "eq":
            result = pyarrow.compute.equal(self._pa_array, self._box_pa(other))
        elif op.__name__ == "ne":
            result = pyarrow.compute.not_equal(self._pa_array, self._box_pa(other))
        else:
            # Comparison is not a meaningful one. We don't want to support sorting by JSON columns.
            raise TypeError(f"{op.__name__} not supported for JSONArray")
        return arrays.ArrowExtensionArray(result)

    def __getitem__(self, item):
        """Select a subset of self."""
        item = indexers.check_array_indexer(self, item)

        if isinstance(item, np.ndarray):
            if not len(item):
                return type(self)(pa.chunked_array([], type=self.dtype.pyarrow_dtype))
            elif item.dtype.kind in "iu":
                return self.take(item)
            else:
                # `check_array_indexer` should verify that the assertion hold true.
                assert item.dtype.kind == "b"
                return type(self)(self._pa_array.filter(item))
        elif isinstance(item, tuple):
            item = indexers.unpack_tuple_and_ellipses(item)

        if common.is_scalar(item) and not common.is_integer(item):
            # e.g. "foo" or 2.5
            # exception message copied from numpy
            raise IndexError(
                r"only integers, slices (`:`), ellipsis (`...`), numpy.newaxis "
                r"(`None`) and integer or boolean arrays are valid indices"
            )

        value = self._pa_array[item]
        if isinstance(value, pa.ChunkedArray):
            return type(self)(value)
        else:
            scalar = JSONArray._deserialize_json(value.as_py())
            if scalar is None:
                return self._dtype.na_value
            else:
                return scalar

    def __iter__(self):
        """Iterate over elements of the array."""
        for value in self._pa_array:
            val = JSONArray._deserialize_json(value.as_py())
            if val is None:
                yield self._dtype.na_value
            else:
                yield val

    def _reduce(
        self, name: str, *, skipna: bool = True, keepdims: bool = False, **kwargs
    ):
        """Return a scalar result of performing the reduction operation."""
        if name in ["min", "max"]:
            raise TypeError("JSONArray does not support min/max reducntion.")
        super()._reduce(name, skipna=skipna, keepdims=keepdims, **kwargs)
