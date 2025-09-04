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
from typing import Callable, Mapping, TypeVar

from bigframes import dtypes
from bigframes.core import expression
import bigframes.core.identifiers as ids
import bigframes.operations.aggregations as agg_ops

TExpression = TypeVar("TExpression", bound="Aggregation")


@dataclasses.dataclass(frozen=True)
class Aggregation(expression.Expression):
    """Represents windowing or aggregation over a column."""

    op: agg_ops.WindowOp = dataclasses.field()

    @property
    def column_references(self) -> typing.Tuple[ids.ColumnId, ...]:
        return tuple(
            itertools.chain.from_iterable(
                map(lambda x: x.column_references, self.inputs)
            )
        )

    @functools.cached_property
    def is_resolved(self) -> bool:
        return all(input.is_resolved for input in self.inputs)

    @functools.cached_property
    def output_type(self) -> dtypes.ExpressionType:
        if not self.is_resolved:
            raise ValueError(f"Type of expression {self.op} has not been fixed.")

        input_types = [input.output_type for input in self.inputs]

        return self.op.output_type(*input_types)

    @property
    @abc.abstractmethod
    def inputs(
        self,
    ) -> typing.Tuple[expression.Expression, ...]:
        ...

    @property
    def free_variables(self) -> typing.Tuple[str, ...]:
        return tuple(
            itertools.chain.from_iterable(map(lambda x: x.free_variables, self.inputs))
        )

    @property
    def is_const(self) -> bool:
        return all(child.is_const for child in self.inputs)

    @abc.abstractmethod
    def replace_args(self: TExpression, *arg) -> TExpression:
        ...

    def transform_children(
        self: TExpression, t: Callable[[expression.Expression], expression.Expression]
    ) -> TExpression:
        return self.replace_args(*(t(arg) for arg in self.inputs))

    def bind_variables(
        self: TExpression,
        bindings: Mapping[str, expression.Expression],
        allow_partial_bindings: bool = False,
    ) -> TExpression:
        return self.transform_children(
            lambda x: x.bind_variables(bindings, allow_partial_bindings)
        )

    def bind_refs(
        self: TExpression,
        bindings: Mapping[ids.ColumnId, expression.Expression],
        allow_partial_bindings: bool = False,
    ) -> TExpression:
        return self.transform_children(
            lambda x: x.bind_refs(bindings, allow_partial_bindings)
        )


@dataclasses.dataclass(frozen=True)
class NullaryAggregation(Aggregation):
    op: agg_ops.NullaryWindowOp = dataclasses.field()

    @property
    def inputs(
        self,
    ) -> typing.Tuple[expression.Expression, ...]:
        return ()

    def replace_args(self, *arg) -> NullaryAggregation:
        return self


@dataclasses.dataclass(frozen=True)
class UnaryAggregation(Aggregation):
    op: agg_ops.UnaryWindowOp
    arg: expression.Expression

    @property
    def inputs(
        self,
    ) -> typing.Tuple[expression.Expression, ...]:
        return (self.arg,)

    def replace_args(self, arg: expression.Expression) -> UnaryAggregation:
        return UnaryAggregation(
            self.op,
            arg,
        )


@dataclasses.dataclass(frozen=True)
class BinaryAggregation(Aggregation):
    op: agg_ops.BinaryAggregateOp = dataclasses.field()
    left: expression.Expression = dataclasses.field()
    right: expression.Expression = dataclasses.field()

    @property
    def inputs(
        self,
    ) -> typing.Tuple[expression.Expression, ...]:
        return (self.left, self.right)

    def replace_args(
        self, larg: expression.Expression, rarg: expression.Expression
    ) -> BinaryAggregation:
        return BinaryAggregation(self.op, larg, rarg)
