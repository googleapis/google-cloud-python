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


def test_iloc_setitem_single_integer(sample_df):
    bf_df = sample_df.copy()
    pd_df = sample_df.to_pandas()

    bf_df.iloc[:, 1] = 99
    pd_df.iloc[:, 1] = 99

    assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_iloc_setitem_single_integer_negative(sample_df):
    bf_df = sample_df.copy()
    pd_df = sample_df.to_pandas()

    bf_df.iloc[:, -1] = 99
    pd_df.iloc[:, -1] = 99

    assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_iloc_setitem_list_integer(sample_df):
    bf_df = sample_df.copy()
    pd_df = sample_df.to_pandas()

    bf_df.iloc[:, [0, 2]] = [99, 88]
    pd_df.iloc[:, [0, 2]] = [99, 88]

    assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_iloc_setitem_slice(sample_df):
    bf_df = sample_df.copy()
    pd_df = sample_df.to_pandas()

    bf_df.iloc[:, 0:2] = 99
    pd_df.iloc[:, 0:2] = 99

    assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_iloc_setitem_boolean_mask(sample_df):
    bf_df = sample_df.copy()
    pd_df = sample_df.to_pandas()

    mask = [True, False, True]
    bf_df.iloc[:, mask] = 99
    pd_df.iloc[:, np.array(mask)] = 99

    assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_iloc_setitem_dataframe(sample_df):
    bf_df = sample_df.copy()
    pd_df = sample_df.to_pandas()

    value_df = bpd.DataFrame({"B": [99, 88, 77], "C": [66, 55, 44]})
    bf_df.iloc[:, 1:3] = value_df
    pd_df.iloc[:, 1:3] = value_df.to_pandas()

    assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_iloc_getitem_single_integer(sample_df):
    bf_df = sample_df
    pd_df = sample_df.to_pandas()

    bf_result = bf_df.iloc[:, 1].to_pandas()
    pd_result = pd_df.iloc[:, 1]

    assert_series_equal(bf_result, pd_result)


def test_iloc_getitem_unordered(sample_df):
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

            # 1. Column indexing only - should NOT raise
            try:
                sample_df.iloc[:, 1]
            except bigframes.exceptions.OrderRequiredError:
                pytest.fail("iloc[:, col] raised OrderRequiredError unexpectedly!")

            # 1b. Column indexing with slice(0, None) (NOT exactly `:` but fine) - should NOT raise
            try:
                sample_df.iloc[slice(0, None), 1]
            except bigframes.exceptions.OrderRequiredError:
                pytest.fail("iloc[0:, col] raised OrderRequiredError unexpectedly!")

            # 1c. Column indexing with slice(None, None, 1) (NOT exactly `:` but fine) - should NOT raise
            try:
                sample_df.iloc[slice(None, None, 1), 1]
            except bigframes.exceptions.OrderRequiredError:
                pytest.fail("iloc[::1, col] raised OrderRequiredError unexpectedly!")

            # 1d. Column indexing with slice(1, None) (row subset) - should RAISE
            with pytest.raises(bigframes.exceptions.OrderRequiredError):
                sample_df.iloc[slice(1, None), 1]

            # 1e. Column indexing with slice(None, 2) (row subset) - should RAISE
            with pytest.raises(bigframes.exceptions.OrderRequiredError):
                sample_df.iloc[slice(None, 2), 1]

            # 2. Column setitem only - should NOT raise
            try:
                bf_df = sample_df.copy()
                bf_df.iloc[:, 1] = 99
            except bigframes.exceptions.OrderRequiredError:
                pytest.fail(
                    "iloc[:, col] = val raised OrderRequiredError unexpectedly!"
                )

            # 3. Row indexing - should RAISE
            with pytest.raises(bigframes.exceptions.OrderRequiredError):
                sample_df.iloc[1, :]

            # 4. Single indexer (row indexing) - should RAISE
            with pytest.raises(bigframes.exceptions.OrderRequiredError):
                sample_df.iloc[1]

    finally:
        session._strictly_ordered = original_strictly_ordered
        session._allow_ambiguity = original_allow_ambiguity


def test_iloc_setitem_errors(sample_df):
    bf_df = sample_df.copy()

    # Out of bounds
    with pytest.raises(IndexError):
        bf_df.iloc[:, 3] = 99

    with pytest.raises(IndexError):
        bf_df.iloc[:, -4] = 99

    # Invalid key type (not slice(None) for rows)
    with pytest.raises(NotImplementedError):
        bf_df.iloc[0, 1] = 99

    # Invalid col indexer type
    with pytest.raises(TypeError):
        bf_df.iloc[:, "B"] = 99
