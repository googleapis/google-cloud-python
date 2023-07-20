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

from dataclasses import dataclass
from enum import Enum
import math
import typing
from typing import Optional, Sequence

import ibis.expr.datatypes as ibis_dtypes
import ibis.expr.types as ibis_types

# TODO(tbergeron): Encode more efficiently
ORDERING_ID_STRING_BASE: int = 10
# Sufficient to store any value up to 2^63
DEFAULT_ORDERING_ID_LENGTH: int = math.ceil(63 * math.log(2, ORDERING_ID_STRING_BASE))


class OrderingDirection(Enum):
    ASC = 1
    DESC = 2

    def reverse(self):
        if self == OrderingDirection.ASC:
            return OrderingDirection.DESC
        else:
            return OrderingDirection.ASC

    @property
    def is_ascending(self) -> bool:
        return self == OrderingDirection.ASC


@dataclass(frozen=True)
class OrderingColumnReference:
    """References a column and how to order with respect to values in that column."""

    column_id: str
    direction: OrderingDirection = OrderingDirection.ASC
    na_last: bool = True

    def with_name(self, name: str):
        return OrderingColumnReference(name, self.direction, self.na_last)

    def with_reverse(self):
        return OrderingColumnReference(
            self.column_id, self.direction.reverse(), not self.na_last
        )


@dataclass(frozen=True)
class ExpressionOrdering:
    """Immutable object that holds information about the ordering of rows in a ArrayValue object."""

    ordering_value_columns: Sequence[OrderingColumnReference] = ()
    ordering_id_column: Optional[OrderingColumnReference] = None
    is_sequential: bool = False
    # Encoding size must be tracked in order to know what how to combine ordering ids across tables (eg how much to pad when combining different length).
    # Also will be needed to determine when length is too large and need to compact ordering id with a ROW_NUMBER operation.
    ordering_encoding_size: int = DEFAULT_ORDERING_ID_LENGTH

    def with_is_sequential(self, is_sequential: bool):
        """Create a copy that is marked as non-sequential.

        This is useful when filtering, but not sorting, an expression.
        """
        return ExpressionOrdering(
            self.ordering_value_columns,
            self.ordering_id_column,
            is_sequential,
            ordering_encoding_size=self.ordering_encoding_size,
        )

    def with_ordering_columns(
        self,
        ordering_value_columns: Sequence[OrderingColumnReference] = (),
        stable: bool = False,
    ):
        """Creates a new ordering that preserves ordering id, but replaces ordering value column list."""
        if stable:
            col_ids_new = [
                ordering_ref.column_id for ordering_ref in ordering_value_columns
            ]
            # Only reference each column once, so discard old referenc if there is a new reference
            old_ordering_keep = [
                ordering_ref
                for ordering_ref in self.ordering_value_columns
                if ordering_ref.column_id not in col_ids_new
            ]
            new_ordering = (*ordering_value_columns, *old_ordering_keep)
        else:  # Not stable, so discard old ordering completely
            new_ordering = tuple(ordering_value_columns)
        return ExpressionOrdering(
            new_ordering,
            self.ordering_id_column,
            is_sequential=False,
            ordering_encoding_size=self.ordering_encoding_size,
        )

    def with_ordering_id(self, ordering_id: str):
        """Creates a new ordering that preserves other properties, but with a different ordering id.

        Useful when reprojecting ordering for implicit joins.
        """
        return ExpressionOrdering(
            self.ordering_value_columns,
            OrderingColumnReference(ordering_id),
            is_sequential=self.is_sequential,
            ordering_encoding_size=self.ordering_encoding_size,
        )

    def with_reverse(self):
        """Reverses the ordering."""
        return ExpressionOrdering(
            tuple([col.with_reverse() for col in self.ordering_value_columns]),
            self.ordering_id_column.with_reverse()
            if self.ordering_id_column is not None
            else None,
            is_sequential=False,
            ordering_encoding_size=self.ordering_encoding_size,
        )

    @property
    def ordering_id(self) -> Optional[str]:
        return self.ordering_id_column.column_id if self.ordering_id_column else None

    @property
    def order_id_defined(self) -> bool:
        """True if ordering is fully defined in ascending order by its ordering id."""
        return bool(
            self.ordering_id_column
            and (not self.ordering_value_columns)
            and self.ordering_id_column.direction == OrderingDirection.ASC
        )

    @property
    def all_ordering_columns(self) -> Sequence[OrderingColumnReference]:
        return (
            list(self.ordering_value_columns)
            if self.ordering_id_column is None
            else [*self.ordering_value_columns, self.ordering_id_column]
        )


def stringify_order_id(
    order_id: ibis_types.Value, length: int = DEFAULT_ORDERING_ID_LENGTH
) -> ibis_types.StringValue:
    """Converts an order id value to string if it is not already a string. MUST produced fixed-length strings."""
    if order_id.type().is_int64():
        # This is very inefficient encoding base-10 string uses only 10 characters per byte(out of 256 bit combinations)
        # Furthermore, if know tighter bounds on order id are known, can produce smaller strings.
        # 19 characters chosen as it can represent any positive Int64 in base-10
        # For missing values, ":" * 19 is used as it is larger than any other value this function produces, so null values will be last.
        string_order_id = (
            typing.cast(
                ibis_types.StringValue,
                typing.cast(ibis_types.IntegerValue, order_id).cast(ibis_dtypes.string),
            )
            .lpad(length, "0")
            .fillna(ibis_types.literal(":" * length))
        )
    else:
        string_order_id = (
            typing.cast(ibis_types.StringValue, order_id)
            .lpad(length, "0")
            .fillna(ibis_types.literal(":" * length))
        )
    return typing.cast(ibis_types.StringValue, string_order_id)
