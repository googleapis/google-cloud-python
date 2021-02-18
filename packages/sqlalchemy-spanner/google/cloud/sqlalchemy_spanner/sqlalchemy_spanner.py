# Copyright 2021 Google LLC
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
from sqlalchemy.sql.compiler import GenericTypeCompiler
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


class SpannerTypeCompiler(GenericTypeCompiler):
    """Spanner types compiler.

    Maps SQLAlchemy types to Spanner data types.
    """

    def visit_INTEGER(self, type_, **kw):
        return "INT64"

    def visit_FLOAT(self, type_, **kw):
        return "FLOAT64"

    def visit_TEXT(self, type_, **kw):
        return "STRING({})".format(type_.length)

    def visit_ARRAY(self, type_, **kw):
        return "ARRAY<{}>".format(self.process(type_.item_type, **kw))

    def visit_BINARY(self, type_, **kw):
        return "BYTES"

    def visit_DECIMAL(self, type_, **kw):
        return "NUMERIC"

    def visit_VARCHAR(self, type_, **kw):
        return "STRING({})".format(type_.length)

    def visit_CHAR(self, type_, **kw):
        return "STRING({})".format(type_.length)

    def visit_BOOLEAN(self, type_, **kw):
        return "BOOL"


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

    type_compiler = SpannerTypeCompiler

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
            connection (Union[
                sqlalchemy.engine.base.Connection,
                sqlalchemy.engine.Engine
            ]):
                SQLAlchemy connection or engine object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            list: The table every column dict-like description.
        """
        if isinstance(connection, Engine):
            connection = connection.connect()

        sql = """
SELECT column_name, spanner_type, is_nullable
FROM information_schema.columns
WHERE
    table_catalog = ''
    AND table_schema = ''
    AND table_name = '{}'
ORDER BY
    table_catalog,
    table_schema,
    table_name,
    ordinal_position
""".format(
            table_name
        )

        cols_desc = []
        with connection.connection.database.snapshot() as snap:
            columns = snap.execute_sql(sql)

            for col in columns:
                type_ = "STRING" if col[1].startswith("STRING") else col[1]

                cols_desc.append(
                    {
                        "name": col[0],
                        "type": _type_map[type_],
                        "nullable": col[2] == "YES",
                        "default": None,
                    }
                )
        return cols_desc

    def get_indexes(self, connection, table_name, schema=None, **kw):
        """Get the table indexes.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (Union[
                sqlalchemy.engine.base.Connection,
                sqlalchemy.engine.Engine
            ]):
                SQLAlchemy connection or engine object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            list: List with indexes description.
        """
        if isinstance(connection, Engine):
            connection = connection.connect()

        sql = """
SELECT
    i.index_name,
    ARRAY_AGG(ic.column_name),
    i.is_unique,
    ARRAY_AGG(ic.column_ordering)
FROM information_schema.indexes as i
JOIN information_schema.index_columns AS ic
    ON ic.index_name = i.index_name AND ic.table_name = i.table_name
WHERE i.table_name="{table_name}"
GROUP BY i.index_name, i.is_unique
""".format(
            table_name=table_name
        )

        ind_desc = []
        with connection.connection.database.snapshot() as snap:
            rows = snap.execute_sql(sql)

            for row in rows:
                ind_desc.append(
                    {
                        "name": row[0],
                        "column_names": row[1],
                        "unique": row[2],
                        "column_sorting": {
                            col: order for col, order in zip(row[1], row[3])
                        },
                    }
                )
        return ind_desc

    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        """Get the table primary key constraint.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (Union[
                sqlalchemy.engine.base.Connection,
                sqlalchemy.engine.Engine
            ]):
                SQLAlchemy connection or engine object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            dict: Dict with the primary key constraint description.
        """
        if isinstance(connection, Engine):
            connection = connection.connect()

        sql = """
SELECT ccu.COLUMN_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu
    ON ccu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
WHERE tc.TABLE_NAME="{table_name}" AND tc.CONSTRAINT_TYPE = "PRIMARY KEY"
""".format(
            table_name=table_name
        )

        cols = []
        with connection.connection.database.snapshot() as snap:
            rows = snap.execute_sql(sql)

            for row in rows:
                cols.append(row[0])

        return {"constrained_columns": cols}

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        """Get the table foreign key constraints.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (Union[
                sqlalchemy.engine.base.Connection,
                sqlalchemy.engine.Engine
            ]):
                SQLAlchemy connection or engine object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            list: Dicts, each of which describes a foreign key constraint.
        """
        if isinstance(connection, Engine):
            connection = connection.connect()

        sql = """
SELECT ccu.COLUMN_NAME, ccu.TABLE_SCHEMA, ccu.TABLE_NAME, ccu.CONSTRAINT_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu
    ON ccu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
WHERE tc.TABLE_NAME="{table_name}" AND tc.CONSTRAINT_TYPE = "FOREIGN KEY"
""".format(
            table_name=table_name
        )

        keys = []
        with connection.connection.database.snapshot() as snap:
            rows = snap.execute_sql(sql)

            for row in rows:
                keys.append(
                    {
                        "constrained_columns": [row[0]],
                        "referred_schema": row[1],
                        "referred_table": row[2],
                        "referred_columns": [row[0]],
                        "name": row[3],
                    }
                )
        return keys

    def get_table_names(self, connection, schema=None, **kw):
        """Get all the tables from the given schema.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (Union[
                sqlalchemy.engine.base.Connection,
                sqlalchemy.engine.Engine
            ]):
                SQLAlchemy connection or engine object.
            schema (str): Optional. Schema name.

        Returns:
            list: Names of the tables within the given schema.
        """
        if isinstance(connection, Engine):
            connection = connection.connect()

        sql = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = '{}'
""".format(
            schema
        )

        table_names = []
        with connection.connection.database.snapshot() as snap:
            rows = snap.execute_sql(sql)

            for row in rows:
                table_names.append(row[0])

        return table_names

    def get_unique_constraints(self, connection, table_name, schema=None, **kw):
        """Get the table unique constraints.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (Union[
                sqlalchemy.engine.base.Connection,
                sqlalchemy.engine.Engine
            ]):
                SQLAlchemy connection or engine object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            dict: Dict with the unique constraints' descriptions.
        """
        if isinstance(connection, Engine):
            connection = connection.connect()

        sql = """
SELECT ccu.CONSTRAINT_NAME, ccu.COLUMN_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu
    ON ccu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
WHERE tc.TABLE_NAME="{table_name}" AND tc.CONSTRAINT_TYPE = "UNIQUE"
""".format(
            table_name=table_name
        )

        cols = []
        with connection.connection.database.snapshot() as snap:
            rows = snap.execute_sql(sql)

            for row in rows:
                cols.append({"name": row[0], "column_names": [row[1]]})

        return cols

    def has_table(self, connection, table_name, schema=None):
        """Check if the given table exists.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (Union[
                sqlalchemy.engine.base.Connection,
                sqlalchemy.engine.Engine
            ]):
                SQLAlchemy connection or engine object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name.

        Returns:
            bool: True, if the given table exists, False otherwise.
        """
        if isinstance(connection, Engine):
            connection = connection.connect()

        with connection.connection.database.snapshot() as snap:
            rows = snap.execute_sql(
                """
SELECT true
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME="{table_name}"
LIMIT 1
""".format(
                    table_name=table_name
                )
            )

            for _ in rows:
                return True

        return False
