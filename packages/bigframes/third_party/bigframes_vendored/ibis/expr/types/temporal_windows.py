# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/expr/types/temporal_windows.py

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from bigframes_vendored.ibis.common.collections import FrozenOrderedDict  # noqa: TCH001
import bigframes_vendored.ibis.common.exceptions as com
from bigframes_vendored.ibis.common.grounds import Concrete
import bigframes_vendored.ibis.expr.operations as ops
from bigframes_vendored.ibis.expr.operations.relations import Unaliased  # noqa: TCH001
import bigframes_vendored.ibis.expr.types as ir
from bigframes_vendored.ibis.expr.types.relations import unwrap_aliases
from public import public

if TYPE_CHECKING:
    from collections.abc import Sequence


@public
class WindowedTable(Concrete):
    """An intermediate table expression to hold windowing information."""

    parent: ir.Table
    time_col: ops.Column
    window_type: Literal["tumble", "hop"] | None = None
    window_size: ir.IntervalScalar | None = None
    window_slide: ir.IntervalScalar | None = None
    window_offset: ir.IntervalScalar | None = None
    groups: FrozenOrderedDict[str, Unaliased[ops.Column]] | None = None
    metrics: FrozenOrderedDict[str, Unaliased[ops.Column]] | None = None

    def __init__(self, time_col: ops.Column, **kwargs):
        if time_col is None:
            raise com.IbisInputError(
                "Window aggregations require `time_col` as an argument"
            )
        super().__init__(time_col=time_col, **kwargs)

    def tumble(
        self,
        size: ir.IntervalScalar,
        offset: ir.IntervalScalar | None = None,
    ) -> WindowedTable:
        return self.copy(window_type="tumble", window_size=size, window_offset=offset)

    def hop(
        self,
        size: ir.IntervalScalar,
        slide: ir.IntervalScalar,
        offset: ir.IntervalScalar | None = None,
    ) -> WindowedTable:
        return self.copy(
            window_type="hop",
            window_size=size,
            window_slide=slide,
            window_offset=offset,
        )

    def aggregate(
        self,
        metrics: Sequence[ir.Scalar] | None = (),
        by: str | ir.Value | Sequence[str] | Sequence[ir.Value] | None = (),
        **kwargs: ir.Value,
    ) -> ir.Table:
        by = self.parent.bind(by)
        metrics = self.parent.bind(metrics, **kwargs)

        by = unwrap_aliases(by)
        metrics = unwrap_aliases(metrics)

        groups = dict(self.groups) if self.groups is not None else {}
        groups.update(by)

        return ops.WindowAggregate(
            self.parent,
            self.window_type,
            self.time_col,
            groups=groups,
            metrics=metrics,
            window_size=self.window_size,
            window_slide=self.window_slide,
            window_offset=self.window_offset,
        ).to_expr()

    agg = aggregate

    def group_by(
        self, *by: str | ir.Value | Sequence[str] | Sequence[ir.Value]
    ) -> WindowedTable:
        by = tuple(v for v in by if v is not None)
        groups = self.parent.bind(*by)
        groups = unwrap_aliases(groups)
        return self.copy(groups=groups)
