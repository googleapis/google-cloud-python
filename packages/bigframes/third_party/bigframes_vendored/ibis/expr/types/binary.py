# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/expr/types/binary.py

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from bigframes_vendored.ibis.expr import types as ir

import bigframes_vendored.ibis.expr.operations as ops
from bigframes_vendored.ibis.expr.types.generic import Column, Scalar, Value
from public import public


@public
class BinaryValue(Value):
    def hashbytes(
        self,
        how: Literal["md5", "sha1", "sha256", "sha512"] = "sha256",
    ) -> ir.BinaryValue:
        """Compute the binary hash value of `arg`.

        Parameters
        ----------
        how
            Hash algorithm to use

        Returns
        -------
        BinaryValue
            Binary expression
        """
        return ops.HashBytes(self, how).to_expr()


@public
class BinaryScalar(Scalar, BinaryValue):
    pass


@public
class BinaryColumn(Column, BinaryValue):
    pass
