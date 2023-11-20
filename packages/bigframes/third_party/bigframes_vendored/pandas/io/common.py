# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/io/common.py
"""Common IO api utilities"""
from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Hashable, Sequence


def dedup_names(
    names: Sequence[Hashable],
    is_potential_multiindex: bool,
) -> Sequence[Hashable]:
    """
    Rename column names if duplicates exist.

    Currently the renaming is done by appending a underscore and an
    autonumeric, but a custom pattern may be supported in the future.

    Examples
    ```
    dedup_names(["x", "y", "x", "x"], is_potential_multiindex=False)
    ['x', 'y', 'x_1', 'x_2']
    ```
    """
    names = list(names)  # so we can index
    counts: DefaultDict[Hashable, int] = defaultdict(int)

    for i, col in enumerate(names):
        cur_count = counts[col]

        while cur_count > 0:
            counts[col] = cur_count + 1

            if is_potential_multiindex:
                # for mypy
                assert isinstance(col, tuple)
                col = col[:-1] + (f"{col[-1]}_{cur_count}",)
            else:
                col = f"{col}_{cur_count}"
            cur_count = counts[col]

        names[i] = col
        counts[col] = cur_count + 1

    return names
