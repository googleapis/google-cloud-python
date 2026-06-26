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

import dataclasses
import dis
import operator
import sys
from types import ModuleType
from typing import Callable

import bigframes.core.py_expressions as py_exprs
from bigframes.core import expression
from bigframes.operations import generic_ops

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


_RETURN_OPNAMES = {"RETURN_VALUE", "RETURN_CONST"}

_UNCONDITIONAL_JUMP_OPNAMES = {
    "JUMP_FORWARD",
    "JUMP_ABSOLUTE",
    "JUMP_BACKWARD",
    "JUMP_BACKWARD_NO_INTERRUPT",
    "JUMP",
    "JUMP_NO_INTERRUPT",
}

_JUMP_IF_FALSE_OPNAMES = {
    "POP_JUMP_IF_FALSE",
    "POP_JUMP_FORWARD_IF_FALSE",
    "POP_JUMP_BACKWARD_IF_FALSE",
}

_JUMP_IF_TRUE_OPNAMES = {
    "POP_JUMP_IF_TRUE",
    "POP_JUMP_FORWARD_IF_TRUE",
    "POP_JUMP_BACKWARD_IF_TRUE",
}

_CONDITIONAL_JUMP_OPNAMES = (
    _JUMP_IF_FALSE_OPNAMES
    | _JUMP_IF_TRUE_OPNAMES
    | {
        "JUMP_IF_FALSE_OR_POP",
        "JUMP_IF_TRUE_OR_POP",
        "POP_JUMP_IF_NONE",
        "POP_JUMP_IF_NOT_NONE",
        "POP_JUMP_FORWARD_IF_NONE",
        "POP_JUMP_FORWARD_IF_NOT_NONE",
        "POP_JUMP_BACKWARD_IF_NONE",
        "POP_JUMP_BACKWARD_IF_NOT_NONE",
    }
)

_ALL_JUMP_OPNAMES = _UNCONDITIONAL_JUMP_OPNAMES | _CONDITIONAL_JUMP_OPNAMES


@dataclasses.dataclass
class BasicBlock:
    start_offset: int
    instructions: list[dis.Instruction]
    successors: list[int] = dataclasses.field(default_factory=list)
    predecessors: list[int] = dataclasses.field(default_factory=list)


def get_block_starts(instructions: list[dis.Instruction]) -> set[int]:
    starts = {0}
    for i, inst in enumerate(instructions):
        opname = inst.opname
        if opname in _ALL_JUMP_OPNAMES:
            if isinstance(inst.argval, int):
                starts.add(inst.argval)
            if i + 1 < len(instructions):
                starts.add(instructions[i + 1].offset)
        elif opname in _RETURN_OPNAMES:
            if i + 1 < len(instructions):
                starts.add(instructions[i + 1].offset)
    return starts


def get_block_successors(block: BasicBlock, next_offsets: dict[int, int]) -> list[int]:
    if not block.instructions:
        return []
    last_inst = block.instructions[-1]
    opname = last_inst.opname
    offset = last_inst.offset

    next_offset = next_offsets.get(offset)

    if opname in _RETURN_OPNAMES:
        return []

    if opname in _UNCONDITIONAL_JUMP_OPNAMES:
        return [last_inst.argval]

    if opname in _CONDITIONAL_JUMP_OPNAMES:
        successors = [last_inst.argval]
        if next_offset is not None:
            successors.append(next_offset)
        return successors

    if next_offset is not None:
        return [next_offset]
    return []


def build_cfg(
    instructions: list[dis.Instruction], next_offsets: dict[int, int]
) -> dict[int, BasicBlock]:
    starts = sorted(list(get_block_starts(instructions)))

    blocks: dict[int, BasicBlock] = {}
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else None
        block_insts = [
            inst
            for inst in instructions
            if start <= inst.offset and (end is None or inst.offset < end)
        ]
        blocks[start] = BasicBlock(start_offset=start, instructions=block_insts)

    for block in blocks.values():
        successors = get_block_successors(block, next_offsets)
        block.successors = successors
        for succ in successors:
            blocks[succ].predecessors.append(block.start_offset)

    return blocks


def topological_sort(blocks: dict[int, BasicBlock]) -> list[int]:
    in_degree = {offset: len(block.predecessors) for offset, block in blocks.items()}
    queue = [offset for offset, deg in in_degree.items() if deg == 0]
    order = []

    while queue:
        queue.sort()
        curr = queue.pop(0)
        order.append(curr)
        for succ in blocks[curr].successors:
            in_degree[succ] -= 1
            if in_degree[succ] == 0:
                queue.append(succ)

    # TODO(b/521549179): Support limited loop analysis (eg unroll loops over a constant range).
    if len(order) != len(blocks):
        raise ValueError(
            "Loops are not supported in the Python function for transpilation."
        )

    return order


def merge_values(
    pairs: list[tuple[expression.Expression, expression.Expression]],
) -> expression.Expression:
    if not pairs:
        raise ValueError("Cannot merge empty list of values")
    if len(pairs) == 1:
        return pairs[0][0]

    val = pairs[-1][0]
    for next_val, next_cond in reversed(pairs[:-1]):
        val = py_exprs.Call(
            py_exprs.PyObject(generic_ops.where_op), (next_val, next_cond, val)
        )
    return val


def _compile_bytecode_to_py_expr(func: Callable) -> expression.Expression:
    instructions = list(dis.get_instructions(func))
    next_offsets = {
        inst.offset: next_inst.offset
        for inst, next_inst in zip(instructions, instructions[1:])
    }

    blocks = build_cfg(instructions, next_offsets)
    order = topological_sort(blocks)

    stack: list[expression.Expression]
    local_vars: dict[str, expression.Expression]

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

    block_outputs: dict[
        int, tuple[list[expression.Expression], dict[str, expression.Expression]]
    ] = {}
    block_reach_conditions: dict[int, expression.Expression] = {
        0: py_exprs.PyObject(True)
    }
    edge_conditions: dict[tuple[int, int], expression.Expression] = {}
    edge_stacks: dict[tuple[int, int], list[expression.Expression]] = {}
    returns: list[tuple[expression.Expression, expression.Expression]] = []

    co = func.__code__
    param_names = list(co.co_varnames[: co.co_argcount])
    kwonly_argcount = co.co_kwonlyargcount
    param_names.extend(
        co.co_varnames[co.co_argcount : co.co_argcount + kwonly_argcount]
    )

    initial_local_vars: dict[str, expression.Expression] = {
        name: expression.UnboundVariableExpression(name) for name in param_names
    }

    for offset in order:
        block = blocks[offset]

        reach_cond: expression.Expression
        if offset == 0:
            reach_cond = py_exprs.PyObject(True)
        else:
            incoming = [
                edge_conditions[(pred, offset)]
                for pred in block.predecessors
                if (pred, offset) in edge_conditions
            ]
            if not incoming:
                continue

            reach_cond = incoming[0]
            for cond in incoming[1:]:
                reach_cond = py_exprs.Call(
                    py_exprs.PyObject(operator.or_), (reach_cond, cond)
                )

        block_reach_conditions[offset] = reach_cond

        if offset == 0:
            stack = []
            local_vars = initial_local_vars.copy()
        else:
            reachable_preds = [
                pred for pred in block.predecessors if (pred, offset) in edge_stacks
            ]
            if not reachable_preds:
                continue

            h = len(edge_stacks[(reachable_preds[0], offset)])
            stack = []
            for i in range(h):
                pairs = [
                    (edge_stacks[(p, offset)][i], edge_conditions[(p, offset)])
                    for p in reachable_preds
                ]
                stack.append(merge_values(pairs))

            all_vars: set[str] = set()
            for p in reachable_preds:
                all_vars.update(block_outputs[p][1].keys())

            local_vars = {}
            for var in all_vars:
                pairs = [
                    (
                        block_outputs[p][1].get(
                            var, expression.UnboundVariableExpression(var)
                        ),
                        edge_conditions[(p, offset)],
                    )
                    for p in reachable_preds
                ]
                local_vars[var] = merge_values(pairs)

        jumped = False
        for inst in block.instructions:
            opname = inst.opname

            match opname:
                case "RESUME" | "PRECALL" | "COPY_FREE_VARS" | "NOT_TAKEN" | "NOP":
                    continue

                case "LOAD_FAST_LOAD_FAST" | "LOAD_FAST_BORROW_LOAD_FAST_BORROW":
                    var1, var2 = inst.argval
                    stack.append(
                        local_vars.get(var1, expression.UnboundVariableExpression(var1))
                    )
                    stack.append(
                        local_vars.get(var2, expression.UnboundVariableExpression(var2))
                    )

                case name if name.startswith("LOAD_FAST"):
                    stack.append(
                        local_vars.get(
                            inst.argval,
                            expression.UnboundVariableExpression(inst.argval),
                        )
                    )

                case "STORE_FAST":
                    if not stack:
                        raise ValueError("Stack is empty")
                    local_vars[inst.argval] = stack.pop()

                case "LOAD_CONST" | "LOAD_SMALL_INT":
                    stack.append(py_exprs.PyObject(inst.argval))

                case "LOAD_DEREF" | "LOAD_FROM_DICT_OR_DEREF":
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

                case "LOAD_GLOBAL":
                    if (
                        sys.version_info >= (3, 11)
                        and inst.arg is not None
                        and (inst.arg & 1)
                    ):
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

                case "LOAD_ATTR" | "LOAD_METHOD":
                    if not stack:
                        raise ValueError("Stack is empty")
                    target = stack.pop()
                    stack.append(py_exprs.GetAttr(target, inst.argval))

                    is_method_lookup = (opname == "LOAD_METHOD") or (
                        opname == "LOAD_ATTR"
                        and sys.version_info >= (3, 12)
                        and inst.arg is not None
                        and (inst.arg & 1)
                    )
                    if is_method_lookup:
                        if isinstance(target, py_exprs.Module):
                            stack.append(_NULL)
                        else:
                            stack.append(target)

                case "PUSH_NULL":
                    stack.append(_NULL)

                case "TO_BOOL":
                    if not stack:
                        raise ValueError("Stack is empty")
                    val = stack.pop()
                    stack.append(
                        py_exprs.Call(
                            py_exprs.PyObject(generic_ops.coerce_to_bool_op),
                            (val,),
                        )
                    )

                case "COPY":
                    idx = inst.arg
                    if idx is None or idx < 1 or len(stack) < idx:
                        raise ValueError(
                            f"Invalid COPY index or stack too small: {idx}"
                        )
                    stack.append(stack[-idx])

                case "UNARY_NOT":
                    if not stack:
                        raise ValueError("Stack is empty")
                    val = stack.pop()
                    val_bool = py_exprs.Call(
                        py_exprs.PyObject(generic_ops.coerce_to_bool_op),
                        (val,),
                    )
                    stack.append(
                        py_exprs.Call(
                            py_exprs.PyObject(operator.not_),
                            (val_bool,),
                        )
                    )

                case "SWAP":
                    idx = inst.arg
                    if idx is None or idx < 1 or len(stack) < idx:
                        raise ValueError(
                            f"Invalid SWAP index or stack too small: {idx}"
                        )
                    stack[-1], stack[-idx] = stack[-idx], stack[-1]

                case "ROT_TWO":
                    if len(stack) < 2:
                        raise ValueError("Stack has < 2 elements")
                    stack[-1], stack[-2] = stack[-2], stack[-1]

                case "ROT_THREE":
                    if len(stack) < 3:
                        raise ValueError("Stack has < 3 elements")
                    stack[-1], stack[-2], stack[-3] = stack[-2], stack[-3], stack[-1]

                case "DUP_TOP":
                    if not stack:
                        raise ValueError("Stack is empty")
                    stack.append(stack[-1])

                case "BINARY_OP":
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
                            py_exprs.PyObject(_BINARY_OP_MAP[op_symbol]),
                            (left, right),
                        )
                    )

                case name if name in _OLD_BINARY_OP_MAP:
                    if len(stack) < 2:
                        raise ValueError("Stack has < 2 elements")
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(
                        py_exprs.Call(
                            py_exprs.PyObject(_OLD_BINARY_OP_MAP[opname]),
                            (left, right),
                        )
                    )

                case "COMPARE_OP":
                    if len(stack) < 2:
                        raise ValueError("Stack has < 2 elements")
                    right = stack.pop()
                    left = stack.pop()
                    op_symbol = inst.argval
                    if op_symbol not in _COMPARE_OP_MAP:
                        raise ValueError(f"Unsupported compare operator: {op_symbol}")
                    stack.append(
                        py_exprs.Call(
                            py_exprs.PyObject(_COMPARE_OP_MAP[op_symbol]),
                            (left, right),
                        )
                    )

                case "UNARY_NEGATIVE" | "UNARY_INVERT":
                    if not stack:
                        raise ValueError("Stack is empty")
                    target = stack.pop()
                    stack.append(
                        py_exprs.Call(
                            py_exprs.PyObject(
                                operator.neg
                                if opname == "UNARY_NEGATIVE"
                                else operator.invert
                            ),
                            (target,),
                        )
                    )

                case "UNARY_POSITIVE":
                    if not stack:
                        raise ValueError("Stack is empty")
                    target = stack.pop()
                    stack.append(
                        py_exprs.Call(py_exprs.PyObject(operator.pos), (target,))
                    )

                case "CALL_INTRINSIC_1":
                    if inst.argrepr == "INTRINSIC_UNARY_POSITIVE":
                        if not stack:
                            raise ValueError("Stack is empty")
                        target = stack.pop()
                        stack.append(
                            py_exprs.Call(py_exprs.PyObject(operator.pos), (target,))
                        )
                    else:
                        raise ValueError(f"Unsupported intrinsic: {inst.argrepr}")

                case "CALL" | "CALL_FUNCTION" | "CALL_METHOD":
                    num_args = inst.arg
                    assert num_args is not None
                    if len(stack) < num_args:
                        raise ValueError(f"Stack has fewer than {num_args} elements")
                    args = [stack.pop() for _ in range(num_args)][::-1]
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

                case "RETURN_VALUE":
                    if not stack:
                        raise ValueError("Stack is empty")
                    returns.append((stack[-1], reach_cond))
                    jumped = True
                    break

                case "RETURN_CONST":
                    returns.append((py_exprs.PyObject(inst.argval), reach_cond))
                    jumped = True
                    break

                case "POP_TOP":
                    if stack:
                        stack.pop()

                case name if name in _ALL_JUMP_OPNAMES:
                    if opname in _UNCONDITIONAL_JUMP_OPNAMES:
                        dest = inst.argval
                        edge_conditions[(offset, dest)] = reach_cond
                        edge_stacks[(offset, dest)] = stack.copy()
                    elif opname in ("JUMP_IF_FALSE_OR_POP", "JUMP_IF_TRUE_OR_POP"):
                        if not stack:
                            raise ValueError("Stack is empty")
                        cond_expr = stack[-1]
                        cond_bool = py_exprs.Call(
                            py_exprs.PyObject(generic_ops.coerce_to_bool_op),
                            (cond_expr,),
                        )
                        dest = inst.argval
                        next_offset = next_offsets.get(inst.offset)
                        if opname == "JUMP_IF_FALSE_OR_POP":
                            not_cond_bool = py_exprs.Call(
                                py_exprs.PyObject(operator.not_), (cond_bool,)
                            )
                            edge_conditions[(offset, dest)] = py_exprs.Call(
                                py_exprs.PyObject(operator.and_),
                                (reach_cond, not_cond_bool),
                            )
                            edge_stacks[(offset, dest)] = stack.copy()
                            if next_offset is not None:
                                edge_conditions[(offset, next_offset)] = py_exprs.Call(
                                    py_exprs.PyObject(operator.and_),
                                    (reach_cond, cond_bool),
                                )
                                edge_stacks[(offset, next_offset)] = stack[:-1]
                        else:  # JUMP_IF_TRUE_OR_POP
                            edge_conditions[(offset, dest)] = py_exprs.Call(
                                py_exprs.PyObject(operator.and_),
                                (reach_cond, cond_bool),
                            )
                            edge_stacks[(offset, dest)] = stack.copy()
                            if next_offset is not None:
                                not_cond_bool = py_exprs.Call(
                                    py_exprs.PyObject(operator.not_), (cond_bool,)
                                )
                                edge_conditions[(offset, next_offset)] = py_exprs.Call(
                                    py_exprs.PyObject(operator.and_),
                                    (reach_cond, not_cond_bool),
                                )
                                edge_stacks[(offset, next_offset)] = stack[:-1]
                    elif (
                        opname in _JUMP_IF_FALSE_OPNAMES
                        or opname in _JUMP_IF_TRUE_OPNAMES
                    ):
                        if not stack:
                            raise ValueError("Stack is empty")
                        cond_expr = stack.pop()
                        cond_expr = py_exprs.Call(
                            py_exprs.PyObject(generic_ops.coerce_to_bool_op),
                            (cond_expr,),
                        )

                        dest = inst.argval
                        next_offset = next_offsets.get(inst.offset)

                        if opname in _JUMP_IF_FALSE_OPNAMES:
                            not_cond_expr = py_exprs.Call(
                                py_exprs.PyObject(operator.not_), (cond_expr,)
                            )
                            edge_conditions[(offset, dest)] = py_exprs.Call(
                                py_exprs.PyObject(operator.and_),
                                (reach_cond, not_cond_expr),
                            )
                            edge_stacks[(offset, dest)] = stack.copy()
                            if next_offset is not None:
                                edge_conditions[(offset, next_offset)] = py_exprs.Call(
                                    py_exprs.PyObject(operator.and_),
                                    (reach_cond, cond_expr),
                                )
                                edge_stacks[(offset, next_offset)] = stack.copy()
                        else:  # opname in _JUMP_IF_TRUE_OPNAMES
                            not_cond_expr = py_exprs.Call(
                                py_exprs.PyObject(operator.not_), (cond_expr,)
                            )
                            edge_conditions[(offset, dest)] = py_exprs.Call(
                                py_exprs.PyObject(operator.and_),
                                (reach_cond, cond_expr),
                            )
                            edge_stacks[(offset, dest)] = stack.copy()
                            if next_offset is not None:
                                edge_conditions[(offset, next_offset)] = py_exprs.Call(
                                    py_exprs.PyObject(operator.and_),
                                    (reach_cond, not_cond_expr),
                                )
                                edge_stacks[(offset, next_offset)] = stack.copy()
                    else:
                        raise ValueError(f"Unsupported jump opcode: {opname}")
                    jumped = True
                    break

                case _:
                    raise ValueError(f"Unsupported opcode: {opname}")

        if not jumped:
            next_offset = next_offsets.get(block.instructions[-1].offset)
            if next_offset is not None:
                edge_conditions[(offset, next_offset)] = reach_cond
                edge_stacks[(offset, next_offset)] = stack.copy()

        block_outputs[offset] = (stack, local_vars)

    if not returns:
        raise ValueError("No return value found")

    return merge_values(returns)


def py_to_expression(func: Callable) -> expression.Expression:
    """
    Try to convert a python function to a BigQuery expression.

    This is "best effort" - if the function contains operations that cannot
    be converted to BigQuery expressions, it will raise an Exception.
    """
    py_expr = _compile_bytecode_to_py_expr(func)
    return py_exprs.resolve_py_exprs(py_expr)
