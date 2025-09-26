# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/expr/operations/maps.py

"""Operations for working with maps."""

from __future__ import annotations

from typing import Optional

from bigframes_vendored.ibis.common.annotations import attribute
import bigframes_vendored.ibis.expr.datatypes as dt
from bigframes_vendored.ibis.expr.operations.core import Value
import bigframes_vendored.ibis.expr.rules as rlz
from public import public


@public
class AIGenerateBool(Value):
    """Generate Bool based on the prompt"""

    prompt: Value
    connection_id: Value[dt.String]
    endpoint: Optional[Value[dt.String]]
    request_type: Value[dt.String]
    model_params: Optional[Value[dt.String]]

    shape = rlz.shape_like("prompt")

    @attribute
    def dtype(self) -> dt.Struct:
        return dt.Struct.from_tuples(
            (("result", dt.bool), ("full_resposne", dt.string), ("status", dt.string))
        )


@public
class AIGenerateInt(Value):
    """Generate integers based on the prompt"""

    prompt: Value
    connection_id: Value[dt.String]
    endpoint: Optional[Value[dt.String]]
    request_type: Value[dt.String]
    model_params: Optional[Value[dt.String]]

    shape = rlz.shape_like("prompt")

    @attribute
    def dtype(self) -> dt.Struct:
        return dt.Struct.from_tuples(
            (("result", dt.int64), ("full_resposne", dt.string), ("status", dt.string))
        )


@public
class AIGenerateDouble(Value):
    """Generate integers based on the prompt"""

    prompt: Value
    connection_id: Value[dt.String]
    endpoint: Optional[Value[dt.String]]
    request_type: Value[dt.String]
    model_params: Optional[Value[dt.String]]

    shape = rlz.shape_like("prompt")

    @attribute
    def dtype(self) -> dt.Struct:
        return dt.Struct.from_tuples(
            (
                ("result", dt.float64),
                ("full_resposne", dt.string),
                ("status", dt.string),
            )
        )
