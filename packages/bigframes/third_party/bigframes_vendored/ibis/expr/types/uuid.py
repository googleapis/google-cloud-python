# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/expr/types/uuid.py

from __future__ import annotations

from bigframes_vendored.ibis.expr.types.generic import Column, Scalar, Value
from public import public


@public
class UUIDValue(Value):
    pass


@public
class UUIDScalar(Scalar, UUIDValue):
    pass


@public
class UUIDColumn(Column, UUIDValue):
    pass
