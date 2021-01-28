# Copyright 2018 Google LLC
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

import re

from sqlalchemy import types
from sqlalchemy.engine.default import DefaultDialect
from google.cloud import spanner_dbapi

# Spanner-to-SQLAlchemy types map
_type_map = {
    "BOOL": types.Boolean,
    "BYTES": types.BINARY,
    "DATE": types.DATE,
    "DATETIME": types.DATETIME,
    "FLOAT": types.Float,
    "INT64": types.BIGINT,
    "INTEGER": types.Integer,
    "NUMERIC": types.DECIMAL,
    "STRING": types.String,
    "TIME": types.TIME,
    "TIMESTAMP": types.TIMESTAMP,
}


class SpannerDialect(DefaultDialect):
    """Cloud Spanner dialect.

    Represents an API layer to control Cloud Spanner database with SQLAlchemy API.
    """

    name = "spanner"
    driver = "spanner"
    positional = False
    paramstyle = "format"
    encoding = "utf-8"

    execute_sequence_format = list

    supports_alter = True
    supports_sane_rowcount = True
    supports_sane_multi_rowcount = False
    supports_default_values = False
    supports_sequences = True
    supports_native_enum = True
    supports_native_boolean = True

    @classmethod
    def dbapi(cls):
        """A pointer to the Cloud Spanner DB API package.

        Used to initiate connections to the Cloud Spanner databases.
        """
        return spanner_dbapi

    def _check_unicode_returns(self, connection, additional_tests=None):
        """Ensure requests are returning Unicode responses."""
        return True

    def create_connect_args(self, url):
        """Parse connection args from the given URL.

        The method prepares args suitable to send to the DB API `connect()` function.

        The given URL follows the style:
        `spanner:///projects/{project-id}/instances/{instance-id}/databases/{database-id}`
        """
        match = re.match(
            (
                r"^projects/(?P<project>.+?)/instances/"
                "(?P<instance>.+?)/databases/(?P<database>.+?)$"
            ),
            url.database,
        )
        return (
            [match.group("instance"), match.group("database"), match.group("project")],
            {},
        )

    def get_columns(self, connection, table_name, schema=None, **kw):
        """Get the table columns description.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            list: The table every column dict-like description.
        """
        sql = """
SELECT COLUMN_NAME, SPANNER_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME="{table_name}"
""".format(
            table_name=table_name
        )

        with connection.connection.database.snapshot() as snap:
            columns = snap.execute_sql(sql)

        cols_desc = []
        for col in columns:
            type_ = "STRING" if col[1].startswith("STRING") else col[1]

            cols_desc.append(
                {
                    "name": col[0],
                    "type": _type_map[type_],
                    "nullable": col[2],
                    "default": None,
                }
            )
        return cols_desc

    def get_indexes(self, connection, table_name, schema=None, **kw):
        """Get the table indexes.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            list: List with indexes description.
        """
        sql = """
SELECT i.INDEX_NAME, ic.COLUMN_NAME, i.IS_UNIQUE, ic.COLUMN_ORDERING
FROM INFORMATION_SCHEMA.INDEXES as i
JOIN INFORMATION_SCHEMA.INDEX_COLUMNS AS ic
    ON ic.INDEX_NAME = i.INDEX_NAME AND ic.TABLE_NAME = i.TABLE_NAME
WHERE i.TABLE_NAME="{table_name}"
""".format(
            table_name=table_name
        )

        with connection.connection.database.snapshot() as snap:
            inds = snap.execute_sql(sql)

        ind_descs = []
        for ind in inds:
            ind_descs.append(
                {
                    "name": ind[0],
                    "column_names": [ind[1]],
                    "unique": ind[2],
                    "column_sorting": {ind[0]: ind[3]},
                }
            )
        return ind_descs

    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        """Get the table primary key constraint.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            dict: Dict with the primary key constraint description.
        """
        sql = """
SELECT ccu.COLUMN_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu
    ON ccu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
WHERE tc.TABLE_NAME="{table_name}" AND tc.CONSTRAINT_TYPE = "PRIMARY KEY"
""".format(
            table_name=table_name
        )

        with connection.connection.database.snapshot() as snap:
            pks = snap.execute_sql(sql)

        cols = []
        for key in pks:
            cols.append(key[0])

        return {"constrained_columns": cols}

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        """Get the table foreign key constraints.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            list: Dicts, each of which describes a foreign key constraint.
        """
        sql = """
SELECT ccu.COLUMN_NAME, ccu.TABLE_SCHEMA, ccu.TABLE_NAME, ccu.CONSTRAINT_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu
    ON ccu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
WHERE tc.TABLE_NAME="{table_name}" AND tc.CONSTRAINT_TYPE = "FOREIGN KEY"
""".format(
            table_name=table_name
        )

        with connection.connection.database.snapshot() as snap:
            fks = snap.execute_sql(sql)

        keys = []
        for key in fks:
            keys.append(
                {
                    "constrained_columns": [key[0]],
                    "referred_schema": key[1],
                    "referred_table": key[2],
                    "referred_columns": [key[0]],
                    "name": key[3],
                }
            )
        return keys
