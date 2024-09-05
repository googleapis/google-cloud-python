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


import packaging.version
import pandas as pd
import pyarrow as pa
import pytest

import bigframes.pandas as bpd

from ...utils import assert_series_equal


@pytest.mark.parametrize(
    ("key"),
    [
        pytest.param(0, id="int"),
        pytest.param(slice(None, None, None), id="default_start_slice"),
        pytest.param(slice(0, None, 1), id="default_stop_slice"),
        pytest.param(slice(0, 2, None), id="default_step_slice"),
    ],
)
def test_getitem(key):
    if packaging.version.Version(pd.__version__) < packaging.version.Version("2.2.0"):
        pytest.skip(
            "https://pandas.pydata.org/docs/whatsnew/v2.2.0.html#series-list-accessor-for-pyarrow-list-data"
        )
    data = [[1], [2, 3], [4, 5, 6]]
    s = bpd.Series(data, dtype=pd.ArrowDtype(pa.list_(pa.int64())))
    pd_s = pd.Series(data, dtype=pd.ArrowDtype(pa.list_(pa.int64())))

    bf_result = s.list[key].to_pandas()
    pd_result = pd_s.list[key]

    assert_series_equal(pd_result, bf_result, check_dtype=False, check_index_type=False)


@pytest.mark.parametrize(
    ("key", "expectation"),
    [
        # Negative index
        (-1, pytest.raises(NotImplementedError)),
        # Slice with negative start
        (slice(-1, None, None), pytest.raises(NotImplementedError)),
        # Slice with negatiev end
        (slice(0, -1, None), pytest.raises(NotImplementedError)),
        # Slice with step not equal to 1
        (slice(0, 2, 2), pytest.raises(NotImplementedError)),
    ],
)
def test_getitem_notsupported(key, expectation):
    data = [[1], [2, 3], [4, 5, 6]]
    s = bpd.Series(data, dtype=pd.ArrowDtype(pa.list_(pa.int64())))

    with expectation as e:
        assert s.list[key] == e


def test_len():
    if packaging.version.Version(pd.__version__) < packaging.version.Version("2.2.0"):
        pytest.skip(
            "https://pandas.pydata.org/docs/whatsnew/v2.2.0.html#series-list-accessor-for-pyarrow-list-data"
        )
    data = [[], [1], [1, 2], [1, 2, 3]]
    s = bpd.Series(data, dtype=pd.ArrowDtype(pa.list_(pa.int64())))
    pd_s = pd.Series(data, dtype=pd.ArrowDtype(pa.list_(pa.int64())))

    bf_result = s.list.len().to_pandas()
    pd_result = pd_s.list.len()

    assert_series_equal(pd_result, bf_result, check_dtype=False, check_index_type=False)
