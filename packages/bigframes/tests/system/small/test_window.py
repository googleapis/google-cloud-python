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
        (lambda x: x.expanding()),
        (lambda x: x.rolling(3, min_periods=3)),
        (lambda x: x.groupby(x % 2).rolling(3, min_periods=3)),
        (lambda x: x.groupby(x % 3).expanding(min_periods=2)),
    ],
    ids=[
        "expanding",
        "rolling",
        "rollinggroupby",
        "expandinggroupby",
    ],
)
@pytest.mark.parametrize(
    ("agg_op"),
    [
        (lambda x: x.sum()),
        (lambda x: x.min()),
        (lambda x: x.max()),
        (lambda x: x.mean()),
        (lambda x: x.count()),
        (lambda x: x.std()),
        (lambda x: x.var()),
    ],
    ids=[
        "sum",
        "min",
        "max",
        "mean",
        "count",
        "std",
        "var",
    ],
)
def test_window_agg_ops(scalars_df_index, scalars_pandas_df_index, windowing, agg_op):
    col_name = "int64_too"
    bf_series = agg_op(windowing(scalars_df_index[col_name])).compute()
    pd_series = agg_op(windowing(scalars_pandas_df_index[col_name]))

    # Pandas always converts to float64, even for min/max/count, which is not desired
    pd_series = pd_series.astype(bf_series.dtype)

    pd.testing.assert_series_equal(
        pd_series,
        bf_series,
    )
