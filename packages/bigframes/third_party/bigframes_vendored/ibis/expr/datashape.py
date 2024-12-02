# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/expr/datashape.py

from __future__ import annotations

from typing import Any

from bigframes_vendored.ibis.common.grounds import Singleton
from public import public


@public
class DataShape(Singleton):
    ndim: int
    SCALAR: Scalar
    COLUMNAR: Columnar

    def is_scalar(self) -> bool:
        return self.ndim == 0

    def is_columnar(self) -> bool:
        return self.ndim == 1

    def is_tabular(self) -> bool:
        return self.ndim == 2

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, DataShape):
            return NotImplemented
        return self.ndim < other.ndim

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, DataShape):
            return NotImplemented
        return self.ndim <= other.ndim

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DataShape):
            return NotImplemented
        return self.ndim == other.ndim

    def __hash__(self) -> int:
        return hash((self.__class__, self.ndim))


@public
class Scalar(DataShape):
    ndim = 0


@public
class Columnar(DataShape):
    ndim = 1


@public
class Tabular(DataShape):
    ndim = 2


# for backward compat
DataShape.SCALAR = Scalar()
DataShape.COLUMNAR = Columnar()
DataShape.TABULAR = Tabular()

scalar = Scalar()
columnar = Columnar()
tabular = Tabular()


public(Any=DataShape)
