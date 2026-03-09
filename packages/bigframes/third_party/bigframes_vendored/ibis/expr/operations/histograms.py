# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/expr/operations/histograms.py

"""Operations for computing histograms."""

from __future__ import annotations

import numbers  # noqa: TCH003
from typing import Literal

from bigframes_vendored.ibis.common.annotations import attribute, ValidationError
from bigframes_vendored.ibis.common.typing import VarTuple  # noqa: TCH001
import bigframes_vendored.ibis.expr.datashape as ds
import bigframes_vendored.ibis.expr.datatypes as dt
from bigframes_vendored.ibis.expr.operations.core import Column, Value
from public import public


@public
class Bucket(Value):
    """Compute the bucket number of a numeric column."""

    arg: Column[dt.Numeric | dt.Boolean]
    buckets: VarTuple[numbers.Real]
    closed: Literal["left", "right"] = "left"
    close_extreme: bool = True
    include_under: bool = False
    include_over: bool = False

    shape = ds.columnar

    @attribute
    def dtype(self):
        return dt.infer(self.nbuckets)

    def __init__(self, buckets, include_under, include_over, **kwargs):
        if not buckets:
            raise ValidationError("Must be at least one bucket edge")
        elif len(buckets) == 1:
            if not include_under or not include_over:
                raise ValidationError(
                    "If one bucket edge provided, must have "
                    "include_under=True and include_over=True"
                )
        super().__init__(
            buckets=buckets,
            include_under=include_under,
            include_over=include_over,
            **kwargs,
        )

    @property
    def nbuckets(self):
        return len(self.buckets) - 1 + self.include_over + self.include_under
