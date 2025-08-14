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

import sys

import numpy as np
import pandas as pd
import pytest

import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


if sys.version_info < (3, 12):
    pytest.skip(
        "Skipping test due to inconsistent SQL formatting on Python < 3.12.",
        allow_module_level=True,
    )


def test_compile_window_w_rolling(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]].sort_index()
    result = bf_df.rolling(window=3).sum()
    snapshot.assert_match(result.sql, "out.sql")


def test_compile_window_w_groupby_rolling(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["bool_col", "int64_col"]].sort_index()
    result = (
        bf_df.groupby(scalar_types_df["bool_col"])
        .rolling(window=3, closed="both")
        .sum()
    )
    snapshot.assert_match(result.sql, "out.sql")


def test_compile_window_w_min_periods(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]].sort_index()
    result = bf_df.expanding(min_periods=3).sum()
    snapshot.assert_match(result.sql, "out.sql")


def test_compile_window_w_range_rolling(compiler_session, snapshot):
    values = np.arange(20)
    pd_df = pd.DataFrame(
        {
            "ts_col": pd.Timestamp("20250101", tz="UTC") + pd.to_timedelta(values, "s"),
            "int_col": values % 4,
            "float_col": values / 2,
        }
    )
    bf_df = compiler_session.read_pandas(pd_df)
    bf_series = bf_df.set_index("ts_col")["int_col"].sort_index()
    result = bf_series.rolling(window="3s").sum()
    snapshot.assert_match(result.to_frame().sql, "out.sql")
