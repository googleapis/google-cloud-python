# Copyright 2020 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"SQL parsing and classification utils."

import datetime
import decimal
import re
from functools import reduce

import sqlparse
from google.cloud import spanner_v1 as spanner

from .exceptions import Error, ProgrammingError
from .parser import parse_values
from .types import DateStr, TimestampStr
from .utils import sanitize_literals_for_upload

TYPES_MAP = {
    bool: spanner.param_types.BOOL,
    bytes: spanner.param_types.BYTES,
    str: spanner.param_types.STRING,
    int: spanner.param_types.INT64,
    float: spanner.param_types.FLOAT64,
    datetime.datetime: spanner.param_types.TIMESTAMP,
    datetime.date: spanner.param_types.DATE,
    DateStr: spanner.param_types.DATE,
    TimestampStr: spanner.param_types.TIMESTAMP,
}

SPANNER_RESERVED_KEYWORDS = {
    "ALL",
    "AND",
    "ANY",
    "ARRAY",
    "AS",
    "ASC",
    "ASSERT_ROWS_MODIFIED",
    "AT",
    "BETWEEN",
    "BY",
    "CASE",
    "CAST",
    "COLLATE",
    "CONTAINS",
    "CREATE",
    "CROSS",
    "CUBE",
    "CURRENT",
    "DEFAULT",
    "DEFINE",
    "DESC",
    "DISTINCT",
    "DROP",
    "ELSE",
    "END",
    "ENUM",
    "ESCAPE",
    "EXCEPT",
    "EXCLUDE",
    "EXISTS",
    "EXTRACT",
    "FALSE",
    "FETCH",
    "FOLLOWING",
    "FOR",
    "FROM",
    "FULL",
    "GROUP",
    "GROUPING",
    "GROUPS",
    "HASH",
    "HAVING",
    "IF",
    "IGNORE",
    "IN",
    "INNER",
    "INTERSECT",
    "INTERVAL",
    "INTO",
    "IS",
    "JOIN",
    "LATERAL",
    "LEFT",
    "LIKE",
    "LIMIT",
    "LOOKUP",
    "MERGE",
    "NATURAL",
    "NEW",
    "NO",
    "NOT",
    "NULL",
    "NULLS",
    "OF",
    "ON",
    "OR",
    "ORDER",
    "OUTER",
    "OVER",
    "PARTITION",
    "PRECEDING",
    "PROTO",
    "RANGE",
    "RECURSIVE",
    "RESPECT",
    "RIGHT",
    "ROLLUP",
    "ROWS",
    "SELECT",
    "SET",
    "SOME",
    "STRUCT",
    "TABLESAMPLE",
    "THEN",
    "TO",
    "TREAT",
    "TRUE",
    "UNBOUNDED",
    "UNION",
    "UNNEST",
    "USING",
    "WHEN",
    "WHERE",
    "WINDOW",
    "WITH",
    "WITHIN",
}

STMT_DDL = "DDL"
STMT_NON_UPDATING = "NON_UPDATING"
STMT_UPDATING = "UPDATING"
STMT_INSERT = "INSERT"

# Heuristic for identifying statements that don't need to be run as updates.
RE_NON_UPDATE = re.compile(r"^\s*(SELECT)", re.IGNORECASE)

RE_WITH = re.compile(r"^\s*(WITH)", re.IGNORECASE)

# DDL statements follow
# https://cloud.google.com/spanner/docs/data-definition-language
RE_DDL = re.compile(r"^\s*(CREATE|ALTER|DROP)", re.IGNORECASE | re.DOTALL)

RE_IS_INSERT = re.compile(r"^\s*(INSERT)", re.IGNORECASE | re.DOTALL)

RE_INSERT = re.compile(
    # Only match the `INSERT INTO <table_name> (columns...)
    # otherwise the rest of the statement could be a complex
    # operation.
    r"^\s*INSERT INTO (?P<table_name>[^\s\(\)]+)\s*\((?P<columns>[^\(\)]+)\)",
    re.IGNORECASE | re.DOTALL,
)

RE_VALUES_TILL_END = re.compile(r"VALUES\s*\(.+$", re.IGNORECASE | re.DOTALL)

RE_VALUES_PYFORMAT = re.compile(
    # To match: (%s, %s,....%s)
    r"(\(\s*%s[^\(\)]+\))",
    re.DOTALL,
)

RE_PYFORMAT = re.compile(r"(%s|%\([^\(\)]+\)s)+", re.DOTALL)


def classify_stmt(query):
    """Determine SQL query type.

    :type query: :class:`str`
    :param query: SQL query.

    :rtype: :class:`str`
    :returns: Query type name.
    """
    if RE_DDL.match(query):
        return STMT_DDL

    if RE_IS_INSERT.match(query):
        return STMT_INSERT

    if RE_NON_UPDATE.match(query) or RE_WITH.match(query):
        # As of 13-March-2020, Cloud Spanner only supports WITH for DQL
        # statements and doesn't yet support WITH for DML statements.
        return STMT_NON_UPDATING

    return STMT_UPDATING


def parse_insert(insert_sql, params):
    """
    Parse an INSERT statement an generate a list of tuples of the form:
        [
            (SQL, params_per_row1),
            (SQL, params_per_row2),
            (SQL, params_per_row3),
            ...
        ]

    There are 4 variants of an INSERT statement:
    a) INSERT INTO <table> (columns...) VALUES (<inlined values>): no params
    b) INSERT INTO <table> (columns...) SELECT_STMT:               no params
    c) INSERT INTO <table> (columns...) VALUES (%s,...):           with params
    d) INSERT INTO <table> (columns...) VALUES (%s,..<EXPR>...)    with params and expressions

    Thus given each of the forms, it will produce a dictionary describing
    how to upload the contents to Cloud Spanner:
    Case a)
            SQL: INSERT INTO T (f1, f2) VALUES (1, 2)
        it produces:
            {
                'sql_params_list': [
                    ('INSERT INTO T (f1, f2) VALUES (1, 2)', None),
                ],
            }

    Case b)
            SQL: 'INSERT INTO T (s, c) SELECT st, zc FROM cus ORDER BY fn, ln',
        it produces:
            {
                'sql_params_list': [
                    ('INSERT INTO T (s, c) SELECT st, zc FROM cus ORDER BY fn, ln', None),
                ]
            }

    Case c)
            SQL: INSERT INTO T (f1, f2) VALUES (%s, %s), (%s, %s)
            Params: ['a', 'b', 'c', 'd']
        it produces:
            {
                'homogenous': True,
                'table': 'T',
                'columns': ['f1', 'f2'],
                'values': [('a', 'b',), ('c', 'd',)],
            }

    Case d)
            SQL: INSERT INTO T (f1, f2) VALUES (%s, LOWER(%s)), (UPPER(%s), %s)
            Params: ['a', 'b', 'c', 'd']
        it produces:
            {
                'sql_params_list': [
                    ('INSERT INTO T (f1, f2) VALUES (%s, LOWER(%s))', ('a', 'b',))
                    ('INSERT INTO T (f1, f2) VALUES (UPPER(%s), %s)', ('c', 'd',))
                ],
            }
    """  # noqa
    match = RE_INSERT.search(insert_sql)

    if not match:
        raise ProgrammingError(
            "Could not parse an INSERT statement from %s" % insert_sql
        )

    after_values_sql = RE_VALUES_TILL_END.findall(insert_sql)
    if not after_values_sql:
        # Case b)
        insert_sql = sanitize_literals_for_upload(insert_sql)
        return {"sql_params_list": [(insert_sql, None)]}

    if not params:
        # Case a) perhaps?
        # Check if any %s exists.

        # pyformat_str_count = after_values_sql.count("%s")
        # if pyformat_str_count > 0:
        #     raise ProgrammingError(
        #         'no params yet there are %d "%%s" tokens' % pyformat_str_count
        #     )
        for item in after_values_sql:
            if item.count("%s") > 0:
                raise ProgrammingError(
                    'no params yet there are %d "%%s" tokens' % item.count("%s")
                )

        insert_sql = sanitize_literals_for_upload(insert_sql)
        # Confirmed case of:
        # SQL: INSERT INTO T (a1, a2) VALUES (1, 2)
        # Params: None
        return {"sql_params_list": [(insert_sql, None)]}

    values_str = after_values_sql[0]
    _, values = parse_values(values_str)

    if values.homogenous():
        # Case c)

        columns = [mi.strip(" `") for mi in match.group("columns").split(",")]
        sql_params_list = []
        insert_sql_preamble = "INSERT INTO %s (%s) VALUES %s" % (
            match.group("table_name"),
            match.group("columns"),
            values.argv[0],
        )
        values_pyformat = [str(arg) for arg in values.argv]
        rows_list = rows_for_insert_or_update(columns, params, values_pyformat)
        insert_sql_preamble = sanitize_literals_for_upload(insert_sql_preamble)
        for row in rows_list:
            sql_params_list.append((insert_sql_preamble, row))

        return {"sql_params_list": sql_params_list}

    # Case d)
    # insert_sql is of the form:
    #   INSERT INTO T(c1, c2) VALUES (%s, %s), (%s, LOWER(%s))

    # Sanity check:
    #  length(all_args) == len(params)
    args_len = reduce(lambda a, b: a + b, [len(arg) for arg in values.argv])
    if args_len != len(params):
        raise ProgrammingError(
            "Invalid length: VALUES(...) len: %d != len(params): %d"
            % (args_len, len(params))
        )

    trim_index = insert_sql.find(values_str)
    before_values_sql = insert_sql[:trim_index]

    sql_param_tuples = []
    for token_arg in values.argv:
        row_sql = before_values_sql + " VALUES%s" % token_arg
        row_sql = sanitize_literals_for_upload(row_sql)
        row_params, params = (
            tuple(params[0 : len(token_arg)]),
            params[len(token_arg) :],
        )
        sql_param_tuples.append((row_sql, row_params))

    return {"sql_params_list": sql_param_tuples}


def rows_for_insert_or_update(columns, params, pyformat_args=None):
    """
    Create a tupled list of params to be used as a single value per
    value that inserted from a statement such as
        SQL:        'INSERT INTO t (f1, f2, f3) VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)'
        Params A:   [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        Params B:   [1, 2, 3, 4, 5, 6, 7, 8, 9]

    We'll have to convert both params types into:
        Params: [(1, 2, 3,), (4, 5, 6,), (7, 8, 9,)]
    """  # noqa

    if not pyformat_args:
        # This is the case where we have for example:
        # SQL:        'INSERT INTO t (f1, f2, f3)'
        # Params A:   [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        # Params B:   [1, 2, 3, 4, 5, 6, 7, 8, 9]
        #
        # We'll have to convert both params types into:
        #           [(1, 2, 3,), (4, 5, 6,), (7, 8, 9,)]
        contains_all_list_or_tuples = True
        for param in params:
            if not (isinstance(param, list) or isinstance(param, tuple)):
                contains_all_list_or_tuples = False
                break

        if contains_all_list_or_tuples:
            # The case with Params A: [(1, 2, 3), (4, 5, 6)]
            # Ensure that each param's length == len(columns)
            columns_len = len(columns)
            for param in params:
                if columns_len != len(param):
                    raise Error(
                        "\nlen(`%s`)=%d\n!=\ncolum_len(`%s`)=%d"
                        % (param, len(param), columns, columns_len)
                    )
            return params
        else:
            # The case with Params B: [1, 2, 3]
            # Insert statements' params are only passed as tuples or lists,
            # yet for do_execute_update, we've got to pass in list of list.
            # https://googleapis.dev/python/spanner/latest/transaction-api.html\
            #           #google.cloud.spanner_v1.transaction.Transaction.insert
            n_stride = len(columns)
    else:
        # This is the case where we have for example:
        # SQL:      'INSERT INTO t (f1, f2, f3) VALUES (%s, %s, %s),
        #           (%s, %s, %s), (%s, %s, %s)'
        # Params:   [1, 2, 3, 4, 5, 6, 7, 8, 9]
        #    which should become
        # Columns:      (f1, f2, f3)
        # new_params:   [(1, 2, 3,), (4, 5, 6,), (7, 8, 9,)]

        # Sanity check 1: all the pyformat_values should have the exact same
        # length.
        first, rest = pyformat_args[0], pyformat_args[1:]
        n_stride = first.count("%s")
        for pyfmt_value in rest:
            n = pyfmt_value.count("%s")
            if n_stride != n:
                raise Error(
                    "\nlen(`%s`)=%d\n!=\nlen(`%s`)=%d"
                    % (first, n_stride, pyfmt_value, n)
                )

        # Sanity check 2: len(params) MUST be a multiple of n_stride aka
        # len(count of %s).
        # so that we can properly group for example:
        #  Given pyformat args:
        #   (%s, %s, %s)
        #  Params:
        #   [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # into
        #   [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        if (len(params) % n_stride) != 0:
            raise ProgrammingError(
                "Invalid length: len(params)=%d MUST be a multiple of "
                "len(pyformat_args)=%d" % (len(params), n_stride)
            )

    # Now chop up the strides.
    strides = []
    for step in range(0, len(params), n_stride):
        stride = tuple(params[step : step + n_stride :])
        strides.append(stride)

    return strides


def sql_pyformat_args_to_spanner(sql, params):
    """
    Transform pyformat set SQL to named arguments for Cloud Spanner.
    It will also unescape previously escaped format specifiers
    like %%s to %s.
    For example:
        SQL:      'SELECT * from t where f1=%s, f2=%s, f3=%s'
        Params:   ('a', 23, '888***')
    becomes:
        SQL:      'SELECT * from t where f1=@a0, f2=@a1, f3=@a2'
        Params:   {'a0': 'a', 'a1': 23, 'a2': '888***'}

    OR
        SQL:      'SELECT * from t where f1=%(f1)s, f2=%(f2)s, f3=%(f3)s'
        Params:   {'f1': 'a', 'f2': 23, 'f3': '888***', 'extra': 'aye')
    becomes:
        SQL:      'SELECT * from t where f1=@a0, f2=@a1, f3=@a2'
        Params:   {'a0': 'a', 'a1': 23, 'a2': '888***'}
    """
    if not params:
        return sanitize_literals_for_upload(sql), params

    found_pyformat_placeholders = RE_PYFORMAT.findall(sql)
    params_is_dict = isinstance(params, dict)

    if params_is_dict:
        if not found_pyformat_placeholders:
            return sanitize_literals_for_upload(sql), params
    else:
        n_params = len(params) if params else 0
        n_matches = len(found_pyformat_placeholders)
        if n_matches != n_params:
            raise Error(
                "pyformat_args mismatch\ngot %d args from %s\n"
                "want %d args in %s"
                % (n_matches, found_pyformat_placeholders, n_params, params)
            )

    named_args = {}
    # We've now got for example:
    # Case a) Params is a non-dict
    #   SQL:      'SELECT * from t where f1=%s, f2=%s, f3=%s'
    #   Params:   ('a', 23, '888***')
    # Case b) Params is a dict and the matches are %(value)s'
    for i, pyfmt in enumerate(found_pyformat_placeholders):
        key = "a%d" % i
        sql = sql.replace(pyfmt, "@" + key, 1)
        if params_is_dict:
            # The '%(key)s' case, so interpolate it.
            resolved_value = pyfmt % params
            named_args[key] = resolved_value
        else:
            named_args[key] = cast_for_spanner(params[i])

    return sanitize_literals_for_upload(sql), named_args


def cast_for_spanner(value):
    """Convert the param to its Cloud Spanner equivalent type.

    :type value: Any
    :param value: Value to convert to a Cloud Spanner type.

    :rtype: Any
    :returns: Value converted to a Cloud Spanner type.
    """
    if isinstance(value, decimal.Decimal):
        return str(value)
    return value


def get_param_types(params):
    """Determine Cloud Spanner types for the given parameters.

    :type params: :class:`dict`
    :param params: Parameters requiring to find Cloud Spanner types.

    :rtype: :class:`dict`
    :returns: The types index for the given parameters.
    """
    if params is None:
        return

    param_types = {}

    for key, value in params.items():
        type_ = type(value)
        if type_ in TYPES_MAP:
            param_types[key] = TYPES_MAP[type_]

    return param_types


def ensure_where_clause(sql):
    """
    Cloud Spanner requires a WHERE clause on UPDATE and DELETE statements.
    Add a dummy WHERE clause if necessary.
    """
    if any(isinstance(token, sqlparse.sql.Where) for token in sqlparse.parse(sql)[0]):
        return sql
    return sql + " WHERE 1=1"


def escape_name(name):
    """
    Apply backticks to the name that either contain '-' or
    ' ', or is a Cloud Spanner's reserved keyword.

    :type name: :class:`str`
    :param name: Name to escape.

    :rtype: :class:`str`
    :returns: Name escaped if it has to be escaped.
    """
    if "-" in name or " " in name or name.upper() in SPANNER_RESERVED_KEYWORDS:
        return "`" + name + "`"
    return name
