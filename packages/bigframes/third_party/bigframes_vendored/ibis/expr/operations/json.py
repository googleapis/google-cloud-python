# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/expr/operations/json.py
from __future__ import annotations

import ibis.expr.datatypes as dt
import ibis.expr.operations.core as ibis_ops_core


class ToJsonString(ibis_ops_core.Unary):
    dtype = dt.string
