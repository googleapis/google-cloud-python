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

from google.cloud.spanner_dbapi.parse_utils import get_param_types
from google.cloud.spanner_dbapi.parse_utils import parse_insert
from google.cloud.spanner_dbapi.parse_utils import sql_pyformat_args_to_spanner
from google.cloud.spanner_v1 import param_types


SQL_LIST_TABLES = """
            SELECT
              t.table_name
            FROM
              information_schema.tables AS t
            WHERE
              t.table_catalog = '' and t.table_schema = ''
            """

SQL_GET_TABLE_COLUMN_SCHEMA = """SELECT
                COLUMN_NAME, IS_NULLABLE, SPANNER_TYPE
            FROM
                INFORMATION_SCHEMA.COLUMNS
            WHERE
                TABLE_SCHEMA = ''
            AND
                TABLE_NAME = @table_name
            """

# This table maps spanner_types to Spanner's data type sizes as per
#   https://cloud.google.com/spanner/docs/data-types#allowable-types
# It is used to map `display_size` to a known type for Cursor.description
# after a row fetch.
# Since ResultMetadata
#   https://cloud.google.com/spanner/docs/reference/rest/v1/ResultSetMetadata
# does not send back the actual size, we have to lookup the respective size.
# Some fields' sizes are dependent upon the dynamic data hence aren't sent back
# by Cloud Spanner.
code_to_display_size = {
    param_types.BOOL.code: 1,
    param_types.DATE.code: 4,
    param_types.FLOAT64.code: 8,
    param_types.INT64.code: 8,
    param_types.TIMESTAMP.code: 12,
}


def _execute_insert_heterogenous(transaction, sql_params_list):
    for sql, params in sql_params_list:
        sql, params = sql_pyformat_args_to_spanner(sql, params)
        param_types = get_param_types(params)
        transaction.execute_update(sql, params=params, param_types=param_types)


def _execute_insert_homogenous(transaction, parts):
    # Perform an insert in one shot.
    table = parts.get("table")
    columns = parts.get("columns")
    values = parts.get("values")
    return transaction.insert(table, columns, values)


def handle_insert(connection, sql, params):
    parts = parse_insert(sql, params)

    # The split between the two styles exists because:
    # in the common case of multiple values being passed
    # with simple pyformat arguments,
    #   SQL: INSERT INTO T (f1, f2) VALUES (%s, %s, %s)
    #   Params:   [(1, 2, 3, 4, 5, 6, 7, 8, 9, 10,)]
    # we can take advantage of a single RPC with:
    #       transaction.insert(table, columns, values)
    # instead of invoking:
    #   with transaction:
    #       for sql, params in sql_params_list:
    #           transaction.execute_sql(sql, params, param_types)
    # which invokes more RPCs and is more costly.

    if parts.get("homogenous"):
        # The common case of multiple values being passed in
        # non-complex pyformat args and need to be uploaded in one RPC.
        return connection.database.run_in_transaction(_execute_insert_homogenous, parts)
    else:
        # All the other cases that are esoteric and need
        #   transaction.execute_sql
        sql_params_list = parts.get("sql_params_list")
        return connection.database.run_in_transaction(
            _execute_insert_heterogenous, sql_params_list
        )


class ColumnInfo:
    """Row column description object."""

    def __init__(
        self,
        name,
        type_code,
        display_size=None,
        internal_size=None,
        precision=None,
        scale=None,
        null_ok=False,
    ):
        self.name = name
        self.type_code = type_code
        self.display_size = display_size
        self.internal_size = internal_size
        self.precision = precision
        self.scale = scale
        self.null_ok = null_ok

        self.fields = (
            self.name,
            self.type_code,
            self.display_size,
            self.internal_size,
            self.precision,
            self.scale,
            self.null_ok,
        )

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, index):
        return self.fields[index]

    def __str__(self):
        str_repr = ", ".join(
            filter(
                lambda part: part is not None,
                [
                    "name='%s'" % self.name,
                    "type_code=%d" % self.type_code,
                    "display_size=%d" % self.display_size
                    if self.display_size
                    else None,
                    "internal_size=%d" % self.internal_size
                    if self.internal_size
                    else None,
                    "precision='%s'" % self.precision if self.precision else None,
                    "scale='%s'" % self.scale if self.scale else None,
                    "null_ok='%s'" % self.null_ok if self.null_ok else None,
                ],
            )
        )
        return "ColumnInfo(%s)" % str_repr
