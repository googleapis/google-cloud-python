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

import bigframes_vendored.sqlglot as sg
import bigframes_vendored.sqlglot.expressions as sge

from bigframes import dtypes
from bigframes.core.compile.sqlglot.expressions import typed_expr


def round_towards_zero(expr: sge.Expression):
    """
    Round a float value to to an integer, always rounding towards zero.

    This is used to handle duration/timedelta emulation mostly.
    """
    return sge.Cast(
        this=sge.If(
            this=sge.GT(this=expr, expression=sge.convert(0)),
            true=sge.Floor(this=expr),
            false=sge.Ceil(this=expr),
        ),
        to="INT64",
    )


def _to_nullable_bool(expr: typed_expr.TypedExpr) -> sge.Expression:
    """
    Cast the value of an expression to bool based on its truthiness. If the value is null, the result is null.
    """
    from_type = expr.dtype
    sg_expr = expr.expr

    if from_type == dtypes.BOOL_DTYPE:
        return sg_expr
    elif dtypes.is_numeric(from_type):
        return sge.NEQ(this=sg_expr, expression=sge.convert(0))
    elif dtypes.is_string_like(from_type):
        return sge.GT(this=sge.func("LENGTH", sg_expr), expression=sge.convert(0))
    elif dtypes.is_array_like(from_type):
        return sge.GT(this=sge.func("ARRAY_LENGTH", sg_expr), expression=sge.convert(0))

    return sge.Is(
        this=sge.paren(sg_expr, copy=False),
        expression=sg.not_(sge.Null(), copy=False),
    )
