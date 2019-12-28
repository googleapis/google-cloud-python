import math

from django.db.models.functions import (
    Cot, Degrees, Left, Log, Pi, Radians, Right, StrIndex, Substr,
)


def cot(self, compiler, connection, **extra_context):
    return self.as_sql(compiler, connection, template='(1 / TAN(%(expressions)s))', **extra_context)


def degrees(self, compiler, connection, **extra_context):
    return self.as_sql(
        compiler, connection,
        template='((%%(expressions)s) * 180 / %s)' % math.pi,
        **extra_context
    )


def left_and_right(self, compiler, connection, **extra_context):
    return self.get_substr().as_spanner(compiler, connection, **extra_context)


def log(self, compiler, connection, **extra_context):
    # This function is usually Log(b, x) returning the logarithm of x to the
    # base b, but on Spanner it's Log(x, b).
    clone = self.copy()
    clone.set_source_expressions(self.get_source_expressions()[::-1])
    return clone.as_sql(compiler, connection, **extra_context)


def pi(self, compiler, connection, **extra_context):
    return self.as_sql(compiler, connection, template=str(math.pi), **extra_context)


def radians(self, compiler, connection, **extra_context):
    return self.as_sql(
        compiler, connection,
        template='((%%(expressions)s) * %s / 180)' % math.pi,
        **extra_context
    )


def strindex(self, compiler, connection, **extra_context):
    return self.as_sql(compiler, connection, function='STRPOS', **extra_context)


def substr(self, compiler, connection, **extra_context):
    return self.as_sql(compiler, connection, function='SUBSTR', **extra_context)


def register_functions():
    Cot.as_spanner = cot
    Degrees.as_spanner = degrees
    Left.as_spanner = left_and_right
    Log.as_spanner = log
    Pi.as_spanner = pi
    Radians.as_spanner = radians
    Right.as_spanner = left_and_right
    StrIndex.as_spanner = strindex
    Substr.as_spanner = substr
