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

from dataclasses import dataclass, field
from enum import Enum
import math
import typing
from typing import Mapping, Optional, Sequence, Set

import ibis.expr.datatypes as ibis_dtypes
import ibis.expr.types as ibis_types

import bigframes.core.expression as expression
import bigframes.core.identifiers as ids

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
class OrderingExpression:
    """References a column and how to order with respect to values in that column."""

    scalar_expression: expression.Expression
    direction: OrderingDirection = OrderingDirection.ASC
    na_last: bool = True

    @property
    def referenced_columns(self) -> Set[ids.ColumnId]:
        return set(self.scalar_expression.column_references)

    def remap_column_refs(
        self,
        mapping: Mapping[ids.ColumnId, ids.ColumnId],
        allow_partial_bindings: bool = False,
    ) -> OrderingExpression:
        return self.bind_refs(
            {old_id: expression.DerefOp(new_id) for old_id, new_id in mapping.items()},
            allow_partial_bindings=allow_partial_bindings,
        )

    def bind_refs(
        self,
        mapping: Mapping[ids.ColumnId, expression.Expression],
        allow_partial_bindings: bool = False,
    ) -> OrderingExpression:
        return OrderingExpression(
            self.scalar_expression.bind_refs(
                mapping, allow_partial_bindings=allow_partial_bindings
            ),
            self.direction,
            self.na_last,
        )

    def with_reverse(self) -> OrderingExpression:
        return OrderingExpression(
            self.scalar_expression, self.direction.reverse(), not self.na_last
        )


# Encoding classes specify additional properties for some ordering representations
@dataclass(frozen=True)
class StringEncoding:
    """String encoded order ids are fixed length and can be concat together in joins."""

    is_encoded: bool = False
    # Encoding size must be tracked in order to know what how to combine ordering ids across tables (eg how much to pad when combining different length).
    # Also will be needed to determine when length is too large and need to compact ordering id with a ROW_NUMBER operation.
    length: int = DEFAULT_ORDERING_ID_LENGTH


@dataclass(frozen=True)
class IntegerEncoding:
    """Integer encoded order ids are guaranteed non-negative."""

    is_encoded: bool = False
    is_sequential: bool = False


@dataclass(frozen=True)
class RowOrdering:
    """Immutable object that holds information about the ordering of rows in a ArrayValue object. May not be unambiguous."""

    ordering_value_columns: typing.Tuple[OrderingExpression, ...] = ()
    integer_encoding: IntegerEncoding = IntegerEncoding(False)
    string_encoding: StringEncoding = StringEncoding(False)

    @property
    def all_ordering_columns(self) -> Sequence[OrderingExpression]:
        return list(self.ordering_value_columns)

    @property
    def referenced_columns(self) -> Set[ids.ColumnId]:
        return set(
            col
            for part in self.ordering_value_columns
            for col in part.referenced_columns
        )

    @property
    def is_string_encoded(self) -> bool:
        """True if ordering is fully defined by a fixed length string column."""
        return self.string_encoding.is_encoded

    @property
    def is_sequential(self) -> bool:
        return self.integer_encoding.is_encoded and self.integer_encoding.is_sequential

    @property
    def is_total_ordering(self) -> bool:
        return False

    @property
    def total_order_col(self) -> Optional[OrderingExpression]:
        """Returns column id of columns that defines total ordering, if such as column exists"""
        return None

    def with_reverse(self) -> RowOrdering:
        """Reverses the ordering."""
        return RowOrdering(
            tuple([col.with_reverse() for col in self.ordering_value_columns]),
        )

    def remap_column_refs(
        self,
        mapping: typing.Mapping[ids.ColumnId, ids.ColumnId],
        allow_partial_bindings: bool = False,
    ) -> RowOrdering:
        new_value_columns = [
            col.remap_column_refs(
                mapping, allow_partial_bindings=allow_partial_bindings
            )
            for col in self.all_ordering_columns
        ]
        return RowOrdering(
            tuple(new_value_columns),
        )

    def with_non_sequential(self):
        """Create a copy that is marked as non-sequential.

        This is useful when filtering, but not sorting, an expression.
        """
        if self.integer_encoding.is_sequential:
            return RowOrdering(
                self.ordering_value_columns,
                integer_encoding=IntegerEncoding(
                    self.integer_encoding.is_encoded, is_sequential=False
                ),
            )

        return self

    def with_ordering_columns(
        self,
        ordering_value_columns: Sequence[OrderingExpression] = (),
    ) -> RowOrdering:
        """Creates a new ordering that reorders by the given columns.

        Args:
            ordering_value_columns:
                In decreasing precedence order, the values used to sort the ordering

        Returns:
            Modified ExpressionOrdering
        """

        # Truncate to remove any unneded col references after all total order cols included
        new_ordering = self._truncate_ordering(
            (*ordering_value_columns, *self.ordering_value_columns)
        )
        return RowOrdering(
            new_ordering,
        )

    def _truncate_ordering(
        self, order_refs: tuple[OrderingExpression, ...]
    ) -> tuple[OrderingExpression, ...]:
        # Truncate once we refer to a full key in bijective operations
        columns_seen: Set[ids.ColumnId] = set()
        truncated_refs = []
        for order_part in order_refs:
            expr = order_part.scalar_expression
            if not set(expr.column_references).issubset(columns_seen):
                if expr.is_bijective:
                    columns_seen.update(expr.column_references)
                truncated_refs.append(order_part)
        return tuple(truncated_refs)


@dataclass(frozen=True)
class TotalOrdering(RowOrdering):
    """Immutable object that holds information about the ordering of rows in a ArrayValue object. Guaranteed to be unambiguous."""

    # A table has a total ordering defined by the identities of a set of 1 or more columns.
    # These columns must always be part of the ordering, in order to guarantee that the ordering is total.
    # Therefore, any modifications(or drops) done to these columns must result in hidden copies being made.
    total_ordering_columns: frozenset[expression.DerefOp] = field(
        default_factory=frozenset
    )

    @classmethod
    def from_offset_col(cls, col: str) -> TotalOrdering:
        return TotalOrdering(
            (ascending_over(col),),
            integer_encoding=IntegerEncoding(True, is_sequential=True),
            total_ordering_columns=frozenset({expression.deref(col)}),
        )

    @classmethod
    def from_primary_key(cls, primary_key: Sequence[str]) -> TotalOrdering:
        return TotalOrdering(
            tuple(ascending_over(col) for col in primary_key),
            total_ordering_columns=frozenset(
                {expression.deref(col) for col in primary_key}
            ),
        )

    @property
    def is_total_ordering(self) -> bool:
        return True

    def with_non_sequential(self):
        """Create a copy that is marked as non-sequential.

        This is useful when filtering, but not sorting, an expression.
        """
        if self.integer_encoding.is_sequential:
            return TotalOrdering(
                self.ordering_value_columns,
                integer_encoding=IntegerEncoding(
                    self.integer_encoding.is_encoded, is_sequential=False
                ),
                total_ordering_columns=self.total_ordering_columns,
            )

        return self

    def with_ordering_columns(
        self,
        ordering_value_columns: Sequence[OrderingExpression] = (),
    ) -> TotalOrdering:
        """Creates a new ordering that reorders by the given columns.

        Args:
            ordering_value_columns:
                In decreasing precedence order, the values used to sort the ordering

        Returns:
            Modified ExpressionOrdering
        """

        # Truncate to remove any unneded col references after all total order cols included
        new_ordering = self._truncate_ordering(
            (*ordering_value_columns, *self.ordering_value_columns)
        )
        return TotalOrdering(
            new_ordering,
            total_ordering_columns=self.total_ordering_columns,
        )

    def _truncate_ordering(
        self, order_refs: tuple[OrderingExpression, ...]
    ) -> tuple[OrderingExpression, ...]:
        # Truncate once we refer to a full key in bijective operations
        must_see = set(ref.id for ref in self.total_ordering_columns)
        columns_seen: Set[ids.ColumnId] = set()
        truncated_refs = []
        for order_part in order_refs:
            expr = order_part.scalar_expression
            if not set(expr.column_references).issubset(columns_seen):
                if expr.is_bijective:
                    columns_seen.update(expr.column_references)
                truncated_refs.append(order_part)
                if columns_seen.issuperset(must_see):
                    return tuple(truncated_refs)
        if len(must_see) == 0:
            return ()
        raise ValueError("Ordering did not contain all total_order_cols")

    def with_reverse(self):
        """Reverses the ordering."""
        return TotalOrdering(
            tuple([col.with_reverse() for col in self.ordering_value_columns]),
            total_ordering_columns=self.total_ordering_columns,
        )

    def remap_column_refs(
        self,
        mapping: typing.Mapping[ids.ColumnId, ids.ColumnId],
        allow_partial_bindings: bool = False,
    ):
        new_value_columns = [
            col.remap_column_refs(
                mapping, allow_partial_bindings=allow_partial_bindings
            )
            for col in self.all_ordering_columns
        ]
        new_total_order = frozenset(
            expression.DerefOp(mapping.get(col_id.id, col_id.id))
            for col_id in self.total_ordering_columns
        )
        return TotalOrdering(
            tuple(new_value_columns),
            integer_encoding=self.integer_encoding,
            string_encoding=self.string_encoding,
            total_ordering_columns=new_total_order,
        )

    @property
    def total_order_col(self) -> Optional[OrderingExpression]:
        """Returns column id of columns that defines total ordering, if such as column exists"""
        if len(self.ordering_value_columns) != 1:
            return None
        order_ref = self.ordering_value_columns[0]
        if order_ref.direction != OrderingDirection.ASC:
            return None
        return order_ref


def encode_order_string(
    order_id: ibis_types.IntegerColumn, length: int = DEFAULT_ORDERING_ID_LENGTH
) -> ibis_types.StringColumn:
    """Converts an order id value to string if it is not already a string. MUST produced fixed-length strings."""
    # This is very inefficient encoding base-10 string uses only 10 characters per byte(out of 256 bit combinations)
    # Furthermore, if know tighter bounds on order id are known, can produce smaller strings.
    # 19 characters chosen as it can represent any positive Int64 in base-10
    # For missing values, ":" * 19 is used as it is larger than any other value this function produces, so null values will be last.
    string_order_id = typing.cast(
        ibis_types.StringValue,
        order_id.cast(ibis_dtypes.string),
    ).lpad(length, "0")
    return typing.cast(ibis_types.StringColumn, string_order_id)


def reencode_order_string(
    order_id: ibis_types.StringColumn, length: int
) -> ibis_types.StringColumn:
    return typing.cast(
        ibis_types.StringColumn,
        (typing.cast(ibis_types.StringValue, order_id).lpad(length, "0")),
    )


# Convenience functions
def ascending_over(id: str, nulls_last: bool = True) -> OrderingExpression:
    return OrderingExpression(expression.deref(id), na_last=nulls_last)


def descending_over(id: str, nulls_last: bool = True) -> OrderingExpression:
    return OrderingExpression(
        expression.deref(id), direction=OrderingDirection.DESC, na_last=nulls_last
    )


@typing.overload
def join_orderings(
    left: TotalOrdering,
    right: TotalOrdering,
    left_id_mapping: Mapping[ids.ColumnId, ids.ColumnId],
    right_id_mapping: Mapping[ids.ColumnId, ids.ColumnId],
    left_order_dominates: bool = True,
) -> TotalOrdering:
    ...


@typing.overload
def join_orderings(
    left: RowOrdering,
    right: RowOrdering,
    left_id_mapping: Mapping[ids.ColumnId, ids.ColumnId],
    right_id_mapping: Mapping[ids.ColumnId, ids.ColumnId],
    left_order_dominates: bool = True,
) -> RowOrdering:
    ...


def join_orderings(
    left: RowOrdering,
    right: RowOrdering,
    left_id_mapping: Mapping[ids.ColumnId, ids.ColumnId],
    right_id_mapping: Mapping[ids.ColumnId, ids.ColumnId],
    left_order_dominates: bool = True,
) -> RowOrdering:
    left_ordering_refs = [
        ref.remap_column_refs(left_id_mapping) for ref in left.all_ordering_columns
    ]
    right_ordering_refs = [
        ref.remap_column_refs(right_id_mapping) for ref in right.all_ordering_columns
    ]
    if left_order_dominates:
        joined_refs = [*left_ordering_refs, *right_ordering_refs]
    else:
        joined_refs = [*right_ordering_refs, *left_ordering_refs]

    if isinstance(left, TotalOrdering) and isinstance(right, TotalOrdering):
        left_total_order_cols = frozenset(
            [left_id_mapping[ref.id] for ref in left.total_ordering_columns]
        )
        right_total_order_cols = frozenset(
            [right_id_mapping[ref.id] for ref in right.total_ordering_columns]
        )
        return TotalOrdering(
            ordering_value_columns=tuple(joined_refs),
            total_ordering_columns=frozenset(
                map(expression.DerefOp, left_total_order_cols | right_total_order_cols)
            ),
        )
    else:
        return RowOrdering(tuple(joined_refs))
