# Copyright 2023 Google LLC
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

import numpy

from tests.system.utils import assert_pandas_index_equal_ignore_index_type


def test_get_index(scalars_df_index, scalars_pandas_df_index):
    index = scalars_df_index.index
    bf_result = index.to_pandas()
    pd_result = scalars_pandas_df_index.index

    assert_pandas_index_equal_ignore_index_type(bf_result, pd_result)


def test_index_shape(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.index.shape
    pd_result = scalars_pandas_df_index.index.shape

    assert bf_result == pd_result


def test_index_len(scalars_df_index, scalars_pandas_df_index):
    bf_result = len(scalars_df_index.index)
    pd_result = len(scalars_pandas_df_index.index)

    assert bf_result == pd_result


def test_index_array(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.index.__array__()
    pd_result = scalars_pandas_df_index.index.__array__()

    numpy.array_equal(bf_result, pd_result)


def test_index_getitem_int(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.index[-2]
    pd_result = scalars_pandas_df_index.index[-2]
    assert bf_result == pd_result


def test_is_monotonic_increasing(scalars_df_index, scalars_pandas_df_index):
    assert (
        scalars_df_index.index.is_monotonic_increasing
        == scalars_pandas_df_index.index.is_monotonic_increasing
    )


def test_is_monotonic_decreasing(scalars_df_index, scalars_pandas_df_index):
    assert (
        scalars_df_index.index.is_monotonic_increasing
        == scalars_pandas_df_index.index.is_monotonic_increasing
    )
