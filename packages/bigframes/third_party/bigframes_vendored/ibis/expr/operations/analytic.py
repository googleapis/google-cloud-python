# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/expr/operations/analytic.py

from __future__ import annotations

import ibis
import ibis.expr.operations as ops
import ibis.expr.rules as rlz


# TODO(swast): We can remove this if ibis adds aggregates over scalar values.
# See: https://github.com/ibis-project/ibis/issues/8698
@ibis.udf.agg.builtin
def count(value: int) -> int:
    """Count of a scalar."""
    return 0  # pragma: NO COVER


class FirstNonNullValue(ops.Analytic):
    """Retrieve the first element."""

    arg: ops.Column
    dtype = rlz.dtype_like("arg")


class LastNonNullValue(ops.Analytic):
    """Retrieve the last element."""

    arg: ops.Column
    dtype = rlz.dtype_like("arg")


__all__ = [
    "count",
    "FirstNonNullValue",
    "LastNonNullValue",
]
