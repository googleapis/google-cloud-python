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
import warnings

import pandas as pd
import pyarrow as pa
import pytest

import bigframes.exceptions
import bigframes.pandas as bpd
from bigframes.testing.utils import assert_pandas_df_equal, assert_series_equal


def test_unordered_mode_sql_no_hash(unordered_session):
    bf_df = unordered_session.read_gbq(
        "bigquery-public-data.ethereum_blockchain.blocks"
    )
    sql = bf_df.sql
    assert "ORDER BY".casefold() not in sql.casefold()
    assert "farm_fingerprint".casefold() not in sql.casefold()


def test_unordered_mode_job_label(unordered_session):
    pd_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}, dtype=pd.Int64Dtype())
    df = bpd.DataFrame(pd_df, session=unordered_session)
    df.to_gbq()
    job_labels = df.query_job.labels  # type:ignore
    assert "bigframes-mode" in job_labels
    assert job_labels["bigframes-mode"] == "unordered"


def test_unordered_mode_cache_aggregate(unordered_session):
    pd_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}, dtype=pd.Int64Dtype())
    df = bpd.DataFrame(pd_df, session=unordered_session)
    mean_diff = df - df.mean()
    mean_diff.cache()
    bf_result = mean_diff.to_pandas(ordered=False)
    pd_result = pd_df - pd_df.mean()

    assert_pandas_df_equal(bf_result, pd_result, ignore_order=True)


def test_unordered_mode_series_peek(unordered_session):
    pd_series = pd.Series([1, 2, 3, 4, 5, 6], dtype=pd.Int64Dtype())
    bf_series = bpd.Series(pd_series, session=unordered_session)
    pd_result = pd_series.groupby(pd_series % 4).sum()
    bf_peek = bf_series.groupby(bf_series % 4).sum().peek(2)

    assert_series_equal(bf_peek, pd_result.reindex(bf_peek.index))


def test_unordered_mode_single_aggregate(unordered_session):
    pd_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}, dtype=pd.Int64Dtype())
    bf_df = bpd.DataFrame(pd_df, session=unordered_session)

    assert bf_df.a.mean() == pd_df.a.mean()


def test_unordered_mode_print(unordered_session):
    pd_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}, dtype=pd.Int64Dtype())
    df = bpd.DataFrame(pd_df, session=unordered_session).cache()
    print(df)


def test_unordered_mode_read_gbq(unordered_session):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
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


def test_unordered_reset_index(unordered_session):
    pd_df = pd.DataFrame({"a": [1, 1, 3], "b": [4, 4, 6]}, dtype=pd.Int64Dtype())
    bf_df = bpd.DataFrame(pd_df, session=unordered_session)

    bf_result = bf_df.set_index("b").reset_index(drop=False)
    pd_result = pd_df.set_index("b").reset_index(drop=False)

    assert_pandas_df_equal(bf_result.to_pandas(), pd_result)


def test_unordered_merge(unordered_session):
    pd_df = pd.DataFrame(
        {"a": [1, 1, 3], "b": [4, 4, 6], "c": [1, 2, 3]}, dtype=pd.Int64Dtype()
    )
    bf_df = bpd.DataFrame(pd_df, session=unordered_session)

    bf_result = bf_df.merge(bf_df, left_on="a", right_on="c")
    pd_result = pd_df.merge(pd_df, left_on="a", right_on="c")

    assert_pandas_df_equal(bf_result.to_pandas(), pd_result, ignore_order=True)


def test_unordered_drop_duplicates_ambiguous(unordered_session):
    pd_df = pd.DataFrame(
        {"a": [1, 1, 1], "b": [4, 4, 6], "c": [1, 1, 3]}, dtype=pd.Int64Dtype()
    )
    bf_df = bpd.DataFrame(pd_df, session=unordered_session)

    # merge first to discard original ordering
    bf_result = (
        bf_df.merge(bf_df, left_on="a", right_on="c")
        .sort_values("c_y")
        .drop_duplicates()
    )
    pd_result = (
        pd_df.merge(pd_df, left_on="a", right_on="c")
        .sort_values("c_y")
        .drop_duplicates()
    )

    assert_pandas_df_equal(bf_result.to_pandas(), pd_result, ignore_order=True)


def test_unordered_mode_cache_preserves_order(unordered_session):
    pd_df = pd.DataFrame(
        {"a": [1, 2, 3, 4, 5, 6], "b": [4, 5, 9, 3, 1, 6]}, dtype=pd.Int64Dtype()
    )
    pd_df.index = pd_df.index.astype(pd.Int64Dtype())
    df = bpd.DataFrame(pd_df, session=unordered_session)
    sorted_df = df.sort_values("b").cache()
    bf_result = sorted_df.to_pandas()
    pd_result = pd_df.sort_values("b")

    # B is unique so unstrict order mode result here should be equivalent to strictly ordered
    assert_pandas_df_equal(bf_result, pd_result, ignore_order=False)


def test_unordered_mode_no_ordering_error(unordered_session):
    pd_df = pd.DataFrame(
        {"a": [1, 2, 3, 4, 5, 1], "b": [4, 5, 9, 3, 1, 6]}, dtype=pd.Int64Dtype()
    )
    pd_df.index = pd_df.index.astype(pd.Int64Dtype())
    df = bpd.DataFrame(pd_df, session=unordered_session)

    with pytest.raises(bigframes.exceptions.OrderRequiredError):
        df.merge(df, on="a").head(3)


def test_unordered_mode_ambiguity_warning(unordered_session):
    pd_df = pd.DataFrame(
        {"a": [1, 2, 3, 4, 5, 1], "b": [4, 5, 9, 3, 1, 6]}, dtype=pd.Int64Dtype()
    )
    pd_df.index = pd_df.index.astype(pd.Int64Dtype())
    df = bpd.DataFrame(pd_df, session=unordered_session)

    with pytest.warns(bigframes.exceptions.AmbiguousWindowWarning):
        df.merge(df, on="a").sort_values("b_x").head(3)


def test_unordered_mode_no_ambiguity_warning(unordered_session):
    pd_df = pd.DataFrame(
        {"a": [1, 2, 3, 4, 5, 1], "b": [4, 5, 9, 3, 1, 6]}, dtype=pd.Int64Dtype()
    )
    pd_df.index = pd_df.index.astype(pd.Int64Dtype())
    df = bpd.DataFrame(pd_df, session=unordered_session)

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        df.groupby("a").head(3)


@pytest.mark.parametrize(
    ("rule", "origin", "data"),
    [
        (
            "5h",
            "epoch",
            {
                "timestamp_col": pd.date_range(
                    start="2021-01-01 13:00:00", periods=30, freq="1h"
                ),
                "int64_col": range(30),
                "int64_too": range(10, 40),
            },
        ),
        (
            "5h",
            "epoch",
            {
                "timestamp_col": pd.DatetimeIndex(
                    pd.date_range(
                        start="2021-01-01 13:00:00", periods=15, freq="1h"
                    ).tolist()
                    + pd.date_range(
                        start="2021-01-01 13:00:00", periods=15, freq="1h"
                    ).tolist()
                ),
                "int64_col": range(30),
                "int64_too": range(10, 40),
            },
        ),
    ],
)
def test__resample_with_index(unordered_session, rule, origin, data):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    col = "timestamp_col"
    scalars_df_index = bpd.DataFrame(data, session=unordered_session).set_index(col)
    scalars_pandas_df_index = pd.DataFrame(data).set_index(col)
    scalars_pandas_df_index.index.name = None

    bf_result = scalars_df_index._resample(rule=rule, origin=origin).min().to_pandas()

    pd_result = scalars_pandas_df_index.resample(rule=rule, origin=origin).min()

    pd.testing.assert_frame_equal(
        bf_result, pd_result, check_dtype=False, check_index_type=False
    )
