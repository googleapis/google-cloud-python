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

import pandas.testing

from bigframes import dtypes


def test_date_series_diff_agg(scalars_dfs):
    bf_df, pd_df = scalars_dfs

    actual_result = bf_df["date_col"].diff().to_pandas()

    expected_result = pd_df["date_col"].diff().astype(dtypes.TIMEDELTA_DTYPE)
    pandas.testing.assert_series_equal(
        actual_result, expected_result, check_index_type=False
    )
