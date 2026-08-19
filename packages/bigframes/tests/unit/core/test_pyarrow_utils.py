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

import itertools

import numpy as np
import pyarrow as pa
import pytest

from bigframes.core import pyarrow_utils

PA_TABLE = pa.table({f"col_{i}": np.random.rand(1000) for i in range(10)})

# 17, 3, 929 coprime
N = 17
MANY_SMALL_BATCHES = PA_TABLE.to_batches(max_chunksize=3)
FEW_BIG_BATCHES = PA_TABLE.to_batches(max_chunksize=929)


@pytest.mark.parametrize(
    ["batches", "page_size"],
    [
        (MANY_SMALL_BATCHES, N),
        (FEW_BIG_BATCHES, N),
    ],
)
def test_chunk_by_row_count(batches, page_size):
    results = list(pyarrow_utils.chunk_by_row_count(batches, page_size=page_size))

    for i, batches in enumerate(results):
        if i != len(results) - 1:
            assert sum(map(lambda x: x.num_rows, batches)) == page_size
        else:
            # final page can be smaller
            assert sum(map(lambda x: x.num_rows, batches)) <= page_size

    reconstructed = pa.Table.from_batches(itertools.chain.from_iterable(results))
    assert reconstructed.equals(PA_TABLE)


@pytest.mark.parametrize(
    ["batches", "max_rows"],
    [
        (MANY_SMALL_BATCHES, N),
        (FEW_BIG_BATCHES, N),
    ],
)
def test_truncate_pyarrow_iterable(batches, max_rows):
    results = list(
        pyarrow_utils.truncate_pyarrow_iterable(batches, max_results=max_rows)
    )

    reconstructed = pa.Table.from_batches(results)
    assert reconstructed.equals(PA_TABLE.slice(length=max_rows))
