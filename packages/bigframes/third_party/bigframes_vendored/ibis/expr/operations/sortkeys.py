# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/expr/operations/sortkeys.py

"""Sort key operations."""

from __future__ import annotations

from bigframes_vendored.ibis.expr.operations.core import Value
import bigframes_vendored.ibis.expr.rules as rlz
from public import public

# TODO(kszucs): move the content of this file to generic.py


# TODO(kszucs): consider to limit its shape to Columnar, we could treat random()
# as a columnar operation too
@public
class SortKey(Value):
    """A sort key."""

    # TODO(kszucs): rename expr to arg or something else except expr
    expr: Value
    ascending: bool = True
    nulls_first: bool = False

    dtype = rlz.dtype_like("expr")
    shape = rlz.shape_like("expr")

    @classmethod
    def __coerce__(cls, key, T=None, S=None):
        key = super().__coerce__(key, T=T, S=S)

        if isinstance(key, cls):
            return key
        else:
            return cls(key)

    @property
    def name(self) -> str:
        return self.expr.name

    @property
    def descending(self) -> bool:
        return not self.ascending
