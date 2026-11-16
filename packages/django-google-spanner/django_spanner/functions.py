# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

"""Various math helper functions."""

import math
import re
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from django.db.models.expressions import Func, Value
from django.db.models.functions import (
    Cast,
    Chr,
    ConcatPair,
    Cot,
    Degrees,
    JSONArray,
    Left,
    Log,
    Ord,
    Pi,
    Radians,
    Right,
    StrIndex,
    Substr,
)

if TYPE_CHECKING:
    from django.db.backends.base.base import BaseDatabaseWrapper
    from django.db.models.sql.compiler import SQLCompiler

_TYPE_PARAMS_RE = re.compile(r"\([^)]*\)")
_TYPES_MAP: Optional[Dict[type, Any]] = None


class IfNull(Func):
    """Represent SQL `IFNULL` function."""

    function = "IFNULL"
    arity = 2


def cast(self, compiler, connection, **extra_context):
    """
    A method to extend Django Cast class. Cast SQL query for given
    parameters.

    :type self: :class:`~django.db.models.functions.Cast`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    # Account for a field's max_length using SUBSTR.
    max_length = getattr(self.output_field, "max_length", None)
    if max_length is not None:
        template = "SUBSTR(" + self.template + ", 0, %s)" % max_length
    else:
        template = self.template
    return self.as_sql(compiler, connection, template=template, **extra_context)


def chr_(self, compiler, connection, **extra_context):
    """
    A method to extend Django Chr class. Returns a SQL query where the code
    points are displayed as a string.

    :type self: :class:`~django.db.models.functions.Chr`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    return self.as_sql(
        compiler,
        connection,
        template="CODE_POINTS_TO_STRING([%(expressions)s])",
        **extra_context,
    )


def concatpair(self, compiler, connection, **extra_context):
    """
    A method to extend Django ConcatPair class. Concatenates a SQL query
    into the sequence of :class:`IfNull` objects.

    :type self: :class:`~django.db.models.functions.ConcatPair`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    # Spanner's CONCAT function returns null if any of its arguments are null.
    # Prevent that by converting null arguments to an empty string.
    clone = self.copy()
    clone.set_source_expressions(
        IfNull(e, Value("")) for e in self.get_source_expressions()
    )
    return clone.as_sql(compiler, connection, **extra_context)


def cot(self, compiler, connection, **extra_context):
    """
    A method to extend Django Cot class. Returns a SQL query of calculated
    trigonometric cotangent function.

    :type self: :class:`~django.db.models.functions.Cot`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    return self.as_sql(
        compiler, connection, template="(1 / TAN(%(expressions)s))", **extra_context
    )


def degrees(self, compiler, connection, **extra_context):
    """
    A method to extend Django Degress class. Returns a SQL query of the
    angle converted to degrees.

    :type self: :class:`~django.db.models.functions.Degrees`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    return self.as_sql(
        compiler,
        connection,
        template="((%%(expressions)s) * 180 / %s)" % math.pi,
        **extra_context,
    )


def json_array(self, compiler, connection, **extra_context):
    """
    A method to extend Django JSONArray class. Returns a SQL query that
    generates a JSON array.

    :type self: :class:`~django.db.models.functions.JSONArray`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    return self.as_sql(
        compiler,
        connection,
        template="TO_JSON_STRING([%(expressions)s])",
        **extra_context,
    )


def left_and_right(self, compiler, connection, **extra_context):
    """A method to extend Django Left and Right classes.

    :type self: :class:`~django.db.models.functions.Left` or
                :class:`~django.db.models.functions.Right`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    return self.get_substr().as_spanner(compiler, connection, **extra_context)


def log(self, compiler, connection, **extra_context):
    """
    A method to extend Django Log class. Returns a SQL query of calculated
    logarithm.

    :type self: :class:`~django.db.models.functions.Log`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    # This function is usually Log(b, x) returning the logarithm of x to the
    # base b, but on Spanner it's Log(x, b).
    clone = self.copy()
    clone.set_source_expressions(self.get_source_expressions()[::-1])
    return clone.as_sql(compiler, connection, **extra_context)


def ord_(self, compiler, connection, **extra_context):
    """
    A method to extend Django Ord class. Returns a SQL query of the
    expression converted to ord.

    :type self: :class:`~django.db.models.functions.Ord`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    return self.as_sql(
        compiler,
        connection,
        template="TO_CODE_POINTS(%(expressions)s)[OFFSET(0)]",
        **extra_context,
    )


def pi(self, compiler, connection, **extra_context):
    """
    A method to extend Django Pi class. Returns a SQL query of the Pi
    constant.

    :type self: :class:`~django.db.models.functions.Pi`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    return self.as_sql(compiler, connection, template=str(math.pi), **extra_context)


def radians(self, compiler, connection, **extra_context):
    """
    A method to extend Django Radians class. Returns a SQL query of the
    angle converted to radians.

    :type self: :class:`~django.db.models.functions.Radians`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    return self.as_sql(
        compiler,
        connection,
        template="((%%(expressions)s) * %s / 180)" % math.pi,
        **extra_context,
    )


def strindex(self, compiler, connection, **extra_context):
    """
    A method to extend Django StrIndex class. Returns a SQL query of the
    string position.

    :type self: :class:`~django.db.models.functions.StrIndex`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    return self.as_sql(compiler, connection, function="STRPOS", **extra_context)


def substr(self, compiler, connection, **extra_context):
    """
    A method to extend Django Substr class. Returns a SQL query of a
    substring.

    :type self: :class:`~django.db.models.functions.Substr`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple(str, list)
    :returns: A tuple where `str` is a string containing ordered SQL parameters
              to be replaced with the elements of the `list`.
    """
    return self.as_sql(compiler, connection, function="SUBSTR", **extra_context)


def _get_types_map() -> Dict[type, Any]:
    """Lazily import ``TYPES_MAP`` to avoid loading spanner_dbapi on import."""
    global _TYPES_MAP
    if _TYPES_MAP is None:
        from google.cloud.spanner_dbapi.parse_utils import TYPES_MAP

        _TYPES_MAP = TYPES_MAP
    return _TYPES_MAP


def value_as_spanner(
    self: Value,
    compiler: "SQLCompiler",
    connection: "BaseDatabaseWrapper",
) -> Tuple[str, List[Any]]:
    """Ensure ``Value`` expressions have an explicit GoogleSQL type.

    GoogleSQL is statically typed and rejects untyped expressions (such as
    literal ``NULL`` or parameters whose Python type is not mapped in
    ``TYPES_MAP``) when no table column provides type context, such as in
    ``CheckConstraint.validate()`` or ``UNION`` queries. When ``output_field``
    defines a Spanner type, cast any untyped ``NULL`` or unmapped parameter to
    that type.

    Examples:
        - ``Value(None, output_field=IntegerField())`` -> ``("CAST(NULL AS INT64)", [])``
        - ``Value(1.5, output_field=FloatField())`` -> ``("CAST(%s AS FLOAT64)", [1.5])``
        - ``Value(1, output_field=IntegerField())`` -> ``("%s", [1])`` (mapped in ``TYPES_MAP``)
    """
    sql, parameters = self.as_sql(compiler, connection)
    output_field = self._output_field_or_none
    if output_field is None:
        return sql, parameters

    types_map = _get_types_map()
    is_untyped_null = sql == "NULL" and not parameters
    is_unmapped_param = (
        sql == "%s" and len(parameters) == 1 and type(parameters[0]) not in types_map
    )
    if not (is_untyped_null or is_unmapped_param):
        return sql, parameters

    database_type = output_field.cast_db_type(connection)
    if not database_type:
        return sql, parameters
    base_type = _TYPE_PARAMS_RE.sub("", database_type)
    if is_untyped_null or parameters[0] is None:
        return f"CAST(NULL AS {base_type})", []
    return f"CAST(%s AS {base_type})", parameters


def register_functions():
    """Register the above methods with the corersponding Django classes."""
    Cast.as_spanner = cast
    Chr.as_spanner = chr_
    ConcatPair.as_spanner = concatpair
    Cot.as_spanner = cot
    Degrees.as_spanner = degrees
    JSONArray.as_spanner = json_array
    Left.as_spanner = left_and_right
    Log.as_spanner = log
    Ord.as_spanner = ord_
    Pi.as_spanner = pi
    Radians.as_spanner = radians
    Right.as_spanner = left_and_right
    StrIndex.as_spanner = strindex
    Substr.as_spanner = substr
    Value.as_spanner = value_as_spanner
