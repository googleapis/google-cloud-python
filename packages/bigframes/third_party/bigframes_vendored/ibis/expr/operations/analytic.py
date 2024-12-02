# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/expr/operations/analytic.py

"""Operations for analytic window functions."""

from __future__ import annotations

from typing import Optional

import bigframes_vendored.ibis.expr.datashape as ds
import bigframes_vendored.ibis.expr.datatypes as dt
from bigframes_vendored.ibis.expr.operations.core import Column, Scalar, Value
import bigframes_vendored.ibis.expr.operations.udf as ibis_udf
import bigframes_vendored.ibis.expr.rules as rlz
from public import public


@public
class Analytic(Value):
    """Base class for analytic window function operations."""

    shape = ds.columnar


class ShiftBase(Analytic):
    """Base class for shift operations."""

    arg: Column[dt.Any]
    offset: Optional[Value[dt.Integer | dt.Interval]] = None
    default: Optional[Value] = None

    dtype = rlz.dtype_like("arg")


@public
class Lag(ShiftBase):
    """Shift a column forward."""


@public
class Lead(ShiftBase):
    """Shift a column backward."""


@public
class RankBase(Analytic):
    """Base class for ranking operations."""

    dtype = dt.int64


@public
class MinRank(RankBase):
    pass


@public
class DenseRank(RankBase):
    pass


@public
class RowNumber(RankBase):
    """Compute the row number over a window, starting from 0."""


@public
class PercentRank(Analytic):
    """Compute the percentile rank over a window."""

    dtype = dt.double


@public
class CumeDist(Analytic):
    """Compute the cumulative distribution function of a column over a window."""

    dtype = dt.double


@public
class NTile(Analytic):
    """Compute the percentile of a column over a window."""

    buckets: Scalar[dt.Integer]

    dtype = dt.int64


@public
class NthValue(Analytic):
    """Retrieve the Nth element of a column over a window."""

    arg: Column[dt.Any]
    nth: Value[dt.Integer]

    dtype = rlz.dtype_like("arg")


public(AnalyticOp=Analytic)


# TODO(swast): We can remove this if ibis adds aggregates over scalar values.
# See: https://github.com/ibis-project/ibis/issues/8698
@public
@ibis_udf.agg.builtin
def count(value: int) -> int:
    """Count of a scalar."""
    return 0  # pragma: NO COVER


@public
class FirstNonNullValue(Analytic):
    """Retrieve the first element."""

    arg: Column
    dtype = rlz.dtype_like("arg")


@public
class LastNonNullValue(Analytic):
    """Retrieve the last element."""

    arg: Column
    dtype = rlz.dtype_like("arg")
