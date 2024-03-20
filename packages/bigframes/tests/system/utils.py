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

import base64
import decimal
import functools
from typing import Iterable, Optional, Set

import geopandas as gpd  # type: ignore
import google.api_core.operation
from google.cloud import bigquery, functions_v2
from google.cloud.functions_v2.types import functions
import numpy as np
import pandas as pd
import pyarrow as pa  # type: ignore
import pytest

from bigframes.functions import remote_function


def skip_legacy_pandas(test):
    @functools.wraps(test)
    def wrapper(*args, **kwds):
        if pd.__version__.startswith("1."):
            pytest.skip("Skips pandas 1.x as not compatible with 2.x behavior.")
        return test(*args, **kwds)

    return wrapper


def assert_pandas_df_equal(df0, df1, ignore_order: bool = False, **kwargs):
    if ignore_order:
        # Sort by a column to get consistent results.
        if df0.index.name != "rowindex":
            df0 = df0.sort_values(
                list(df0.columns.drop("geography_col", errors="ignore"))
            ).reset_index(drop=True)
            df1 = df1.sort_values(
                list(df1.columns.drop("geography_col", errors="ignore"))
            ).reset_index(drop=True)
        else:
            df0 = df0.sort_index()
            df1 = df1.sort_index()

    pd.testing.assert_frame_equal(df0, df1, **kwargs)


def assert_series_equal(
    left: pd.Series, right: pd.Series, ignore_order: bool = False, **kwargs
):
    if ignore_order:
        if left.index.name is None:
            left = left.sort_values().reset_index(drop=True)
            right = right.sort_values().reset_index(drop=True)
        else:
            left = left.sort_index()
            right = right.sort_index()

    pd.testing.assert_series_equal(left, right, **kwargs)


def _standardize_index(idx):
    return pd.Index(list(idx), name=idx.name)


def assert_pandas_index_equal_ignore_index_type(idx0, idx1):
    idx0 = _standardize_index(idx0)
    idx1 = _standardize_index(idx1)

    pd.testing.assert_index_equal(idx0, idx1)


def convert_pandas_dtypes(df: pd.DataFrame, bytes_col: bool):
    """Convert pandas dataframe dtypes compatible with bigframes dataframe."""

    # TODO(chelsealin): updates the function to accept dtypes as input rather than
    # hard-code the column names here.

    # Convert basic types columns
    df["bool_col"] = df["bool_col"].astype(pd.BooleanDtype())
    df["int64_col"] = df["int64_col"].astype(pd.Int64Dtype())
    df["int64_too"] = df["int64_too"].astype(pd.Int64Dtype())
    df["float64_col"] = df["float64_col"].astype(pd.Float64Dtype())
    df["string_col"] = df["string_col"].astype(pd.StringDtype(storage="pyarrow"))

    if "rowindex" in df.columns:
        df["rowindex"] = df["rowindex"].astype(pd.Int64Dtype())
    if "rowindex_2" in df.columns:
        df["rowindex_2"] = df["rowindex_2"].astype(pd.Int64Dtype())

    # Convert time types columns. The `astype` works for Pandas 2.0 but hits an assert
    # error at Pandas 1.5. Hence, we have to convert to arrow table and convert back
    # to pandas dataframe.
    if not isinstance(df["date_col"].dtype, pd.ArrowDtype):
        df["date_col"] = pd.to_datetime(df["date_col"], format="%Y-%m-%d")
        arrow_table = pa.Table.from_pandas(
            pd.DataFrame(df, columns=["date_col"]),
            schema=pa.schema([("date_col", pa.date32())]),
        )
        df["date_col"] = arrow_table.to_pandas(types_mapper=pd.ArrowDtype)["date_col"]

    if not isinstance(df["datetime_col"].dtype, pd.ArrowDtype):
        df["datetime_col"] = pd.to_datetime(
            df["datetime_col"], format="%Y-%m-%d %H:%M:%S"
        )
        arrow_table = pa.Table.from_pandas(
            pd.DataFrame(df, columns=["datetime_col"]),
            schema=pa.schema([("datetime_col", pa.timestamp("us"))]),
        )
        df["datetime_col"] = arrow_table.to_pandas(types_mapper=pd.ArrowDtype)[
            "datetime_col"
        ]

    if not isinstance(df["time_col"].dtype, pd.ArrowDtype):
        df["time_col"] = pd.to_datetime(df["time_col"], format="%H:%M:%S.%f")
        arrow_table = pa.Table.from_pandas(
            pd.DataFrame(df, columns=["time_col"]),
            schema=pa.schema([("time_col", pa.time64("us"))]),
        )
        df["time_col"] = arrow_table.to_pandas(types_mapper=pd.ArrowDtype)["time_col"]

    if not isinstance(df["timestamp_col"].dtype, pd.ArrowDtype):
        df["timestamp_col"] = pd.to_datetime(
            df["timestamp_col"], format="%Y-%m-%d %H:%M:%S.%f%Z"
        )
        arrow_table = pa.Table.from_pandas(
            pd.DataFrame(df, columns=["timestamp_col"]),
            schema=pa.schema([("timestamp_col", pa.timestamp("us", tz="UTC"))]),
        )
        df["timestamp_col"] = arrow_table.to_pandas(types_mapper=pd.ArrowDtype)[
            "timestamp_col"
        ]

    # Convert geography types columns.
    if "geography_col" in df.columns:
        df["geography_col"] = df["geography_col"].astype(
            pd.StringDtype(storage="pyarrow")
        )
        df["geography_col"] = gpd.GeoSeries.from_wkt(
            df["geography_col"].replace({np.nan: None})
        )

    if bytes_col and not isinstance(df["bytes_col"].dtype, pd.ArrowDtype):
        df["bytes_col"] = df["bytes_col"].apply(
            lambda value: base64.b64decode(value) if not pd.isnull(value) else value
        )
        arrow_table = pa.Table.from_pandas(
            pd.DataFrame(df, columns=["bytes_col"]),
            schema=pa.schema([("bytes_col", pa.binary())]),
        )
        df["bytes_col"] = arrow_table.to_pandas(types_mapper=pd.ArrowDtype)["bytes_col"]

    if not isinstance(df["numeric_col"].dtype, pd.ArrowDtype):
        # Convert numeric types column.
        df["numeric_col"] = df["numeric_col"].apply(
            lambda value: decimal.Decimal(str(value)) if value else None  # type: ignore
        )
        arrow_table = pa.Table.from_pandas(
            pd.DataFrame(df, columns=["numeric_col"]),
            schema=pa.schema([("numeric_col", pa.decimal128(38, 9))]),
        )
        df["numeric_col"] = arrow_table.to_pandas(types_mapper=pd.ArrowDtype)[
            "numeric_col"
        ]


def assert_pandas_df_equal_pca_components(actual, expected, **kwargs):
    """Compare two pandas dataframes representing PCA components. The columns
    required to be present in the dataframes are:
        numerical_value: numeric,
        categorical_value: List[object(category, value)]

    The index types of `actual` and `expected` are ignored in the comparison.

    Args:
        actual: Actual Pandas DataFrame

        expected: Expected Pandas DataFrame

        kwargs: kwargs to use in `pandas.testing.assert_series_equal` per column
    """
    # Compare the index, columns and values separately, as the polarity of the
    # PCA vectors can be arbitrary
    pd.testing.assert_index_equal(
        actual.index, expected.index.astype(actual.index.dtype)
    )  # dtype agnostic index comparison
    pd.testing.assert_index_equal(actual.columns, expected.columns)
    for column in expected.columns:
        try:
            pd.testing.assert_series_equal(actual[column], expected[column], **kwargs)
        except AssertionError:
            if column not in {"numerical_value", "categorical_value"}:
                raise

            # Allow for sign difference per numeric/categorical column
            if column == "numerical_value":
                actual_ = -actual[column]
                expected_ = expected[column]
            else:
                # In this column each element is an array of objects, where the
                # object has attributes "category" and "value". For the sake of
                # comparison let's normalize by flipping the polarity of "value".
                def normalize_array_of_objects(arr, reverse_polarity=False):
                    newarr = []
                    for element in arr:
                        newelement = dict(element)
                        if reverse_polarity:
                            newelement["value"] = -newelement["value"]
                        newarr.append(newelement)
                    return sorted(newarr, key=lambda d: d["category"])

                actual_ = actual[column].apply(normalize_array_of_objects, args=(True,))
                expected_ = expected[column].apply(normalize_array_of_objects)

            pd.testing.assert_series_equal(actual_, expected_, **kwargs)


def assert_pandas_df_equal_pca(actual, expected, **kwargs):
    """Compare two pandas dataframes representing PCA predictions. The columns
    in the dataframes are expected to be numeric.

    Args:
        actual: Actual Pandas DataFrame

        expected: Expected Pandas DataFrame

        kwargs: kwargs to use in `pandas.testing.assert_series_equal` per column
    """
    # Compare the index, columns and values separately, as the polarity of the
    # PCA vector can be arbitrary
    pd.testing.assert_index_equal(actual.index, expected.index)
    pd.testing.assert_index_equal(actual.columns, expected.columns)
    for column in expected.columns:
        try:
            pd.testing.assert_series_equal(actual[column], expected[column], **kwargs)
        except AssertionError:
            # Allow for sign difference per column
            pd.testing.assert_series_equal(-actual[column], expected[column], **kwargs)


def get_remote_function_endpoints(
    bigquery_client: bigquery.Client, dataset_id: str
) -> Set[str]:
    """Get endpoints used by the remote functions in a datset"""
    endpoints = set()
    routines = bigquery_client.list_routines(dataset=dataset_id)
    for routine in routines:
        rf_options = routine._properties.get("remoteFunctionOptions")
        if not rf_options:
            continue
        rf_endpoint = rf_options.get("endpoint")
        if rf_endpoint:
            endpoints.add(rf_endpoint)
    return endpoints


def get_cloud_functions(
    functions_client: functions_v2.FunctionServiceClient,
    project: str,
    location: str,
    name: Optional[str] = None,
    name_prefix: Optional[str] = None,
) -> Iterable[functions.ListFunctionsResponse]:
    """Get the cloud functions in the given project and location."""

    assert (
        not name or not name_prefix
    ), "Either 'name' or 'name_prefix' can be passed but not both."

    _, location = remote_function.get_remote_function_locations(location)
    parent = f"projects/{project}/locations/{location}"
    request = functions_v2.ListFunctionsRequest(parent=parent)
    page_result = functions_client.list_functions(request=request)
    for response in page_result:
        # If name is provided and it does not match then skip
        if bool(name):
            full_name = parent + f"/functions/{name}"
            if response.name != full_name:
                continue
        # If name prefix is provided and it does not match then skip
        elif bool(name_prefix):
            full_name_prefix = parent + f"/functions/{name_prefix}"
            if not response.name.startswith(full_name_prefix):
                continue

        yield response


def delete_cloud_function(
    functions_client: functions_v2.FunctionServiceClient, full_name: str
) -> google.api_core.operation.Operation:
    """Delete a cloud function with the given fully qualified name."""
    request = functions_v2.DeleteFunctionRequest(name=full_name)
    operation = functions_client.delete_function(request=request)
    return operation


def get_first_file_from_wildcard(path):
    return path.replace("*", "000000000000")
