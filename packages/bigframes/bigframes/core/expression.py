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
import itertools
import typing
from typing import Mapping, Union

import bigframes.dtypes as dtypes
import bigframes.operations
import bigframes.operations.aggregations as agg_ops


def const(value: typing.Hashable, dtype: dtypes.ExpressionType = None) -> Expression:
    return ScalarConstantExpression(value, dtype or dtypes.infer_literal_type(value))


def free_var(id: str) -> UnboundVariableExpression:
    return UnboundVariableExpression(id)


@dataclasses.dataclass(frozen=True)
class Aggregation(abc.ABC):
    """Represents windowing or aggregation over a column."""

    op: agg_ops.WindowOp = dataclasses.field()

    @abc.abstractmethod
    def output_type(
        self, input_types: dict[str, dtypes.ExpressionType]
    ) -> dtypes.ExpressionType:
        ...


@dataclasses.dataclass(frozen=True)
class UnaryAggregation(Aggregation):
    op: agg_ops.UnaryWindowOp = dataclasses.field()
    arg: Union[
        UnboundVariableExpression, ScalarConstantExpression
    ] = dataclasses.field()

    def output_type(
        self, input_types: dict[str, bigframes.dtypes.Dtype]
    ) -> dtypes.ExpressionType:
        return self.op.output_type(self.arg.output_type(input_types))


@dataclasses.dataclass(frozen=True)
class BinaryAggregation(Aggregation):
    op: agg_ops.BinaryAggregateOp = dataclasses.field()
    left: Union[
        UnboundVariableExpression, ScalarConstantExpression
    ] = dataclasses.field()
    right: Union[
        UnboundVariableExpression, ScalarConstantExpression
    ] = dataclasses.field()

    def output_type(
        self, input_types: dict[str, bigframes.dtypes.Dtype]
    ) -> dtypes.ExpressionType:
        return self.op.output_type(
            self.left.output_type(input_types), self.right.output_type(input_types)
        )


@dataclasses.dataclass(frozen=True)
class Expression(abc.ABC):
    """An expression represents a computation taking N scalar inputs and producing a single output scalar."""

    @property
    def unbound_variables(self) -> typing.Tuple[str, ...]:
        return ()

    def rename(self, name_mapping: Mapping[str, str]) -> Expression:
        return self

    @property
    @abc.abstractmethod
    def is_const(self) -> bool:
        ...

    @abc.abstractmethod
    def output_type(
        self, input_types: dict[str, dtypes.ExpressionType]
    ) -> dtypes.ExpressionType:
        ...

    @abc.abstractmethod
    def bind_all_variables(self, bindings: Mapping[str, Expression]) -> Expression:
        """Replace all variables with expression given in `bindings`."""
        ...

    @property
    def is_bijective(self) -> bool:
        return False

    @property
    def is_identity(self) -> bool:
        """True for identity operation that does not transform input."""
        return False


@dataclasses.dataclass(frozen=True)
class ScalarConstantExpression(Expression):
    """An expression representing a scalar constant."""

    # TODO: Further constrain?
    value: typing.Hashable
    dtype: dtypes.ExpressionType = None

    @property
    def is_const(self) -> bool:
        return True

    def output_type(
        self, input_types: dict[str, bigframes.dtypes.Dtype]
    ) -> dtypes.ExpressionType:
        return self.dtype

    def bind_all_variables(self, bindings: Mapping[str, Expression]) -> Expression:
        return self

    @property
    def is_bijective(self) -> bool:
        # () <-> value
        return True


@dataclasses.dataclass(frozen=True)
class UnboundVariableExpression(Expression):
    """A variable expression representing an unbound variable."""

    id: str

    @property
    def unbound_variables(self) -> typing.Tuple[str, ...]:
        return (self.id,)

    def rename(self, name_mapping: Mapping[str, str]) -> Expression:
        if self.id in name_mapping:
            return UnboundVariableExpression(name_mapping[self.id])
        else:
            return self

    @property
    def is_const(self) -> bool:
        return False

    def output_type(
        self, input_types: dict[str, bigframes.dtypes.Dtype]
    ) -> dtypes.ExpressionType:
        if self.id in input_types:
            return input_types[self.id]
        else:
            raise ValueError(f"Type of variable {self.id} has not been fixed.")

    def bind_all_variables(self, bindings: Mapping[str, Expression]) -> Expression:
        if self.id in bindings.keys():
            return bindings[self.id]
        else:
            raise ValueError(f"Variable {self.id} remains unbound")

    @property
    def is_bijective(self) -> bool:
        return True

    @property
    def is_identity(self) -> bool:
        return True


@dataclasses.dataclass(frozen=True)
class OpExpression(Expression):
    """An expression representing a scalar operation applied to 1 or more argument sub-expressions."""

    op: bigframes.operations.RowOp
    inputs: typing.Tuple[Expression, ...]

    def __post_init__(self):
        assert self.op.arguments == len(self.inputs)

    @property
    def unbound_variables(self) -> typing.Tuple[str, ...]:
        return tuple(
            itertools.chain.from_iterable(
                map(lambda x: x.unbound_variables, self.inputs)
            )
        )

    def rename(self, name_mapping: Mapping[str, str]) -> Expression:
        return OpExpression(
            self.op, tuple(input.rename(name_mapping) for input in self.inputs)
        )

    @property
    def is_const(self) -> bool:
        return all(child.is_const for child in self.inputs)

    def output_type(
        self, input_types: dict[str, dtypes.ExpressionType]
    ) -> dtypes.ExpressionType:
        operand_types = tuple(
            map(lambda x: x.output_type(input_types=input_types), self.inputs)
        )
        return self.op.output_type(*operand_types)

    def bind_all_variables(self, bindings: Mapping[str, Expression]) -> Expression:
        return OpExpression(
            self.op,
            tuple(input.bind_all_variables(bindings) for input in self.inputs),
        )

    @property
    def is_bijective(self) -> bool:
        # TODO: Mark individual functions as bijective?
        return False
