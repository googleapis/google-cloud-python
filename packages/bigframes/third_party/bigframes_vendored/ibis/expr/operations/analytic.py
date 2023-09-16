# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/expr/operations/analytic.py

from __future__ import annotations

from ibis.expr.operations.analytic import Analytic
import ibis.expr.rules as rlz


class FirstNonNullValue(Analytic):
    """Retrieve the first element."""

    arg = rlz.column(rlz.any)
    output_dtype = rlz.dtype_like("arg")


class LastNonNullValue(Analytic):
    """Retrieve the last element."""

    arg = rlz.column(rlz.any)
    output_dtype = rlz.dtype_like("arg")


__all__ = [
    "FirstNonNullValue",
    "LastNonNullValue",
]
