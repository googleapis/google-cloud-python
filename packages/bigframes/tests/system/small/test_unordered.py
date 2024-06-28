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
import pyarrow as pa
import pytest

import bigframes.exceptions
import bigframes.pandas as bpd
from tests.system.utils import assert_pandas_df_equal, skip_legacy_pandas


def test_unordered_mode_cache_aggregate(unordered_session):
    pd_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}, dtype=pd.Int64Dtype())
    df = bpd.DataFrame(pd_df, session=unordered_session)
    mean_diff = df - df.mean()
    mean_diff.cache()
    bf_result = mean_diff.to_pandas(ordered=False)
    pd_result = pd_df - pd_df.mean()

    assert_pandas_df_equal(bf_result, pd_result, ignore_order=True)


@skip_legacy_pandas
def test_unordered_mode_read_gbq(unordered_session):
    df = unordered_session.read_gbq(
        """SELECT
        [1, 3, 2] AS array_column,
        STRUCT(
            "a" AS string_field,
            1.2 AS float_field) AS struct_column"""
    )
    expected = pd.DataFrame(
        {
            "array_column": pd.Series(
                [[1, 3, 2]],
                dtype=(pd.ArrowDtype(pa.list_(pa.int64()))),
            ),
            "struct_column": pd.Series(
                [{"string_field": "a", "float_field": 1.2}],
                dtype=pd.ArrowDtype(
                    pa.struct(
                        [
                            ("string_field", pa.string()),
                            ("float_field", pa.float64()),
                        ]
                    )
                ),
            ),
        }
    )
    # Don't need ignore_order as there is only 1 row
    assert_pandas_df_equal(df.to_pandas(), expected)


@pytest.mark.parametrize(
    ("keep"),
    [
        pytest.param(
            "first",
            marks=pytest.mark.xfail(raises=bigframes.exceptions.OrderRequiredError),
        ),
        pytest.param(
            False,
        ),
    ],
)
def test_unordered_drop_duplicates(unordered_session, keep):
    pd_df = pd.DataFrame({"a": [1, 1, 3], "b": [4, 4, 6]}, dtype=pd.Int64Dtype())
    bf_df = bpd.DataFrame(pd_df, session=unordered_session)

    bf_result = bf_df.drop_duplicates(keep=keep)
    pd_result = pd_df.drop_duplicates(keep=keep)

    assert_pandas_df_equal(bf_result.to_pandas(), pd_result, ignore_order=True)


@pytest.mark.parametrize(
    ("function"),
    [
        pytest.param(
            lambda x: x.cumsum(),
            id="cumsum",
        ),
        pytest.param(
            lambda x: x.idxmin(),
            id="idxmin",
        ),
        pytest.param(
            lambda x: x.a.iloc[1::2],
            id="series_iloc",
        ),
    ],
)
def test_unordered_mode_blocks_windowing(unordered_session, function):
    pd_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}, dtype=pd.Int64Dtype())
    df = bpd.DataFrame(pd_df, session=unordered_session)
    with pytest.raises(
        bigframes.exceptions.OrderRequiredError,
        match=r"Op.*not supported when strict ordering is disabled",
    ):
        function(df)
