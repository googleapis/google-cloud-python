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

import bigframes.operations


@dataclasses.dataclass(frozen=True)
class Expression(abc.ABC):
    """An expression represents a computation taking N scalar inputs and producing a single output scalar."""

    @property
    def unbound_variables(self) -> typing.Tuple[str, ...]:
        return ()


@dataclasses.dataclass(frozen=True)
class ScalarConstantExpression(Expression):
    """An expression representing a scalar constant."""

    # TODO: Further constrain?
    value: typing.Hashable


@dataclasses.dataclass(frozen=True)
class UnboundVariableExpression(Expression):
    """A variable expression representing an unbound variable."""

    id: str

    @property
    def unbound_variables(self) -> typing.Tuple[str, ...]:
        return (self.id,)


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
