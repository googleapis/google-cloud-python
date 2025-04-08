# Copyright 2024 Google LLC
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

"""Methods that deal with local pandas/pyarrow dataframes."""

from __future__ import annotations

import dataclasses
import functools
from typing import cast, Union
import uuid

import geopandas  # type: ignore
import numpy as np
import pandas
import pyarrow as pa

import bigframes.core.schema as schemata
import bigframes.dtypes


@dataclasses.dataclass(frozen=True)
class LocalTableMetadata:
    total_bytes: int
    row_count: int

    @classmethod
    def from_arrow(cls, table: pa.Table) -> LocalTableMetadata:
        return cls(total_bytes=table.nbytes, row_count=table.num_rows)


_MANAGED_STORAGE_TYPES_OVERRIDES: dict[bigframes.dtypes.Dtype, pa.DataType] = {
    # wkt to be precise
    bigframes.dtypes.GEO_DTYPE: pa.string()
}


@dataclasses.dataclass(frozen=True)
class ManagedArrowTable:
    data: pa.Table = dataclasses.field(hash=False)
    schema: schemata.ArraySchema = dataclasses.field(hash=False)
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()

    @functools.cached_property
    def metadata(self) -> LocalTableMetadata:
        return LocalTableMetadata.from_arrow(self.data)

    @classmethod
    def from_pandas(cls, dataframe: pandas.DataFrame) -> ManagedArrowTable:
        """Creates managed table from pandas. Ignores index, col names must be unique strings"""
        columns: list[pa.ChunkedArray] = []
        fields: list[schemata.SchemaItem] = []
        column_names = list(dataframe.columns)
        assert len(column_names) == len(set(column_names))

        for name, col in dataframe.items():
            new_arr, bf_type = _adapt_pandas_series(col)
            columns.append(new_arr)
            fields.append(schemata.SchemaItem(str(name), bf_type))

        return ManagedArrowTable(
            pa.table(columns, names=column_names), schemata.ArraySchema(tuple(fields))
        )

    @classmethod
    def from_pyarrow(self, table: pa.Table) -> ManagedArrowTable:
        columns: list[pa.ChunkedArray] = []
        fields: list[schemata.SchemaItem] = []
        for name, arr in zip(table.column_names, table.columns):
            new_arr, bf_type = _adapt_arrow_array(arr)
            columns.append(new_arr)
            fields.append(schemata.SchemaItem(name, bf_type))

        return ManagedArrowTable(
            pa.table(columns, names=table.column_names),
            schemata.ArraySchema(tuple(fields)),
        )

    def validate(self):
        # TODO: Content-based validation for some datatypes (eg json, wkt, list) where logical domain is smaller than pyarrow type
        for bf_field, arrow_field in zip(self.schema.items, self.data.schema):
            expected_arrow_type = _get_managed_storage_type(bf_field.dtype)
            arrow_type = arrow_field.type
            if expected_arrow_type != arrow_type:
                raise TypeError(
                    f"Field {bf_field} has arrow array type: {arrow_type}, expected type: {expected_arrow_type}"
                )


def _get_managed_storage_type(dtype: bigframes.dtypes.Dtype) -> pa.DataType:
    if dtype in _MANAGED_STORAGE_TYPES_OVERRIDES.keys():
        return _MANAGED_STORAGE_TYPES_OVERRIDES[dtype]
    else:
        return bigframes.dtypes.bigframes_dtype_to_arrow_dtype(dtype)


def _adapt_pandas_series(
    series: pandas.Series,
) -> tuple[Union[pa.ChunkedArray, pa.Array], bigframes.dtypes.Dtype]:
    # Mostly rely on pyarrow conversions, but have to convert geo without its help.
    if series.dtype == bigframes.dtypes.GEO_DTYPE:
        series = geopandas.GeoSeries(series).to_wkt(rounding_precision=-1)
        return pa.array(series, type=pa.string()), bigframes.dtypes.GEO_DTYPE
    try:
        return _adapt_arrow_array(pa.array(series))
    except Exception as e:
        if series.dtype == np.dtype("O"):
            try:
                series = series.astype(bigframes.dtypes.GEO_DTYPE)
            except TypeError:
                pass
        raise e


def _adapt_arrow_array(
    array: Union[pa.ChunkedArray, pa.Array]
) -> tuple[Union[pa.ChunkedArray, pa.Array], bigframes.dtypes.Dtype]:
    target_type = _arrow_type_replacements(array.type)
    if target_type != array.type:
        # TODO: Maybe warn if lossy conversion?
        array = array.cast(target_type)
    bf_type = bigframes.dtypes.arrow_dtype_to_bigframes_dtype(target_type)
    storage_type = _get_managed_storage_type(bf_type)
    if storage_type != array.type:
        raise TypeError(
            f"Expected {bf_type} to use arrow {storage_type}, instead got {array.type}"
        )
    return array, bf_type


def _arrow_type_replacements(type: pa.DataType) -> pa.DataType:
    if pa.types.is_timestamp(type):
        # This is potentially lossy, but BigFrames doesn't support ns
        new_tz = "UTC" if (type.tz is not None) else None
        return pa.timestamp(unit="us", tz=new_tz)
    if pa.types.is_time64(type):
        # This is potentially lossy, but BigFrames doesn't support ns
        return pa.time64("us")
    if pa.types.is_duration(type):
        # This is potentially lossy, but BigFrames doesn't support ns
        return pa.duration("us")
    if pa.types.is_decimal128(type):
        return pa.decimal128(38, 9)
    if pa.types.is_decimal256(type):
        return pa.decimal256(76, 38)
    if pa.types.is_large_string(type):
        # simple string type can handle the largest strings needed
        return pa.string()
    if pa.types.is_null(type):
        # null as a type not allowed, default type is float64 for bigframes
        return pa.float64()
    if pa.types.is_list(type):
        new_field_t = _arrow_type_replacements(type.value_type)
        if new_field_t != type.value_type:
            return pa.list_(new_field_t)
        return type
    if pa.types.is_struct(type):
        struct_type = cast(pa.StructType, type)
        new_fields: list[pa.Field] = []
        for i in range(struct_type.num_fields):
            field = struct_type.field(i)
            field.with_type(_arrow_type_replacements(field.type))
            new_fields.append(field.with_type(_arrow_type_replacements(field.type)))
        return pa.struct(new_fields)
    else:
        return type
