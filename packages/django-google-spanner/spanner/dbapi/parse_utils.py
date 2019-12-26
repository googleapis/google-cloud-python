# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import decimal
import re

import sqlparse
from google.cloud import spanner_v1 as spanner

from .exceptions import Error
from .types import DateStr, TimestampStr

STMT_DDL = 'DDL'
STMT_NON_UPDATING = 'NON_UPDATING'
STMT_UPDATING = 'UPDATING'
STMT_INSERT = 'INSERT'

# Heuristic for identifying statements that don't need to be run as updates.
re_NON_UPDATE = re.compile(r'^\s*(SELECT|ANALYZE|AUDIT|EXPLAIN|SHOW)', re.IGNORECASE)

# DDL statements follow https://cloud.google.com/spanner/docs/data-definition-language
re_DDL = re.compile(r'^\s*(CREATE|ALTER|DROP)', re.IGNORECASE | re.DOTALL)

re_IS_INSERT = re.compile(r'^\s*(INSERT)', re.IGNORECASE | re.DOTALL)


def classify_stmt(sql):
    if re_DDL.match(sql):
        return STMT_DDL
    elif re_IS_INSERT.match(sql):
        return STMT_INSERT
    elif re_NON_UPDATE.match(sql):
        return STMT_NON_UPDATING
    else:
        return STMT_UPDATING


re_INSERT = re.compile(
    # Only match the `INSERT INTO <table_name> (columns...)
    # otherwise the rest of the statement could be a complex
    # operation.
    r'^\s*INSERT INTO (?P<table_name>[^\s\(\)]+)\s+\((?P<columns>[^\(\)]+)\)',
    re.IGNORECASE | re.DOTALL,
)

re_VALUES_TILL_END = re.compile(
    r'VALUES\s*\(.+$',
    re.IGNORECASE | re.DOTALL,
)

re_VALUES_PYFORMAT = re.compile(
    # To match: (%s, %s,....%s)
    r'(\(\s*%s[^\(\)]+\))',
    re.DOTALL,
)


def strip_backticks(name):
    """
    Strip backticks off of quoted names For example, '`no`' (a Spanner reserved
    word) becomes 'no'.
    """
    has_quotes = name.startswith('`') and name.endswith('`')
    return name[1:-1] if has_quotes else name


def parse_insert(insert_sql):
    match = re_INSERT.search(insert_sql)
    if not match:
        return None

    parsed = {
        'table': strip_backticks(match.group('table_name')),
        'columns': [
            strip_backticks(mi.strip())
            for mi in match.group('columns').split(',')
        ],
    }
    after_VALUES_sql = re_VALUES_TILL_END.findall(insert_sql)
    if after_VALUES_sql:
        values_pyformat = re_VALUES_PYFORMAT.findall(after_VALUES_sql[0])
        if values_pyformat:
            parsed['values_pyformat'] = values_pyformat

    return parsed


def rows_for_insert_or_update(columns, params, pyformat_args=None):
    """
    Create a tupled list of params to be used as a single value per
    value that inserted from a statement such as
        SQL:        'INSERT INTO t (f1, f2, f3) VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)'
        Params A:   [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        Params B:   [1, 2, 3, 4, 5, 6, 7, 8, 9]

    We'll have to convert both params types into:
        Params: [(1, 2, 3,), (4, 5, 6,), (7, 8, 9,)]
    """

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
                    raise Error('\nlen(`%s`)=%d\n!=\ncolum_len(`%s`)=%d' % (
                        param, len(param), columns, columns_len))
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
        # SQL:      'INSERT INTO t (f1, f2, f3) VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)'
        # Params:   [1, 2, 3, 4, 5, 6, 7, 8, 9]
        #    which should become
        # Columns:      (f1, f2, f3)
        # new_params:   [(1, 2, 3,), (4, 5, 6,), (7, 8, 9,)]

        # Sanity check: all the pyformat_values should have the exact same length.
        first, rest = pyformat_args[0], pyformat_args[1:]
        n_stride = first.count('%s')
        for pyfmt_value in rest:
            n = pyfmt_value.count('%s')
            if n_stride != n:
                raise Error('\nlen(`%s`)=%d\n!=\nlen(`%s`)=%d' % (
                    first, n_stride, pyfmt_value, n))

    # Now chop up the strides.
    strides = []
    for step in range(0, len(params), n_stride):
        stride = tuple(params[step:step+n_stride:])
        strides.append(stride)

    return strides


re_PYFORMAT = re.compile(r'(%s|%\([^\(\)]+\)s)+', re.DOTALL)


def sql_pyformat_args_to_spanner(sql, params):
    """
    Transform pyformat set SQL to named arguments for Cloud Spanner.
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
        return sql, params

    found_pyformat_placeholders = re_PYFORMAT.findall(sql)
    params_is_dict = isinstance(params, dict)

    if params_is_dict:
        if not found_pyformat_placeholders:
            return sql, params
    else:
        n_params = len(params) if params else 0
        n_matches = len(found_pyformat_placeholders)
        if n_matches != n_params:
            raise Error(
                'pyformat_args mismatch\ngot %d args from %s\n'
                'want %d args in %s' % (n_matches, found_pyformat_placeholders, n_params, params))

    if len(params) == 0:
        return sql, params

    named_args = {}
    # We've now got for example:
    # Case a) Params is a non-dict
    #   SQL:      'SELECT * from t where f1=%s, f2=%s, f3=%s'
    #   Params:   ('a', 23, '888***')
    # Case b) Params is a dict and the matches are %(value)s'
    for i, pyfmt in enumerate(found_pyformat_placeholders):
        key = 'a%d' % i
        sql = sql.replace(pyfmt, '@'+key, 1)
        if params_is_dict:
            # The '%(key)s' case, so interpolate it.
            resolved_value = pyfmt % params
            named_args[key] = resolved_value
        else:
            named_args[key] = cast_for_spanner(params[i])

    return sql, named_args


def cast_for_spanner(param):
    """Convert param to its Cloud Spanner equivalent type."""
    if isinstance(param, decimal.Decimal):
        return float(param)
    else:
        return param


def get_param_types(params):
    """
    Return a dictionary of spanner.param_types for a dictionary of parameters.
    """
    if params is None:
        return None
    param_types = {}
    for key, value in params.items():
        if isinstance(value, bool):
            param_types[key] = spanner.param_types.BOOL
        elif isinstance(value, float):
            param_types[key] = spanner.param_types.FLOAT64
        elif isinstance(value, int):
            param_types[key] = spanner.param_types.INT64
        elif isinstance(value, TimestampStr):
            param_types[key] = spanner.param_types.TIMESTAMP
        elif isinstance(value, DateStr):
            param_types[key] = spanner.param_types.DATE
        elif isinstance(value, str):
            param_types[key] = spanner.param_types.STRING
    return param_types


def ensure_where_clause(sql):
    """
    Cloud Spanner requires a WHERE clause on UPDATE and DELETE statements.
    Add a dummy WHERE clause if necessary.
    """
    if any(isinstance(token, sqlparse.sql.Where) for token in sqlparse.parse(sql)[0]):
        return sql
    return sql + ' WHERE 1=1'


SPANNER_RESERVED_KEYWORDS = {
    'ALL',
    'AND',
    'ANY',
    'ARRAY',
    'AS',
    'ASC',
    'ASSERT_ROWS_MODIFIED',
    'AT',
    'BETWEEN',
    'BY',
    'CASE',
    'CAST',
    'COLLATE',
    'CONTAINS',
    'CREATE',
    'CROSS',
    'CUBE',
    'CURRENT',
    'DEFAULT',
    'DEFINE',
    'DESC',
    'DISTINCT',
    'DROP',
    'ELSE',
    'END',
    'ENUM',
    'ESCAPE',
    'EXCEPT',
    'EXCLUDE',
    'EXISTS',
    'EXTRACT',
    'FALSE',
    'FETCH',
    'FOLLOWING',
    'FOR',
    'FROM',
    'FULL',
    'GROUP',
    'GROUPING',
    'GROUPS',
    'HASH',
    'HAVING',
    'IF',
    'IGNORE',
    'IN',
    'INNER',
    'INTERSECT',
    'INTERVAL',
    'INTO',
    'IS',
    'JOIN',
    'LATERAL',
    'LEFT',
    'LIKE',
    'LIMIT',
    'LOOKUP',
    'MERGE',
    'NATURAL',
    'NEW',
    'NO',
    'NOT',
    'NULL',
    'NULLS',
    'OF',
    'ON',
    'OR',
    'ORDER',
    'OUTER',
    'OVER',
    'PARTITION',
    'PRECEDING',
    'PROTO',
    'RANGE',
    'RECURSIVE',
    'RESPECT',
    'RIGHT',
    'ROLLUP',
    'ROWS',
    'SELECT',
    'SET',
    'SOME',
    'STRUCT',
    'TABLESAMPLE',
    'THEN',
    'TO',
    'TREAT',
    'TRUE',
    'UNBOUNDED',
    'UNION',
    'UNNEST',
    'USING',
    'WHEN',
    'WHERE',
    'WINDOW',
    'WITH',
    'WITHIN',
}


def escape_name(name):
    """
    Escape name by applying backticks to value that either
    contain '-' or are any of Cloud Spanner's reserved keywords.
    """
    if '-' in name or ' ' in name or name.upper() in SPANNER_RESERVED_KEYWORDS:
        return '`' + name + '`'
    return name
