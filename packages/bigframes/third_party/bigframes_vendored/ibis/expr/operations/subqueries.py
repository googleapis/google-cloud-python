# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/expr/operations/subqueries.py
"""Subquery operations."""

from __future__ import annotations

from bigframes_vendored.ibis.common.annotations import attribute
from bigframes_vendored.ibis.common.exceptions import IntegrityError
import bigframes_vendored.ibis.expr.datashape as ds
import bigframes_vendored.ibis.expr.datatypes as dt
from bigframes_vendored.ibis.expr.operations.core import Value
from bigframes_vendored.ibis.expr.operations.relations import Relation  # noqa: TCH001
import bigframes_vendored.ibis.expr.rules as rlz
from public import public


@public
class Subquery(Value):
    """Base class for subquery operations."""

    rel: Relation

    @attribute
    def relations(self):
        return frozenset()


@public
class ExistsSubquery(Subquery):
    """Check if a subquery returns any rows."""

    dtype = dt.boolean
    shape = ds.columnar


@public
class ScalarSubquery(Subquery):
    """A subquery that returns a single scalar value."""

    shape = ds.scalar

    def __init__(self, rel):
        if len(rel.schema) != 1:
            raise IntegrityError(
                "Relation passed to ScalarSubquery() must have exactly one "
                f"column, got {len(rel.schema)}"
            )
        super().__init__(rel=rel)

    @attribute
    def value(self):
        (value,) = self.rel.values.values()
        return value

    @attribute
    def dtype(self):
        return self.value.dtype


@public
class InSubquery(Subquery):
    """Check if a value is in the result of a subquery."""

    needle: Value

    dtype = dt.boolean
    shape = rlz.shape_like("needle")

    def __init__(self, rel, needle):
        if len(rel.schema) != 1:
            raise IntegrityError(
                "Relation passed to InSubquery() must have exactly one "
                f"column, got {len(rel.schema)}"
            )
        (value,) = rel.values.values()
        if not rlz.comparable(value, needle):
            raise IntegrityError(f"{needle!r} is not comparable to {value!r}")
        super().__init__(rel=rel, needle=needle)

    @attribute
    def value(self):
        (value,) = self.rel.values.values()
        return value

    @attribute
    def relations(self):
        return self.needle.relations
