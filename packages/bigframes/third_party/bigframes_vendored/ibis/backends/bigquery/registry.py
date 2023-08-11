# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/backends/bigquery/registry.py
"""Module to convert from Ibis expression to SQL string."""

from ibis.backends.bigquery.registry import OPERATION_REGISTRY

import third_party.bigframes_vendored.ibis.expr.operations as vendored_ibis_ops


def _approx_quantiles(translator, op: vendored_ibis_ops.ApproximateMultiQuantile):
    arg = translator.translate(op.arg)
    num_bins = translator.translate(op.num_bins)
    return f"APPROX_QUANTILES({arg}, {num_bins})"


patched_ops = {
    vendored_ibis_ops.ApproximateMultiQuantile: _approx_quantiles,
}

OPERATION_REGISTRY.update(patched_ops)
