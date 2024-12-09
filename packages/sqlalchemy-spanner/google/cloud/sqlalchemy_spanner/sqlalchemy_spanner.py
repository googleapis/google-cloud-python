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
from google.api_core.client_options import ClientOptions
from google.auth.credentials import AnonymousCredentials
from google.cloud.spanner_v1 import Client
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.sql import elements
from sqlalchemy import ForeignKeyConstraint, types
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.default import DefaultDialect, DefaultExecutionContext
from sqlalchemy.event import listens_for
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.pool import Pool
from sqlalchemy.sql.compiler import (
    selectable,
    DDLCompiler,
    GenericTypeCompiler,
    IdentifierPreparer,
    SQLCompiler,
    OPERATORS,
    RESERVED_WORDS,
)
from sqlalchemy.sql.default_comparator import operator_lookup
from sqlalchemy.sql.operators import json_getitem_op
from sqlalchemy.sql import expression

from google.cloud.spanner_v1.data_types import JsonObject
from google.cloud import spanner_dbapi
from google.cloud.sqlalchemy_spanner._opentelemetry_tracing import trace_call
import sqlalchemy

USING_SQLACLCHEMY_20 = False
if sqlalchemy.__version__.split(".")[0] == "2":
    USING_SQLACLCHEMY_20 = True

if USING_SQLACLCHEMY_20:
    from sqlalchemy.engine.reflection import ObjectKind


@listens_for(Pool, "reset")
def reset_connection(dbapi_conn, connection_record, reset_state=None):
    """An event of returning a connection back to a pool."""
    if hasattr(dbapi_conn, "connection"):
        dbapi_conn = dbapi_conn.connection
    if isinstance(dbapi_conn, spanner_dbapi.Connection):
        if dbapi_conn.inside_transaction:
            dbapi_conn.rollback()

        dbapi_conn.staleness = None
        dbapi_conn.read_only = False
    else:
        dbapi_conn.rollback()


# register a method to get a single value of a JSON object
OPERATORS[json_getitem_op] = operator_lookup["json_getitem_op"]


# Spanner-to-SQLAlchemy types map
_type_map = {
    "BOOL": types.Boolean,
    "BYTES": types.LargeBinary,
    "DATE": types.DATE,
    "DATETIME": types.DATETIME,
    "FLOAT32": types.REAL,
    "FLOAT64": types.Float,
    "INT64": types.BIGINT,
    "NUMERIC": types.NUMERIC(precision=38, scale=9),
    "STRING": types.String,
    "TIME": types.TIME,
    "TIMESTAMP": types.TIMESTAMP,
    "ARRAY": types.ARRAY,
    "JSON": types.JSON,
}


_type_map_inv = {
    types.Boolean: "BOOL",
    types.BINARY: "BYTES(MAX)",
    types.LargeBinary: "BYTES(MAX)",
    types.DATE: "DATE",
    types.DATETIME: "DATETIME",
    types.REAL: "FLOAT32",
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

        read_only = self.execution_options.get("read_only")
        if read_only is not None:
            self._dbapi_connection.connection.read_only = read_only

        staleness = self.execution_options.get("staleness")
        if staleness is not None:
            self._dbapi_connection.connection.staleness = staleness

        priority = self.execution_options.get("request_priority")
        if priority is not None:
            self._dbapi_connection.connection.request_priority = priority

    def fire_sequence(self, seq, type_):
        """Builds a statement for fetching next value of the sequence."""
        return self._execute_scalar(
            (
                "SELECT GET_NEXT_SEQUENCE_VALUE(SEQUENCE %s)"
                % self.identifier_preparer.format_sequence(seq)
            ),
            type_,
        )


class SpannerIdentifierPreparer(IdentifierPreparer):
    """Identifiers compiler.

    In Cloud Spanner backticks "`" are used for keywords escaping.
    """

    reserved_words = RESERVED_WORDS.copy()
    reserved_words.update(spanner_dbapi.parse_utils.SPANNER_RESERVED_KEYWORDS)
    reserved_words_lc = set(map(str.lower, reserved_words))

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
            lc_value in self.reserved_words_lc
            or value[0] in self.illegal_initial_characters
            or not self.legal_characters.match(str(value))
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

    def visit_now_func(self, func, **kwargs):
        return "current_timestamp"

    def visit_empty_set_expr(self, type_, **kw):
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

    def _generate_generic_binary(self, binary, opstring, eager_grouping=False, **kw):
        """The method is overriden to process JSON data type cases."""
        _in_binary = kw.get("_in_binary", False)

        kw["_in_binary"] = True

        if isinstance(opstring, str):
            text = (
                binary.left._compiler_dispatch(
                    self, eager_grouping=eager_grouping, **kw
                )
                + opstring
                + binary.right._compiler_dispatch(
                    self, eager_grouping=eager_grouping, **kw
                )
            )
            if _in_binary and eager_grouping:
                text = "(%s)" % text
        else:
            # got JSON data
            right_value = getattr(
                binary.right, "value", None
            ) or binary.right._compiler_dispatch(
                self, eager_grouping=eager_grouping, **kw
            )

            text = (
                binary.left._compiler_dispatch(
                    self, eager_grouping=eager_grouping, **kw
                )
                + """, "$."""
                + str(right_value)
                + '"'
            )
            text = "JSON_VALUE(%s)" % text

        return text

    def visit_json_path_getitem_op_binary(self, binary, operator, **kw):
        """Build a JSON_VALUE() function call."""
        expr = """JSON_VALUE(%s, "$.%s")"""

        return expr % (
            self.process(binary.left, **kw),
            self.process(binary.right, **kw),
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
        if value is None and not type_.should_evaluate_none:
            # issue #10535 - handle NULL in the compiler without placing
            # this onto each type, except for "evaluate None" types
            # (e.g. JSON)
            return self.process(elements.Null._instance())

        raw = ["\\", "'", '"', "\n", "\t", "\r"]
        if isinstance(value, str) and any(single in value for single in raw):
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
                text += f"\n LIMIT {9223372036854775807-select._offset}"
            text += " OFFSET " + self.process(select._offset_clause, **kw)
        return text

    def returning_clause(self, stmt, returning_cols, **kw):
        columns = [
            self._label_select_column(None, c, True, False, {})
            for c in expression._select_iterables(returning_cols)
        ]

        return "THEN RETURN " + ", ".join(columns)

    def visit_sequence(self, seq, **kw):
        """Builds a statement for fetching next value of the sequence."""
        return " GET_NEXT_SEQUENCE_VALUE(SEQUENCE %s)" % self.preparer.format_sequence(
            seq
        )


class SpannerDDLCompiler(DDLCompiler):
    """Spanner DDL statements compiler."""

    def get_column_specification(self, column, **kwargs):
        """Build new column specifications.

        Overridden to move the NOT NULL statement to front
        of a computed column expression definitions.
        """
        colspec = (
            self.preparer.format_column(column)
            + " "
            + self.dialect.type_compiler.process(column.type, type_expression=column)
        )
        if not column.nullable:
            colspec += " NOT NULL"

        default = self.get_column_default_string(column)
        if default is not None:
            colspec += " DEFAULT (" + default + ")"

        if hasattr(column, "computed") and column.computed is not None:
            colspec += " " + self.process(column.computed)

        return colspec

    def visit_computed_column(self, generated, **kw):
        """Computed column operator."""
        text = "AS (%s) STORED" % self.sql_compiler.process(
            generated.sqltext, include_table=False, literal_binds=True
        )
        return text

    def visit_drop_table(self, drop_table, **kw):
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

        return indexes + constrs + super().visit_drop_table(drop_table)

    def visit_primary_key_constraint(self, constraint, **kw):
        """Build primary key definition.

        Primary key in Spanner is defined outside of a table columns definition, see:
        https://cloud.google.com/spanner/docs/getting-started/python#create_a_database

        The method returns None to omit primary key in a table columns definition.
        """
        return None

    def visit_unique_constraint(self, constraint, **kw):
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

        if "TEMPORARY" in table._prefixes:
            raise NotImplementedError("Temporary tables are not supported.")

        if table.kwargs.get("spanner_interleave_in"):
            post_cmds += ",\nINTERLEAVE IN PARENT {}".format(
                table.kwargs["spanner_interleave_in"]
            )

            if table.kwargs.get("spanner_interleave_on_delete_cascade"):
                post_cmds += " ON DELETE CASCADE"

        return post_cmds

    def visit_create_index(
        self, create, include_schema=False, include_table_schema=True, **kw
    ):
        text = super().visit_create_index(
            create, include_schema, include_table_schema, **kw
        )
        index = create.element
        if "spanner" in index.dialect_options:
            options = index.dialect_options["spanner"]
            if "storing" in options:
                storing = options["storing"]
                storing_columns = [
                    index.table.c[col] if isinstance(col, str) else col
                    for col in storing
                ]
                text += " STORING (%s)" % ", ".join(
                    [self.preparer.quote(c.name) for c in storing_columns]
                )
        return text

    def get_identity_options(self, identity_options):
        text = ["sequence_kind = 'bit_reversed_positive'"]
        if identity_options.start is not None:
            text.append("start_with_counter = %d" % identity_options.start)
        return ", ".join(text)

    def visit_create_sequence(self, create, prefix=None, **kw):
        """Builds a ``CREATE SEQUENCE`` statement for the sequence."""
        text = "CREATE SEQUENCE %s" % self.preparer.format_sequence(create.element)
        options = self.get_identity_options(create.element)
        if options:
            text += " OPTIONS (" + options + ")"
        return text

    def visit_drop_sequence(self, drop, **kw):
        """Builds a ``DROP SEQUENCE`` statement for the sequence."""
        return "DROP SEQUENCE %s" % self.preparer.format_sequence(drop.element)


class SpannerTypeCompiler(GenericTypeCompiler):
    """Spanner types compiler.

    Maps SQLAlchemy types to Spanner data types.
    """

    def visit_INTEGER(self, type_, **kw):
        return "INT64"

    def visit_DOUBLE(self, type_, **kw):
        return "FLOAT64"

    def visit_FLOAT(self, type_, **kw):
        # Note: This was added before Spanner supported FLOAT32.
        # Changing this now to generate a FLOAT32 would be a breaking change.
        # Users therefore have to use REAL to generate a FLOAT32 column.
        return "FLOAT64"

    def visit_REAL(self, type_, **kw):
        return "FLOAT32"

    def visit_TEXT(self, type_, **kw):
        return "STRING({})".format(type_.length or "MAX")

    def visit_ARRAY(self, type_, **kw):
        return "ARRAY<{}>".format(self.process(type_.item_type, **kw))

    def visit_BINARY(self, type_, **kw):  # pragma: no cover
        """
        The BINARY type is superseded by large_binary in
        newer versions of SQLAlchemy (>1.4).
        """
        return "BYTES({})".format(type_.length or "MAX")

    def visit_large_binary(self, type_, **kw):  # pragma: no cover
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

    def visit_JSON(self, type_, **kw):
        return "JSON"


class SpannerDialect(DefaultDialect):
    """Cloud Spanner dialect.

    Represents an API layer to control Cloud Spanner database with SQLAlchemy API.
    """

    name = "spanner+spanner"
    driver = "spanner"
    positional = False
    paramstyle = "format"
    encoding = "utf-8"
    max_identifier_length = 256
    _legacy_binary_type_literal_encoding = "utf-8"

    execute_sequence_format = list

    supports_alter = True
    supports_sane_rowcount = False
    supports_sane_multi_rowcount = False
    supports_default_values = False
    supports_sequences = True
    sequences_optional = False
    supports_native_enum = True
    supports_native_boolean = True
    supports_native_decimal = True
    supports_statement_cache = True

    insert_returning = True
    update_returning = True
    delete_returning = True

    ddl_compiler = SpannerDDLCompiler
    preparer = SpannerIdentifierPreparer
    statement_compiler = SpannerSQLCompiler
    type_compiler = SpannerTypeCompiler
    execution_ctx_cls = SpannerExecutionContext
    _json_serializer = JsonObject
    _json_deserializer = JsonObject

    @classmethod
    def dbapi(cls):
        """A pointer to the Cloud Spanner DB API package.

        Used to initiate connections to the Cloud Spanner databases.
        """
        return spanner_dbapi

    @classmethod
    def import_dbapi(cls):
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

    def _get_table_type_query(self, kind, append_query):
        """
        Generates WHERE condition for Kind of Object.
        Spanner supports Table and View.
        """
        if not USING_SQLACLCHEMY_20:
            return ""

        kind = ObjectKind.TABLE if kind is None else kind
        if kind == ObjectKind.MATERIALIZED_VIEW:
            raise NotImplementedError("Spanner does not support MATERIALIZED VIEWS")
        switch_case = {
            ObjectKind.ANY: ["BASE TABLE", "VIEW"],
            ObjectKind.TABLE: ["BASE TABLE"],
            ObjectKind.VIEW: ["VIEW"],
            ObjectKind.ANY_VIEW: ["VIEW"],
        }

        table_type_query = ""
        for table_type in switch_case[kind]:
            query = f"t.table_type = '{table_type}'"
            if table_type_query != "":
                table_type_query = table_type_query + " OR " + query
            else:
                table_type_query = query

        table_type_query = "(" + table_type_query + ") "
        if append_query:
            table_type_query = table_type_query + " AND "
        return table_type_query

    def _get_table_filter_query(
        self, filter_names, info_schema_table, append_query=False
    ):
        """
        Generates WHERE query for tables or views for which
        information is reflected.
        """
        table_filter_query = ""
        if filter_names is not None:
            for table_name in filter_names:
                query = f"{info_schema_table}.table_name = '{table_name}'"
                if table_filter_query != "":
                    table_filter_query = table_filter_query + " OR " + query
                else:
                    table_filter_query = query
            table_filter_query = "(" + table_filter_query + ") "
            if append_query:
                table_filter_query = table_filter_query + " AND "

        return table_filter_query

    def create_connect_args(self, url):
        """Parse connection args from the given URL.

        The method prepares args suitable to send to the DB API `connect()` function.

        The given URL follows the style:
        `spanner:///projects/{project-id}/instances/{instance-id}/databases/{database-id}`
        or `spanner:///projects/{project-id}/instances/{instance-id}`. For the latter,
        database operations will be not be possible and if required a new engine with
        database-id set will need to be created.
        """
        match = re.match(
            (
                r"^projects/(?P<project>.+?)/instances/"
                "(?P<instance>.+?)(/databases/(?P<database>.+)|$)"
            ),
            url.database,
        )
        dist = pkg_resources.get_distribution("sqlalchemy-spanner")
        options = {"user_agent": f"gl-{dist.project_name}/{dist.version}"}
        connect_opts = url.translate_connect_args()
        if (
            "host" in connect_opts
            and "port" in connect_opts
            and "password" in connect_opts
        ):
            # Create a test client that connects to a local Spanner (mock) server.
            if (
                connect_opts["host"] == "localhost"
                and connect_opts["password"] == "AnonymousCredentials"
            ):
                client = Client(
                    project=match.group("project"),
                    credentials=AnonymousCredentials(),
                    client_options=ClientOptions(
                        api_endpoint=f"{connect_opts['host']}:{connect_opts['port']}",
                    ),
                )
                options["client"] = client
        return (
            [match.group("instance"), match.group("database"), match.group("project")],
            options,
        )

    @engine_to_connection
    def get_view_names(self, connection, schema=None, **kw):
        """
        Gets a list of view names.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            schema (str): Optional. Schema name

        Returns:
            list: List of view names.
        """
        sql = """
            SELECT table_name
            FROM information_schema.views
            WHERE TABLE_SCHEMA='{}'
            """.format(
            schema or ""
        )

        all_views = []
        with connection.connection.database.snapshot() as snap:
            rows = list(snap.execute_sql(sql))
            for view in rows:
                all_views.append(view[0])

        return all_views

    @engine_to_connection
    def get_sequence_names(self, connection, schema=None, **kw):
        """
        Return a list of all sequence names available in the database.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            schema (str): Optional. Schema name

        Returns:
            list: List of sequence names.
        """
        sql = """
            SELECT name
            FROM information_schema.sequences
            WHERE SCHEMA='{}'
            """.format(
            schema or ""
        )
        all_sequences = []
        with connection.connection.database.snapshot() as snap:
            rows = list(snap.execute_sql(sql))
            for seq in rows:
                all_sequences.append(seq[0])

        return all_sequences

    @engine_to_connection
    def get_view_definition(self, connection, view_name, schema=None, **kw):
        """
        Gets definition of a particular view.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            view_name (str): Name of the view.
            schema (str): Optional. Schema name

        Returns:
            str: Definition of view.
        """
        sql = """
            SELECT view_definition
            FROM information_schema.views
            WHERE TABLE_SCHEMA='{schema_name}' AND TABLE_NAME='{view_name}'
            """.format(
            schema_name=schema or "", view_name=view_name
        )

        with connection.connection.database.snapshot() as snap:
            rows = list(snap.execute_sql(sql))
            if rows == []:
                raise NoSuchTableError(f"{schema if schema else ''}.{view_name}")
            result = rows[0][0]

        return result

    @engine_to_connection
    def get_multi_columns(
        self, connection, schema=None, filter_names=None, scope=None, kind=None, **kw
    ):
        """
        Return information about columns in all objects in the given
        schema.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            schema (str): Optional. Schema name
            filter_names (Sequence[str]): Optional. Optionally return information
                only for the objects listed here.
            scope (sqlalchemy.engine.reflection.ObjectScope): Optional. Specifies
                if columns of default, temporary or any tables
                should be reflected. Spanner does not support temporary.
            kind (sqlalchemy.engine.reflection.ObjectKind): Optional. Specifies the
                type of objects to reflect.

        Returns:
            dictionary: a dictionary where the keys are two-tuple schema,table-name
                and the values are list of dictionaries, each representing the
                definition of a database column.
                The schema is ``None`` if no schema is provided.
        """
        table_filter_query = self._get_table_filter_query(filter_names, "col", True)
        schema_filter_query = " col.table_schema = '{schema}' AND ".format(
            schema=schema or ""
        )
        table_type_query = self._get_table_type_query(kind, True)

        sql = """
            SELECT col.table_schema, col.table_name, col.column_name,
                col.spanner_type, col.is_nullable, col.generation_expression
            FROM information_schema.columns as col
            JOIN information_schema.tables AS t
                USING (TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME)
            WHERE
                {table_filter_query}
                {table_type_query}
                {schema_filter_query}
                col.table_catalog = ''
            ORDER BY
                col.table_catalog,
                col.table_schema,
                col.table_name,
                col.ordinal_position
        """.format(
            table_filter_query=table_filter_query,
            table_type_query=table_type_query,
            schema_filter_query=schema_filter_query,
        )
        with connection.connection.database.snapshot() as snap:
            columns = list(snap.execute_sql(sql))
            result_dict = {}

            for col in columns:
                column_info = {
                    "name": col[2],
                    "type": self._designate_type(col[3]),
                    "nullable": col[4] == "YES",
                    "default": None,
                }

                if col[5] is not None:
                    column_info["computed"] = {
                        "persisted": True,
                        "sqltext": col[5],
                    }
                col[0] = col[0] or None
                table_info = result_dict.get((col[0], col[1]), [])
                table_info.append(column_info)
                result_dict[(col[0], col[1])] = table_info

        return result_dict

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
        kind = None if not USING_SQLACLCHEMY_20 else ObjectKind.ANY
        dict = self.get_multi_columns(
            connection, schema=schema, filter_names=[table_name], kind=kind
        )
        schema = schema or None
        return dict.get((schema, table_name), [])

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
    def get_multi_indexes(
        self, connection, schema=None, filter_names=None, scope=None, kind=None, **kw
    ):
        """
        Return information about indexes in all objects
        in the given schema.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            schema (str): Optional. Schema name.
            filter_names (Sequence[str]): Optional. Optionally return information
                only for the objects listed here.
            scope (sqlalchemy.engine.reflection.ObjectScope): Optional. Specifies
                if columns of default, temporary or any tables
                should be reflected. Spanner does not support temporary.
            kind (sqlalchemy.engine.reflection.ObjectKind): Optional. Specifies the
                type of objects to reflect.

        Returns:
            dictionary: a dictionary where the keys are two-tuple schema,table-name
                and the values are list of dictionaries, each representing the
                definition of an index.
                The schema is ``None`` if no schema is provided.
        """
        table_filter_query = self._get_table_filter_query(filter_names, "i", True)
        schema_filter_query = " i.table_schema = '{schema}' AND ".format(
            schema=schema or ""
        )
        table_type_query = self._get_table_type_query(kind, True)

        sql = """
            SELECT
               i.table_schema,
               i.table_name,
               i.index_name,
               (
                   SELECT ARRAY_AGG(ic.column_name)
                   FROM information_schema.index_columns ic
                   WHERE ic.index_name = i.index_name
                   AND ic.table_catalog = i.table_catalog
                   AND ic.table_schema = i.table_schema
                   AND ic.table_name = i.table_name
                   AND ic.column_ordering is not null
               ) as columns,
               i.is_unique,
               (
                   SELECT ARRAY_AGG(ic.column_ordering)
                   FROM information_schema.index_columns ic
                   WHERE ic.index_name = i.index_name
                   AND ic.table_catalog = i.table_catalog
                   AND ic.table_schema = i.table_schema
                   AND ic.table_name = i.table_name
                   AND ic.column_ordering is not null
               ) as column_orderings,
               (
                   SELECT ARRAY_AGG(storing.column_name)
                   FROM information_schema.index_columns storing
                   WHERE storing.index_name = i.index_name
                   AND storing.table_catalog = i.table_catalog
                   AND storing.table_schema = i.table_schema
                   AND storing.table_name = i.table_name
                   AND storing.column_ordering is null
               ) as storing_columns,
            FROM information_schema.indexes as i
            JOIN information_schema.tables AS t
                ON  i.table_catalog = t.table_catalog
                AND i.table_schema = t.table_schema
                AND i.table_name = t.table_name
            WHERE
                {table_filter_query}
                {table_type_query}
                {schema_filter_query}
                i.index_type != 'PRIMARY_KEY'
                AND i.spanner_is_managed = FALSE
            GROUP BY i.table_catalog, i.table_schema, i.table_name,
                     i.index_name, i.is_unique
            ORDER BY i.index_name
        """.format(
            table_filter_query=table_filter_query,
            table_type_query=table_type_query,
            schema_filter_query=schema_filter_query,
        )

        with connection.connection.database.snapshot() as snap:
            rows = list(snap.execute_sql(sql))
            result_dict = {}

            for row in rows:
                dialect_options = {}
                include_columns = row[6]
                if include_columns:
                    dialect_options["spanner_storing"] = include_columns
                index_info = {
                    "name": row[2],
                    "column_names": row[3],
                    "unique": row[4],
                    "column_sorting": {
                        col: order.lower() for col, order in zip(row[3], row[5])
                    },
                    "include_columns": include_columns if include_columns else [],
                    "dialect_options": dialect_options,
                }
                row[0] = row[0] or None
                table_info = result_dict.get((row[0], row[1]), [])
                table_info.append(index_info)
                result_dict[(row[0], row[1])] = table_info

        return result_dict

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
        kind = None if not USING_SQLACLCHEMY_20 else ObjectKind.ANY
        dict = self.get_multi_indexes(
            connection, schema=schema, filter_names=[table_name], kind=kind
        )
        schema = schema or None
        return dict.get((schema, table_name), [])

    @engine_to_connection
    def get_multi_pk_constraint(
        self, connection, schema=None, filter_names=None, scope=None, kind=None, **kw
    ):
        """
        Return information about primary key constraints in
        all tables in the given schema.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            schema (str): Optional. Schema name
            filter_names (Sequence[str]): Optional. Optionally return information
                only for the objects listed here.
            scope (sqlalchemy.engine.reflection.ObjectScope): Optional. Specifies
                if columns of default, temporary or any tables
                should be reflected. Spanner does not support temporary.
            kind (sqlalchemy.engine.reflection.ObjectKind): Optional. Specifies the
                type of objects to reflect.

        Returns:
            dictionary: a dictionary where the keys are two-tuple schema,table-name
                and the values are list of dictionaries, each representing the
                definition of a primary key constraint.
                The schema is ``None`` if no schema is provided.
        """
        table_filter_query = self._get_table_filter_query(filter_names, "tc", True)
        schema_filter_query = " tc.table_schema = '{schema}' AND ".format(
            schema=schema or ""
        )
        table_type_query = self._get_table_type_query(kind, True)

        sql = """
            SELECT tc.table_schema, tc.table_name, ccu.COLUMN_NAME
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
            JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu
                USING (TABLE_CATALOG, TABLE_SCHEMA, CONSTRAINT_NAME)
            JOIN information_schema.tables AS t
                ON  tc.TABLE_CATALOG = t.TABLE_CATALOG
                AND tc.TABLE_SCHEMA = t.TABLE_SCHEMA
                AND tc.TABLE_NAME = t.TABLE_NAME
            WHERE {table_filter_query} {table_type_query}
            {schema_filter_query} tc.CONSTRAINT_TYPE = "PRIMARY KEY"
        """.format(
            table_filter_query=table_filter_query,
            table_type_query=table_type_query,
            schema_filter_query=schema_filter_query,
        )

        with connection.connection.database.snapshot() as snap:
            rows = list(snap.execute_sql(sql))
            result_dict = {}

            for row in rows:
                row[0] = row[0] or None
                table_info = result_dict.get(
                    (row[0], row[1]), {"constrained_columns": []}
                )
                table_info["constrained_columns"].append(row[2])
                result_dict[(row[0], row[1])] = table_info

        return result_dict

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
        kind = None if not USING_SQLACLCHEMY_20 else ObjectKind.ANY
        dict = self.get_multi_pk_constraint(
            connection, schema=schema, filter_names=[table_name], kind=kind
        )
        schema = schema or None
        return dict.get((schema, table_name), [])

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
    def get_multi_foreign_keys(
        self, connection, schema=None, filter_names=None, scope=None, kind=None, **kw
    ):
        """
        Return information about foreign_keys in all tables
        in the given schema.

        The method is used by SQLAlchemy introspection systems.

        Args:
            connection (sqlalchemy.engine.base.Connection):
                SQLAlchemy connection or engine object.
            schema (str): Optional. Schema name
            filter_names (Sequence[str]): Optional. Optionally return information
                only for the objects listed here.
            scope (sqlalchemy.engine.reflection.ObjectScope): Optional. Specifies
                if columns of default, temporary or any tables
                should be reflected. Spanner does not support temporary.
            kind (sqlalchemy.engine.reflection.ObjectKind): Optional. Specifies the
                type of objects to reflect.

        Returns:
            dictionary: a dictionary where the keys are two-tuple schema,table-name
                and the values are list of dictionaries, each representing
                a foreign key definition.
                The schema is ``None`` if no schema is provided.
        """
        table_filter_query = self._get_table_filter_query(filter_names, "tc", True)
        schema_filter_query = " tc.table_schema = '{schema}' AND".format(
            schema=schema or ""
        )
        table_type_query = self._get_table_type_query(kind, True)

        sql = """
        SELECT
            tc.table_schema,
            tc.table_name,
            tc.constraint_name,
            ctu.table_name,
            ctu.table_schema,
            ARRAY_AGG(DISTINCT ccu.column_name),
            ARRAY_AGG(
                DISTINCT CONCAT(
                    CAST(kcu.ordinal_position AS STRING),
                    '_____',
                    kcu.column_name
                )
            )
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.constraint_column_usage AS ccu
                USING (table_catalog, table_schema, constraint_name)
            JOIN information_schema.constraint_table_usage AS ctu
                ON ctu.table_catalog = tc.table_catalog
                and ctu.table_schema = tc.table_schema
                and ctu.constraint_name = tc.constraint_name
            JOIN information_schema.key_column_usage AS kcu
                ON kcu.table_catalog = tc.table_catalog
                and kcu.table_schema = tc.table_schema
                and kcu.constraint_name = tc.constraint_name
            JOIN information_schema.tables AS t
                ON t.table_catalog = tc.table_catalog
                and t.table_schema = tc.table_schema
                and t.table_name = tc.table_name
            WHERE
                {table_filter_query}
                {table_type_query}
                {schema_filter_query}
                tc.constraint_type = "FOREIGN KEY"
            GROUP BY tc.table_name, tc.table_schema, tc.constraint_name,
            ctu.table_name, ctu.table_schema
            """.format(
            table_filter_query=table_filter_query,
            table_type_query=table_type_query,
            schema_filter_query=schema_filter_query,
        )

        with connection.connection.database.snapshot() as snap:
            rows = list(snap.execute_sql(sql))
            result_dict = {}

            for row in rows:
                # Due to Spanner limitations, arrays order is not guaranteed during
                # aggregation. Still, for constraints it's vital to keep the order
                # of the referred columns, otherwise SQLAlchemy and Alembic may start
                # to occasionally drop and recreate constraints. To avoid this, the
                # method uses prefixes with the `key_column_usage.ordinal_position`
                # values to ensure the columns are aggregated into an array in the
                # correct order. Prefixes are only used under the hood. For more details
                # see the issue:
                # https://github.com/googleapis/python-spanner-sqlalchemy/issues/271
                #
                # The solution seem a bit clumsy, and should be improved as soon as a
                # better approach found.
                row[0] = row[0] or None
                table_info = result_dict.get((row[0], row[1]), [])
                for index, value in enumerate(sorted(row[6])):
                    row[6][index] = value.split("_____")[1]

                fk_info = {
                    "name": row[2],
                    "referred_table": row[3],
                    "referred_schema": row[4] or None,
                    "referred_columns": row[5],
                    "constrained_columns": row[6],
                }

                table_info.append(fk_info)
                result_dict[(row[0], row[1])] = table_info

        return result_dict

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
        kind = None if not USING_SQLACLCHEMY_20 else ObjectKind.ANY
        dict = self.get_multi_foreign_keys(
            connection, schema=schema, filter_names=[table_name], kind=kind
        )
        schema = schema or None
        return dict.get((schema, table_name), [])

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
WHERE table_type = 'BASE TABLE' AND table_schema = '{schema}'
""".format(
            schema=schema or ""
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
    USING (TABLE_CATALOG, TABLE_SCHEMA, CONSTRAINT_NAME)
WHERE
    tc.TABLE_NAME="{table_name}"
    AND tc.TABLE_SCHEMA="{table_schema}"
    AND tc.CONSTRAINT_TYPE = "UNIQUE"
    AND tc.CONSTRAINT_NAME IS NOT NULL
""".format(
            table_schema=schema or "", table_name=table_name
        )

        cols = []
        with connection.connection.database.snapshot() as snap:
            rows = snap.execute_sql(sql)

            for row in rows:
                cols.append({"name": row[0], "column_names": [row[1]]})

        return cols

    @engine_to_connection
    def has_table(self, connection, table_name, schema=None, **kw):
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
WHERE TABLE_SCHEMA="{table_schema}" AND TABLE_NAME="{table_name}"
LIMIT 1
""".format(
                    table_schema=schema or "", table_name=table_name
                )
            )

            for _ in rows:
                return True

        return False

    @engine_to_connection
    def has_sequence(self, connection, sequence_name, schema=None, **kw):
        """Check the existence of a particular sequence in the database.

        Given a :class:`_engine.Connection` object and a string
        `sequence_name`, return True if the given sequence exists in
        the database, False otherwise.
        """

        with connection.connection.database.snapshot() as snap:
            rows = snap.execute_sql(
                """
                SELECT true
                FROM INFORMATION_SCHEMA.SEQUENCES
                WHERE NAME="{sequence_name}"
                AND SCHEMA="{schema}"
                LIMIT 1
                """.format(
                    sequence_name=sequence_name, schema=schema or ""
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
            trace_attributes = {
                "db.instance": dbapi_connection.database.name
                if dbapi_connection.database
                else ""
            }
            with trace_call("SpannerSqlAlchemy.Rollback", trace_attributes):
                dbapi_connection.rollback()

    def do_commit(self, dbapi_connection):
        trace_attributes = {
            "db.instance": dbapi_connection.database.name
            if dbapi_connection.database
            else ""
        }
        with trace_call("SpannerSqlAlchemy.Commit", trace_attributes):
            dbapi_connection.commit()

    def do_close(self, dbapi_connection):
        trace_attributes = {
            "db.instance": dbapi_connection.database.name
            if dbapi_connection.database
            else ""
        }
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
@compiles(ColumnNullable, "spanner+spanner")
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
@compiles(ColumnType, "spanner+spanner")
def visit_column_type(
    element: "ColumnType", compiler: "SpannerDDLCompiler", **kw
) -> str:
    return "%s %s %s %s" % (
        alter_table(compiler, element.table_name, element.schema),
        alter_column(compiler, element.column_name),
        "%s" % format_type(compiler, element.type_),
        "" if element.existing_nullable else "NOT NULL",
    )
