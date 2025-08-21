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

import dataclasses
from typing import cast

import numpy as np
import pandas as pd

from bigframes import dtypes
from bigframes.core import bigframe_node, expression
from bigframes.core.rewrite import op_lowering
from bigframes.operations import (
    comparison_ops,
    datetime_ops,
    generic_ops,
    json_ops,
    numeric_ops,
)
import bigframes.operations as ops

# TODO: Would be more precise to actually have separate op set for polars ops (where they diverge from the original ops)


@dataclasses.dataclass
class CoerceArgsRule(op_lowering.OpLoweringRule):
    op_type: type[ops.BinaryOp]

    @property
    def op(self) -> type[ops.ScalarOp]:
        return self.op_type

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, self.op_type)
        larg, rarg = _coerce_comparables(expr.children[0], expr.children[1])
        return expr.op.as_expr(larg, rarg)


class LowerAddRule(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return numeric_ops.AddOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, numeric_ops.AddOp)
        larg, rarg = expr.children[0], expr.children[1]

        if (
            larg.output_type == dtypes.BOOL_DTYPE
            and rarg.output_type == dtypes.BOOL_DTYPE
        ):
            int_result = expr.op.as_expr(
                ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(larg),
                ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(rarg),
            )
            return ops.AsTypeOp(to_type=dtypes.BOOL_DTYPE).as_expr(int_result)

        if dtypes.is_string_like(larg.output_type) and dtypes.is_string_like(
            rarg.output_type
        ):
            return ops.strconcat_op.as_expr(larg, rarg)

        if larg.output_type == dtypes.BOOL_DTYPE:
            larg = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(larg)
        if rarg.output_type == dtypes.BOOL_DTYPE:
            rarg = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(rarg)

        if (
            larg.output_type == dtypes.DATE_DTYPE
            and rarg.output_type == dtypes.TIMEDELTA_DTYPE
        ):
            larg = ops.AsTypeOp(to_type=dtypes.DATETIME_DTYPE).as_expr(larg)

        if (
            larg.output_type == dtypes.TIMEDELTA_DTYPE
            and rarg.output_type == dtypes.DATE_DTYPE
        ):
            rarg = ops.AsTypeOp(to_type=dtypes.DATETIME_DTYPE).as_expr(rarg)

        return expr.op.as_expr(larg, rarg)


class LowerSubRule(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return numeric_ops.SubOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, numeric_ops.SubOp)
        larg, rarg = expr.children[0], expr.children[1]

        if (
            larg.output_type == dtypes.BOOL_DTYPE
            and rarg.output_type == dtypes.BOOL_DTYPE
        ):
            int_result = expr.op.as_expr(
                ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(larg),
                ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(rarg),
            )
            return ops.AsTypeOp(to_type=dtypes.BOOL_DTYPE).as_expr(int_result)

        if larg.output_type == dtypes.BOOL_DTYPE:
            larg = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(larg)
        if rarg.output_type == dtypes.BOOL_DTYPE:
            rarg = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(rarg)

        if (
            larg.output_type == dtypes.DATE_DTYPE
            and rarg.output_type == dtypes.TIMEDELTA_DTYPE
        ):
            larg = ops.AsTypeOp(to_type=dtypes.DATETIME_DTYPE).as_expr(larg)

        return expr.op.as_expr(larg, rarg)


@dataclasses.dataclass
class LowerMulRule(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return numeric_ops.MulOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, numeric_ops.MulOp)
        larg, rarg = expr.children[0], expr.children[1]

        if (
            larg.output_type == dtypes.BOOL_DTYPE
            and rarg.output_type == dtypes.BOOL_DTYPE
        ):
            int_result = expr.op.as_expr(
                ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(larg),
                ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(rarg),
            )
            return ops.AsTypeOp(to_type=dtypes.BOOL_DTYPE).as_expr(int_result)

        if (
            larg.output_type == dtypes.BOOL_DTYPE
            and rarg.output_type != dtypes.BOOL_DTYPE
        ):
            larg = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(larg)
        if (
            rarg.output_type == dtypes.BOOL_DTYPE
            and larg.output_type != dtypes.BOOL_DTYPE
        ):
            rarg = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(rarg)

        return expr.op.as_expr(larg, rarg)


class LowerDivRule(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return numeric_ops.DivOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, numeric_ops.DivOp)

        dividend = expr.children[0]
        divisor = expr.children[1]

        if dividend.output_type == dtypes.TIMEDELTA_DTYPE and dtypes.is_numeric(
            divisor.output_type
        ):
            # exact same as floordiv impl for timedelta
            numeric_result = ops.floordiv_op.as_expr(
                ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(dividend), divisor
            )
            int_result = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(numeric_result)
            return ops.AsTypeOp(to_type=dtypes.TIMEDELTA_DTYPE).as_expr(int_result)

        if (
            dividend.output_type == dtypes.BOOL_DTYPE
            and divisor.output_type == dtypes.BOOL_DTYPE
        ):
            int_result = expr.op.as_expr(
                ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(dividend),
                ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(divisor),
            )
            return ops.AsTypeOp(to_type=dtypes.BOOL_DTYPE).as_expr(int_result)

        # polars divide doesn't like bools, convert to int always
        # convert numerics to float always
        if dividend.output_type == dtypes.BOOL_DTYPE:
            dividend = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(dividend)
        elif dividend.output_type in (dtypes.BIGNUMERIC_DTYPE, dtypes.NUMERIC_DTYPE):
            dividend = ops.AsTypeOp(to_type=dtypes.FLOAT_DTYPE).as_expr(dividend)
        if divisor.output_type == dtypes.BOOL_DTYPE:
            divisor = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(divisor)

        return numeric_ops.div_op.as_expr(dividend, divisor)


class LowerFloorDivRule(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return numeric_ops.FloorDivOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, numeric_ops.FloorDivOp)

        dividend = expr.children[0]
        divisor = expr.children[1]

        if (
            dividend.output_type == dtypes.TIMEDELTA_DTYPE
            and divisor.output_type == dtypes.TIMEDELTA_DTYPE
        ):
            int_result = expr.op.as_expr(
                ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(dividend),
                ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(divisor),
            )
            return int_result
        if dividend.output_type == dtypes.TIMEDELTA_DTYPE and dtypes.is_numeric(
            divisor.output_type
        ):
            # this is pretty fragile as zero will break it, and must fit back into int
            numeric_result = expr.op.as_expr(
                ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(dividend), divisor
            )
            int_result = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(numeric_result)
            return ops.AsTypeOp(to_type=dtypes.TIMEDELTA_DTYPE).as_expr(int_result)

        if dividend.output_type == dtypes.BOOL_DTYPE:
            dividend = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(dividend)
        if divisor.output_type == dtypes.BOOL_DTYPE:
            divisor = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(divisor)

        if expr.output_type != dtypes.FLOAT_DTYPE:
            # need to guard against zero divisor
            # multiply dividend in this case to propagate nulls
            return ops.where_op.as_expr(
                ops.mul_op.as_expr(dividend, expression.const(0)),
                ops.eq_op.as_expr(divisor, expression.const(0)),
                numeric_ops.floordiv_op.as_expr(dividend, divisor),
            )
        else:
            return expr.op.as_expr(dividend, divisor)


class LowerModRule(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return numeric_ops.ModOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        og_expr = expr
        assert isinstance(expr.op, numeric_ops.ModOp)
        larg, rarg = expr.children[0], expr.children[1]

        if (
            larg.output_type == dtypes.TIMEDELTA_DTYPE
            and rarg.output_type == dtypes.TIMEDELTA_DTYPE
        ):
            larg_int = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(larg)
            rarg_int = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(rarg)
            int_result = expr.op.as_expr(larg_int, rarg_int)
            w_zero_handling = ops.where_op.as_expr(
                int_result,
                ops.ne_op.as_expr(rarg_int, expression.const(0)),
                ops.mul_op.as_expr(rarg_int, expression.const(0)),
            )
            return ops.AsTypeOp(to_type=dtypes.TIMEDELTA_DTYPE).as_expr(w_zero_handling)

        if larg.output_type == dtypes.BOOL_DTYPE:
            larg = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(larg)
        if rarg.output_type == dtypes.BOOL_DTYPE:
            rarg = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(rarg)

        wo_bools = expr.op.as_expr(larg, rarg)

        if og_expr.output_type == dtypes.INT_DTYPE:
            return ops.where_op.as_expr(
                wo_bools,
                ops.ne_op.as_expr(rarg, expression.const(0)),
                ops.mul_op.as_expr(rarg, expression.const(0)),
            )
        return wo_bools


class LowerAsTypeRule(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return ops.AsTypeOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, ops.AsTypeOp)
        return _lower_cast(expr.op, expr.inputs[0])


def invert_bytes(byte_string):
    inverted_bytes = ~np.frombuffer(byte_string, dtype=np.uint8)
    return inverted_bytes.tobytes()


class LowerInvertOp(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return generic_ops.InvertOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, generic_ops.InvertOp)
        arg = expr.children[0]
        if arg.output_type == dtypes.BYTES_DTYPE:
            return generic_ops.PyUdfOp(invert_bytes, dtypes.BYTES_DTYPE).as_expr(
                expr.inputs[0]
            )
        return expr


class LowerIsinOp(op_lowering.OpLoweringRule):
    @property
    def op(self) -> type[ops.ScalarOp]:
        return generic_ops.IsInOp

    def lower(self, expr: expression.OpExpression) -> expression.Expression:
        assert isinstance(expr.op, generic_ops.IsInOp)
        arg = expr.children[0]
        new_values = []
        match_nulls = False
        for val in expr.op.values:
            # coercible, non-coercible
            # float NaN/inf should be treated as distinct from 'true' null values
            if cast(bool, pd.isna(val)) and not isinstance(val, float):
                if expr.op.match_nulls:
                    match_nulls = True
            elif dtypes.is_compatible(val, arg.output_type):
                new_values.append(val)
            else:
                pass

        new_isin = ops.IsInOp(tuple(new_values), match_nulls=False).as_expr(arg)
        if match_nulls:
            return ops.coalesce_op.as_expr(new_isin, expression.const(True))
        else:
            # polars propagates nulls, so need to coalesce to false
            return ops.coalesce_op.as_expr(new_isin, expression.const(False))


def _coerce_comparables(
    expr1: expression.Expression,
    expr2: expression.Expression,
    *,
    bools_only: bool = False
):
    if bools_only:
        if (
            expr1.output_type != dtypes.BOOL_DTYPE
            and expr2.output_type != dtypes.BOOL_DTYPE
        ):
            return expr1, expr2

    target_type = dtypes.coerce_to_common(expr1.output_type, expr2.output_type)
    if expr1.output_type != target_type:
        expr1 = _lower_cast(ops.AsTypeOp(target_type), expr1)
    if expr2.output_type != target_type:
        expr2 = _lower_cast(ops.AsTypeOp(target_type), expr2)
    return expr1, expr2


def _lower_cast(cast_op: ops.AsTypeOp, arg: expression.Expression):
    if arg.output_type == cast_op.to_type:
        return arg

    if arg.output_type == dtypes.JSON_DTYPE:
        return json_ops.JSONDecode(cast_op.to_type).as_expr(arg)
    if (
        arg.output_type == dtypes.STRING_DTYPE
        and cast_op.to_type == dtypes.DATETIME_DTYPE
    ):
        return datetime_ops.ParseDatetimeOp().as_expr(arg)
    if (
        arg.output_type == dtypes.STRING_DTYPE
        and cast_op.to_type == dtypes.TIMESTAMP_DTYPE
    ):
        return datetime_ops.ParseTimestampOp().as_expr(arg)
    # date -> string casting
    if (
        arg.output_type == dtypes.DATETIME_DTYPE
        and cast_op.to_type == dtypes.STRING_DTYPE
    ):
        return datetime_ops.StrftimeOp("%Y-%m-%d %H:%M:%S").as_expr(arg)
    if arg.output_type == dtypes.TIME_DTYPE and cast_op.to_type == dtypes.STRING_DTYPE:
        return datetime_ops.StrftimeOp("%H:%M:%S.%6f").as_expr(arg)
    if (
        arg.output_type == dtypes.TIMESTAMP_DTYPE
        and cast_op.to_type == dtypes.STRING_DTYPE
    ):
        return datetime_ops.StrftimeOp("%Y-%m-%d %H:%M:%S%.6f%:::z").as_expr(arg)
    if arg.output_type == dtypes.BOOL_DTYPE and cast_op.to_type == dtypes.STRING_DTYPE:
        # bool -> decimal needs two-step cast
        new_arg = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(arg)
        is_true_cond = ops.eq_op.as_expr(arg, expression.const(True))
        is_false_cond = ops.eq_op.as_expr(arg, expression.const(False))
        return ops.CaseWhenOp().as_expr(
            is_true_cond,
            expression.const("True"),
            is_false_cond,
            expression.const("False"),
        )
    if arg.output_type == dtypes.BOOL_DTYPE and dtypes.is_numeric(cast_op.to_type):
        # bool -> decimal needs two-step cast
        new_arg = ops.AsTypeOp(to_type=dtypes.INT_DTYPE).as_expr(arg)
        return cast_op.as_expr(new_arg)
    if arg.output_type == dtypes.TIME_DTYPE and dtypes.is_numeric(cast_op.to_type):
        # polars cast gives nanoseconds, so convert to microseconds
        return numeric_ops.floordiv_op.as_expr(
            cast_op.as_expr(arg), expression.const(1000)
        )
    if dtypes.is_numeric(arg.output_type) and cast_op.to_type == dtypes.TIME_DTYPE:
        return cast_op.as_expr(ops.mul_op.as_expr(expression.const(1000), arg))
    return cast_op.as_expr(arg)


LOWER_COMPARISONS = tuple(
    CoerceArgsRule(op)
    for op in (
        comparison_ops.EqOp,
        comparison_ops.EqNullsMatchOp,
        comparison_ops.NeOp,
        comparison_ops.LtOp,
        comparison_ops.GtOp,
        comparison_ops.LeOp,
        comparison_ops.GeOp,
    )
)

POLARS_LOWERING_RULES = (
    *LOWER_COMPARISONS,
    LowerAddRule(),
    LowerSubRule(),
    LowerMulRule(),
    LowerDivRule(),
    LowerFloorDivRule(),
    LowerModRule(),
    LowerAsTypeRule(),
    LowerInvertOp(),
    LowerIsinOp(),
)


def lower_ops_to_polars(root: bigframe_node.BigFrameNode) -> bigframe_node.BigFrameNode:
    return op_lowering.lower_ops(root, rules=POLARS_LOWERING_RULES)
