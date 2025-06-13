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


def test_local_data_small_sizes_round_trip():
    pyarrow_version = int(pa.__version__.split(".")[0])

    int8s = [126, 127, -127, -128, 0, 1, -1]
    uint8s = [254, 255, 1, 0, 128, 129, 127]
    int16s = [32766, 32767, -32766, -32767, 0, 1, -1]
    uint16s = [65534, 65535, 1, 0, 32768, 32769, 32767]
    int32s = [2**31 - 2, 2**31 - 1, -(2**31) + 1, -(2**31), 0, 1, -1]
    uint32s = [2**32 - 2, 2**32 - 1, 1, 0, 2**31, 2**31 + 1, 2**31 - 1]
    float16s = [
        # Test some edge cases from:
        # https://en.wikipedia.org/wiki/Half-precision_floating-point_format#Precision_limitations
        float.fromhex("0x1.0p-24"),  # (2 ** -24).hex()
        float.fromhex("-0x1.0p-24"),
        float.fromhex("0x1.ffcp-13"),  # ((2 ** -12) - (2 ** -23)).hex()
        float.fromhex("-0x1.ffcp-13"),
        0,
        float.fromhex("0x1.ffcp+14"),  # (32768.0 - 16).hex()
        float.fromhex("-0x1.ffcp+14"),
    ]
    float32s = [
        # Test some edge cases from:
        # https://en.wikipedia.org/wiki/Single-precision_floating-point_format#Notable_single-precision_cases
        # and
        # https://en.wikipedia.org/wiki/Single-precision_floating-point_format#Precision_limitations_on_decimal_values_(between_1_and_16777216)
        float.fromhex("0x1.0p-149"),  # (2 ** -149).hex()
        float.fromhex("-0x1.0p-149"),  # (2 ** -149).hex()
        float.fromhex("0x1.fffffep-1"),  # (1.0 - (2 ** -24)).hex()
        float.fromhex("-0x1.fffffep-1"),
        0,
        float.fromhex("0x1.fffffcp-127"),  # ((2 ** -126) * (1 - 2 ** -23)).hex()
        float.fromhex("-0x1.fffffcp-127"),  # ((2 ** -126) * (1 - 2 ** -23)).hex()
    ]
    small_data = {
        "int8": pd.Series(int8s, dtype=pd.Int8Dtype()),
        "int16": pd.Series(int16s, dtype=pd.Int16Dtype()),
        "int32": pd.Series(int32s, dtype=pd.Int32Dtype()),
        "uint8": pd.Series(uint8s, dtype=pd.UInt8Dtype()),
        "uint16": pd.Series(uint16s, dtype=pd.UInt16Dtype()),
        "uint32": pd.Series(uint32s, dtype=pd.UInt32Dtype()),
        "float32": pd.Series(float32s, dtype="float32"),
    }
    expected_data = {
        "int8": pd.Series(int8s, dtype=pd.Int64Dtype()),
        "int16": pd.Series(int16s, dtype=pd.Int64Dtype()),
        "int32": pd.Series(int32s, dtype=pd.Int64Dtype()),
        "uint8": pd.Series(uint8s, dtype=pd.Int64Dtype()),
        "uint16": pd.Series(uint16s, dtype=pd.Int64Dtype()),
        "uint32": pd.Series(uint32s, dtype=pd.Int64Dtype()),
        "float32": pd.Series(float32s, dtype=pd.Float64Dtype()),
    }

    # Casting from float16 added in version 16.
    # https://arrow.apache.org/blog/2024/04/20/16.0.0-release/#:~:text=Enhancements,New%20Features
    if pyarrow_version >= 16:
        small_data["float16"] = pd.Series(float16s, dtype="float16")
        expected_data["float16"] = pd.Series(float16s, dtype=pd.Float64Dtype())

    small_pd = pd.DataFrame(small_data)
    local_entry = local_data.ManagedArrowTable.from_pandas(small_pd)
    result = pd.DataFrame(local_entry.itertuples(), columns=small_pd.columns)

    expected = pd.DataFrame(expected_data)
    pandas.testing.assert_frame_equal(expected, result, check_dtype=False)


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


def test_local_data_equal_self():
    local_entry = local_data.ManagedArrowTable.from_pandas(pd_data)
    assert local_entry == local_entry
    assert hash(local_entry) == hash(local_entry)


def test_local_data_not_equal_other():
    local_entry = local_data.ManagedArrowTable.from_pandas(pd_data)
    local_entry2 = local_data.ManagedArrowTable.from_pandas(pd_data[::2])
    assert local_entry != local_entry2
    assert hash(local_entry) != hash(local_entry2)
