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

from bigframes.testing.utils import assert_pandas_df_equal


@pytest.mark.parametrize(
    ("merge_how",),
    [
        ("inner",),
        ("outer",),
        ("left",),
        ("right",),
    ],
)
def test_merge_after_filter(baseball_schedules_df, merge_how):
    on = ["awayTeamName"]
    left_columns = [
        "gameId",
        "year",
        "homeTeamName",
        "awayTeamName",
        "duration_minutes",
    ]
    right_columns = [
        "gameId",
        "year",
        "homeTeamName",
        "awayTeamName",
        "duration_minutes",
    ]

    left = baseball_schedules_df[left_columns]
    left = left[left["homeTeamName"] == "Rays"]
    # Offset the rows somewhat so that outer join can have an effect.
    right = baseball_schedules_df[right_columns]
    right = right[right["homeTeamName"] == "White Sox"]

    df = left.merge(right, on=on, how=merge_how)
    bf_result = df.to_pandas()

    left_pandas = baseball_schedules_df.to_pandas()[left_columns]
    left_pandas = left_pandas[left_pandas["homeTeamName"] == "Rays"]

    right_pandas = baseball_schedules_df.to_pandas()[right_columns]
    right_pandas = right_pandas[right_pandas["homeTeamName"] == "White Sox"]

    pd_result = pd.merge(
        left_pandas,
        right_pandas,
        merge_how,
        on,
        sort=True,
    )

    assert_pandas_df_equal(bf_result, pd_result, ignore_order=True)
