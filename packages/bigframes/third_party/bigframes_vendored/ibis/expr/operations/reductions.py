# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/expr/operations/reductions.py

from __future__ import annotations

import ibis.expr.datatypes as dt
from ibis.expr.operations.reductions import Filterable, Reduction
import ibis.expr.rules as rlz


class ApproximateMultiQuantile(Filterable, Reduction):
    """Calculate (approximately) evenly-spaced quantiles.

    See: https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_quantiles
    """

    arg = rlz.any
    num_bins = rlz.value(dt.int64)
    output_dtype = dt.Array(dt.float64)


__all__ = [
    "ApproximateMultiQuantile",
]
