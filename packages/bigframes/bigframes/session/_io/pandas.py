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

import dataclasses
import typing
from typing import Collection, Union

import bigframes_vendored.constants as constants
import geopandas  # type: ignore
import pandas
import pandas.arrays
import pyarrow  # type: ignore
import pyarrow.compute  # type: ignore
import pyarrow.types  # type: ignore

import bigframes.core.schema
import bigframes.dtypes
import bigframes.features


@dataclasses.dataclass(frozen=True)
class DataFrameAndLabels:
    df: pandas.DataFrame
    column_labels: Collection
    index_labels: Collection
    ordering_col: str
    col_type_overrides: typing.Dict[str, bigframes.dtypes.Dtype]


def _arrow_to_pandas_arrowdtype(
    column: pyarrow.Array, dtype: pandas.ArrowDtype
) -> pandas.Series:
    if (
        pyarrow.types.is_list(dtype.pyarrow_dtype)
        and not bigframes.features.PANDAS_VERSIONS.is_arrow_list_dtype_usable
    ):
        # This version of pandas doesn't really support ArrowDtype
        # well. See internal issue 321013333 where array type has
        # several problems converting a string.
        return pandas.Series(
            column.to_pylist(),  # type: ignore
            dtype="object",
        )

    # Avoid conversion logic if we are backing the pandas Series by the
    # arrow array.
    return pandas.Series(
        pandas.arrays.ArrowExtensionArray(column),  # type: ignore
        dtype=dtype,
    )


def arrow_to_pandas(
    arrow_table: Union[pyarrow.Table, pyarrow.RecordBatch],
    schema: bigframes.core.schema.ArraySchema,
):
    if len(schema) != arrow_table.num_columns:
        raise ValueError(
            f"Number of types {len(schema)} doesn't match number of columns "
            f"{arrow_table.num_columns}. {constants.FEEDBACK_LINK}"
        )

    serieses = {}
    for field, column in zip(arrow_table.schema, arrow_table):
        dtype = schema.get_type(field.name)

        if dtype == geopandas.array.GeometryDtype():
            series = geopandas.GeoSeries.from_wkt(
                # Use `to_pylist()` is a workaround for TypeError: object of type
                # 'pyarrow.lib.StringScalar' has no len() on older pyarrow,
                # geopandas, shapely combinations.
                column.to_pylist(),
                # BigQuery geography type is based on the WGS84 reference ellipsoid.
                crs="EPSG:4326",
            )
        elif dtype == pandas.Float64Dtype():
            # Preserve NA/NaN distinction. Note: This is currently needed, even if we use
            # nullable Float64Dtype in the types_mapper. See:
            # https://github.com/pandas-dev/pandas/issues/55668
            mask = pyarrow.compute.is_null(column)
            nonnull = pyarrow.compute.fill_null(column, float("nan"))
            # Regarding type: ignore, this class has been public at this
            # location since pandas 1.2.0. See:
            # https://pandas.pydata.org/docs/dev/reference/api/pandas.arrays.FloatingArray.html
            pd_array = pandas.arrays.FloatingArray(  # type: ignore
                nonnull.to_numpy()
                if isinstance(nonnull, pyarrow.ChunkedArray)
                else nonnull.to_numpy(zero_copy_only=False),
                mask.to_numpy()
                if isinstance(mask, pyarrow.ChunkedArray)
                else mask.to_numpy(zero_copy_only=False),
            )
            series = pandas.Series(pd_array, dtype=dtype)
        elif dtype == pandas.Int64Dtype():
            # Avoid out-of-bounds errors in Pandas 1.5.x, which incorrectly
            # casts to float64 in an intermediate step.
            mask = pyarrow.compute.is_null(column)
            nonnull = pyarrow.compute.fill_null(column, 0)
            pd_array = pandas.arrays.IntegerArray(
                nonnull.to_numpy()
                if isinstance(nonnull, pyarrow.ChunkedArray)
                else nonnull.to_numpy(zero_copy_only=False),
                mask.to_numpy()
                if isinstance(mask, pyarrow.ChunkedArray)
                else mask.to_numpy(zero_copy_only=False),
            )
            series = pandas.Series(pd_array, dtype=dtype)
        elif dtype == bigframes.dtypes.STRING_DTYPE:
            # Pyarrow may be large_string
            # Need to manually cast, as some pandas versions break otherwise
            series = column.cast(pyarrow.string()).to_pandas(
                types_mapper=lambda _: dtype
            )
        elif isinstance(dtype, pandas.ArrowDtype):
            series = _arrow_to_pandas_arrowdtype(column, dtype)
        else:
            series = column.to_pandas(types_mapper=lambda _: dtype)

        serieses[field.name] = series

    return pandas.DataFrame(serieses)
