# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/expr/operations/arrays.py
from __future__ import annotations

import ibis.expr.datatypes as dt
from ibis.expr.operations.core import Unary


class GenerateArray(Unary):
    """
    Generates an array of values, similar to ibis.range(), but with simpler and
    more efficient SQL generation.
    """

    dtype = dt.Array(dt.int64)


class SafeCastToDatetime(Unary):
    dtype = dt.Timestamp(timezone=None)
