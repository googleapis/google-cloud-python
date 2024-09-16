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

import pytest

import bigframes.dtypes as dtypes
from bigframes.operations.aggregations import (
    all_op,
    any_op,
    count_op,
    dense_rank_op,
    first_op,
    is_agg_op_supported,
    max_op,
    mean_op,
    median_op,
    min_op,
    nunique_op,
    product_op,
    rank_op,
    size_op,
    std_op,
    sum_op,
    var_op,
)

_ALL_OPS = set(
    [
        size_op,
        sum_op,
        mean_op,
        median_op,
        product_op,
        max_op,
        min_op,
        std_op,
        var_op,
        count_op,
        nunique_op,
        rank_op,
        dense_rank_op,
        all_op,
        any_op,
        first_op,
    ]
)
_STRING_SUPPORTED_OPS = set([count_op, nunique_op])


@pytest.mark.parametrize("dtype", dtypes.NUMERIC_BIGFRAMES_TYPES_PERMISSIVE)
@pytest.mark.parametrize("op", _ALL_OPS)
def test_is_agg_op_supported_numerical_support_all(dtype, op):
    assert is_agg_op_supported(dtype, op) is True


@pytest.mark.parametrize("dtype", [dtypes.STRING_DTYPE])
@pytest.mark.parametrize("op", _STRING_SUPPORTED_OPS)
def test_is_agg_op_supported_string_support_ops(dtype, op):
    assert is_agg_op_supported(dtype, op) is True


@pytest.mark.parametrize("dtype", [dtypes.STRING_DTYPE])
@pytest.mark.parametrize("op", _ALL_OPS - _STRING_SUPPORTED_OPS)
def test_is_agg_op_supported_string_not_support_ops(dtype, op):
    assert is_agg_op_supported(dtype, op) is False


@pytest.mark.parametrize(
    "dtype",
    [
        dtypes.BYTES_DTYPE,
        dtypes.DATE_DTYPE,
        dtypes.TIME_DTYPE,
        dtypes.DATETIME_DTYPE,
        dtypes.TIMESTAMP_DTYPE,
        dtypes.GEO_DTYPE,
    ],
)
@pytest.mark.parametrize("op", _ALL_OPS)
def test_is_agg_op_supported_non_numerical_no_support(dtype, op):
    assert is_agg_op_supported(dtype, op) is False
