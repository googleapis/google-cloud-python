# Copyright 2025 Google LLC
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

import pandas as pd
import pytest

import bigframes.bigquery as bbq
import bigframes.dtypes as dtypes
import bigframes.pandas as bpd


def test_sql_scalar_for_all_scalar_types(scalars_df_null_index):
    series = bbq.sql_scalar(
        """
        CAST({0} AS INT64)
        + BYTE_LENGTH({1})
        + UNIX_DATE({2})
        + EXTRACT(YEAR FROM {3})
        + ST_NUMPOINTS({4})
        + LEAST(
            {5},
            CAST({6} AS INT64),
            CAST({7} AS INT64)
        ) + CHAR_LENGTH({8})
        + EXTRACT(SECOND FROM {9})
        + UNIX_SECONDS({10})
        """,
        columns=[
            # Try to include all scalar types in a single test.
            scalars_df_null_index["bool_col"],
            scalars_df_null_index["bytes_col"],
            scalars_df_null_index["date_col"],
            scalars_df_null_index["datetime_col"],
            scalars_df_null_index["geography_col"],
            scalars_df_null_index["int64_col"],
            scalars_df_null_index["numeric_col"],
            scalars_df_null_index["float64_col"],
            scalars_df_null_index["string_col"],
            scalars_df_null_index["time_col"],
            scalars_df_null_index["timestamp_col"],
        ],
    )
    result = series.to_pandas()
    assert len(result) == len(scalars_df_null_index)


def test_sql_scalar_for_bool_series(scalars_df_index):
    series: bpd.Series = scalars_df_index["bool_col"]
    result = bbq.sql_scalar("CAST({0} AS INT64)", [series])
    expected = series.astype(dtypes.INT_DTYPE)
    expected.name = None
    pd.testing.assert_series_equal(result.to_pandas(), expected.to_pandas())


@pytest.mark.parametrize(
    ("column_name"),
    [
        pytest.param("bool_col"),
        pytest.param("bytes_col"),
        pytest.param("date_col"),
        pytest.param("datetime_col"),
        pytest.param("geography_col"),
        pytest.param("int64_col"),
        pytest.param("numeric_col"),
        pytest.param("float64_col"),
        pytest.param("string_col"),
        pytest.param("time_col"),
        pytest.param("timestamp_col"),
    ],
)
def test_sql_scalar_outputs_all_scalar_types(scalars_df_index, column_name):
    series: bpd.Series = scalars_df_index[column_name]
    result = bbq.sql_scalar("{0}", [series])
    expected = series
    expected.name = None
    pd.testing.assert_series_equal(result.to_pandas(), expected.to_pandas())


def test_sql_scalar_for_array_series(repeated_df):
    result = bbq.sql_scalar(
        """
        ARRAY_LENGTH({0}) + ARRAY_LENGTH({1}) + ARRAY_LENGTH({2})
        + ARRAY_LENGTH({3}) + ARRAY_LENGTH({4}) + ARRAY_LENGTH({5})
        + ARRAY_LENGTH({6})
        """,
        [
            repeated_df["int_list_col"],
            repeated_df["bool_list_col"],
            repeated_df["float_list_col"],
            repeated_df["date_list_col"],
            repeated_df["date_time_list_col"],
            repeated_df["numeric_list_col"],
            repeated_df["string_list_col"],
        ],
    )

    expected = (
        repeated_df["int_list_col"].list.len()
        + repeated_df["bool_list_col"].list.len()
        + repeated_df["float_list_col"].list.len()
        + repeated_df["date_list_col"].list.len()
        + repeated_df["date_time_list_col"].list.len()
        + repeated_df["numeric_list_col"].list.len()
        + repeated_df["string_list_col"].list.len()
    )
    pd.testing.assert_series_equal(result.to_pandas(), expected.to_pandas())


def test_sql_scalar_outputs_array_series(repeated_df):
    result = bbq.sql_scalar("{0}", [repeated_df["int_list_col"]])
    expected = repeated_df["int_list_col"]
    expected.name = None
    pd.testing.assert_series_equal(result.to_pandas(), expected.to_pandas())


def test_sql_scalar_for_struct_series(nested_structs_df):
    result = bbq.sql_scalar(
        "CHAR_LENGTH({0}.name) + {0}.age",
        [nested_structs_df["person"]],
    )
    expected = nested_structs_df["person"].struct.field(
        "name"
    ).str.len() + nested_structs_df["person"].struct.field("age")
    pd.testing.assert_series_equal(result.to_pandas(), expected.to_pandas())


def test_sql_scalar_outputs_struct_series(nested_structs_df):
    result = bbq.sql_scalar("{0}", [nested_structs_df["person"]])
    expected = nested_structs_df["person"]
    expected.name = None
    pd.testing.assert_series_equal(result.to_pandas(), expected.to_pandas())


def test_sql_scalar_for_json_series(json_df):
    result = bbq.sql_scalar(
        """JSON_VALUE({0}, '$.int_value')""",
        [
            json_df["json_col"],
        ],
    )
    expected = bbq.json_value(json_df["json_col"], "$.int_value")
    expected.name = None
    pd.testing.assert_series_equal(result.to_pandas(), expected.to_pandas())


def test_sql_scalar_outputs_json_series(json_df):
    result = bbq.sql_scalar("{0}", [json_df["json_col"]])
    expected = json_df["json_col"]
    expected.name = None
    pd.testing.assert_series_equal(result.to_pandas(), expected.to_pandas())
