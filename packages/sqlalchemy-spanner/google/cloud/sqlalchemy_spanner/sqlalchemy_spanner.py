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

import pkg_resources
import re

from alembic.ddl.base import (
    ColumnNullable,
    ColumnType,
    alter_column,
    alter_table,
    format_type,
)
from sqlalchemy import ForeignKeyConstraint, types, util
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.default import DefaultDialect, DefaultExecutionContext
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.compiler import (
    selectable,
    DDLCompiler,
    GenericTypeCompiler,
    IdentifierPreparer,
    SQLCompiler,
    RESERVED_WORDS,
)

from google.cloud import spanner_dbapi
from google.cloud.sqlalchemy_spanner._opentelemetry_tracing import trace_call

# Spanner-to-SQLAlchemy types map
_type_map = {
    "BOOL": types.Boolean,
    "BYTES": types.LargeBinary,
    "DATE": types.DATE,
    "DATETIME": types.DATETIME,
    "FLOAT64": types.Float,
    "INT64": types.BIGINT,
    "NUMERIC": types.NUMERIC(precision=38, scale=9),
    "STRING": types.String,
    "TIME": types.TIME,
    "TIMESTAMP": types.TIMESTAMP,
    "ARRAY": types.ARRAY,
}

_type_map_inv = {
    types.Boolean: "BOOL",
    types.BINARY: "BYTES(MAX)",
    types.LargeBinary: "BYTES(MAX)",
    types.DATE: "DATE",
    types.DATETIME: "DATETIME",
    types.Float: "FLOAT64",
    types.BIGINT: "INT64",
    types.DECIMAL: "NUMERIC",
    types.String: "STRING",
    types.TIME: "TIME",
    types.TIMESTAMP: "TIMESTAMP",
    types.Integer: "INT64",
    types.NullType: "INT64",
}

_compound_keywords = {
    selectable.CompoundSelect.UNION: "UNION DISTINCT",
    selectable.CompoundSelect.UNION_ALL: "UNION ALL",
    selectable.CompoundSelect.EXCEPT: "EXCEPT DISTINCT",
    selectable.CompoundSelect.EXCEPT_ALL: "EXCEPT ALL",
    selectable.CompoundSelect.INTERSECT: "INTERSECT DISTINCT",
    selectable.CompoundSelect.INTERSECT_ALL: "INTERSECT ALL",
}

_max_size = 2621440


def int_from_size(size_str):
    """Convert a string column length to an integer value.

    Args:
        size_str (str): The column length or the 'MAX' keyword.

    Returns:
        int: The column length value.
    """
    return _max_size if size_str == "MAX" else int(size_str)


def engine_to_connection(function):
    """
    Decorator to initiate a connection to a
    database in case of an engine-related use.
    """

    def wrapper(self, connection, *args, **kwargs):
        """
        Args:
            connection (Union[
                sqlalchemy.engine.base.Connection,
                sqlalchemy.engine.Engine
            ]):
                SQLAlchemy connection or engine object.
        """
        if isinstance(connection, Engine):
            connection = connection.connect()

        return function(self, connection, *args, **kwargs)

    return wrapper


class SpannerExecutionContext(DefaultExecutionContext):
    def pre_exec(self):
        """
        Apply execution options to the DB API connection before
        executing the next SQL operation.
        """
        super(SpannerExecutionContext, self).pre_exec()

        read_only = self.execution_options.get("read_only", None)
        if read_only is not None:
            self._dbapi_connection.connection.read_only = read_only


class SpannerIdentifierPreparer(IdentifierPreparer):
    """Identifiers compiler.

    In Cloud Spanner backticks "`" are used for keywords escaping.
    """

    reserved_words = RESERVED_WORDS.copy()
    reserved_words.update(spanner_dbapi.parse_utils.SPANNER_RESERVED_KEYWORDS)

    def __init__(self, dialect):
        super(SpannerIdentifierPreparer, self).__init__(
            dialect, initial_quote="`", final_quote="`"
        )

    def _requires_quotes(self, value):
        """Return True if the given identifier requires quoting."""
        lc_value = value.lower()
        if lc_value == '"unicode"':  # don't escape default Spanner colation
            return False

        return (
            lc_value in self.reserved_words
            or value[0] in self.illegal_initial_characters
            or not self.legal_characters.match(util.text_type(value))
            or (lc_value != value)
        )


class SpannerSQLCompiler(SQLCompiler):
    """Spanner SQL statements compiler."""

    compound_keywords = _compound_keywords

    def get_from_hint_text(self, _, text):
        """Return a hint text.

        Overriden to avoid adding square brackets to the hint text.

        Args:
            text (str): The hint text.
        """
        return text

    def visit_empty_set_expr(self, type_):
        """Return an empty set expression of the given type.

        Args:
            type_ (sqlalchemy.sql.sqltypes.SchemaType):
                A SQLAlchemy data type.

        Returns:
            str: A query to select an empty set of the given type.
        """
        return "SELECT CAST(1 AS {}) FROM (SELECT 1) WHERE 1 != 1".format(
            _type_map_inv[type(type_[0])]
        )

    def visit_like_op_binary(self, binary, operator, **kw):
        """Build a LIKE clause."""
        if binary.modifiers.get("escape", None):
            raise NotImplementedError("ESCAPE keyword is not supported by Spanner")

        # TODO: use ternary here, not "and"/ "or"
        return "%s LIKE %s" % (
            binary.left._compiler_dispatch(self, **kw),
            binary.right._compiler_dispatch(self, **kw),
        )

    def render_literal_value(self, value, type_):
        """Render the value of a bind parameter as a quoted literal.

        This is used for statement sections that do not accept bind parameters
        on the target driver/database.

        This should be implemented by subclasses using the quoting services
        of the DBAPI.

        Cloud spanner supports prefixed backslash to escape non-alphanumeric characters
        in string. Override the method to add  additional escape before using it to
        generate a SQL statement.
        """
        raw = ["\\", "'", '"', "\n", "\t", "\r"]
        if type(value) == str and any(single in value for single in raw):
            value = 'r"""{}"""'.format(value)
            return value
        else:
            processor = type_._cached_literal_processor(self.dialect)
            if processor:
                return processor(value)
            else:
                raise NotImplementedError(
                    "Don't know how to literal-quote value %r" % value
                )

    def limit_clause(self, select, **kw):
        """Build LIMIT-OFFSET clause.

        Spanner doesn't support using OFFSET without a LIMIT
        clause. It also doesn't support negative LIMITs, while
        SQLAlchemy support both.

        The method builds LIMIT-OFFSET clauses as usual, with
        only difference: when OFFSET is used without an explicit
        LIMIT, the dialect compiles a statement with a LIMIT
        set to the biggest integer value.

        Args:
            (sqlalchemy.sql.selectable.Select): Select clause object.

        Returns:
            str: LIMIT-OFFSET clause.
        """
        text = ""
        if select._limit_clause is not None:
            text += "\n LIMIT " + self.process(select._limit_clause, **kw)
        if select._offset_clause is not None:
            if select._limit_clause is None:
                text += "\n LIMIT 9223372036854775805"
            text += " OFFSET " + self.process(select._offset_clause, **kw)
        return text


class SpannerDDLCompiler(DDLCompiler):
    """Spanner DDL statements compiler."""

    def visit_drop_table(self, drop_table):
        """
        Cloud Spanner doesn't drop tables which have indexes
        or foreign key constraints. This method builds several DDL
        statements separated by semicolons to drop the indexes and
        foreign keys constraints of the table before the DROP TABLE
        statement.

        Args:
            (sqlalchemy.schema.DropTable): DROP TABLE statement object.

        Returns:
            str:
                DDL statements separated by semicolons, which will
                sequentially drop indexes, foreign keys constraints
                and then the table itself.
        """
        constrs = ""
        for cons in drop_table.element.constraints:
            if isinstance(cons, ForeignKeyConstraint) and cons.name:
                constrs += "ALTER TABLE {table} DROP CONSTRAINT {constr};".format(
                    table=drop_table.element.name,
                    constr=self.preparer.quote(cons.name),
                )

        indexes = ""
        for index in drop_table.element.indexes:
            indexes += "DROP INDEX {};".format(self.preparer.quote(index.name))

        return indexes + constrs + str(drop_table)

    def visit_primary_key_constraint(self, constraint):
        """Build primary key definition.

        Primary key in Spanner is defined outside of a table columns definition, see:
        https://cloud.google.com/spanner/docs/getting-started/python#create_a_database

        The method returns None to omit primary key in a table columns definition.
        """
        return None

    def visit_unique_constraint(self, constraint):
        """Unique constraints in Spanner are defined with indexes:
        https://cloud.google.com/spanner/docs/secondary-indexes#unique-indexes

        The method throws an exception to notify user that in
        Spanner unique constraints are done with unique indexes.
        """
        raise spanner_dbapi.exceptions.ProgrammingError(
            "Spanner doesn't support direct UNIQUE constraints creation. "
            "Create UNIQUE indexes instead."
        )

    def post_create_table(self, table):
        """Build statements to be executed after CREATE TABLE.

        Includes "primary key" and "interleaved table" statements generation.

        Args:
            table (sqlalchemy.schema.Table): Table to create.

        Returns:
            str: primary key difinition to add to the table CREATE request.
        """
        cols = [col.name for col in table.primary_key.columns]
        post_cmds = " PRIMARY KEY ({})".format(", ".join(cols))

        if table.kwargs.get("spanner_interleave_in"):
            post_cmds += ",\nINTERLEAVE IN PARENT {}".format(
                table.kwargs["spanner_interleave_in"]
            )

            if table.kwargs.get("spanner_interleave_on_delete_cascade"):
                post_cmds += " ON DELETE CASCADE"

        return post_cmds


class SpannerTypeCompiler(GenericTypeCompiler):
    """Spanner types compiler.

    Maps SQLAlchemy types to Spanner data types.
    """

    def visit_INTEGER(self, type_, **kw):
        return "INT64"

    def visit_FLOAT(self, type_, **kw):
        return "FLOAT64"

    def visit_TEXT(self, type_, **kw):
        return "STRING({})".format(type_.length or "MAX")

    def visit_ARRAY(self, type_, **kw):
        return "ARRAY<{}>".format(self.process(type_.item_type, **kw))

    def visit_BINARY(self, type_, **kw):
        return "BYTES({})".format(type_.length or "MAX")

    def visit_large_binary(self, type_, **kw):
        return "BYTES({})".format(type_.length or "MAX")

    def visit_DECIMAL(self, type_, **kw):
        return "NUMERIC"

    def visit_VARCHAR(self, type_, **kw):
        return "STRING({})".format(type_.length or "MAX")

    def visit_CHAR(self, type_, **kw):
        return "STRING({})".format(type_.length or "MAX")

    def visit_BOOLEAN(self, type_, **kw):
        return "BOOL"

    def visit_DATETIME(self, type_, **kw):
        return "TIMESTAMP"

    def visit_NUMERIC(self, type_, **kw):
        return "NUMERIC"

    def visit_BIGINT(self, type_, **kw):
        return "INT64"


class SpannerDialect(DefaultDialect):
    """Cloud Spanner dialect.

    Represents an API layer to control Cloud Spanner database with SQLAlchemy API.
    """

    name = "spanner"
    driver = "spanner"
    positional = False
    paramstyle = "format"
    encoding = "utf-8"
    max_identifier_length = 128

    execute_sequence_format = list

    supports_alter = True
    supports_sane_rowcount = False
    supports_sane_multi_rowcount = False
    supports_default_values = False
    supports_sequences = True
    supports_native_enum = True
    supports_native_boolean = True
    supports_native_decimal = True

    ddl_compiler = SpannerDDLCompiler
    preparer = SpannerIdentifierPreparer
    statement_compiler = SpannerSQLCompiler
    type_compiler = SpannerTypeCompiler
    execution_ctx_cls = SpannerExecutionContext

    @classmethod
    def dbapi(cls):
        """A pointer to the Cloud Spanner DB API package.

        Used to initiate connections to the Cloud Spanner databases.
        """
        return spanner_dbapi

    @property
    def default_isolation_level(self):
        """Default isolation level name.

        Returns:
            str: default isolation level.
        """
        return "SERIALIZABLE"

    @default_isolation_level.setter
    def default_isolation_level(self, value):
        """Default isolation level should not be changed."""
        pass

    def _check_unicode_returns(self, connection, additional_tests=None):
        """Ensure requests are returning Unicode responses."""
        return True

    def _get_default_schema_name(self, _):
        """Get default Cloud Spanner schema name.

        Returns:
            str: Schema name.
        """
        return ""

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
        dist = pkg_resources.get_distribution("sqlalchemy-spanner")
        return (
            [match.group("instance"), match.group("database"), match.group("project")],
            {"user_agent": dist.project_name + "/" + dist.version},
        )

    @engine_to_connection
    def get_columns(self, connection, table_name, schema=None, **kw):
        """Get the table columns description.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            list: The table every column dict-like description.
        """
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
                cols_desc.append(
                    {
                        "name": col[0],
                        "type": self._designate_type(col[1]),
                        "nullable": col[2] == "YES",
                        "default": None,
                    }
                )
        return cols_desc

    def _designate_type(self, str_repr):
        """
        Designate an SQLAlchemy data type from a Spanner
        string representation.

        Args:
            str_repr (str): String representation of a type.

        Returns:
            An SQLAlchemy data type.
        """
        if str_repr.startswith("STRING"):
            end = str_repr.index(")")
            size = int_from_size(str_repr[7:end])
            return _type_map["STRING"](length=size)
        # add test creating a table with bytes
        elif str_repr.startswith("BYTES"):
            end = str_repr.index(")")
            size = int_from_size(str_repr[6:end])
            return _type_map["BYTES"](length=size)
        elif str_repr.startswith("ARRAY"):
            inner_type_str = str_repr[6:-1]
            inner_type = self._designate_type(inner_type_str)
            return _type_map["ARRAY"](inner_type)
        else:
            return _type_map[str_repr]

    @engine_to_connection
    def get_indexes(self, connection, table_name, schema=None, **kw):
        """Get the table indexes.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            list: List with indexes description.
        """
        sql = """
SELECT
    i.index_name,
    ARRAY_AGG(ic.column_name),
    i.is_unique,
    ARRAY_AGG(ic.column_ordering)
FROM information_schema.indexes as i
JOIN information_schema.index_columns AS ic
    ON ic.index_name = i.index_name AND ic.table_name = i.table_name
WHERE
    i.table_name="{table_name}"
    AND i.index_type != 'PRIMARY_KEY'
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

    @engine_to_connection
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        """Get the table primary key constraint.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
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

        cols = []
        with connection.connection.database.snapshot() as snap:
            rows = snap.execute_sql(sql)

            for row in rows:
                cols.append(row[0])

        return {"constrained_columns": cols}

    @engine_to_connection
    def get_schema_names(self, connection, **kw):
        """Get all the schemas in the database.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.

        Returns:
            list: Schema names.
        """
        schemas = []
        with connection.connection.database.snapshot() as snap:
            rows = snap.execute_sql(
                "SELECT schema_name FROM information_schema.schemata"
            )

            for row in rows:
                schemas.append(row[0])

        return schemas

    @engine_to_connection
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        """Get the table foreign key constraints.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            list: Dicts, each of which describes a foreign key constraint.
        """
        sql = """
SELECT
    tc.constraint_name,
    ctu.table_name,
    ctu.table_schema,
    ARRAY_AGG(DISTINCT ccu.column_name),
    ARRAY_AGG(kcu.column_name)
FROM information_schema.table_constraints AS tc
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
JOIN information_schema.constraint_table_usage AS ctu
    ON ctu.constraint_name = tc.constraint_name
JOIN information_schema.key_column_usage AS kcu
    ON kcu.constraint_name = tc.constraint_name
WHERE
    tc.table_name="{table_name}"
    AND tc.constraint_type = "FOREIGN KEY"
GROUP BY tc.constraint_name, ctu.table_name, ctu.table_schema
""".format(
            table_name=table_name
        )

        keys = []
        with connection.connection.database.snapshot() as snap:
            rows = snap.execute_sql(sql)

            for row in rows:
                keys.append(
                    {
                        "name": row[0],
                        "referred_table": row[1],
                        "referred_schema": row[2] or None,
                        "referred_columns": row[3],
                        "constrained_columns": row[4],
                    }
                )
        return keys

    @engine_to_connection
    def get_table_names(self, connection, schema=None, **kw):
        """Get all the tables from the given schema.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            schema (str): Optional. Schema name.

        Returns:
            list: Names of the tables within the given schema.
        """
        sql = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = '{}'
""".format(
            schema or ""
        )

        table_names = []
        with connection.connection.database.snapshot() as snap:
            rows = snap.execute_sql(sql)

            for row in rows:
                table_names.append(row[0])

        return table_names

    @engine_to_connection
    def get_unique_constraints(self, connection, table_name, schema=None, **kw):
        """Get the table unique constraints.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name

        Returns:
            dict: Dict with the unique constraints' descriptions.
        """
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

    @engine_to_connection
    def has_table(self, connection, table_name, schema=None):
        """Check if the given table exists.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            table_name (str): Name of the table to introspect.
            schema (str): Optional. Schema name.

        Returns:
            bool: True, if the given table exists, False otherwise.
        """
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

    def set_isolation_level(self, conn_proxy, level):
        """Set the connection isolation level.

        Args:
            conn_proxy (
                Union[
                    sqlalchemy.pool._ConnectionFairy,
                    spanner_dbapi.connection.Connection,
                ]
            ):
                Database connection proxy object or the connection iself.
            level (string): Isolation level.
        """
        if isinstance(conn_proxy, spanner_dbapi.Connection):
            conn = conn_proxy
        else:
            conn = conn_proxy.connection

        conn.autocommit = level == "AUTOCOMMIT"

    def get_isolation_level(self, conn_proxy):
        """Get the connection isolation level.

        Args:
            conn_proxy (
                Union[
                    sqlalchemy.pool._ConnectionFairy,
                    spanner_dbapi.connection.Connection,
                ]
            ):
                Database connection proxy object or the connection iself.

        Returns:
            str: the connection isolation level.
        """
        if isinstance(conn_proxy, spanner_dbapi.Connection):
            conn = conn_proxy
        else:
            conn = conn_proxy.connection

        return "AUTOCOMMIT" if conn.autocommit else "SERIALIZABLE"

    def do_rollback(self, dbapi_connection):
        """
        To prevent rollback exception, don't rollback
        committed/rolled back transactions.
        """
        if not isinstance(dbapi_connection, spanner_dbapi.Connection):
            dbapi_connection = dbapi_connection.connection

        if dbapi_connection._transaction and (
            dbapi_connection._transaction.rolled_back
            or dbapi_connection._transaction.committed
        ):
            pass
        else:
            trace_attributes = {"db.instance": dbapi_connection.database.name}
            with trace_call("SpannerSqlAlchemy.Rollback", trace_attributes):
                dbapi_connection.rollback()

    def do_commit(self, dbapi_connection):
        trace_attributes = {"db.instance": dbapi_connection.database.name}
        with trace_call("SpannerSqlAlchemy.Commit", trace_attributes):
            dbapi_connection.commit()

    def do_close(self, dbapi_connection):
        trace_attributes = {"db.instance": dbapi_connection.database.name}
        with trace_call("SpannerSqlAlchemy.Close", trace_attributes):
            dbapi_connection.close()

    def do_executemany(self, cursor, statement, parameters, context=None):
        trace_attributes = {
            "db.statement": statement,
            "db.params": parameters,
            "db.instance": cursor.connection.database.name,
        }
        with trace_call("SpannerSqlAlchemy.ExecuteMany", trace_attributes):
            cursor.executemany(statement, parameters)

    def do_execute(self, cursor, statement, parameters, context=None):
        trace_attributes = {
            "db.statement": statement,
            "db.params": parameters,
            "db.instance": cursor.connection.database.name,
        }
        with trace_call("SpannerSqlAlchemy.Execute", trace_attributes):
            cursor.execute(statement, parameters)

    def do_execute_no_params(self, cursor, statement, context=None):
        trace_attributes = {
            "db.statement": statement,
            "db.instance": cursor.connection.database.name,
        }
        with trace_call("SpannerSqlAlchemy.ExecuteNoParams", trace_attributes):
            cursor.execute(statement)


# Alembic ALTER operation override
@compiles(ColumnNullable, "spanner")
def visit_column_nullable(
    element: "ColumnNullable", compiler: "SpannerDDLCompiler", **kw
) -> str:
    return "%s %s %s %s" % (
        alter_table(compiler, element.table_name, element.schema),
        alter_column(compiler, element.column_name),
        format_type(compiler, element.existing_type),
        "" if element.nullable else "NOT NULL",
    )


# Alembic ALTER operation override
@compiles(ColumnType, "spanner")
def visit_column_type(
    element: "ColumnType", compiler: "SpannerDDLCompiler", **kw
) -> str:
    return "%s %s %s" % (
        alter_table(compiler, element.table_name, element.schema),
        alter_column(compiler, element.column_name),
        "%s" % format_type(compiler, element.type_),
    )
