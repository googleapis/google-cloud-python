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

import pandas as pd
import pytest


@pytest.mark.parametrize(
    ("windowing"),
    [
        pytest.param(lambda x: x.expanding(), id="expanding"),
        pytest.param(lambda x: x.rolling(3, min_periods=3), id="rolling"),
        pytest.param(
            lambda x: x.groupby(x % 2).rolling(3, min_periods=3), id="rollinggroupby"
        ),
        pytest.param(
            lambda x: x.groupby(x % 3).expanding(min_periods=2), id="expandinggroupby"
        ),
    ],
)
@pytest.mark.parametrize(
    ("agg_op"),
    [
        pytest.param(lambda x: x.sum(), id="sum"),
        pytest.param(lambda x: x.min(), id="min"),
        pytest.param(lambda x: x.max(), id="max"),
        pytest.param(lambda x: x.mean(), id="mean"),
        pytest.param(lambda x: x.count(), id="count"),
        pytest.param(lambda x: x.std(), id="std"),
        pytest.param(lambda x: x.var(), id="var"),
    ],
)
def test_series_window_agg_ops(
    scalars_df_index, scalars_pandas_df_index, windowing, agg_op
):
    col_name = "int64_too"
    bf_series = agg_op(windowing(scalars_df_index[col_name])).to_pandas()
    pd_series = agg_op(windowing(scalars_pandas_df_index[col_name]))

    # Pandas always converts to float64, even for min/max/count, which is not desired
    pd_series = pd_series.astype(bf_series.dtype)

    pd.testing.assert_series_equal(
        pd_series,
        bf_series,
    )


@pytest.mark.parametrize(
    ("windowing"),
    [
        pytest.param(lambda x: x.expanding(), id="expanding"),
        pytest.param(lambda x: x.rolling(3, min_periods=3), id="rolling"),
        pytest.param(
            lambda x: x.groupby(level=0).rolling(3, min_periods=3), id="rollinggroupby"
        ),
        pytest.param(
            lambda x: x.groupby("int64_too").expanding(min_periods=2),
            id="expandinggroupby",
        ),
    ],
)
@pytest.mark.parametrize(
    ("agg_op"),
    [
        pytest.param(lambda x: x.sum(), id="sum"),
        pytest.param(lambda x: x.min(), id="min"),
        pytest.param(lambda x: x.max(), id="max"),
        pytest.param(lambda x: x.mean(), id="mean"),
        pytest.param(lambda x: x.count(), id="count"),
        pytest.param(lambda x: x.std(), id="std"),
        pytest.param(lambda x: x.var(), id="var"),
    ],
)
def test_dataframe_window_agg_ops(
    scalars_df_index, scalars_pandas_df_index, windowing, agg_op
):
    scalars_df_index = scalars_df_index.set_index("bool_col")
    scalars_pandas_df_index = scalars_pandas_df_index.set_index("bool_col")
    col_names = ["int64_too", "float64_col"]
    bf_result = agg_op(windowing(scalars_df_index[col_names])).to_pandas()
    pd_result = agg_op(windowing(scalars_pandas_df_index[col_names]))

    pd.testing.assert_frame_equal(pd_result, bf_result, check_dtype=False)
