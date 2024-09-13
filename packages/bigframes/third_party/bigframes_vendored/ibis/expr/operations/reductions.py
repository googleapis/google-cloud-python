# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/expr/operations/reductions.py

from __future__ import annotations

import ibis.common.annotations as ibis_annotations
from ibis.common.typing import VarTuple
import ibis.expr.datatypes as dt
import ibis.expr.operations.core as ibis_ops_core
from ibis.expr.operations.reductions import Filterable, Reduction


class ArrayAggregate(Filterable, Reduction):
    """
    Collects the elements of this expression into an ordered array. Similar to
    the ibis `ArrayCollect`, but adds `order_by_*` and `distinct_only` parameters.
    """

    arg: ibis_ops_core.Column
    order_by: VarTuple[ibis_ops_core.Value] = ()

    @ibis_annotations.attribute
    def dtype(self):
        return dt.Array(self.arg.dtype)


__all__ = ["ArrayAggregate"]
