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

from packaging import version
import pandas as pd
import pandas.testing
import pytest


@pytest.mark.parametrize("level", [None, 0, 1, "level0", "level1"])
def test_unique(session, level):
    if version.Version(pd.__version__) < version.Version("2.0.0"):
        pytest.skip("StringDtype for multi-index not supported until Pandas 2.0")
    arrays = [
        pd.Series(["A", "A", "B", "B", "A"], dtype=pd.StringDtype(storage="pyarrow")),
        pd.Series([1, 2, 1, 2, 1], dtype=pd.Int64Dtype()),
    ]
    pd_idx = pd.MultiIndex.from_arrays(arrays, names=["level0", "level1"])
    bf_idx = session.read_pandas(pd_idx)

    actual_result = bf_idx.unique(level).to_pandas()

    expected_result = pd_idx.unique(level)
    pandas.testing.assert_index_equal(actual_result, expected_result)
