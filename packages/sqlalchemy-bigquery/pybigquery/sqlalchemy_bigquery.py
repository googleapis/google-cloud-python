"""Integration between SQLAlchemy and BigQuery."""

from __future__ import absolute_import
from __future__ import unicode_literals

from google.cloud.bigquery import dbapi
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy import types, util
from sqlalchemy.sql.compiler import SQLCompiler, IdentifierPreparer
from sqlalchemy.engine.default import DefaultDialect, DefaultExecutionContext
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import Column


class UniversalSet(object):
    """
    Set containing everything
    https://github.com/dropbox/PyHive/blob/master/pyhive/common.py
    """

    def __contains__(self, item):
        return True


class BigQueryIdentifierPreparer(IdentifierPreparer):
    """
    Set containing everything
    https://github.com/dropbox/PyHive/blob/master/pyhive/sqlalchemy_presto.py
    """
    reserved_words = UniversalSet()

    def __init__(self, dialect):
        super(BigQueryIdentifierPreparer, self).__init__(
            dialect,
            initial_quote="`",
        )

    def format_label(self, *args, **kwargs):
        # Replace dots with underscores in labels
        result = super(BigQueryIdentifierPreparer, self).format_label(*args, **kwargs)
        return result.replace('.', '_')


_type_map = {
    'STRING': types.String,
    'BOOLEAN': types.Boolean,
    'INTEGER': types.Integer,
    'FLOAT': types.Float,
    'TIMESTAMP': types.TIMESTAMP,
    'DATETIME': types.DATETIME,
    'DATE': types.DATE,
    'BYTES': types.BINARY,
    'TIME': types.TIME,
    'RECORD': types.JSON,
}


class BigQueryExecutionContext(DefaultExecutionContext):
    def create_cursor(self):
        # Set arraysize
        c = super(BigQueryExecutionContext, self).create_cursor()
        if self.dialect.arraysize:
            c.arraysize = self.dialect.arraysize
        return c


class BigQueryCompiler(SQLCompiler):
    def __init__(self, dialect, statement, column_keys=None,
                 inline=False, **kwargs):
        if isinstance(statement, Column):
             kwargs['compile_kwargs'] = util.immutabledict({'include_table': False})
        super(BigQueryCompiler, self).__init__(dialect, statement, column_keys, inline, **kwargs)

    def visit_label(self, *args, **kwargs):
        # Use labels in GROUP BY clause
        if len(kwargs) == 0 or len(kwargs) == 1:
            kwargs['render_label_as_label'] = args[0]
        result = super(BigQueryCompiler, self).visit_label(*args, **kwargs)
        return result


class BigQueryDialect(DefaultDialect):
    name = 'bigquery'
    driver = 'bigquery'
    preparer = BigQueryIdentifierPreparer
    statement_compiler = BigQueryCompiler
    execution_ctx_cls = BigQueryExecutionContext
    supports_alter = False
    supports_pk_autoincrement = False
    supports_default_values = False
    supports_empty_insert = False
    supports_unicode_statements = True
    supports_unicode_binds = True
    returns_unicode_strings = True
    description_encoding = None
    supports_native_boolean = True
    supports_simple_order_by_label = True
    postfetch_lastrowid = False

    def __init__(self, arraysize=5000, credentials_path=None, *args, **kwargs):
        super(BigQueryDialect, self).__init__(*args, **kwargs)
        self.arraysize = arraysize
        self.credentials_path = credentials_path

    @classmethod
    def dbapi(cls):
        return dbapi

    def create_connect_args(self, url):
        if self.credentials_path:
            client = bigquery.Client.from_service_account_json(self.credentials_path)
        else:
            client = bigquery.Client(url.host)
        return ([client], {})

    def _split_table_name(self, full_table_name):
        # Split full_table_name to get project, dataset and table name
        dataset = None
        table_name = None
        project = None

        table_name_split = full_table_name.split('.')
        if len(table_name_split) == 2:
            dataset, table_name = table_name_split
        elif len(table_name_split) == 3:
            project, dataset, table_name = table_name_split

        return (project, dataset, table_name)

    def _get_table(self, connection, table_name, schema=None):
        if isinstance(connection, Engine):
            connection = connection.connect()

        project, dataset, table_name_prepared = self._split_table_name(table_name)
        if dataset is None and schema is not None:
            dataset = schema
            table_name_prepared = table_name

        table = connection.connection._client.dataset(dataset, project=project).table(table_name_prepared)
        try:
            t = connection.connection._client.get_table(table)
        except NotFound as e:
            raise NoSuchTableError(table_name)
        return t

    def has_table(self, connection, table_name, schema=None):
        try:
            self._get_table(connection, table_name, schema)
            return True
        except NoSuchTableError:
            return False

    def get_columns(self, connection, table_name, schema=None, **kw):
        table = self._get_table(connection, table_name, schema)
        columns = table.schema
        result = []
        for col in columns:
            try:
                coltype = _type_map[col.field_type]
            except KeyError:
                util.warn("Did not recognize type '%s' of column '%s'" % (col.field_type, col.name))

            result.append({
                'name': col.name,
                'type': types.ARRAY if col.mode == 'REPEATED' else coltype,
                'nullable': col.mode == 'NULLABLE' or col.mode == 'REPEATED',
                'default': None,
            })

        return result

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        # BigQuery has no support for foreign keys.
        return []

    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        # BigQuery has no support for primary keys.
        return []

    def get_indexes(self, connection, table_name, schema=None, **kw):
        # BigQuery has no support for indexes.
        return []

    def get_schema_names(self, connection, **kw):
        if isinstance(connection, Engine):
            connection = connection.connect()

        datasets = connection.connection._client.list_datasets()
        return [d.dataset_id for d in datasets]

    def get_table_names(self, connection, schema=None, **kw):
        if isinstance(connection, Engine):
            connection = connection.connect()

        datasets = connection.connection._client.list_datasets()
        result = []
        for d in datasets:
            if schema is not None and d.dataset_id != schema:
                continue
            tables = connection.connection._client.list_tables(d.reference)
            for t in tables:
                result.append(d.dataset_id + '.' + t.table_id)
        return result

    def do_rollback(self, dbapi_connection):
        # BigQuery has no support for transactions.
        pass

    def _check_unicode_returns(self, connection, additional_tests=None):
        # requests gives back Unicode strings
        return True

    def _check_unicode_description(self, connection):
        # requests gives back Unicode strings
        return True
