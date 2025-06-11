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


import packaging.version
import pandas as pd
import pyarrow as pa
import pytest

from bigframes.testing.utils import assert_series_equal


@pytest.mark.parametrize(
    ("key"),
    [
        pytest.param(0, id="int"),
        pytest.param(slice(None, None, None), id="default_start_slice"),
        pytest.param(slice(0, None, 1), id="default_stop_slice"),
        pytest.param(slice(0, 2, None), id="default_step_slice"),
    ],
)
@pytest.mark.parametrize(
    ("column_name", "dtype"),
    [
        pytest.param("int_list_col", pd.ArrowDtype(pa.list_(pa.int64()))),
        pytest.param("bool_list_col", pd.ArrowDtype(pa.list_(pa.bool_()))),
        pytest.param("float_list_col", pd.ArrowDtype(pa.list_(pa.float64()))),
        pytest.param("date_list_col", pd.ArrowDtype(pa.list_(pa.date32()))),
        pytest.param("date_time_list_col", pd.ArrowDtype(pa.list_(pa.timestamp("us")))),
        pytest.param("numeric_list_col", pd.ArrowDtype(pa.list_(pa.decimal128(38, 9)))),
        pytest.param("string_list_col", pd.ArrowDtype(pa.list_(pa.string()))),
    ],
)
def test_getitem(key, column_name, dtype, repeated_df, repeated_pandas_df):
    if packaging.version.Version(pd.__version__) < packaging.version.Version("2.2.0"):
        pytest.skip(
            "https://pandas.pydata.org/docs/whatsnew/v2.2.0.html#series-list-accessor-for-pyarrow-list-data"
        )

    bf_result = repeated_df[column_name].list[key].to_pandas()
    pd_result = repeated_pandas_df[column_name].astype(dtype).list[key]

    assert_series_equal(
        pd_result,
        bf_result,
        check_dtype=False,
        check_index_type=False,
        check_names=False,
    )


@pytest.mark.parametrize(
    ("key", "expectation"),
    [
        # Negative index
        (-1, pytest.raises(NotImplementedError)),
        # Slice with negative start
        (slice(-1, None, None), pytest.raises(NotImplementedError)),
        # Slice with negatiev end
        (slice(0, -1, None), pytest.raises(NotImplementedError)),
        # Slice with step not equal to 1
        (slice(0, 2, 2), pytest.raises(NotImplementedError)),
    ],
)
def test_getitem_notsupported(key, expectation, repeated_df):
    with expectation as e:
        assert repeated_df["int_list_col"].list[key] == e


@pytest.mark.parametrize(
    ("column_name", "dtype"),
    [
        pytest.param("int_list_col", pd.ArrowDtype(pa.list_(pa.int64()))),
        pytest.param("bool_list_col", pd.ArrowDtype(pa.list_(pa.bool_()))),
        pytest.param("float_list_col", pd.ArrowDtype(pa.list_(pa.float64()))),
        pytest.param("date_list_col", pd.ArrowDtype(pa.list_(pa.date32()))),
        pytest.param("date_time_list_col", pd.ArrowDtype(pa.list_(pa.timestamp("us")))),
        pytest.param("numeric_list_col", pd.ArrowDtype(pa.list_(pa.decimal128(38, 9)))),
        pytest.param("string_list_col", pd.ArrowDtype(pa.list_(pa.string()))),
    ],
)
def test_len(column_name, dtype, repeated_df, repeated_pandas_df):
    if packaging.version.Version(pd.__version__) < packaging.version.Version("2.2.0"):
        pytest.skip(
            "https://pandas.pydata.org/docs/whatsnew/v2.2.0.html#series-list-accessor-for-pyarrow-list-data"
        )

    bf_result = repeated_df[column_name].list.len().to_pandas()
    pd_result = repeated_pandas_df[column_name].astype(dtype).list.len()

    assert_series_equal(
        pd_result,
        bf_result,
        check_dtype=False,
        check_index_type=False,
        check_names=False,
    )
