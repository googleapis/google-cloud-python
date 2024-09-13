# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/expr/operations/json.py
from __future__ import annotations

import ibis.expr.datatypes as dt
import ibis.expr.operations.core as ibis_ops_core


# TODO(swast): Remove once supported upstream.
# See: https://github.com/ibis-project/ibis/issues/9542
class ToJsonString(ibis_ops_core.Unary):
    dtype = dt.string
