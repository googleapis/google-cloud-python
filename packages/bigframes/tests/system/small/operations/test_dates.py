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


import datetime

import pandas as pd
import pandas.testing

from bigframes import dtypes


def test_date_diff_between_series(session):
    pd_df = pd.DataFrame(
        {
            "col_1": [datetime.date(2025, 1, 2), datetime.date(2025, 2, 1)],
            "col_2": [datetime.date(2024, 1, 2), datetime.date(2026, 1, 30)],
        }
    ).astype(dtypes.DATE_DTYPE)
    bf_df = session.read_pandas(pd_df)

    actual_result = (bf_df["col_1"] - bf_df["col_2"]).to_pandas()

    expected_result = (pd_df["col_1"] - pd_df["col_2"]).astype(dtypes.TIMEDELTA_DTYPE)
    pandas.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_date_diff_literal_sub_series(scalars_dfs):
    bf_df, pd_df = scalars_dfs
    literal = datetime.date(2030, 5, 20)

    actual_result = (literal - bf_df["date_col"]).to_pandas()

    expected_result = (literal - pd_df["date_col"]).astype(dtypes.TIMEDELTA_DTYPE)
    pandas.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_date_diff_series_sub_literal(scalars_dfs):
    bf_df, pd_df = scalars_dfs
    literal = datetime.date(1980, 5, 20)

    actual_result = (bf_df["date_col"] - literal).to_pandas()

    expected_result = (pd_df["date_col"] - literal).astype(dtypes.TIMEDELTA_DTYPE)
    pandas.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )


def test_date_series_diff_agg(scalars_dfs):
    bf_df, pd_df = scalars_dfs

    actual_result = bf_df["date_col"].diff().to_pandas()

    expected_result = pd_df["date_col"].diff().astype(dtypes.TIMEDELTA_DTYPE)
    pandas.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )
