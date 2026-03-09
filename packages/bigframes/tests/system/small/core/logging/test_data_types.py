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

from typing import Sequence

import pandas as pd
import pyarrow as pa

from bigframes import dtypes
from bigframes.core.logging import data_types
import bigframes.pandas as bpd


def encode_types(inputs: Sequence[dtypes.Dtype]) -> str:
    encoded_val = 0
    for t in inputs:
        encoded_val = encoded_val | data_types._get_dtype_mask(t)

    return f"{encoded_val:x}"


def test_get_type_refs_no_op(scalars_df_index):
    node = scalars_df_index._block._expr.node
    expected_types: list[dtypes.Dtype] = []

    assert data_types.encode_type_refs(node) == encode_types(expected_types)


def test_get_type_refs_projection(scalars_df_index):
    node = (
        scalars_df_index["datetime_col"] - scalars_df_index["datetime_col"]
    )._block._expr.node
    expected_types = [dtypes.DATETIME_DTYPE, dtypes.TIMEDELTA_DTYPE]

    assert data_types.encode_type_refs(node) == encode_types(expected_types)


def test_get_type_refs_filter(scalars_df_index):
    node = scalars_df_index[scalars_df_index["int64_col"] > 0]._block._expr.node
    expected_types = [dtypes.INT_DTYPE, dtypes.BOOL_DTYPE]

    assert data_types.encode_type_refs(node) == encode_types(expected_types)


def test_get_type_refs_order_by(scalars_df_index):
    node = scalars_df_index.sort_index()._block._expr.node
    expected_types = [dtypes.INT_DTYPE]

    assert data_types.encode_type_refs(node) == encode_types(expected_types)


def test_get_type_refs_join(scalars_df_index):
    node = (
        scalars_df_index[["int64_col"]].merge(
            scalars_df_index[["float64_col"]],
            left_on="int64_col",
            right_on="float64_col",
        )
    )._block._expr.node
    expected_types = [dtypes.INT_DTYPE, dtypes.FLOAT_DTYPE]

    assert data_types.encode_type_refs(node) == encode_types(expected_types)


def test_get_type_refs_isin(scalars_df_index):
    node = scalars_df_index["string_col"].isin(["a"])._block._expr.node
    expected_types = [dtypes.STRING_DTYPE, dtypes.BOOL_DTYPE]

    assert data_types.encode_type_refs(node) == encode_types(expected_types)


def test_get_type_refs_agg(scalars_df_index):
    node = scalars_df_index[["bool_col", "string_col"]].count()._block._expr.node
    expected_types = [
        dtypes.INT_DTYPE,
        dtypes.BOOL_DTYPE,
        dtypes.STRING_DTYPE,
        dtypes.FLOAT_DTYPE,
    ]

    assert data_types.encode_type_refs(node) == encode_types(expected_types)


def test_get_type_refs_window(scalars_df_index):
    node = (
        scalars_df_index[["string_col", "bool_col"]]
        .groupby("string_col")
        .rolling(window=3)
        .count()
        ._block._expr.node
    )
    expected_types = [dtypes.STRING_DTYPE, dtypes.BOOL_DTYPE, dtypes.INT_DTYPE]

    assert data_types.encode_type_refs(node) == encode_types(expected_types)


def test_get_type_refs_explode():
    df = bpd.DataFrame({"A": ["a", "b"], "B": [[1, 2], [3, 4, 5]]})
    node = df.explode("B")._block._expr.node
    expected_types = [pd.ArrowDtype(pa.list_(pa.int64()))]

    assert data_types.encode_type_refs(node) == encode_types(expected_types)
