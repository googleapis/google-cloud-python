# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/expr/operations/generic.py
"""Generic value operations."""

from __future__ import annotations

import itertools
from typing import Annotated, Any
from typing import Literal as LiteralType
from typing import Optional

from bigframes_vendored.ibis.common.annotations import attribute
from bigframes_vendored.ibis.common.deferred import Deferred  # noqa: TCH001
from bigframes_vendored.ibis.common.grounds import Singleton
from bigframes_vendored.ibis.common.patterns import InstanceOf, Length  # noqa: TCH001
from bigframes_vendored.ibis.common.typing import VarTuple  # noqa: TCH001
import bigframes_vendored.ibis.expr.datashape as ds
import bigframes_vendored.ibis.expr.datatypes as dt
from bigframes_vendored.ibis.expr.operations.core import Scalar, Unary, Value
from bigframes_vendored.ibis.expr.operations.relations import Relation  # noqa: TCH001
import bigframes_vendored.ibis.expr.rules as rlz
from public import public
from typing_extensions import TypeVar


@public
class RowID(Value):
    """The row number of the returned result."""

    name = "rowid"
    table: Relation

    shape = ds.columnar
    dtype = dt.int64

    @attribute
    def relations(self):
        return frozenset({self.table})


@public
class Cast(Value):
    """Explicitly cast a value to a specific data type."""

    arg: Value
    to: dt.DataType

    shape = rlz.shape_like("arg")

    @property
    def name(self):
        return f"{self.__class__.__name__}({self.arg.name}, {self.to})"

    @property
    def dtype(self):
        return self.to


@public
class TryCast(Value):
    """Try to cast a value to a specific data type."""

    arg: Value
    to: dt.DataType

    shape = rlz.shape_like("arg")

    @property
    def dtype(self):
        return self.to


@public
class TypeOf(Unary):
    """Return the _database_ data type of the input expression."""

    dtype = dt.string


@public
class IsNull(Unary):
    """Return true if values are null."""

    dtype = dt.boolean


@public
class NotNull(Unary):
    """Returns true if values are not null."""

    dtype = dt.boolean


@public
class NullIf(Value):
    """Return NULL if an expression equals some specific value."""

    arg: Value
    null_if_expr: Value

    dtype = rlz.dtype_like("args")
    shape = rlz.shape_like("args")


@public
class Coalesce(Value):
    """Return the first non-null expression from a tuple of expressions."""

    arg: Annotated[VarTuple[Value], Length(at_least=1)]

    shape = rlz.shape_like("arg")
    dtype = rlz.dtype_like("arg")


@public
class Greatest(Value):
    """Return the largest value from a tuple of expressions."""

    arg: Annotated[VarTuple[Value], Length(at_least=1)]

    shape = rlz.shape_like("arg")
    dtype = rlz.dtype_like("arg")


@public
class Least(Value):
    """Return the smallest value from a tuple of expressions."""

    arg: Annotated[VarTuple[Value], Length(at_least=1)]

    shape = rlz.shape_like("arg")
    dtype = rlz.dtype_like("arg")


T = TypeVar("T", bound=dt.DataType, covariant=True)


@public
class Literal(Scalar[T]):
    """A constant value."""

    value: Annotated[Any, ~InstanceOf(Deferred)]
    dtype: T

    shape = ds.scalar

    def __init__(self, value, dtype):
        # normalize ensures that the value is a valid value for the given dtype
        value = dt.normalize(dtype, value)
        super().__init__(value=value, dtype=dtype)

    @property
    def name(self):
        if self.dtype.is_interval():
            return f"{self.value!r}{self.dtype.unit.short}"
        return repr(self.value)


NULL = Literal(None, dt.null)


@public
class ScalarParameter(Scalar):
    _counter = itertools.count()

    dtype: dt.DataType
    counter: Optional[int] = None

    shape = ds.scalar

    def __init__(self, dtype, counter):
        if counter is None:
            counter = next(self._counter)
        super().__init__(dtype=dtype, counter=counter)

    @property
    def name(self):
        return f"param_{self.counter:d}"


@public
class Constant(Scalar, Singleton):
    """A function that produces a constant."""

    shape = ds.scalar


@public
class Impure(Value):
    pass


@public
class TimestampNow(Constant):
    """Return the current timestamp."""

    dtype = dt.timestamp


@public
class DateNow(Constant):
    """Return the current date."""

    dtype = dt.date


@public
class RandomScalar(Impure):
    """Return a random scalar between 0 and 1."""

    dtype = dt.float64
    shape = ds.scalar


@public
class RandomUUID(Impure):
    """Return a random UUID."""

    dtype = dt.uuid
    shape = ds.scalar


@public
class E(Constant):
    """The mathematical constant e."""

    dtype = dt.float64


@public
class Pi(Constant):
    """The mathematical constant pi."""

    dtype = dt.float64


@public
class Hash(Value):
    """Return the hash of a value."""

    arg: Value

    dtype = dt.int64
    shape = rlz.shape_like("arg")


@public
class HashBytes(Value):
    arg: Value[dt.String | dt.Binary]
    how: LiteralType[
        "md5",  # noqa: F821
        "MD5",  # noqa: F821
        "sha1",  # noqa: F821
        "SHA1",  # noqa: F821
        "SHA224",  # noqa: F821
        "sha256",  # noqa: F821
        "SHA256",  # noqa: F821
        "sha512",  # noqa: F821
        "intHash32",  # noqa: F821
        "intHash64",  # noqa: F821
        "cityHash64",  # noqa: F821
        "sipHash64",  # noqa: F821
        "sipHash128",  # noqa: F821
    ]

    dtype = dt.binary
    shape = rlz.shape_like("arg")


@public
class HexDigest(Value):
    """Return the hexadecimal digest of a value."""

    arg: Value[dt.String | dt.Binary]
    how: LiteralType[
        "md5",  # noqa: F821
        "sha1",  # noqa: F821
        "sha256",  # noqa: F821
        "sha512",  # noqa: F821
    ]

    dtype = dt.str
    shape = rlz.shape_like("arg")


# TODO(kszucs): we should merge the case operations by making the
# cases, results and default optional arguments like they are in
# api.py
@public
class SimpleCase(Value):
    """Simple case statement."""

    base: Value
    cases: VarTuple[Value]
    results: VarTuple[Value]
    default: Value

    shape = rlz.shape_like("base")

    def __init__(self, cases, results, **kwargs):
        assert len(cases) == len(results)
        super().__init__(cases=cases, results=results, **kwargs)

    @attribute
    def dtype(self):
        values = [*self.results, self.default]
        return rlz.highest_precedence_dtype(values)


@public
class SearchedCase(Value):
    """Searched case statement."""

    cases: VarTuple[Value[dt.Boolean]]
    results: VarTuple[Value]
    default: Value

    def __init__(self, cases, results, default):
        assert len(cases) == len(results)
        if default.dtype.is_null():
            default = Cast(default, rlz.highest_precedence_dtype(results))
        super().__init__(cases=cases, results=results, default=default)

    @attribute
    def shape(self):
        return rlz.highest_precedence_shape((*self.cases, *self.results, self.default))

    @attribute
    def dtype(self):
        exprs = [*self.results, self.default]
        return rlz.highest_precedence_dtype(exprs)


@public
class SqlScalar(Value):
    """Inject a SQL string as a scalar value."""

    sql_template: str
    values: VarTuple[Value]
    output_type: dt.DataType

    shape = ds.scalar

    @property
    def dtype(self):
        return self.output_type


public(NULL=NULL)
