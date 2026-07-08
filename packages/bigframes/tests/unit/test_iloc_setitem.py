# Copyright 2026 Google LLC
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

from typing import Generator

import numpy as np
import pandas as pd
import pytest

import bigframes
import bigframes.pandas as bpd
from bigframes.testing.utils import assert_frame_equal, assert_series_equal

pytest.importorskip("polars")


@pytest.fixture(scope="module", autouse=True)
def session() -> Generator[bigframes.Session, None, None]:
    import bigframes.core.global_session
    from bigframes.testing import polars_session

    session = polars_session.TestSession()
    with bigframes.core.global_session._GlobalSessionContext(session):
        yield session


@pytest.fixture
def sample_df() -> bpd.DataFrame:
    pd_df = pd.DataFrame(
        {
            "A": [1, 2, 3],
            "B": [4, 5, 6],
            "C": [7, 8, 9],
        }
    )
    return bpd.read_pandas(pd_df)


def test_iloc_setitem_column_single_integer(sample_df):
    bf_df = sample_df.copy()
    pd_df = sample_df.to_pandas()

    bf_df.iloc[:, 1] = 99
    pd_df.iloc[:, 1] = 99

    assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_iloc_setitem_column_single_integer_negative(sample_df):
    bf_df = sample_df.copy()
    pd_df = sample_df.to_pandas()

    bf_df.iloc[:, -1] = 99
    pd_df.iloc[:, -1] = 99

    assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_iloc_setitem_columns_list_integer(sample_df):
    bf_df = sample_df.copy()
    pd_df = sample_df.to_pandas()

    bf_df.iloc[:, [0, 2]] = [99, 88]
    pd_df.iloc[:, [0, 2]] = [99, 88]

    assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_iloc_setitem_columns_slice(sample_df):
    bf_df = sample_df.copy()
    pd_df = sample_df.to_pandas()

    bf_df.iloc[:, 0:2] = 99
    pd_df.iloc[:, 0:2] = 99

    assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_iloc_setitem_columns_boolean_mask(sample_df):
    bf_df = sample_df.copy()
    pd_df = sample_df.to_pandas()

    mask = [True, False, True]
    bf_df.iloc[:, mask] = 99
    pd_df.iloc[:, np.array(mask)] = 99

    assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_iloc_setitem_columns_dataframe(sample_df):
    bf_df = sample_df.copy()
    pd_df = sample_df.to_pandas()

    value_df = bpd.DataFrame({"B": [99, 88, 77], "C": [66, 55, 44]})
    bf_df.iloc[:, 1:3] = value_df
    pd_df.iloc[:, 1:3] = value_df.to_pandas()

    assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_iloc_getitem_column_single_integer(sample_df):
    bf_df = sample_df
    pd_df = sample_df.to_pandas()

    bf_result = bf_df.iloc[:, 1].to_pandas()
    pd_result = pd_df.iloc[:, 1]

    assert_series_equal(bf_result, pd_result)


@pytest.fixture
def unordered_sample_df(sample_df: bpd.DataFrame) -> Generator[bpd.DataFrame, None, None]:
    session = sample_df._session
    original_strictly_ordered = session._strictly_ordered
    original_allow_ambiguity = session._allow_ambiguity

    try:
        session._strictly_ordered = False
        session._allow_ambiguity = True

        import unittest.mock as mock

        with (
            mock.patch.object(
                type(sample_df._block.expr),
                "order_ambiguous",
                new_callable=mock.PropertyMock,
            ) as mock_ambiguous,
            mock.patch.object(
                type(sample_df._block),
                "explicitly_ordered",
                new_callable=mock.PropertyMock,
            ) as mock_explicit,
        ):
            mock_ambiguous.return_value = True
            mock_explicit.return_value = False
            yield sample_df
    finally:
        session._strictly_ordered = original_strictly_ordered
        session._allow_ambiguity = original_allow_ambiguity


@pytest.mark.parametrize(
    ["key", "value", "expected_error"],
    [
        pytest.param((slice(None), 1), None, None, id="col_index"),
        pytest.param((slice(0, None), 1), None, None, id="col_index_slice_0_none"),
        pytest.param(
            (slice(None, None, 1), 1), None, None, id="col_index_slice_none_none_1"
        ),
        pytest.param(
            (slice(1, None), 1),
            None,
            bigframes.exceptions.OrderRequiredError,
            id="col_index_slice_1_none",
        ),
        pytest.param(
            (slice(None, 2), 1),
            None,
            bigframes.exceptions.OrderRequiredError,
            id="col_index_slice_none_2",
        ),
        pytest.param((slice(None), 1), 99, None, id="col_setitem"),
        pytest.param(
            (1, slice(None)),
            None,
            bigframes.exceptions.OrderRequiredError,
            id="row_index_slice",
        ),
        pytest.param(
            1,
            None,
            bigframes.exceptions.OrderRequiredError,
            id="single_row_index",
        ),
    ],
)
def test_iloc_getitem_unordered(unordered_sample_df, key, value, expected_error):
    if value is not None:
        bf_df = unordered_sample_df.copy()
        bf_df.iloc[key] = value
    elif expected_error is not None:
        with pytest.raises(expected_error):
            unordered_sample_df.iloc[key]
    else:
        unordered_sample_df.iloc[key]


@pytest.mark.parametrize(
    ["key", "expected_error"],
    [
        pytest.param((slice(None), 3), IndexError, id="out_of_bounds_positive"),
        pytest.param((slice(None), -4), IndexError, id="out_of_bounds_negative"),
        pytest.param((0, 1), NotImplementedError, id="invalid_row_indexer"),
        pytest.param((slice(None), "B"), TypeError, id="invalid_col_indexer_type"),
    ],
)
def test_iloc_setitem_column_errors(sample_df, key, expected_error):
    bf_df = sample_df.copy()

    with pytest.raises(expected_error):
        bf_df.iloc[key] = 99
