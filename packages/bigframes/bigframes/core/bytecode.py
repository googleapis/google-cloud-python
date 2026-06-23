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

import dis
import operator
import sys
from types import ModuleType
from typing import Callable

import bigframes.core.py_expressions as py_exprs
from bigframes.core import expression

_BINARY_OP_MAP = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "**": operator.pow,
}

_COMPARE_OP_MAP = {
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
}

_OLD_BINARY_OP_MAP = {
    "BINARY_ADD": operator.add,
    "INPLACE_ADD": operator.add,
    "BINARY_SUBTRACT": operator.sub,
    "INPLACE_SUBTRACT": operator.sub,
    "BINARY_MULTIPLY": operator.mul,
    "INPLACE_MULTIPLY": operator.mul,
    "BINARY_TRUE_DIVIDE": operator.truediv,
    "INPLACE_TRUE_DIVIDE": operator.truediv,
    "BINARY_FLOOR_DIVIDE": operator.floordiv,
    "INPLACE_FLOOR_DIVIDE": operator.floordiv,
    "BINARY_MODULO": operator.mod,
    "INPLACE_MODULO": operator.mod,
    "BINARY_POWER": operator.pow,
    "INPLACE_POWER": operator.pow,
}


_NULL = py_exprs.PyObject(None)


def _compile_bytecode_to_py_expr(func: Callable) -> expression.Expression:
    instructions = list(dis.get_instructions(func))

    stack: list[expression.Expression] = []
    globals_dict = func.__globals__
    import builtins

    builtins_dict = builtins.__dict__

    closure_dict = {}
    if func.__closure__:
        free_vars = func.__code__.co_freevars
        for var, cell in zip(free_vars, func.__closure__):
            try:
                closure_dict[var] = cell.cell_contents
            except ValueError:
                pass

    for inst in instructions:
        opname = inst.opname

        if opname in ("RESUME", "PRECALL"):
            continue

        elif opname in ("LOAD_FAST_LOAD_FAST", "LOAD_FAST_BORROW_LOAD_FAST_BORROW"):
            var1, var2 = inst.argval
            stack.append(expression.UnboundVariableExpression(var1))
            stack.append(expression.UnboundVariableExpression(var2))

        elif opname.startswith("LOAD_FAST"):
            stack.append(expression.UnboundVariableExpression(inst.argval))

        elif opname in ("LOAD_CONST", "LOAD_SMALL_INT"):
            stack.append(py_exprs.PyObject(inst.argval))

        elif opname == "LOAD_GLOBAL":
            # In Python 3.11+, the lowest bit of inst.arg indicates that a NULL
            # should be pushed before the global variable.
            if sys.version_info >= (3, 11) and inst.arg is not None and (inst.arg & 1):
                stack.append(_NULL)
            name = inst.argval
            found = False
            val = None
            if name in closure_dict:
                val = closure_dict[name]
                found = True
            elif name in globals_dict:
                val = globals_dict[name]
                found = True
            elif name in builtins_dict:
                val = builtins_dict[name]
                found = True

            if found:
                if isinstance(val, ModuleType):
                    stack.append(py_exprs.Module(val))
                else:
                    stack.append(py_exprs.PyObject(val))
            else:
                stack.append(expression.UnboundVariableExpression(name))

        elif opname in ("LOAD_ATTR", "LOAD_METHOD"):
            if not stack:
                raise ValueError("Stack is empty")
            target = stack.pop()
            stack.append(py_exprs.GetAttr(target, inst.argval))
            if opname == "LOAD_METHOD":
                if isinstance(target, py_exprs.Module):
                    stack.append(_NULL)
                else:
                    stack.append(target)

        elif opname == "PUSH_NULL":
            stack.append(_NULL)

        elif opname == "BINARY_OP":
            if len(stack) < 2:
                raise ValueError("Stack is empty")
            right = stack.pop()
            left = stack.pop()
            op_symbol = inst.argrepr
            if not op_symbol and isinstance(inst.argval, str):
                op_symbol = inst.argval
            if op_symbol and op_symbol.endswith("="):
                op_symbol = op_symbol[:-1]

            if op_symbol not in _BINARY_OP_MAP:
                raise ValueError(f"Unsupported binary operator: {op_symbol}")
            stack.append(
                py_exprs.Call(
                    py_exprs.PyObject(_BINARY_OP_MAP[op_symbol]), (left, right)
                )
            )

        # Support older Python versions compatibility
        elif opname in _OLD_BINARY_OP_MAP:
            if len(stack) < 2:
                raise ValueError("Stack has < 2 elements")
            right = stack.pop()
            left = stack.pop()
            stack.append(
                py_exprs.Call(
                    py_exprs.PyObject(_OLD_BINARY_OP_MAP[opname]), (left, right)
                )
            )

        elif opname == "COMPARE_OP":
            if len(stack) < 2:
                raise ValueError("Stack has < 2 elements")
            right = stack.pop()
            left = stack.pop()
            op_symbol = inst.argval
            if op_symbol not in _COMPARE_OP_MAP:
                raise ValueError(f"Unsupported compare operator: {op_symbol}")
            stack.append(
                py_exprs.Call(
                    py_exprs.PyObject(_COMPARE_OP_MAP[op_symbol]), (left, right)
                )
            )

        elif opname in ("UNARY_NEGATIVE", "UNARY_INVERT"):
            if not stack:
                raise ValueError("Stack is empty")
            target = stack.pop()
            stack.append(
                py_exprs.Call(
                    py_exprs.PyObject(
                        operator.neg if opname == "UNARY_NEGATIVE" else operator.invert
                    ),
                    (target,),
                )
            )

        elif opname == "UNARY_POSITIVE":
            if not stack:
                raise ValueError("Stack is empty")
            target = stack.pop()
            stack.append(py_exprs.Call(py_exprs.PyObject(operator.pos), (target,)))

        elif opname == "CALL_INTRINSIC_1":
            if inst.argrepr == "INTRINSIC_UNARY_POSITIVE":
                if not stack:
                    raise ValueError("Stack is empty")
                target = stack.pop()
                stack.append(py_exprs.Call(py_exprs.PyObject(operator.pos), (target,)))
            else:
                raise ValueError(f"Unsupported intrinsic: {inst.argrepr}")

        elif opname in ("CALL", "CALL_FUNCTION", "CALL_METHOD"):
            num_args = inst.arg
            assert num_args is not None
            if len(stack) < num_args:
                raise ValueError("Stack has < 2 elements")
            args = [stack.pop() for _ in range(num_args)][::-1]
            # In Python 3.11, LOAD_GLOBAL with NULL push puts NULL below the global.
            # If NULL is below the callable on the stack, swap them to match
            # the expected layout [callable, NULL].
            if len(stack) >= 2 and stack[-2] == _NULL:
                stack[-1], stack[-2] = stack[-2], stack[-1]
            if stack and stack[-1] == _NULL:
                stack.pop()
            elif (
                stack
                and stack[-1] != _NULL
                and isinstance(stack[-1], expression.Expression)
            ):
                self_arg = stack.pop()
                args = [self_arg] + args
            if not stack:
                raise ValueError("Stack is empty")
            callable_expr = stack.pop()
            stack.append(py_exprs.Call(callable_expr, tuple(args)))

        elif opname == "RETURN_VALUE":
            if not stack:
                raise ValueError("Stack is empty")
            return stack[-1]

        elif opname in ("STORE_FAST", "POP_TOP"):
            if stack:
                stack.pop()

        else:
            raise ValueError(f"Unsupported opcode: {opname}")

    raise ValueError("No return value found")


def py_to_expression(func: Callable) -> expression.Expression:
    """
    Try to convert a python function to a BigQuery expression.

    This is "best effort" - if the function contains operations that cannot
    be converted to BigQuery expressions, it will raise an Exception.
    """
    py_expr = _compile_bytecode_to_py_expr(func)
    return py_exprs.resolve_py_exprs(py_expr)
