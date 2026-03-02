# Copyright 2026 Google LLC
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
from typing import Any, Hashable

import bigframes_vendored.pandas.core.col as pd_col

from bigframes.core import agg_expressions, window_spec
import bigframes.core.expression as bf_expression
import bigframes.operations as bf_ops
import bigframes.operations.aggregations as agg_ops


# Not to be confused with the Expression class in `bigframes.core.expressions`
# Name collision unintended
@dataclasses.dataclass(frozen=True)
class Expression:
    __doc__ = pd_col.Expression.__doc__

    _value: bf_expression.Expression

    def _apply_unary(self, op: bf_ops.UnaryOp) -> Expression:
        return Expression(op.as_expr(self._value))

    def _apply_unary_agg(self, op: agg_ops.UnaryAggregateOp) -> Expression:
        # We probably shouldn't need to windowize here, but block apis expect pre-windowized expressions
        # Later on, we will probably have col expressions in windowed context, so will need to defer windowization
        # instead of automatically applying the default unbound window
        agg_expr = op.as_expr(self._value)
        return Expression(
            agg_expressions.WindowExpression(agg_expr, window_spec.unbound())
        )

    def _apply_binary(self, other: Any, op: bf_ops.BinaryOp, reverse: bool = False):
        if isinstance(other, Expression):
            other_value = other._value
        else:
            other_value = bf_expression.const(other)
        if reverse:
            return Expression(op.as_expr(other_value, self._value))
        else:
            return Expression(op.as_expr(self._value, other_value))

    def __add__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.add_op)

    def __radd__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.add_op, reverse=True)

    def __sub__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.sub_op)

    def __rsub__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.sub_op, reverse=True)

    def __mul__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.mul_op)

    def __rmul__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.mul_op, reverse=True)

    def __truediv__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.div_op)

    def __rtruediv__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.div_op, reverse=True)

    def __floordiv__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.floordiv_op)

    def __rfloordiv__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.floordiv_op, reverse=True)

    def __ge__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.ge_op)

    def __gt__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.gt_op)

    def __le__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.le_op)

    def __lt__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.lt_op)

    def __eq__(self, other: object) -> Expression:  # type: ignore
        return self._apply_binary(other, bf_ops.eq_op)

    def __ne__(self, other: object) -> Expression:  # type: ignore
        return self._apply_binary(other, bf_ops.ne_op)

    def __mod__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.mod_op)

    def __rmod__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.mod_op, reverse=True)

    def __and__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.and_op)

    def __rand__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.and_op, reverse=True)

    def __or__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.or_op)

    def __ror__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.or_op, reverse=True)

    def __xor__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.xor_op)

    def __rxor__(self, other: Any) -> Expression:
        return self._apply_binary(other, bf_ops.xor_op, reverse=True)

    def __invert__(self) -> Expression:
        return self._apply_unary(bf_ops.invert_op)

    def sum(self) -> Expression:
        return self._apply_unary_agg(agg_ops.sum_op)

    def mean(self) -> Expression:
        return self._apply_unary_agg(agg_ops.mean_op)

    def var(self) -> Expression:
        return self._apply_unary_agg(agg_ops.var_op)

    def std(self) -> Expression:
        return self._apply_unary_agg(agg_ops.std_op)

    def min(self) -> Expression:
        return self._apply_unary_agg(agg_ops.min_op)

    def max(self) -> Expression:
        return self._apply_unary_agg(agg_ops.max_op)


def col(col_name: Hashable) -> Expression:
    return Expression(bf_expression.free_var(col_name))


col.__doc__ = pd_col.col.__doc__
