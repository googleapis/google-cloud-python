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

import pytest

from bigframes.core import window_spec


@pytest.mark.parametrize(("start", "end"), [(-1, -2), (1, -2), (2, 1)])
def test_invalid_rows_window_boundary_raise_error(start, end):
    with pytest.raises(ValueError):
        window_spec.RowsWindowBounds(start, end)


@pytest.mark.parametrize(("start", "end"), [(-1, -2), (1, -2), (2, 1)])
def test_invalid_range_window_boundary_raise_error(start, end):
    with pytest.raises(ValueError):
        window_spec.RangeWindowBounds(start, end)


@pytest.mark.parametrize(
    ("window", "closed", "start", "end"),
    [
        pytest.param(3, "left", -3, -1, id="left"),
        pytest.param(3, "right", -2, 0, id="right"),
        pytest.param(3, "neither", -2, -1, id="neither"),
        pytest.param(3, "both", -3, 0, id="both"),
    ],
)
def test_rows_window_bounds_from_window_size(window, closed, start, end):
    actual_result = window_spec.RowsWindowBounds.from_window_size(window, closed)

    expected_result = window_spec.RowsWindowBounds(start, end)
    assert actual_result == expected_result


def test_rows_window_bounds_from_window_size_invalid_closed_raise_error():
    with pytest.raises(ValueError):
        window_spec.RowsWindowBounds.from_window_size(3, "whatever")  # type:ignore
