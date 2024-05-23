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


import pandas as pd
import pytest

import bigframes.exceptions
import bigframes.pandas as bpd
from tests.system.utils import skip_legacy_pandas


def test_empty_index_materialize(
    scalars_df_empty_index, scalars_pandas_df_default_index
):
    bf_result = scalars_df_empty_index.to_pandas()
    pd.testing.assert_frame_equal(
        bf_result, scalars_pandas_df_default_index, check_index_type=False
    )


def test_empty_index_series_repr(
    scalars_df_empty_index, scalars_pandas_df_default_index
):
    bf_result = scalars_df_empty_index["int64_too"].head(5).__repr__()
    pd_result = (
        scalars_pandas_df_default_index["int64_too"]
        .head(5)
        .to_string(dtype=True, index=False, length=False, name=True)
    )
    assert bf_result == pd_result


def test_empty_index_dataframe_repr(
    scalars_df_empty_index, scalars_pandas_df_default_index
):
    bf_result = scalars_df_empty_index[["int64_too", "int64_col"]].head(5).__repr__()
    pd_result = (
        scalars_pandas_df_default_index[["int64_too", "int64_col"]]
        .head(5)
        .to_string(index=False)
    )
    assert bf_result == pd_result + "\n\n[5 rows x 2 columns]"


def test_empty_index_reset_index(
    scalars_df_empty_index, scalars_pandas_df_default_index
):
    bf_result = scalars_df_empty_index.reset_index().to_pandas()
    pd_result = scalars_pandas_df_default_index.reset_index(drop=True)
    pd.testing.assert_frame_equal(bf_result, pd_result, check_index_type=False)


def test_empty_index_set_index(scalars_df_empty_index, scalars_pandas_df_default_index):
    bf_result = scalars_df_empty_index.set_index("int64_col").to_pandas()
    pd_result = scalars_pandas_df_default_index.set_index("int64_col")
    pd.testing.assert_frame_equal(bf_result, pd_result)


def test_empty_index_concat(scalars_df_empty_index, scalars_pandas_df_default_index):
    bf_result = bpd.concat(
        [scalars_df_empty_index, scalars_df_empty_index], axis=0
    ).to_pandas()
    pd_result = pd.concat(
        [scalars_pandas_df_default_index, scalars_pandas_df_default_index], axis=0
    )
    pd.testing.assert_frame_equal(bf_result, pd_result.reset_index(drop=True))


def test_empty_index_aggregate(scalars_df_empty_index, scalars_pandas_df_default_index):
    bf_result = scalars_df_empty_index.count().to_pandas()
    pd_result = scalars_pandas_df_default_index.count()

    pd_result.index = pd_result.index.astype("string[pyarrow]")

    pd.testing.assert_series_equal(
        bf_result, pd_result, check_dtype=False, check_index_type=False
    )


def test_empty_index_groupby_aggregate(
    scalars_df_empty_index, scalars_pandas_df_default_index
):
    bf_result = scalars_df_empty_index.groupby("int64_col").count().to_pandas()
    pd_result = scalars_pandas_df_default_index.groupby("int64_col").count()

    pd.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


@skip_legacy_pandas
def test_empty_index_analytic(scalars_df_empty_index, scalars_pandas_df_default_index):
    bf_result = scalars_df_empty_index["int64_col"].cumsum().to_pandas()
    pd_result = scalars_pandas_df_default_index["int64_col"].cumsum()
    pd.testing.assert_series_equal(
        bf_result, pd_result.reset_index(drop=True), check_dtype=False
    )


def test_empty_index_groupby_analytic(
    scalars_df_empty_index, scalars_pandas_df_default_index
):
    bf_result = (
        scalars_df_empty_index.groupby("bool_col")["int64_col"].cummax().to_pandas()
    )
    pd_result = scalars_pandas_df_default_index.groupby("bool_col")[
        "int64_col"
    ].cummax()
    pd.testing.assert_series_equal(
        bf_result, pd_result.reset_index(drop=True), check_dtype=False
    )


@skip_legacy_pandas
def test_empty_index_stack(scalars_df_empty_index, scalars_pandas_df_default_index):
    stacking_cols = ["int64_col", "int64_too"]
    bf_result = scalars_df_empty_index[stacking_cols].stack().to_pandas()
    pd_result = (
        scalars_pandas_df_default_index[stacking_cols]
        .stack(future_stack=True)
        .droplevel(level=0, axis=0)
    )
    pd_result.index = pd_result.index.astype(bf_result.index.dtype)
    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
        check_dtype=False,
    )


def test_empty_index_series_self_aligns(
    scalars_df_empty_index, scalars_pandas_df_default_index
):
    bf_result = (
        scalars_df_empty_index["int64_col"] + scalars_df_empty_index["int64_too"]
    )
    pd_result = (
        scalars_pandas_df_default_index["int64_col"]
        + scalars_pandas_df_default_index["int64_too"]
    )
    pd.testing.assert_series_equal(
        bf_result.to_pandas(), pd_result.reset_index(drop=True), check_dtype=False
    )


def test_empty_index_df_self_aligns(
    scalars_df_empty_index, scalars_pandas_df_default_index
):
    bf_result = (
        scalars_df_empty_index[["int64_col", "float64_col"]]
        + scalars_df_empty_index[["int64_col", "float64_col"]]
    )
    pd_result = (
        scalars_pandas_df_default_index[["int64_col", "float64_col"]]
        + scalars_pandas_df_default_index[["int64_col", "float64_col"]]
    )
    pd.testing.assert_frame_equal(
        bf_result.to_pandas(), pd_result.reset_index(drop=True), check_dtype=False
    )


def test_empty_index_setitem(scalars_df_empty_index, scalars_pandas_df_default_index):
    bf_result = scalars_df_empty_index.copy()
    bf_result["new_col"] = (
        scalars_df_empty_index["int64_col"] + scalars_df_empty_index["float64_col"]
    )
    pd_result = scalars_pandas_df_default_index.copy()
    pd_result["new_col"] = (
        scalars_pandas_df_default_index["int64_col"]
        + scalars_pandas_df_default_index["float64_col"]
    )
    pd.testing.assert_frame_equal(
        bf_result.to_pandas(), pd_result.reset_index(drop=True), check_dtype=False
    )


def test_empty_index_df_concat(scalars_df_empty_index, scalars_pandas_df_default_index):
    bf_result = bpd.concat([scalars_df_empty_index, scalars_df_empty_index])
    pd_result = pd.concat(
        [scalars_pandas_df_default_index, scalars_pandas_df_default_index]
    )
    pd.testing.assert_frame_equal(
        bf_result.to_pandas(), pd_result.reset_index(drop=True), check_dtype=False
    )


def test_empty_index_align_error(scalars_df_empty_index):
    with pytest.raises(bigframes.exceptions.NullIndexError):
        _ = (
            scalars_df_empty_index["int64_col"]
            + scalars_df_empty_index["int64_col"].cumsum()
        )


def test_empty_index_loc_error(scalars_df_empty_index):
    with pytest.raises(bigframes.exceptions.NullIndexError):
        scalars_df_empty_index["int64_col"].loc[1]


def test_empty_index_at_error(scalars_df_empty_index):
    with pytest.raises(bigframes.exceptions.NullIndexError):
        scalars_df_empty_index["int64_col"].at[1]


def test_empty_index_idxmin_error(scalars_df_empty_index):
    with pytest.raises(bigframes.exceptions.NullIndexError):
        scalars_df_empty_index[["int64_col", "int64_too"]].idxmin()


def test_empty_index_index_property(scalars_df_empty_index):
    with pytest.raises(bigframes.exceptions.NullIndexError):
        _ = scalars_df_empty_index.index


def test_empty_index_transpose(scalars_df_empty_index):
    with pytest.raises(bigframes.exceptions.NullIndexError):
        _ = scalars_df_empty_index.T
