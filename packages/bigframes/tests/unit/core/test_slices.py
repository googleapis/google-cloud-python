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

import bigframes.core.slices as slices


@pytest.mark.parametrize(
    ["slice", "input_rows", "expected"],
    [
        ((1, 2, 3), 3, 1),
        ((-3, 400, None), 401, 2),
        ((5, 505, None), 300, 295),
        ((1, 10, 4), 10, 3),
        ((1, 9, 4), 10, 2),
        ((-1, -10, -4), 10, 3),
        ((-1, -10, 4), 10, 0),
        ((99, 100, 1), 9, 0),
    ],
)
def test_slice_row_count(slice, input_rows, expected):
    assert expected == slices.slice_output_rows(slice, input_rows)


@pytest.mark.parametrize(
    ["slice", "input_rows", "expected"],
    [
        ((1, 2, 3), 3, (1, 2, 3)),
        ((-3, 400, None), 401, (-3, 400, None)),
        ((5, 505, None), 300, (5, None, None)),
        ((99, 100, 1), 9, (99, None, None)),
    ],
)
def test_remove_unused_parts(slice, input_rows, expected):
    assert expected == slices.remove_unused_parts(slice, input_rows)


@pytest.mark.parametrize(
    ["slice", "input_rows", "expected"],
    [
        ((1, 2, 3), 3, (1, 2, 3)),
        ((-3, 400, None), 401, (398, 400, 1)),
        ((5, 505, None), 300, (5, 300, 1)),
        ((None, None, None), 300, (0, None, 1)),
        ((None, None, -1), 300, (299, None, -1)),
    ],
)
def test_to_forward_offsets(slice, input_rows, expected):
    assert expected == slices.to_forward_offsets(slice, input_rows)
