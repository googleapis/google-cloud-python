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

import abc
import dataclasses
import functools
import itertools
import typing
from typing import Callable, Generator, Mapping, TypeVar, Union

import pandas as pd

from bigframes import dtypes
from bigframes.core import field
import bigframes.core.identifiers as ids
import bigframes.operations
import bigframes.operations.aggregations as agg_ops


def const(
    value: typing.Hashable, dtype: dtypes.ExpressionType = None
) -> ScalarConstantExpression:
    return ScalarConstantExpression(value, dtype or dtypes.infer_literal_type(value))


def deref(name: str) -> DerefOp:
    return DerefOp(ids.ColumnId(name))


def free_var(id: str) -> UnboundVariableExpression:
    return UnboundVariableExpression(id)


@dataclasses.dataclass(frozen=True)
class Aggregation(abc.ABC):
    """Represents windowing or aggregation over a column."""

    op: agg_ops.WindowOp = dataclasses.field()

    @abc.abstractmethod
    def output_type(
        self, input_fields: Mapping[ids.ColumnId, field.Field]
    ) -> dtypes.ExpressionType:
        ...

    @property
    def column_references(self) -> typing.Tuple[ids.ColumnId, ...]:
        return ()

    @abc.abstractmethod
    def remap_column_refs(
        self,
        name_mapping: Mapping[ids.ColumnId, ids.ColumnId],
        allow_partial_bindings: bool = False,
    ) -> Aggregation:
        ...


@dataclasses.dataclass(frozen=True)
class NullaryAggregation(Aggregation):
    op: agg_ops.NullaryWindowOp = dataclasses.field()

    def output_type(
        self, input_fields: Mapping[ids.ColumnId, field.Field]
    ) -> dtypes.ExpressionType:
        return self.op.output_type()

    def remap_column_refs(
        self,
        name_mapping: Mapping[ids.ColumnId, ids.ColumnId],
        allow_partial_bindings: bool = False,
    ) -> NullaryAggregation:
        return self


@dataclasses.dataclass(frozen=True)
class UnaryAggregation(Aggregation):
    op: agg_ops.UnaryWindowOp
    arg: Union[DerefOp, ScalarConstantExpression]

    def output_type(
        self, input_fields: Mapping[ids.ColumnId, field.Field]
    ) -> dtypes.ExpressionType:
        # TODO(b/419300717) Remove resolutions once defers are cleaned up.
        resolved_expr = bind_schema_fields(self.arg, input_fields)
        assert resolved_expr.is_resolved

        return self.op.output_type(resolved_expr.output_type)

    @property
    def column_references(self) -> typing.Tuple[ids.ColumnId, ...]:
        return self.arg.column_references

    def remap_column_refs(
        self,
        name_mapping: Mapping[ids.ColumnId, ids.ColumnId],
        allow_partial_bindings: bool = False,
    ) -> UnaryAggregation:
        return UnaryAggregation(
            self.op,
            self.arg.remap_column_refs(
                name_mapping, allow_partial_bindings=allow_partial_bindings
            ),
        )


@dataclasses.dataclass(frozen=True)
class BinaryAggregation(Aggregation):
    op: agg_ops.BinaryAggregateOp = dataclasses.field()
    left: Union[DerefOp, ScalarConstantExpression] = dataclasses.field()
    right: Union[DerefOp, ScalarConstantExpression] = dataclasses.field()

    def output_type(
        self, input_fields: Mapping[ids.ColumnId, field.Field]
    ) -> dtypes.ExpressionType:
        # TODO(b/419300717) Remove resolutions once defers are cleaned up.
        left_resolved_expr = bind_schema_fields(self.left, input_fields)
        assert left_resolved_expr.is_resolved
        right_resolved_expr = bind_schema_fields(self.right, input_fields)
        assert right_resolved_expr.is_resolved

        return self.op.output_type(
            left_resolved_expr.output_type, left_resolved_expr.output_type
        )

    @property
    def column_references(self) -> typing.Tuple[ids.ColumnId, ...]:
        return (*self.left.column_references, *self.right.column_references)

    def remap_column_refs(
        self,
        name_mapping: Mapping[ids.ColumnId, ids.ColumnId],
        allow_partial_bindings: bool = False,
    ) -> BinaryAggregation:
        return BinaryAggregation(
            self.op,
            self.left.remap_column_refs(
                name_mapping, allow_partial_bindings=allow_partial_bindings
            ),
            self.right.remap_column_refs(
                name_mapping, allow_partial_bindings=allow_partial_bindings
            ),
        )


TExpression = TypeVar("TExpression", bound="Expression")


@dataclasses.dataclass(frozen=True)
class Expression(abc.ABC):
    """An expression represents a computation taking N scalar inputs and producing a single output scalar."""

    @property
    def free_variables(self) -> typing.Tuple[str, ...]:
        return ()

    @property
    def children(self) -> typing.Tuple[Expression, ...]:
        return ()

    @property
    def expensive(self) -> bool:
        return any(
            isinstance(ex, OpExpression) and ex.op.expensive for ex in self.walk()
        )

    @property
    def nullable(self) -> bool:
        return True

    @property
    @abc.abstractmethod
    def column_references(self) -> typing.Tuple[ids.ColumnId, ...]:
        ...

    def remap_column_refs(
        self: TExpression,
        name_mapping: Mapping[ids.ColumnId, ids.ColumnId],
        allow_partial_bindings: bool = False,
    ) -> TExpression:
        return self.bind_refs(
            {old_id: DerefOp(new_id) for old_id, new_id in name_mapping.items()},  # type: ignore
            allow_partial_bindings=allow_partial_bindings,
        )

    @property
    @abc.abstractmethod
    def is_const(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def is_resolved(self) -> bool:
        """
        Returns true if and only if the expression's output type and nullability is available.
        """
        ...

    @property
    @abc.abstractmethod
    def output_type(self) -> dtypes.ExpressionType:
        ...

    @abc.abstractmethod
    def bind_refs(
        self,
        bindings: Mapping[ids.ColumnId, Expression],
        allow_partial_bindings: bool = False,
    ) -> Expression:
        """Replace variables with expression given in `bindings`.

        If allow_partial_bindings is False, validate that all free variables are bound to a new value.
        """
        ...

    @abc.abstractmethod
    def bind_variables(
        self, bindings: Mapping[str, Expression], allow_partial_bindings: bool = False
    ) -> Expression:
        """Replace variables with expression given in `bindings`.

        If allow_partial_bindings is False, validate that all free variables are bound to a new value.
        """
        ...

    @property
    def is_bijective(self) -> bool:
        return False

    @property
    def deterministic(self) -> bool:
        return True

    @property
    def is_identity(self) -> bool:
        """True for identity operation that does not transform input."""
        return False

    @abc.abstractmethod
    def transform_children(self, t: Callable[[Expression], Expression]) -> Expression:
        ...

    def walk(self) -> Generator[Expression, None, None]:
        yield self
        for child in self.children:
            yield from child.children


@dataclasses.dataclass(frozen=True)
class ScalarConstantExpression(Expression):
    """An expression representing a scalar constant."""

    # TODO: Further constrain?
    value: typing.Hashable
    dtype: dtypes.ExpressionType = None

    @property
    def is_const(self) -> bool:
        return True

    @property
    def column_references(self) -> typing.Tuple[ids.ColumnId, ...]:
        return ()

    @property
    def nullable(self) -> bool:
        return pd.isna(self.value)  # type: ignore

    @property
    def is_resolved(self) -> bool:
        return True

    @property
    def output_type(self) -> dtypes.ExpressionType:
        return self.dtype

    def bind_variables(
        self, bindings: Mapping[str, Expression], allow_partial_bindings: bool = False
    ) -> Expression:
        return self

    def bind_refs(
        self,
        bindings: Mapping[ids.ColumnId, Expression],
        allow_partial_bindings: bool = False,
    ) -> ScalarConstantExpression:
        return self

    @property
    def is_bijective(self) -> bool:
        # () <-> value
        return True

    def __eq__(self, other):
        if not isinstance(other, ScalarConstantExpression):
            return False

        # With python 3.13 and the pre-release version of pandas,
        # NA == NA is NA instead of True
        if pd.isna(self.value) and pd.isna(other.value):  # type: ignore
            return self.dtype == other.dtype

        return self.value == other.value and self.dtype == other.dtype

    def transform_children(self, t: Callable[[Expression], Expression]) -> Expression:
        return self


@dataclasses.dataclass(frozen=True)
class UnboundVariableExpression(Expression):
    """A variable expression representing an unbound variable."""

    id: str

    @property
    def free_variables(self) -> typing.Tuple[str, ...]:
        return (self.id,)

    @property
    def is_const(self) -> bool:
        return False

    @property
    def column_references(self) -> typing.Tuple[ids.ColumnId, ...]:
        return ()

    @property
    def is_resolved(self):
        return False

    @property
    def output_type(self) -> dtypes.ExpressionType:
        raise ValueError(f"Type of variable {self.id} has not been fixed.")

    def bind_refs(
        self,
        bindings: Mapping[ids.ColumnId, Expression],
        allow_partial_bindings: bool = False,
    ) -> UnboundVariableExpression:
        return self

    def bind_variables(
        self, bindings: Mapping[str, Expression], allow_partial_bindings: bool = False
    ) -> Expression:
        if self.id in bindings.keys():
            return bindings[self.id]
        elif not allow_partial_bindings:
            raise ValueError(f"Variable {self.id} remains unbound")
        return self

    @property
    def is_bijective(self) -> bool:
        return True

    @property
    def is_identity(self) -> bool:
        return True

    def transform_children(self, t: Callable[[Expression], Expression]) -> Expression:
        return self


@dataclasses.dataclass(frozen=True)
class DerefOp(Expression):
    """An expression that refers to a column by ID."""

    id: ids.ColumnId

    @property
    def column_references(self) -> typing.Tuple[ids.ColumnId, ...]:
        return (self.id,)

    @property
    def is_const(self) -> bool:
        return False

    @property
    def nullable(self) -> bool:
        # Safe default, need to actually bind input schema to determine
        return True

    @property
    def is_resolved(self) -> bool:
        return False

    @property
    def output_type(self) -> dtypes.ExpressionType:
        raise ValueError(f"Type of variable {self.id} has not been fixed.")

    def bind_variables(
        self, bindings: Mapping[str, Expression], allow_partial_bindings: bool = False
    ) -> Expression:
        return self

    def bind_refs(
        self,
        bindings: Mapping[ids.ColumnId, Expression],
        allow_partial_bindings: bool = False,
    ) -> Expression:
        if self.id in bindings.keys():
            return bindings[self.id]
        elif not allow_partial_bindings:
            raise ValueError(f"Variable {self.id} remains unbound")
        return self

    @property
    def is_bijective(self) -> bool:
        return True

    @property
    def is_identity(self) -> bool:
        return True

    def transform_children(self, t: Callable[[Expression], Expression]) -> Expression:
        return self


@dataclasses.dataclass(frozen=True)
class ResolvedDerefOp(DerefOp):
    """An expression that refers to a column by ID and resolved with schema bound."""

    dtype: dtypes.Dtype
    is_nullable: bool

    @classmethod
    def from_field(cls, f: field.Field):
        return cls(id=f.id, dtype=f.dtype, is_nullable=f.nullable)

    @property
    def is_resolved(self) -> bool:
        return True

    @property
    def nullable(self) -> bool:
        return self.is_nullable

    @property
    def output_type(self) -> dtypes.ExpressionType:
        return self.dtype


@dataclasses.dataclass(frozen=True)
class OpExpression(Expression):
    """An expression representing a scalar operation applied to 1 or more argument sub-expressions."""

    op: bigframes.operations.ScalarOp
    inputs: typing.Tuple[Expression, ...]

    @property
    def column_references(
        self,
    ) -> typing.Tuple[bigframes.core.identifiers.ColumnId, ...]:
        return tuple(
            itertools.chain.from_iterable(
                map(lambda x: x.column_references, self.inputs)
            )
        )

    @property
    def free_variables(self) -> typing.Tuple[str, ...]:
        return tuple(
            itertools.chain.from_iterable(map(lambda x: x.free_variables, self.inputs))
        )

    @property
    def is_const(self) -> bool:
        return all(child.is_const for child in self.inputs)

    @property
    def children(self):
        return self.inputs

    @property
    def nullable(self) -> bool:
        # This is very conservative, need to label null properties of individual ops to get more precise
        null_free = self.is_identity and not any(
            child.nullable for child in self.inputs
        )
        return not null_free

    @functools.cached_property
    def is_resolved(self) -> bool:
        return all(input.is_resolved for input in self.inputs)

    @functools.cached_property
    def output_type(self) -> dtypes.ExpressionType:
        if not self.is_resolved:
            raise ValueError(f"Type of expression {self.op.name} has not been fixed.")

        input_types = [input.output_type for input in self.inputs]

        return self.op.output_type(*input_types)

    def bind_variables(
        self, bindings: Mapping[str, Expression], allow_partial_bindings: bool = False
    ) -> OpExpression:
        return OpExpression(
            self.op,
            tuple(
                input.bind_variables(
                    bindings, allow_partial_bindings=allow_partial_bindings
                )
                for input in self.inputs
            ),
        )

    def bind_refs(
        self,
        bindings: Mapping[ids.ColumnId, Expression],
        allow_partial_bindings: bool = False,
    ) -> OpExpression:
        return OpExpression(
            self.op,
            tuple(
                input.bind_refs(bindings, allow_partial_bindings=allow_partial_bindings)
                for input in self.inputs
            ),
        )

    @property
    def is_bijective(self) -> bool:
        # TODO: Mark individual functions as bijective?
        return all(input.is_bijective for input in self.inputs) and self.op.is_bijective

    @property
    def deterministic(self) -> bool:
        return (
            all(input.deterministic for input in self.inputs) and self.op.deterministic
        )

    def transform_children(self, t: Callable[[Expression], Expression]) -> Expression:
        new_inputs = tuple(t(input) for input in self.inputs)
        if new_inputs != self.inputs:
            return dataclasses.replace(self, inputs=new_inputs)
        return self


def bind_schema_fields(
    expr: Expression, field_by_id: Mapping[ids.ColumnId, field.Field]
) -> Expression:
    """
    Updates `DerefOp` expressions by replacing column IDs with actual schema fields(columns).

    We can only deduct an expression's output type and nullability after binding schema fields to
    all its deref expressions.
    """
    if expr.is_resolved:
        return expr

    expr_by_id = {
        id: ResolvedDerefOp.from_field(field) for id, field in field_by_id.items()
    }
    return expr.bind_refs(expr_by_id)


RefOrConstant = Union[DerefOp, ScalarConstantExpression]
