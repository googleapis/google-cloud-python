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

from __future__ import annotations

import dataclasses
import typing

from bigframes import dtypes
import bigframes.operations.type as op_typing

if typing.TYPE_CHECKING:
    # Avoids circular dependency
    import bigframes.core.expression


class RowOp(typing.Protocol):
    @property
    def name(self) -> str:
        ...

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        ...

    @property
    def is_monotonic(self) -> bool:
        """Whether the row operation preserves total ordering. Can be pruned from ordering expressions."""
        ...

    @property
    def is_bijective(self) -> bool:
        """Whether the operation has a 1:1 mapping between inputs and outputs"""
        ...

    @property
    def deterministic(self) -> bool:
        """Whether the operation is deterministic" (given deterministic inputs)"""
        ...

    @property
    def expensive(self) -> bool:
        """Whether the operation is expensive to calculate. Such ops shouldn't be inlined if referenced multiple places."""
        ...


@dataclasses.dataclass(frozen=True)
class ScalarOp:
    @property
    def name(self) -> str:
        raise NotImplementedError("RowOp abstract base class has no implementation")

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        raise NotImplementedError("Abstract operation has no output type")

    @property
    def is_monotonic(self) -> bool:
        """Whether the row operation preserves total ordering. Can be pruned from ordering expressions."""
        return False

    @property
    def is_bijective(self) -> bool:
        """Whether the operation has a 1:1 mapping between inputs and outputs"""
        return False

    @property
    def deterministic(self) -> bool:
        """Whether the operation is deterministic" (given deterministic inputs)"""
        return True

    @property
    def expensive(self) -> bool:
        return False


@dataclasses.dataclass(frozen=True)
class NaryOp(ScalarOp):
    def as_expr(
        self,
        *exprs: typing.Union[str, bigframes.core.expression.Expression],
    ) -> bigframes.core.expression.Expression:
        import bigframes.core.expression

        # Keep this in sync with output_type and compilers
        inputs: list[bigframes.core.expression.Expression] = []

        for expr in exprs:
            inputs.append(_convert_expr_input(expr))

        return bigframes.core.expression.OpExpression(
            self,
            tuple(inputs),
        )


# These classes can be used to create simple ops that don't take local parameters
# All is needed is a unique name, and to register an implementation in ibis_mappings.py
@dataclasses.dataclass(frozen=True)
class UnaryOp(ScalarOp):
    @property
    def arguments(self) -> int:
        return 1

    def as_expr(
        self, input_id: typing.Union[str, bigframes.core.expression.Expression] = "arg"
    ) -> bigframes.core.expression.Expression:
        import bigframes.core.expression

        return bigframes.core.expression.OpExpression(
            self, (_convert_expr_input(input_id),)
        )


@dataclasses.dataclass(frozen=True)
class BinaryOp(ScalarOp):
    @property
    def arguments(self) -> int:
        return 2

    def as_expr(
        self,
        left_input: typing.Union[str, bigframes.core.expression.Expression] = "arg1",
        right_input: typing.Union[str, bigframes.core.expression.Expression] = "arg2",
    ) -> bigframes.core.expression.Expression:
        import bigframes.core.expression

        return bigframes.core.expression.OpExpression(
            self,
            (
                _convert_expr_input(left_input),
                _convert_expr_input(right_input),
            ),
        )


@dataclasses.dataclass(frozen=True)
class TernaryOp(ScalarOp):
    @property
    def arguments(self) -> int:
        return 3

    def as_expr(
        self,
        input1: typing.Union[str, bigframes.core.expression.Expression] = "arg1",
        input2: typing.Union[str, bigframes.core.expression.Expression] = "arg2",
        input3: typing.Union[str, bigframes.core.expression.Expression] = "arg3",
    ) -> bigframes.core.expression.Expression:
        import bigframes.core.expression

        return bigframes.core.expression.OpExpression(
            self,
            (
                _convert_expr_input(input1),
                _convert_expr_input(input2),
                _convert_expr_input(input3),
            ),
        )


def _convert_expr_input(
    input: typing.Union[str, bigframes.core.expression.Expression]
) -> bigframes.core.expression.Expression:
    """Allows creating column references with just a string"""
    import bigframes.core.expression

    if isinstance(input, str):
        return bigframes.core.expression.deref(input)
    else:
        return input


# Operation Factories
def create_unary_op(
    name: str, type_signature: op_typing.UnaryTypeSignature
) -> type[UnaryOp]:
    return dataclasses.make_dataclass(
        name,
        [
            ("name", typing.ClassVar[str], name),
            ("output_type", typing.ClassVar[typing.Callable], type_signature.as_method),
        ],
        bases=(UnaryOp,),
        frozen=True,
    )


def create_binary_op(
    name: str, type_signature: op_typing.BinaryTypeSignature
) -> type[BinaryOp]:
    return dataclasses.make_dataclass(
        name,
        [
            ("name", typing.ClassVar[str], name),
            ("output_type", typing.ClassVar[typing.Callable], type_signature.as_method),
        ],
        bases=(BinaryOp,),
        frozen=True,
    )
