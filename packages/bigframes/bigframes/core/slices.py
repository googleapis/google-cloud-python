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

from __future__ import annotations

from typing import Optional


def to_forward_offsets(
    slice: tuple[Optional[int], Optional[int], Optional[int]], input_rows: int
) -> tuple[int, Optional[int], int]:
    """Redefine the slice to use forward offsets for start and stop indices."""
    step = slice[2] or 1
    stop = slice[1]
    start = slice[0]

    # normalize start to positive number
    if start is None:
        start = 0 if (step > 0) else (input_rows - 1)
    elif start < 0:
        start = max(0, input_rows + start)
    else:  # start >= 0
        # Clip start to either beginning or end depending on step direction
        start = min(start, input_rows - 1) if step < 0 else start

    if stop is None:
        stop = None
    elif stop < 0:
        if step > 0:
            stop = max(0, input_rows + stop)
        else:
            stop = input_rows + stop if (input_rows + stop >= 0) else None
    else:
        stop = min(stop, input_rows)

    return (start, stop, step)


def remove_unused_parts(
    slice: tuple[Optional[int], Optional[int], Optional[int]], input_rows: int
) -> tuple[Optional[int], Optional[int], Optional[int]]:
    """Makes a slice component null if it doesn't impact slice semantics."""
    start, stop, step = slice
    is_forward = (step is None) or (step > 0)
    if start is not None:
        if is_forward and ((start == 0) or (start <= -input_rows)):
            start = None
        elif (not is_forward) and ((start == -1) or (start >= (input_rows - 1))):
            start = None
    if stop is not None:
        if is_forward and (stop >= input_rows):
            stop = None
        elif (not is_forward) and (stop <= (-input_rows - 1)):
            stop = None
    if step == 1:
        step = None
    return start, stop, step


def slice_output_rows(
    slice: tuple[Optional[int], Optional[int], Optional[int]], input_size: int
) -> int:
    """Given input_size, returns the number of rows returned after the slice operation."""
    slice = to_forward_offsets(slice, input_size)
    start, stop, step = slice

    if step > 0:
        if stop is None:
            stop = input_size
        length = max(0, (stop - start + step - 1) // step)
    else:
        if stop is None:
            stop = -1
        length = max(0, (start - stop - step - 1) // -step)
    return length


def is_noop(
    slice_def: tuple[Optional[int], Optional[int], Optional[int]],
    input_size: Optional[int],
) -> bool:
    """Returns true iff the slice op is a no-op returning the input array."""
    if input_size:
        start, stop, step = remove_unused_parts(slice_def, input_size)
    else:
        start, stop, step = slice_def
    return (not start) and (stop is None) and ((step is None) or (step == 1))


def is_reverse(
    slice_def: tuple[Optional[int], Optional[int], Optional[int]],
    input_size: Optional[int],
) -> bool:
    """Returns true iff the slice op is a pure reverse op, equivalent to df[::-1]"""
    if input_size:
        start, stop, step = remove_unused_parts(slice_def, input_size)
    else:
        start, stop, step = slice_def
    return (start is None) and (stop is None) and (step == -1)
