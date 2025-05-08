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
import pandas as pd
import pandas.testing
import pyarrow as pa

from bigframes import dtypes
from bigframes.core import local_data

pd_data = pd.DataFrame(
    {
        "ints": [10, 20, 30, 40],
        "nested_ints": [[1, 2], [3, 4, 5], [], [20, 30]],
        "structs": [{"a": 100}, {}, {"b": 200}, {"b": 300}],
    }
)

pd_data_normalized = pd.DataFrame(
    {
        "ints": pd.Series([10, 20, 30, 40], dtype=dtypes.INT_DTYPE),
        "nested_ints": pd.Series(
            [[1, 2], [3, 4, 5], [], [20, 30]], dtype=pd.ArrowDtype(pa.list_(pa.int64()))
        ),
        "structs": pd.Series(
            [{"a": 100}, {}, {"b": 200}, {"b": 300}],
            dtype=pd.ArrowDtype(pa.struct({"a": pa.int64(), "b": pa.int64()})),
        ),
    }
)


def test_local_data_well_formed_round_trip():
    local_entry = local_data.ManagedArrowTable.from_pandas(pd_data)
    result = pd.DataFrame(local_entry.itertuples(), columns=pd_data.columns)
    pandas.testing.assert_frame_equal(pd_data_normalized, result, check_dtype=False)


def test_local_data_well_formed_round_trip_chunked():
    pa_table = pa.Table.from_pandas(pd_data, preserve_index=False)
    as_rechunked_pyarrow = pa.Table.from_batches(pa_table.to_batches(max_chunksize=2))
    local_entry = local_data.ManagedArrowTable.from_pyarrow(as_rechunked_pyarrow)
    result = pd.DataFrame(local_entry.itertuples(), columns=pd_data.columns)
    pandas.testing.assert_frame_equal(pd_data_normalized, result, check_dtype=False)


def test_local_data_well_formed_round_trip_sliced():
    pa_table = pa.Table.from_pandas(pd_data, preserve_index=False)
    as_rechunked_pyarrow = pa.Table.from_batches(pa_table.slice(2, 4).to_batches())
    local_entry = local_data.ManagedArrowTable.from_pyarrow(as_rechunked_pyarrow)
    result = pd.DataFrame(local_entry.itertuples(), columns=pd_data.columns)
    pandas.testing.assert_frame_equal(
        pd_data_normalized[2:4].reset_index(drop=True),
        result.reset_index(drop=True),
        check_dtype=False,
    )
