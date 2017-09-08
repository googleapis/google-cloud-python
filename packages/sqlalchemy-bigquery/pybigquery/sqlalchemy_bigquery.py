"""Integration between SQLAlchemy and BigQuery."""

from __future__ import absolute_import
from __future__ import unicode_literals

from google.cloud.bigquery import dbapi
from google.cloud import bigquery
from google.api.core.exceptions import NotFound
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy import types, util
from sqlalchemy.sql.compiler import SQLCompiler, IdentifierPreparer
from sqlalchemy.engine.default import DefaultDialect, DefaultExecutionContext


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
            initial_quote='',
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
    'TIME': types.TIME
    # TODO
    # 'RECORD'
}


class BigQueryExecutionContext(DefaultExecutionContext):
    def create_cursor(self):
        # Set arraysize
        c = super().create_cursor()
        if self.dialect.arraysize:
            c.arraysize = self.dialect.arraysize
        return c


class BigQueryCompiler(SQLCompiler):
    def visit_label(self, *args, **kwargs):
        # Hacky solution to use labels in GROUP BY clause
        if len(kwargs) == 1:
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

    def __init__(self, arraysize=5000, **kwargs):
        super().__init__(**kwargs)
        self.arraysize = arraysize

    @classmethod
    def dbapi(cls):
        return dbapi

    def create_connect_args(self, url):
        client = bigquery.Client(url.host) if url.host else None
        return ([client], {})

    def _split_table_name(self, table_name):
        dataset, table_name = table_name.split('.')
        return (dataset, table_name)

    def has_table(self, connection, table_name, schema=None):
        dataset, table_name = self._split_table_name(table_name)
        return connection.connection._client.dataset(dataset).table(table_name).exists()

    def get_columns(self, connection, table_name, schema=None, **kw):

        dataset, table_name = self._split_table_name(table_name)
        table = connection.connection._client.dataset(dataset).table(table_name)

        table.reload()
        columns = table.schema
        result = []
        for col in columns:
            try:
                coltype = _type_map[col.field_type]
            except KeyError:
                util.warn("Did not recognize type '%s' of column '%s'" % (col.field_type, col.name))

            result.append({
                'name': col.name,
                'type': coltype,
                'nullable': True if col.mode == 'NULLABLE' else False,
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

    def get_table_names(self, connection, schema=None, **kw):
        datasets = connection.connection._client.list_datasets()
        result = []
        for d in datasets:
            tables = d.list_tables()
            for t in tables:
                result.append(d.name + '.' + t.name)
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

