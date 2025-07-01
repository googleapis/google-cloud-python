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
import io
import itertools
import json
from typing import Any, Callable, cast, Generator, Iterable, Literal, Optional, Union
import uuid

import geopandas  # type: ignore
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet  # type: ignore

from bigframes.core import pyarrow_utils
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
    bigframes.dtypes.GEO_DTYPE: pa.string(),
    # Just json as string
    bigframes.dtypes.JSON_DTYPE: pa.string(),
}


@dataclasses.dataclass(frozen=True)
class ManagedArrowTable:
    data: pa.Table = dataclasses.field(hash=False, compare=False)
    schema: schemata.ArraySchema = dataclasses.field(hash=False, compare=False)
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)

    @functools.cached_property
    def metadata(self) -> LocalTableMetadata:
        return LocalTableMetadata.from_arrow(self.data)

    @classmethod
    def from_pandas(cls, dataframe: pd.DataFrame) -> ManagedArrowTable:
        """Creates managed table from pandas. Ignores index, col names must be unique strings"""
        columns: list[pa.ChunkedArray] = []
        fields: list[schemata.SchemaItem] = []
        column_names = list(dataframe.columns)
        assert len(column_names) == len(set(column_names))

        for name, col in dataframe.items():
            new_arr, bf_type = _adapt_pandas_series(col)
            columns.append(new_arr)
            fields.append(schemata.SchemaItem(str(name), bf_type))

        mat = ManagedArrowTable(
            pa.table(columns, names=column_names), schemata.ArraySchema(tuple(fields))
        )
        mat.validate()
        return mat

    @classmethod
    def from_pyarrow(self, table: pa.Table) -> ManagedArrowTable:
        columns: list[pa.ChunkedArray] = []
        fields: list[schemata.SchemaItem] = []
        for name, arr in zip(table.column_names, table.columns):
            new_arr, bf_type = _adapt_chunked_array(arr)
            columns.append(new_arr)
            fields.append(schemata.SchemaItem(name, bf_type))

        mat = ManagedArrowTable(
            pa.table(columns, names=table.column_names),
            schemata.ArraySchema(tuple(fields)),
        )
        mat.validate()
        return mat

    def to_arrow(
        self,
        *,
        offsets_col: Optional[str] = None,
        geo_format: Literal["wkb", "wkt"] = "wkt",
        duration_type: Literal["int", "duration"] = "duration",
        json_type: Literal["string"] = "string",
    ) -> tuple[pa.Schema, Iterable[pa.RecordBatch]]:
        if geo_format != "wkt":
            raise NotImplementedError(f"geo format {geo_format} not yet implemented")
        assert json_type == "string"

        batches = self.data.to_batches()
        schema = self.data.schema
        if duration_type == "int":
            schema = _schema_durations_to_ints(schema)
            batches = map(
                functools.partial(pyarrow_utils.cast_batch, schema=schema), batches
            )

        if offsets_col is not None:
            return schema.append(pa.field(offsets_col, pa.int64())), _append_offsets(
                batches, offsets_col
            )
        else:
            return schema, batches

    def to_pyarrow_table(
        self,
        *,
        offsets_col: Optional[str] = None,
        geo_format: Literal["wkb", "wkt"] = "wkt",
        duration_type: Literal["int", "duration"] = "duration",
        json_type: Literal["string"] = "string",
    ) -> pa.Table:
        schema, batches = self.to_arrow(
            offsets_col=offsets_col,
            geo_format=geo_format,
            duration_type=duration_type,
            json_type=json_type,
        )
        return pa.Table.from_batches(batches, schema)

    def to_parquet(
        self,
        dst: Union[str, io.IOBase],
        *,
        offsets_col: Optional[str] = None,
        geo_format: Literal["wkb", "wkt"] = "wkt",
        duration_type: Literal["int", "duration"] = "duration",
        json_type: Literal["string"] = "string",
    ):
        pa_table = self.to_pyarrow_table(
            offsets_col=offsets_col,
            geo_format=geo_format,
            duration_type=duration_type,
            json_type=json_type,
        )
        pyarrow.parquet.write_table(pa_table, where=dst)

    def itertuples(
        self,
        *,
        geo_format: Literal["wkb", "wkt"] = "wkt",
        duration_type: Literal["int", "timedelta"] = "timedelta",
        json_type: Literal["string", "object"] = "string",
    ) -> Iterable[tuple]:
        """
        Yield each row as an unlabeled tuple.

        Row-wise iteration of columnar data is slow, avoid if possible.
        """
        for row_dict in _iter_table(
            self.data,
            self.schema,
            geo_format=geo_format,
            duration_type=duration_type,
            json_type=json_type,
        ):
            yield tuple(row_dict.values())

    def validate(self):
        for bf_field, arrow_field in zip(self.schema.items, self.data.schema):
            expected_arrow_type = _get_managed_storage_type(bf_field.dtype)
            arrow_type = arrow_field.type
            if expected_arrow_type != arrow_type:
                raise TypeError(
                    f"Field {bf_field} has arrow array type: {arrow_type}, expected type: {expected_arrow_type}"
                )


# Sequential iterator, but could split into batches and leverage parallelism for speed
def _iter_table(
    table: pa.Table,
    schema: schemata.ArraySchema,
    *,
    geo_format: Literal["wkb", "wkt"] = "wkt",
    duration_type: Literal["int", "timedelta"] = "timedelta",
    json_type: Literal["string", "object"] = "string",
) -> Generator[dict[str, Any], None, None]:
    """For when you feel like iterating row-wise over a column store. Don't expect speed."""

    if geo_format != "wkt":
        raise NotImplementedError(f"geo format {geo_format} not yet implemented")

    @functools.singledispatch
    def iter_array(
        array: pa.Array, dtype: bigframes.dtypes.Dtype
    ) -> Generator[Any, None, None]:
        values = array.to_pylist()
        if dtype == bigframes.dtypes.JSON_DTYPE:
            if json_type == "object":
                yield from map(lambda x: json.loads(x) if x is not None else x, values)
            else:
                yield from values
        elif dtype == bigframes.dtypes.TIMEDELTA_DTYPE:
            if duration_type == "int":
                yield from map(
                    lambda x: ((x.days * 3600 * 24) + x.seconds) * 1_000_000
                    + x.microseconds
                    if x is not None
                    else x,
                    values,
                )
            else:
                yield from values
        else:
            yield from values

    @iter_array.register
    def _(
        array: pa.ListArray, dtype: bigframes.dtypes.Dtype
    ) -> Generator[Any, None, None]:
        value_generator = iter_array(
            array.flatten(), bigframes.dtypes.get_array_inner_type(dtype)
        )
        for (start, end) in _pairwise(array.offsets):
            arr_size = end.as_py() - start.as_py()
            yield list(itertools.islice(value_generator, arr_size))

    @iter_array.register
    def _(
        array: pa.StructArray, dtype: bigframes.dtypes.Dtype
    ) -> Generator[Any, None, None]:
        # yield from each subarray
        sub_generators: dict[str, Generator[Any, None, None]] = {}
        for field_name, dtype in bigframes.dtypes.get_struct_fields(dtype).items():
            sub_generators[field_name] = iter_array(array.field(field_name), dtype)

        keys = list(sub_generators.keys())
        for row_values in zip(*sub_generators.values()):
            yield {key: value for key, value in zip(keys, row_values)}

    for batch in table.to_batches():
        sub_generators: dict[str, Generator[Any, None, None]] = {}
        for field in schema.items:
            sub_generators[field.column] = iter_array(
                batch.column(field.column), field.dtype
            )

        keys = list(sub_generators.keys())
        for row_values in zip(*sub_generators.values()):
            yield {key: value for key, value in zip(keys, row_values)}


def _adapt_pandas_series(
    series: pd.Series,
) -> tuple[Union[pa.ChunkedArray, pa.Array], bigframes.dtypes.Dtype]:
    # Mostly rely on pyarrow conversions, but have to convert geo without its help.
    if series.dtype == bigframes.dtypes.GEO_DTYPE:
        # geoseries produces eg "POINT (1, 1)", while bq uses style "POINT(1, 1)"
        # we normalize to bq style for consistency
        series = (
            geopandas.GeoSeries(series)
            .to_wkt(rounding_precision=-1)
            .str.replace(r"(\w+) \(", repl=r"\1(", regex=True)
        )
        return pa.array(series, type=pa.string()), bigframes.dtypes.GEO_DTYPE
    try:
        return _adapt_arrow_array(pa.array(series))
    except pa.ArrowInvalid as e:
        if series.dtype == np.dtype("O"):
            try:
                return _adapt_pandas_series(series.astype(bigframes.dtypes.GEO_DTYPE))
            except TypeError:
                # Prefer original error
                pass
        raise e


def _adapt_chunked_array(
    chunked_array: pa.ChunkedArray,
) -> tuple[pa.ChunkedArray, bigframes.dtypes.Dtype]:
    if len(chunked_array.chunks) == 0:
        return _adapt_arrow_array(chunked_array.combine_chunks())
    dtype = None
    arrays = []
    for chunk in chunked_array.chunks:
        array, arr_dtype = _adapt_arrow_array(chunk)
        arrays.append(array)
        dtype = dtype or arr_dtype
    assert dtype is not None
    return pa.chunked_array(arrays), dtype


def _adapt_arrow_array(array: pa.Array) -> tuple[pa.Array, bigframes.dtypes.Dtype]:
    """Normalize the array to managed storage types. Preserve shapes, only transforms values."""
    if array.offset != 0:  # Offset arrays don't have all operations implemented
        return _adapt_arrow_array(pa.concat_arrays([array]))

    if pa.types.is_struct(array.type):
        assert isinstance(array, pa.StructArray)
        assert isinstance(array.type, pa.StructType)
        arrays = []
        dtypes = []
        pa_fields = []
        for i in range(array.type.num_fields):
            field_array, field_type = _adapt_arrow_array(array.field(i))
            arrays.append(field_array)
            dtypes.append(field_type)
            pa_fields.append(pa.field(array.type.field(i).name, field_array.type))
        struct_array = pa.StructArray.from_arrays(
            arrays=arrays, fields=pa_fields, mask=array.is_null()
        )
        dtype = bigframes.dtypes.struct_type(
            [(field.name, dtype) for field, dtype in zip(pa_fields, dtypes)]
        )
        return struct_array, dtype
    if pa.types.is_list(array.type):
        assert isinstance(array, pa.ListArray)
        values, values_type = _adapt_arrow_array(array.values)
        new_value = pa.ListArray.from_arrays(
            array.offsets, values, mask=array.is_null()
        )
        return new_value.fill_null([]), bigframes.dtypes.list_type(values_type)
    if array.type == bigframes.dtypes.JSON_ARROW_TYPE:
        return _canonicalize_json(array), bigframes.dtypes.JSON_DTYPE
    target_type = logical_type_replacements(array.type)
    if target_type != array.type:
        # TODO: Maybe warn if lossy conversion?
        array = array.cast(target_type)
    bf_type = bigframes.dtypes.arrow_dtype_to_bigframes_dtype(
        target_type, allow_lossless_cast=True
    )

    storage_type = _get_managed_storage_type(bf_type)
    if storage_type != array.type:
        array = array.cast(storage_type)
    return array, bf_type


def _canonicalize_json(array: pa.Array) -> pa.Array:
    def _canonicalize_scalar(json_string):
        if json_string is None:
            return None
        # This is the canonical form that bq uses when emitting json
        # The sorted keys and unambiguous whitespace ensures a 1:1 mapping
        # between syntax and semantics.
        return json.dumps(
            json.loads(json_string), sort_keys=True, separators=(",", ":")
        )

    return pa.array(
        [_canonicalize_scalar(value) for value in array.to_pylist()], type=pa.string()
    )


def _get_managed_storage_type(dtype: bigframes.dtypes.Dtype) -> pa.DataType:
    if dtype in _MANAGED_STORAGE_TYPES_OVERRIDES.keys():
        return _MANAGED_STORAGE_TYPES_OVERRIDES[dtype]
    return _physical_type_replacements(
        bigframes.dtypes.bigframes_dtype_to_arrow_dtype(dtype)
    )


def _recursive_map_types(
    f: Callable[[pa.DataType], pa.DataType]
) -> Callable[[pa.DataType], pa.DataType]:
    @functools.wraps(f)
    def recursive_f(type: pa.DataType) -> pa.DataType:
        if pa.types.is_list(type):
            new_field_t = recursive_f(type.value_type)
            if new_field_t != type.value_type:
                return pa.list_(new_field_t)
            return type
        # polars can produce large lists, and we want to map these down to regular lists
        if pa.types.is_large_list(type):
            new_field_t = recursive_f(type.value_type)
            return pa.list_(new_field_t)
        if pa.types.is_struct(type):
            struct_type = cast(pa.StructType, type)
            new_fields: list[pa.Field] = []
            for i in range(struct_type.num_fields):
                field = struct_type.field(i)
                new_fields.append(field.with_type(recursive_f(field.type)))
            return pa.struct(new_fields)
        return f(type)

    return recursive_f


@_recursive_map_types
def logical_type_replacements(type: pa.DataType) -> pa.DataType:
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
    if pa.types.is_large_binary(type):
        # simple string type can handle the largest strings needed
        return pa.binary()
    if pa.types.is_dictionary(type):
        return logical_type_replacements(type.value_type)
    if pa.types.is_null(type):
        # null as a type not allowed, default type is float64 for bigframes
        return pa.float64()
    else:
        return type


_ARROW_MANAGED_STORAGE_OVERRIDES = {
    bigframes.dtypes._BIGFRAMES_TO_ARROW[bf_dtype]: arrow_type
    for bf_dtype, arrow_type in _MANAGED_STORAGE_TYPES_OVERRIDES.items()
    if bf_dtype in bigframes.dtypes._BIGFRAMES_TO_ARROW
}


@_recursive_map_types
def _physical_type_replacements(dtype: pa.DataType) -> pa.DataType:
    if dtype in _ARROW_MANAGED_STORAGE_OVERRIDES:
        return _ARROW_MANAGED_STORAGE_OVERRIDES[dtype]
    return dtype


def _append_offsets(
    batches: Iterable[pa.RecordBatch], offsets_col_name: str
) -> Iterable[pa.RecordBatch]:
    offset = 0
    for batch in batches:
        offsets = pa.array(range(offset, offset + batch.num_rows), type=pa.int64())
        batch_w_offsets = pa.record_batch(
            [*batch.columns, offsets],
            schema=batch.schema.append(pa.field(offsets_col_name, pa.int64())),
        )
        offset += batch.num_rows
        yield batch_w_offsets


@_recursive_map_types
def _durations_to_ints(type: pa.DataType) -> pa.DataType:
    if pa.types.is_duration(type):
        return pa.int64()
    return type


def _schema_durations_to_ints(schema: pa.Schema) -> pa.Schema:
    return pa.schema(
        pa.field(field.name, _durations_to_ints(field.type)) for field in schema
    )


def _pairwise(iterable):
    do_yield = False
    a = None
    b = None
    for item in iterable:
        a = b
        b = item
        if do_yield:
            yield (a, b)
        else:
            do_yield = True
