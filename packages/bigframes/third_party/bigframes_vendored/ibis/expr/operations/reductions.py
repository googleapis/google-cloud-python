# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/expr/operations/reductions.py

from __future__ import annotations

import ibis.expr.datatypes as dt
import ibis.expr.operations.core as ibis_ops_core
from ibis.expr.operations.reductions import Filterable, Reduction


class ApproximateMultiQuantile(Filterable, Reduction):
    """Calculate (approximately) evenly-spaced quantiles.

    See: https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_quantiles
    """

    arg: ibis_ops_core.Value
    num_bins: ibis_ops_core.Value[dt.Int64]
    dtype = dt.Array(dt.float64)


__all__ = [
    "ApproximateMultiQuantile",
]
