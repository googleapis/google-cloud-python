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

import numpy as np
import pandas as pd
import pytest

import bigframes
from bigframes.testing.utils import assert_pandas_df_equal

large_dataframe = pd.DataFrame(np.random.rand(10000, 10), dtype="Float64")
large_dataframe.index = large_dataframe.index.astype("Int64")


def test_read_pandas_defer_noop(session: bigframes.Session):
    pytest.importorskip("pandas", minversion="2.0.0")
    bf_df = session.read_pandas(large_dataframe, write_engine="_deferred")

    assert_pandas_df_equal(large_dataframe, bf_df.to_pandas())


def test_read_pandas_defer_cumsum(session: bigframes.Session):
    pytest.importorskip("pandas", minversion="2.0.0")
    bf_df = session.read_pandas(large_dataframe, write_engine="_deferred")
    bf_df = bf_df.cumsum()

    assert_pandas_df_equal(large_dataframe.cumsum(), bf_df.to_pandas())


def test_read_pandas_defer_cache_cumsum_cumsum(session: bigframes.Session):
    pytest.importorskip("pandas", minversion="2.0.0")
    bf_df = session.read_pandas(large_dataframe, write_engine="_deferred")
    bf_df = bf_df.cumsum().cache().cumsum()

    assert_pandas_df_equal(large_dataframe.cumsum().cumsum(), bf_df.to_pandas())


def test_read_pandas_defer_peek(session: bigframes.Session):
    pytest.importorskip("pandas", minversion="2.0.0")
    bf_df = session.read_pandas(large_dataframe, write_engine="_deferred")
    bf_result = bf_df.peek(15)

    assert len(bf_result) == 15
    assert_pandas_df_equal(large_dataframe.loc[bf_result.index], bf_result)
