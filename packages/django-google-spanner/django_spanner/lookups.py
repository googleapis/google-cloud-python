# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from typing import TYPE_CHECKING, Any, Tuple

from django.db.models.fields.json import (
    HasKeyLookup,
    KeyTextTransform,
    KeyTransform,
    KeyTransformIExact,
)
from django.db.models.lookups import (
    Contains,
    EndsWith,
    Exact,
    GreaterThan,
    GreaterThanOrEqual,
    IContains,
    IEndsWith,
    IExact,
    IRegex,
    IStartsWith,
    LessThan,
    LessThanOrEqual,
    Lookup,
    Regex,
    StartsWith,
)

if TYPE_CHECKING:
    from django.db.backends.base.base import BaseDatabaseWrapper
    from django.db.models.sql.compiler import SQLCompiler


def _pattern_lookup_sql(
    lookup: "Lookup",
    compiler: "SQLCompiler",
    connection: "BaseDatabaseWrapper",
    *,
    strip_left: int,
    strip_right: int,
) -> Tuple[str, str, Tuple[Any, ...]]:
    """Compile a string pattern lookup using literal Spanner string functions.

    Django's PatternLookup.process_rhs wraps direct scalar values with leading
    or trailing '%' wildcards. Strip those added wildcards when present and
    cast the RHS expression to STRING (wrapped in UPPER for case-insensitive
    lookups) so equality, STRPOS, STARTS_WITH, and ENDS_WITH treat all
    characters literally.
    """
    lhs_sql, lhs_params = lookup.process_lhs(compiler, connection)
    # For plain and JSON iexact lookups, call Lookup.process_rhs directly:
    # Spanner needs neither prep_for_iexact_query nor KeyTransformIExact's
    # MySQL-only logic, and IExact.process_rhs crashes when a subquery returns
    # tuple params and tries to assign params[0] in place.
    if isinstance(lookup, IExact) and type(lookup).process_rhs in (
        IExact.process_rhs,
        KeyTransformIExact.process_rhs,
    ):
        rhs_sql, rhs_params = Lookup.process_rhs(lookup, compiler, connection)
    else:
        rhs_sql, rhs_params = lookup.process_rhs(compiler, connection)
    params = list(lhs_params)
    params.extend(rhs_params)
    # For direct Python values (e.g. float or Decimal), send str(val) so
    # CAST(%s AS STRING) preserves formatting and works across parameter types,
    # after stripping any '%' wildcards Django added. SQL expressions handle
    # their own casts.
    if lookup.rhs_is_direct_value() and rhs_params and not lookup.bilateral_transforms:
        rhs_index = len(lhs_params)
        value = str(params[rhs_index])
        end = -strip_right if strip_right else None
        params[rhs_index] = value[strip_left:end]
    rhs_cast = f"CAST({rhs_sql} AS STRING)"
    if lookup.lookup_name.startswith("i"):
        rhs_cast = f"UPPER({rhs_cast})"
    return lhs_sql, rhs_cast, tuple(params)


def iexact(self, compiler, connection):
    """A method to extend Django IExact class.

    :type self: :class:`~django.db.models.lookups.IExact`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompiler`
    :param compiler: The query compiler responsible for generating the query.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple[str, tuple]
    :returns: A tuple of the SQL request and parameters.
    """
    lhs_sql, rhs_cast, params = _pattern_lookup_sql(
        self, compiler, connection, strip_left=0, strip_right=0
    )
    return f"{lhs_sql} = {rhs_cast}", params


def contains(self, compiler, connection):
    """A method to extend Django Contains and IContains classes.

    :type self: :class:`~django.db.models.lookups.Contains` or
                :class:`~django.db.models.lookups.IContains`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompiler`
    :param compiler: The query compiler responsible for generating the query.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple[str, tuple]
    :returns: A tuple of the SQL request and parameters.
    """
    lhs_sql, rhs_cast, params = _pattern_lookup_sql(
        self, compiler, connection, strip_left=1, strip_right=1
    )
    return f"STRPOS({lhs_sql}, {rhs_cast}) > 0", params


def regex(self, compiler, connection):
    """A method to extend Django Regex and IRegex classes.

    :type self: :class:`~django.db.models.lookups.Regex` or
                :class:`~django.db.models.lookups.IRegex`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompiler`
    :param compiler: The query compiler responsible for generating the query.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple[str, tuple]
    :returns: A tuple of the SQL request and parameters.
    """
    lhs_sql, lhs_params = self.process_lhs(compiler, connection)
    rhs_sql, rhs_params = self.process_rhs(compiler, connection)
    params = list(lhs_params)
    params.extend(rhs_params)
    is_iregex = self.lookup_name.startswith("i")
    if self.rhs_is_direct_value() and rhs_params and not self.bilateral_transforms:
        rhs_sql = self.get_rhs_op(connection, rhs_sql)
        rhs_idx = len(lhs_params)
        if is_iregex:
            params[rhs_idx] = "(?i)%s" % params[rhs_idx]
        else:
            params[rhs_idx] = str(params[rhs_idx])
        # rhs_sql is REGEXP_CONTAINS(%s, %%s), and lhs_sql is the column name.
        return rhs_sql % lhs_sql, tuple(params)
    else:
        # rhs_sql is the expression/column to use as the base of the regular
        # expression.
        if is_iregex:
            rhs_sql = "CONCAT('(?i)', " + rhs_sql + ")"
        return "REGEXP_CONTAINS(%s, %s)" % (lhs_sql, rhs_sql), tuple(params)


def startswith_endswith(self, compiler, connection):
    """A method to extend Django StartsWith, IStartsWith, EndsWith, and
    IEndsWith classes.

    :type self: :class:`~django.db.models.lookups.StartsWith` or
                :class:`~django.db.models.lookups.IStartsWith` or
                :class:`~django.db.models.lookups.EndsWith` or
                :class:`~django.db.models.lookups.IEndsWith`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompiler`
    :param compiler: The query compiler responsible for generating the query.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple[str, tuple]
    :returns: A tuple of the SQL request and parameters.
    """
    is_endswith = "endswith" in self.lookup_name
    lhs_sql, rhs_cast, params = _pattern_lookup_sql(
        self,
        compiler,
        connection,
        strip_left=1 if is_endswith else 0,
        strip_right=0 if is_endswith else 1,
    )
    function = "ENDS_WITH" if is_endswith else "STARTS_WITH"
    return f"{function}({lhs_sql}, {rhs_cast})", params


def cast_param_to_float(self, compiler, connection):
    """A method to extend Django Exact, GreaterThan, GreaterThanOrEqual,
    LessThan, and LessThanOrEqual classes.

    :type self: :class:`~django.db.models.lookups.Exact` or
                :class:`~django.db.models.lookups.GreaterThan` or
                :class:`~django.db.models.lookups.GreaterThanOrEqual` or
                :class:`~django.db.models.lookups.LessThan` or
                :class:`~django.db.models.lookups.LessThanOrEqual`
    :param self: the instance of the class that owns this method.

    :type compiler: :class:`~django_spanner.compiler.SQLCompilerst`
    :param compiler: The query compiler responsible for generating the query.
                     Must have a compile method, returning a (sql, [params])
                     tuple. Calling compiler(value) will return a quoted
                     `value`.

    :type connection: :class:`~google.cloud.spanner_dbapi.connection.Connection`
    :param connection: The Spanner database connection used for the current
                       query.

    :rtype: tuple[str, str]
    :returns: A tuple of the SQL request and float parameters.
    """
    sql, params = self.as_sql(compiler, connection)
    params = list(params) if params else []
    if params:
        # Cast remote field lookups that must be integer but come in as string.
        if hasattr(self.lhs.output_field, "get_path_info"):
            for i, field in enumerate(
                self.lhs.output_field.get_path_info()[-1].target_fields
            ):
                if field.rel_db_type(connection) == "INT64" and isinstance(
                    params[i], str
                ):
                    params[i] = int(params[i])
    return sql, tuple(params)


def _compile_json_path(connection, key_transforms):
    if hasattr(connection.ops, "compile_json_path"):
        return connection.ops.compile_json_path(key_transforms)
    from django.db.models.fields.json import compile_json_path

    return compile_json_path(key_transforms)


def _quote_json_path(json_path):
    """Inline a compiled JSONPath as a safely escaped GoogleSQL string literal."""
    escaped = json_path.replace("\\", "\\\\").replace("'", "\\'").replace("%", "%%")
    return f"'{escaped}'"


def key_transform_as_spanner(self, compiler, connection):
    lhs, params, key_transforms = self.preprocess_lhs(compiler, connection)
    json_path = _quote_json_path(_compile_json_path(connection, key_transforms))
    return f"JSON_QUERY({lhs}, {json_path})", tuple(params)


def key_text_transform_as_spanner(self, compiler, connection):
    lhs, params, key_transforms = self.preprocess_lhs(compiler, connection)
    json_path = _quote_json_path(_compile_json_path(connection, key_transforms))
    return f"JSON_VALUE({lhs}, {json_path})", tuple(params)


def has_key_lookup_as_spanner(self, compiler, connection):
    sql_parts = []
    params = []
    for lhs_sql, lhs_params, rhs_json_path in self._as_sql_parts(compiler, connection):
        json_path = _quote_json_path(rhs_json_path)
        sql_parts.append(f"JSON_QUERY({lhs_sql}, {json_path}) IS NOT NULL")
        params.extend(lhs_params)
    return self._combine_sql_parts(sql_parts), tuple(params)


def register_lookups():
    """Registers the above methods with the corersponding Django classes."""
    Contains.as_spanner = contains
    IContains.as_spanner = contains
    IExact.as_spanner = iexact
    Regex.as_spanner = regex
    IRegex.as_spanner = regex
    EndsWith.as_spanner = startswith_endswith
    IEndsWith.as_spanner = startswith_endswith
    StartsWith.as_spanner = startswith_endswith
    IStartsWith.as_spanner = startswith_endswith
    Exact.as_spanner = cast_param_to_float
    GreaterThan.as_spanner = cast_param_to_float
    GreaterThanOrEqual.as_spanner = cast_param_to_float
    LessThan.as_spanner = cast_param_to_float
    LessThanOrEqual.as_spanner = cast_param_to_float
    KeyTransform.as_spanner = key_transform_as_spanner
    KeyTextTransform.as_spanner = key_text_transform_as_spanner
    HasKeyLookup.as_spanner = has_key_lookup_as_spanner
