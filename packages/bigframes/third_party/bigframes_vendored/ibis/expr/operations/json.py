# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/expr/operations/json.py
"""Operations for working with JSON data."""

from __future__ import annotations

from bigframes_vendored.ibis.common.annotations import attribute
import bigframes_vendored.ibis.expr.datatypes as dt
from bigframes_vendored.ibis.expr.operations import Unary, Value
import bigframes_vendored.ibis.expr.rules as rlz
from public import public


@public
class JSONGetItem(Value):
    """Get a value from a JSON object or array."""

    arg: Value[dt.JSON]
    index: Value[dt.String | dt.Integer]

    dtype = rlz.dtype_like("arg")
    shape = rlz.shape_like("args")


@public
class ToJSONArray(Value):
    """Convert a value to an array of JSON objects."""

    arg: Value[dt.JSON]

    shape = rlz.shape_like("arg")

    @attribute
    def dtype(self) -> dt.DataType:
        return dt.Array(self.arg.dtype)


@public
class ToJSONMap(Value):
    """Convert a value to a map of string to JSON."""

    arg: Value[dt.JSON]

    shape = rlz.shape_like("arg")

    @attribute
    def dtype(self) -> dt.DataType:
        return dt.Map(dt.string, self.arg.dtype)


@public
class UnwrapJSONString(Value):
    """Unwrap a JSON string into an engine-native string."""

    arg: Value[dt.JSON]

    dtype = dt.string
    shape = rlz.shape_like("arg")


@public
class UnwrapJSONInt64(Value):
    """Unwrap a JSON number into an engine-native int64."""

    arg: Value[dt.JSON]

    dtype = dt.int64
    shape = rlz.shape_like("arg")


@public
class UnwrapJSONFloat64(Value):
    """Unwrap a JSON number into an engine-native float64."""

    arg: Value[dt.JSON]

    dtype = dt.float64
    shape = rlz.shape_like("arg")


@public
class UnwrapJSONBoolean(Value):
    """Unwrap a JSON bool into an engine-native bool."""

    arg: Value[dt.JSON]

    dtype = dt.boolean
    shape = rlz.shape_like("arg")


# TODO(swast): Remove once supported upstream.
# See: https://github.com/ibis-project/ibis/issues/9542
@public
class ToJsonString(Unary):
    dtype = dt.string
