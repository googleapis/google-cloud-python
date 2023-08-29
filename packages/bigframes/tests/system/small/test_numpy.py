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

import numpy as np
import pandas as pd
import pytest


@pytest.mark.parametrize(
    ("opname",),
    [
        ("sin",),
        ("cos",),
        ("tan",),
        ("arcsin",),
        ("arccos",),
        ("arctan",),
        ("sinh",),
        ("cosh",),
        ("tanh",),
        ("arcsinh",),
        ("arccosh",),
        ("arctanh",),
        ("exp",),
        ("log",),
        ("log10",),
        ("sqrt",),
        ("abs",),
    ],
)
def test_series_ufuncs(floats_pd, floats_bf, opname):
    bf_result = getattr(np, opname)(floats_bf).to_pandas()
    pd_result = getattr(np, opname)(floats_pd)

    pd.testing.assert_series_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("opname",),
    [
        ("sin",),
        ("cos",),
        ("tan",),
        ("log",),
        ("log10",),
        ("sqrt",),
        ("abs",),
    ],
)
def test_df_ufuncs(scalars_dfs, opname):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = getattr(np, opname)(
        scalars_df[["float64_col", "int64_col"]]
    ).to_pandas()
    pd_result = getattr(np, opname)(scalars_pandas_df[["float64_col", "int64_col"]])

    pd.testing.assert_frame_equal(bf_result, pd_result)
