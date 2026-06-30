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
import itertools
import operator
from types import ModuleType
from typing import Callable, Hashable, Mapping, Optional, Tuple

import bigframes.operations.python_op_maps as python_op_maps
from bigframes import dtypes
from bigframes.core import identifiers
from bigframes.core import window_spec as window_specs
from bigframes.core.expression import (
    Expression,
    OpExpression,
    UnboundVariableExpression,
    const,
    deref,
)
from bigframes.operations import (
    NUMPY_TO_BINOP,
    NUMPY_TO_OP,
    ScalarOp,
    generic_ops,
    numeric_ops,
)

_CALLABLE_TO_OP = {
    **NUMPY_TO_OP,
    **NUMPY_TO_BINOP,
}

_BUILTIN_CALLABLES = {
    str: generic_ops.AsTypeOp(dtypes.STRING_DTYPE),
    abs: numeric_ops.abs_op,
}


@dataclasses.dataclass(frozen=True)
class GetAttr(Expression):
    input: Expression
    attr: str

    @property
    def column_references(
        self,
    ) -> Tuple[identifiers.ColumnId, ...]:
        return self.input.column_references

    @property
    def free_variables(self) -> tuple[Hashable, ...]:
        return self.input.free_variables

    @property
    def is_const(self) -> bool:
        return False

    @property
    def children(self):
        return (self.input,)

    @property
    def nullable(self) -> bool:
        return True

    @property
    def is_resolved(self) -> bool:
        return False

    @property
    def output_type(self) -> dtypes.ExpressionType:
        raise ValueError(f"Type of expression {self} has not been fixed.")

    @property
    def is_bijective(self) -> bool:
        # TODO: Mark individual functions as bijective?
        return False

    @property
    def deterministic(self) -> bool:
        return True

    def transform_children(self, t: Callable[[Expression], Expression]) -> Expression:
        new_input = t(self.input)
        if new_input != self.input:
            return dataclasses.replace(self, input=new_input)
        return self

    def bind_variables(
        self,
        bindings: Mapping[Hashable, Expression],
        allow_partial_bindings: bool = False,
    ) -> GetAttr:
        return GetAttr(
            self.input.bind_variables(
                bindings, allow_partial_bindings=allow_partial_bindings
            ),
            self.attr,
        )

    def bind_refs(
        self,
        bindings: Mapping[identifiers.ColumnId, Expression],
        allow_partial_bindings: bool = False,
    ) -> GetAttr:
        return GetAttr(
            self.input.bind_refs(
                bindings, allow_partial_bindings=allow_partial_bindings
            ),
            self.attr,
        )


@dataclasses.dataclass(frozen=True)
class GetItem(Expression):
    input: Expression
    key: Expression

    @property
    def column_references(self) -> Tuple[identifiers.ColumnId, ...]:
        return self.input.column_references + self.key.column_references

    @property
    def free_variables(self) -> tuple[Hashable, ...]:
        return self.input.free_variables + self.key.free_variables

    @property
    def is_const(self) -> bool:
        return False

    @property
    def children(self):
        return (self.input, self.key)

    @property
    def nullable(self) -> bool:
        return True

    @property
    def is_resolved(self) -> bool:
        return False

    @property
    def output_type(self) -> dtypes.ExpressionType:
        raise ValueError(f"Type of expression {self} has not been fixed.")

    @property
    def is_bijective(self) -> bool:
        return False

    @property
    def deterministic(self) -> bool:
        return True

    def transform_children(self, t: Callable[[Expression], Expression]) -> Expression:
        new_input = t(self.input)
        new_key = t(self.key)
        if new_input != self.input or new_key != self.key:
            return dataclasses.replace(self, input=new_input, key=new_key)
        return self

    def bind_variables(
        self,
        bindings: Mapping[Hashable, Expression],
        allow_partial_bindings: bool = False,
    ) -> GetItem:
        return GetItem(
            self.input.bind_variables(
                bindings, allow_partial_bindings=allow_partial_bindings
            ),
            self.key.bind_variables(
                bindings, allow_partial_bindings=allow_partial_bindings
            ),
        )

    def bind_refs(
        self,
        bindings: Mapping[identifiers.ColumnId, Expression],
        allow_partial_bindings: bool = False,
    ) -> GetItem:
        return GetItem(
            self.input.bind_refs(
                bindings, allow_partial_bindings=allow_partial_bindings
            ),
            self.key.bind_refs(bindings, allow_partial_bindings=allow_partial_bindings),
        )


@dataclasses.dataclass(frozen=True)
class Module(Expression):
    """An expression representing a module reference."""

    module: ModuleType

    @property
    def is_const(self) -> bool:
        return True

    @property
    def column_references(self) -> Tuple[identifiers.ColumnId, ...]:
        return ()

    @property
    def nullable(self) -> bool:
        return True  # type: ignore

    @property
    def is_resolved(self) -> bool:
        return False

    @property
    def output_type(self) -> dtypes.ExpressionType:
        raise ValueError("Module expression does not have a type.")

    def bind_variables(
        self,
        bindings: Mapping[Hashable, Expression],
        allow_partial_bindings: bool = False,
    ) -> Expression:
        return self

    def bind_refs(
        self,
        bindings: Mapping[identifiers.ColumnId, Expression],
        allow_partial_bindings: bool = False,
    ) -> Module:
        return self

    @property
    def is_bijective(self) -> bool:
        # () <-> value
        return True

    def transform_children(self, t: Callable[[Expression], Expression]) -> Expression:
        return self


@dataclasses.dataclass(frozen=True)
class PyObject(Expression):
    """An expression representing a module reference."""

    value: Hashable

    @property
    def is_const(self) -> bool:
        return True

    @property
    def column_references(self) -> Tuple[identifiers.ColumnId, ...]:
        return ()

    @property
    def nullable(self) -> bool:
        return True  # type: ignore

    @property
    def is_resolved(self) -> bool:
        return False

    @property
    def output_type(self) -> dtypes.ExpressionType:
        raise ValueError("PyObject expression does not have a type.")

    def bind_variables(
        self,
        bindings: Mapping[Hashable, Expression],
        allow_partial_bindings: bool = False,
    ) -> Expression:
        return self

    def bind_refs(
        self,
        bindings: Mapping[identifiers.ColumnId, Expression],
        allow_partial_bindings: bool = False,
    ) -> PyObject:
        return self

    @property
    def is_bijective(self) -> bool:
        # () <-> value
        return True

    def transform_children(self, t: Callable[[Expression], Expression]) -> Expression:
        return self


@dataclasses.dataclass(frozen=True)
class Call(Expression):
    """An expression representing a scalar constant."""

    # TODO: Further constrain?
    callable: Expression
    inputs: Tuple[Expression, ...]

    @property
    def column_references(
        self,
    ) -> Tuple[identifiers.ColumnId, ...]:
        return tuple(
            itertools.chain.from_iterable(
                map(lambda x: x.column_references, self.children)
            )
        )

    @property
    def free_variables(self) -> tuple[Hashable, ...]:
        return tuple(
            itertools.chain.from_iterable(
                map(lambda x: x.free_variables, self.children)
            )
        )

    @property
    def is_const(self) -> bool:
        return False

    @property
    def children(self):
        return (self.callable, *self.inputs)

    @property
    def nullable(self) -> bool:
        return True

    @property
    def is_resolved(self) -> bool:
        return False

    @property
    def output_type(self) -> dtypes.ExpressionType:
        raise ValueError(f"Type of expression {self} has not been fixed.")

    @property
    def is_bijective(self) -> bool:
        # TODO: Mark individual functions as bijective?
        return False

    @property
    def deterministic(self) -> bool:
        return True

    def transform_children(self, t: Callable[[Expression], Expression]) -> Expression:
        return dataclasses.replace(
            self,
            callable=t(self.callable),
            inputs=tuple(t(input) for input in self.inputs),
        )

    def bind_variables(
        self,
        bindings: Mapping[Hashable, Expression],
        allow_partial_bindings: bool = False,
    ) -> Call:
        return Call(
            callable=self.callable.bind_variables(
                bindings, allow_partial_bindings=allow_partial_bindings
            ),
            inputs=tuple(
                input.bind_variables(
                    bindings, allow_partial_bindings=allow_partial_bindings
                )
                for input in self.inputs
            ),
        )

    def bind_refs(
        self,
        bindings: Mapping[identifiers.ColumnId, Expression],
        allow_partial_bindings: bool = False,
    ) -> Call:
        return Call(
            callable=self.callable.bind_refs(
                bindings, allow_partial_bindings=allow_partial_bindings
            ),
            inputs=tuple(
                input.bind_refs(bindings, allow_partial_bindings=allow_partial_bindings)
                for input in self.inputs
            ),
        )


# TODO: Mode that resolves free variable attrs as columns
def resolve_py_exprs(
    expression: Expression,
    series_arg: Optional[str] = None,
    series_attrs: Mapping[Hashable, str] | None = None,
    col_series_args: Mapping[str, str] | None = None,
    window_spec: window_specs.WindowSpec | None = None,
) -> Expression:
    """
    Replace all PyObject, attribute, item, and call expressions bottom-up.

    This function translates unresolved python expressions (like GetAttr, GetItem,
    Call, PyObject) into resolved BigQuery expressions (like OpExpression, DerefOp,
    Aggregation, ScalarConstantExpression) by binding them to the specified context.

    Args:
        expression: The unresolved python expression to translate.
        series_arg: The name of the parameter representing the row (for row-wise UDFs like
            apply axis=1) or the DataFrame group (for DataFrameGroupBy.apply).
        series_attrs: A mapping of attribute/item names to column IDs for the series_arg.
            When GetAttr(series_arg, attr) or GetItem(series_arg, key) is encountered,
            it is resolved to deref(column_id).
        col_series_args: A mapping of parameter names to column IDs for parameters that
            represent a single Series/column directly (for SeriesGroupBy.apply). When
            UnboundVariableExpression(arg_name) is encountered and arg_name is in
            col_series_args, it is resolved directly to deref(column_id).
        window_spec: Optional window spec. When provided, aggregations inside calls will
            be converted to WindowExpression using this spec.

    Returns:
        The resolved BigQuery Expression.
    """

    def resolve_expr_if_call(expr: Expression) -> Expression:
        if isinstance(expr, Call):
            return resolve_call(expr, window_spec=window_spec)
        return expr

    def resolve_attrs(expr: Expression) -> Expression:
        if isinstance(expr, GetAttr):
            return _resolve_getattr(expr, series_arg, series_attrs)
        if isinstance(expr, GetItem):
            return _resolve_getitem(expr, series_arg, series_attrs, col_series_args)
        return expr

    def resolve_series_var(expr: Expression) -> Expression:
        if (
            col_series_args is not None
            and isinstance(expr, UnboundVariableExpression)
            and isinstance(expr.id, str)
            and expr.id in col_series_args
        ):
            return deref(col_series_args[expr.id])
        return expr

    def resolve_pyobjs(expr: Expression) -> Expression:
        if isinstance(expr, PyObject):
            return const(expr.value)
        return expr

    wo_calls = expression.bottom_up(resolve_expr_if_call)
    wo_attrs = wo_calls.bottom_up(resolve_attrs)
    wo_vars = wo_attrs.bottom_up(resolve_series_var)
    return wo_vars.bottom_up(resolve_pyobjs)


def _resolve_getattr(
    expression: GetAttr,
    series_arg: Optional[str],
    series_attrs: Mapping[Hashable, str] | None,
) -> Expression:
    if isinstance(expression.input, Module):
        # resolves things like Math.pi
        return PyObject(getattr(expression.input.module, expression.attr))
    # Resolve attribute access on the series/row argument
    if (
        series_arg is not None
        and series_attrs is not None
        and isinstance(expression.input, UnboundVariableExpression)
        and expression.input.id == series_arg
        and expression.attr in series_attrs
    ):
        return deref(series_attrs[expression.attr])
    return expression


def _resolve_getitem(
    expression: GetItem,
    series_arg: Optional[str],
    series_attrs: Mapping[Hashable, str] | None,
    col_series_args: Mapping[str, str] | None,
) -> Expression:
    # Resolve subscript/item access on the series/row argument
    from bigframes.core.expression import ScalarConstantExpression

    key_val = None
    if isinstance(expression.key, PyObject):
        key_val = expression.key.value
    elif isinstance(expression.key, ScalarConstantExpression):
        key_val = expression.key.value

    is_series_var = (
        series_arg is not None
        and isinstance(expression.input, UnboundVariableExpression)
        and expression.input.id == series_arg
    )

    if is_series_var and series_attrs is not None:
        if key_val is None:
            raise NotImplementedError("Dynamic column lookup is not supported.")
        if key_val in series_attrs:
            return deref(series_attrs[key_val])
        else:
            raise KeyError(f"Column '{key_val}' not found.")

    is_columnar_var = (
        col_series_args is not None
        and isinstance(expression.input, UnboundVariableExpression)
        and expression.input.id in col_series_args
    )

    if is_columnar_var:
        raise NotImplementedError(
            "Subscripting a Series/column is not supported in this UDF context."
        )

    # Scalar context (struct/array getitem ops)
    import bigframes.operations.generic_ops as generic_ops

    if key_val is not None:
        if isinstance(key_val, (str, int)):
            return OpExpression(generic_ops.GetItemOp(key_val), (expression.input,))
        else:
            raise NotImplementedError(
                f"Subscript key of type '{type(key_val).__name__}' is not supported."
            )
    else:
        return OpExpression(
            generic_ops.DynamicGetItemOp(), (expression.input, expression.key)
        )


def resolve_call(
    call: Call, window_spec: window_specs.WindowSpec | None = None
) -> Expression:
    callable = call.callable
    if isinstance(callable, GetAttr):
        attr = callable.attr
        if isinstance(callable.input, Module):
            fn = getattr(callable.input.module, attr)
            if fn in python_op_maps.PYTHON_TO_BIGFRAMES:
                op = python_op_maps.PYTHON_TO_BIGFRAMES[fn]
                return OpExpression(op, call.inputs)
            if fn in _CALLABLE_TO_OP:
                op = _CALLABLE_TO_OP[fn]
                return OpExpression(op, call.inputs)
        else:
            # Method call on an expression (e.g. df.col.sum() or s.mean())
            try:
                import bigframes.operations.aggregations as agg_ops

                agg_op, _ = agg_ops.lookup_agg_func(attr)
                import bigframes.core.agg_expressions as agg_exprs

                if isinstance(agg_op, agg_ops.UnaryAggregateOp):
                    agg_expr: agg_exprs.Aggregation = agg_exprs.UnaryAggregation(
                        agg_op, callable.input
                    )
                    if window_spec is not None:
                        return agg_exprs.WindowExpression(agg_expr, window_spec)
                    return agg_expr
                elif isinstance(agg_op, agg_ops.NullaryAggregateOp):
                    agg_expr = agg_exprs.NullaryAggregation(agg_op)
                    if window_spec is not None:
                        return agg_exprs.WindowExpression(agg_expr, window_spec)
                    return agg_expr
            except ValueError:
                pass

            # Support common scalar method calls on Series/expressions
            if (method_op := python_op_maps.series_method_to_op(attr)) is not None:
                if isinstance(method_op, ScalarOp):
                    return OpExpression(method_op, (callable.input,))

    elif isinstance(callable, PyObject):
        if callable.value == operator.getitem:
            return GetItem(call.inputs[0], call.inputs[1])
        if isinstance(callable.value, ScalarOp):
            return OpExpression(callable.value, call.inputs)
        if callable.value in python_op_maps.PYTHON_TO_BIGFRAMES:
            op = python_op_maps.PYTHON_TO_BIGFRAMES[callable.value]  # type: ignore
            return OpExpression(op, call.inputs)
        if callable.value in _BUILTIN_CALLABLES:
            return OpExpression(_BUILTIN_CALLABLES[callable.value], call.inputs)

    raise NotImplementedError(
        f"No implementation available for call expression: {call}"
    )
