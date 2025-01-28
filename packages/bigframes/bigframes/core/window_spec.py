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
from __future__ import annotations

from dataclasses import dataclass, replace
import itertools
from typing import Mapping, Optional, Set, Tuple, Union

import bigframes.core.expression as ex
import bigframes.core.identifiers as ids
import bigframes.core.ordering as orderings


# Unbound Windows
def unbound(
    grouping_keys: Tuple[str, ...] = (),
    min_periods: int = 0,
    ordering: Tuple[orderings.OrderingExpression, ...] = (),
) -> WindowSpec:
    """
    Create an unbound window.

    Args:
        grouping_keys:
            Columns ids of grouping keys
        min_periods (int, default 0):
            Minimum number of input rows to generate output.
        ordering:
            Orders the rows within the window.

    Returns:
        WindowSpec
    """
    return WindowSpec(
        grouping_keys=tuple(map(ex.deref, grouping_keys)),
        min_periods=min_periods,
        ordering=ordering,
    )


### Rows-based Windows
def rows(
    grouping_keys: Tuple[str, ...] = (),
    preceding: Optional[int] = None,
    following: Optional[int] = None,
    min_periods: int = 0,
    ordering: Tuple[orderings.OrderingExpression, ...] = (),
) -> WindowSpec:
    """
    Create a row-bounded window.

    Args:
        grouping_keys:
            Columns ids of grouping keys
        preceding:
            number of preceding rows to include. If None, include all preceding rows
        following:
            number of following rows to include. If None, include all following rows
        min_periods (int, default 0):
            Minimum number of input rows to generate output.
        ordering:
            Ordering to apply on top of based dataframe ordering
    Returns:
        WindowSpec
    """
    bounds = RowsWindowBounds(preceding=preceding, following=following)
    return WindowSpec(
        grouping_keys=tuple(map(ex.deref, grouping_keys)),
        bounds=bounds,
        min_periods=min_periods,
        ordering=ordering,
    )


def cumulative_rows(
    grouping_keys: Tuple[str, ...] = (), min_periods: int = 0
) -> WindowSpec:
    """
    Create a expanding window that includes all preceding rows

    Args:
        grouping_keys:
            Columns ids of grouping keys
        min_periods (int, default 0):
            Minimum number of input rows to generate output.
    Returns:
        WindowSpec
    """
    bounds = RowsWindowBounds(following=0)
    return WindowSpec(
        grouping_keys=tuple(map(ex.deref, grouping_keys)),
        bounds=bounds,
        min_periods=min_periods,
    )


def inverse_cumulative_rows(
    grouping_keys: Tuple[str, ...] = (), min_periods: int = 0
) -> WindowSpec:
    """
    Create a shrinking window that includes all following rows

    Args:
        grouping_keys:
            Columns ids of grouping keys
        min_periods (int, default 0):
            Minimum number of input rows to generate output.
    Returns:
        WindowSpec
    """
    bounds = RowsWindowBounds(preceding=0)
    return WindowSpec(
        grouping_keys=tuple(map(ex.deref, grouping_keys)),
        bounds=bounds,
        min_periods=min_periods,
    )


### Struct Classes


@dataclass(frozen=True)
class RowsWindowBounds:
    preceding: Optional[int] = None
    following: Optional[int] = None


# TODO: Expand to datetime offsets
OffsetType = Union[float, int]


@dataclass(frozen=True)
class RangeWindowBounds:
    preceding: Optional[OffsetType] = None
    following: Optional[OffsetType] = None


@dataclass(frozen=True)
class WindowSpec:
    """
    Specifies a window over which aggregate and analytic function may be applied.
    grouping_keys: set of column ids to group on
    preceding: Number of preceding rows in the window
    following: Number of preceding rows in the window
    ordering: List of columns ids and ordering direction to override base ordering
    """

    grouping_keys: Tuple[ex.DerefOp, ...] = tuple()
    ordering: Tuple[orderings.OrderingExpression, ...] = tuple()
    bounds: Union[RowsWindowBounds, RangeWindowBounds, None] = None
    min_periods: int = 0

    @property
    def row_bounded(self):
        """
        Whether the window is bounded by row offsets.

        This is relevant for determining whether the window requires a total order
        to calculate deterministically.
        """
        return isinstance(self.bounds, RowsWindowBounds)

    @property
    def all_referenced_columns(self) -> Set[ids.ColumnId]:
        """
        Return list of all variables reference ind the window.
        """
        ordering_vars = itertools.chain.from_iterable(
            item.scalar_expression.column_references for item in self.ordering
        )
        return set(itertools.chain((i.id for i in self.grouping_keys), ordering_vars))

    def without_order(self) -> WindowSpec:
        """Removes ordering clause if ordering isn't required to define bounds."""
        if self.row_bounded:
            raise ValueError("Cannot remove order from row-bounded window")
        return replace(self, ordering=())

    def remap_column_refs(
        self,
        mapping: Mapping[ids.ColumnId, ids.ColumnId],
        allow_partial_bindings: bool = False,
    ) -> WindowSpec:
        return WindowSpec(
            grouping_keys=tuple(
                key.remap_column_refs(mapping, allow_partial_bindings)
                for key in self.grouping_keys
            ),
            ordering=tuple(
                order_part.remap_column_refs(mapping, allow_partial_bindings)
                for order_part in self.ordering
            ),
            bounds=self.bounds,
            min_periods=self.min_periods,
        )
