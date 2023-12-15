# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/expr/operations/analytic.py

from __future__ import annotations

import ibis.expr.operations as ops
import ibis.expr.rules as rlz


class FirstNonNullValue(ops.Analytic):
    """Retrieve the first element."""

    arg: ops.Column
    dtype = rlz.dtype_like("arg")


class LastNonNullValue(ops.Analytic):
    """Retrieve the last element."""

    arg: ops.Column
    dtype = rlz.dtype_like("arg")


__all__ = [
    "FirstNonNullValue",
    "LastNonNullValue",
]
