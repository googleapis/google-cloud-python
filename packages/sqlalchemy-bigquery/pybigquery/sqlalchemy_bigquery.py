"""Integration between SQLAlchemy and BigQuery."""

from __future__ import absolute_import
from __future__ import unicode_literals

import operator

from google import auth
from google.cloud import bigquery
from google.cloud.bigquery import dbapi
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery.table import TableReference
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy import types, util
from sqlalchemy.sql.compiler import SQLCompiler, GenericTypeCompiler, DDLCompiler, IdentifierPreparer
from sqlalchemy.engine.default import DefaultDialect, DefaultExecutionContext
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql import elements
import re

from .parse_url import parse_url

FIELD_ILLEGAL_CHARACTERS = re.compile(r'[^\w]+')


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

    def quote_column(self, value):
        """
        Quote a column.
        Fields are quoted separately from the record name.
        """

        parts = value.split('.')
        return '.'.join(self.quote_identifier(x) for x in parts)

    def quote(self, ident, force=None, column=False):
        """
        Conditionally quote an identifier.
        """

        force = getattr(ident, "quote", None)

        if force is None:
            if ident in self._strings:
                return self._strings[ident]
            else:
                if self._requires_quotes(ident):
                    self._strings[ident] = self.quote_column(ident) if column else self.quote_identifier(ident)
                else:
                    self._strings[ident] = ident
                return self._strings[ident]
        elif force:
            return self.quote_column(ident) if column else self.quote_identifier(ident)
        else:
            return ident

    def format_label(self, label, name=None):
        name = name or label.name

        # Fields must start with a letter or underscore
        if not name[0].isalpha() and name[0] != '_':
            name = "_" + name

        # Fields must contain only letters, numbers, and underscores
        name = FIELD_ILLEGAL_CHARACTERS.sub('_', name)

        result = self.quote(name)
        return result


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
    'NUMERIC': types.DECIMAL,
}

STRING = _type_map['STRING']
BOOLEAN = _type_map['BOOLEAN']
INTEGER = _type_map['INTEGER']
FLOAT = _type_map['FLOAT']
TIMESTAMP = _type_map['TIMESTAMP']
DATETIME = _type_map['DATETIME']
DATE = _type_map['DATE']
BYTES = _type_map['BYTES']
TIME = _type_map['TIME']
RECORD = _type_map['RECORD']
NUMERIC = _type_map['NUMERIC']


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

    def visit_select(self, *args, **kwargs):
        """
        Use labels for every column.
        This ensures that fields won't contain duplicate names
        """

        args[0].use_labels = True
        return super(BigQueryCompiler, self).visit_select(*args, **kwargs)

    def visit_column(self, column, add_to_result_map=None,
                     include_table=True, **kwargs):

        name = orig_name = column.name
        if name is None:
            name = self._fallback_column_name(column)

        is_literal = column.is_literal
        if not is_literal and isinstance(name, elements._truncated_label):
            name = self._truncated_identifier("colident", name)

        if add_to_result_map is not None:
            add_to_result_map(
                name,
                orig_name,
                (column, name, column.key),
                column.type
            )

        if is_literal:
            name = self.escape_literal_column(name)
        else:
            name = self.preparer.quote(name, column=True)
        table = column.table
        if table is None or not include_table or not table.named_with_column:
            return name
        else:
            effective_schema = self.preparer.schema_for_object(table)

            if effective_schema:
                schema_prefix = self.preparer.quote_schema(
                    effective_schema) + '.'
            else:
                schema_prefix = ''
            tablename = table.name
            if isinstance(tablename, elements._truncated_label):
                tablename = self._truncated_identifier("alias", tablename)
            return schema_prefix + \
                self.preparer.quote(tablename) + \
                "." + name

    def visit_label(self, *args, within_group_by=False, **kwargs):
        # Use labels in GROUP BY clause.
        #
        # Flag set in the group_by_clause method. Works around missing
        # equivalent to supports_simple_order_by_label for group by.
        if within_group_by:
            kwargs['render_label_as_label'] = args[0]
        return super(BigQueryCompiler, self).visit_label(*args, **kwargs)

    def group_by_clause(self, select, **kw):
        return super(BigQueryCompiler, self).group_by_clause(
            select, **kw, within_group_by=True
        )


class BigQueryTypeCompiler(GenericTypeCompiler):

    def visit_integer(self, type_, **kw):
        return 'INT64'

    def visit_float(self, type_, **kw):
        return 'FLOAT64'

    def visit_text(self, type_, **kw):
        return 'STRING'

    def visit_string(self, type_, **kw):
        return 'STRING'

    def visit_ARRAY(self, type_, **kw):
        return "ARRAY<{}>".format(self.process(type_.item_type, **kw))

    def visit_BINARY(self, type_, **kw):
        return 'BYTES'

    def visit_NUMERIC(self, type_, **kw):
        return 'NUMERIC'

    def visit_DECIMAL(self, type_, **kw):
        return 'NUMERIC'


class BigQueryDDLCompiler(DDLCompiler):

    # BigQuery has no support for foreign keys.
    def visit_foreign_key_constraint(self, constraint):
        return None

    # BigQuery has no support for primary keys.
    def visit_primary_key_constraint(self, constraint):
        return None

    def get_column_specification(self, column, **kwargs):
        colspec = super(BigQueryDDLCompiler, self).get_column_specification(column, **kwargs)
        if column.doc is not None:
            colspec = '{} OPTIONS(description={})'.format(colspec, self.preparer.quote(column.doc))
        return colspec

    def post_create_table(self, table):
        bq_opts = table.dialect_options['bigquery']
        opts = []
        if 'description' in bq_opts:
            opts.append('description={}'.format(self.preparer.quote(bq_opts['description'])))
        if 'friendly_name' in bq_opts:
            opts.append('friendly_name={}'.format(self.preparer.quote(bq_opts['friendly_name'])))
        if opts:
            return '\nOPTIONS({})'.format(', '.join(opts))
        return ''


class BigQueryDialect(DefaultDialect):
    name = 'bigquery'
    driver = 'bigquery'
    preparer = BigQueryIdentifierPreparer
    statement_compiler = BigQueryCompiler
    type_compiler = BigQueryTypeCompiler
    ddl_compiler = BigQueryDDLCompiler
    execution_ctx_cls = BigQueryExecutionContext
    supports_alter = False
    supports_pk_autoincrement = False
    supports_default_values = False
    supports_empty_insert = False
    supports_multiline_insert = True
    supports_unicode_statements = True
    supports_unicode_binds = True
    supports_native_decimal = True
    returns_unicode_strings = True
    description_encoding = None
    supports_native_boolean = True
    supports_simple_order_by_label = True
    postfetch_lastrowid = False

    def __init__(
            self,
            arraysize=5000,
            credentials_path=None,
            location=None,
            credentials_info=None,
            *args, **kwargs):
        super(BigQueryDialect, self).__init__(*args, **kwargs)
        self.arraysize = arraysize
        self.credentials_path = credentials_path
        self.credentials_info = credentials_info
        self.location = location
        self.dataset_id = None

    @classmethod
    def dbapi(cls):
        return dbapi

    @staticmethod
    def _build_formatted_table_id(table):
        """Build '<dataset_id>.<table_id>' string using given table."""
        return "{}.{}".format(table.reference.dataset_id, table.table_id)

    @staticmethod
    def _add_default_dataset_to_job_config(job_config, project_id, dataset_id):
        # If dataset_id is set, then we know the job_config isn't None
        if dataset_id:
            # If project_id is missing, use default project_id for the current environment
            if not project_id:
                _, project_id = auth.default()

            job_config.default_dataset = '{}.{}'.format(project_id, dataset_id)

    def _create_client_from_credentials(self, credentials, default_query_job_config, project_id):
        if project_id is None:
            project_id = credentials.project_id

        scopes = (
                'https://www.googleapis.com/auth/bigquery',
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/drive'
            )
        credentials = credentials.with_scopes(scopes)

        self._add_default_dataset_to_job_config(default_query_job_config, project_id, self.dataset_id)

        return bigquery.Client(
                project=project_id,
                credentials=credentials,
                location=self.location,
                default_query_job_config=default_query_job_config,
            )

    def create_connect_args(self, url):
        project_id, location, dataset_id, arraysize, credentials_path, default_query_job_config = parse_url(url)

        self.arraysize = self.arraysize or arraysize
        self.location = location or self.location
        self.credentials_path = credentials_path or self.credentials_path
        self.dataset_id = dataset_id

        if self.credentials_path:
            credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
            client = self._create_client_from_credentials(credentials, default_query_job_config, project_id)

        elif self.credentials_info:
            credentials = service_account.Credentials.from_service_account_info(self.credentials_info)
            client = self._create_client_from_credentials(credentials, default_query_job_config, project_id)

        else:
            self._add_default_dataset_to_job_config(default_query_job_config, project_id, dataset_id)

            client = bigquery.Client(
                project=project_id,
                location=self.location,
                default_query_job_config=default_query_job_config
            )

        return ([client], {})

    def _json_deserializer(self, row):
        """JSON deserializer for RECORD types.

        The DB-API layer already deserializes JSON to a dictionary, so this
        just returns the input.
        """
        return row

    def _get_table_or_view_names(self, connection, table_type, schema=None):
        current_schema = schema or self.dataset_id
        get_table_name = self._build_formatted_table_id \
            if self.dataset_id is None else \
            operator.attrgetter("table_id")

        client = connection.connection._client
        datasets = client.list_datasets()

        result = []
        for dataset in datasets:
            if current_schema is not None and current_schema != dataset.dataset_id:
                continue

            tables = client.list_tables(dataset.reference)
            for table in tables:
                if table_type == table.table_type:
                    result.append(get_table_name(table))
        return result

    @staticmethod
    def _split_table_name(full_table_name):
        # Split full_table_name to get project, dataset and table name
        dataset = None
        table_name = None
        project = None

        table_name_split = full_table_name.split('.')
        if len(table_name_split) == 1:
            table_name = full_table_name
        elif len(table_name_split) == 2:
            dataset, table_name = table_name_split
        elif len(table_name_split) == 3:
            project, dataset, table_name = table_name_split
        else:
            raise ValueError("Did not understand table_name: {}".format(full_table_name))

        return (project, dataset, table_name)

    def _table_reference(self, provided_schema_name, provided_table_name,
                         client_project):
        project_id_from_table, dataset_id_from_table, table_id = self._split_table_name(provided_table_name)
        project_id_from_schema = None
        dataset_id_from_schema = None
        if provided_schema_name is not None:
            provided_schema_name_split = provided_schema_name.split('.')
            if len(provided_schema_name_split) == 0:
                pass
            elif len(provided_schema_name_split) == 1:
                if dataset_id_from_table:
                    project_id_from_schema = provided_schema_name_split[0]
                else:
                    dataset_id_from_schema = provided_schema_name_split[0]
            elif len(provided_schema_name_split) == 2:
                project_id_from_schema = provided_schema_name_split[0]
                dataset_id_from_schema = provided_schema_name_split[1]
            else:
                raise ValueError("Did not understand schema: {}".format(provided_schema_name))
        if (dataset_id_from_schema and dataset_id_from_table and
           dataset_id_from_schema != dataset_id_from_table):
            raise ValueError(
                "dataset_id specified in schema and table_name disagree: "
                "got {} in schema, and {} in table_name".format(
                    dataset_id_from_schema, dataset_id_from_table
                )
            )
        if (project_id_from_schema and project_id_from_table and
           project_id_from_schema != project_id_from_table):
            raise ValueError(
                "project_id specified in schema and table_name disagree: "
                "got {} in schema, and {} in table_name".format(
                    project_id_from_schema, project_id_from_table
                )
            )
        project_id = project_id_from_schema or project_id_from_table or client_project
        dataset_id = dataset_id_from_schema or dataset_id_from_table or self.dataset_id

        table_ref = TableReference.from_string("{}.{}.{}".format(
            project_id, dataset_id, table_id
        ))
        return table_ref

    def _get_table(self, connection, table_name, schema=None):
        if isinstance(connection, Engine):
            connection = connection.connect()

        client = connection.connection._client

        table_ref = self._table_reference(schema, table_name, client.project)
        try:
            table = client.get_table(table_ref)
        except NotFound:
            raise NoSuchTableError(table_name)
        return table

    def has_table(self, connection, table_name, schema=None):
        try:
            self._get_table(connection, table_name, schema)
            return True
        except NoSuchTableError:
            return False

    def _get_columns_helper(self, columns, cur_columns):
        """
        Recurse into record type and return all the nested field names.
        As contributed by @sumedhsakdeo on issue #17
        """
        results = []
        for col in columns:
            results += [SchemaField(name='.'.join(col.name for col in cur_columns + [col]),
                                    field_type=col.field_type,
                                    mode=col.mode,
                                    description=col.description,
                                    fields=col.fields)]
            if col.field_type == 'RECORD':
                cur_columns.append(col)
                results += self._get_columns_helper(col.fields, cur_columns)
                cur_columns.pop()
        return results

    def get_columns(self, connection, table_name, schema=None, **kw):
        table = self._get_table(connection, table_name, schema)
        columns = self._get_columns_helper(table.schema, [])
        result = []
        for col in columns:
            try:
                coltype = _type_map[col.field_type]
            except KeyError:
                util.warn("Did not recognize type '%s' of column '%s'" % (col.field_type, col.name))

            result.append({
                'name': col.name,
                'type': types.ARRAY(coltype) if col.mode == 'REPEATED' else coltype,
                'nullable': col.mode == 'NULLABLE' or col.mode == 'REPEATED',
                'default': None,
            })

        return result

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        # BigQuery has no support for foreign keys.
        return []

    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        # BigQuery has no support for primary keys.
        return {'constrained_columns': []}

    def get_indexes(self, connection, table_name, schema=None, **kw):
        table = self._get_table(connection, table_name, schema)
        indexes = []
        if table.time_partitioning:
            indexes.append({'name': 'partition',
                            'column_names': [table.time_partitioning.field],
                            'unique': False})
        if table.clustering_fields:
            indexes.append({'name': 'clustering',
                            'column_names': table.clustering_fields,
                            'unique': False})
        return indexes

    def get_schema_names(self, connection, **kw):
        if isinstance(connection, Engine):
            connection = connection.connect()

        datasets = connection.connection._client.list_datasets()
        if self.dataset_id is not None:
            return [d.dataset_id for d in datasets if d.dataset_id == self.dataset_id]
        else:
            return [d.dataset_id for d in datasets]

    def get_table_names(self, connection, schema=None, **kw):
        if isinstance(connection, Engine):
            connection = connection.connect()

        return self._get_table_or_view_names(connection, "TABLE", schema)

    def get_view_names(self, connection, schema=None, **kw):
        if isinstance(connection, Engine):
            connection = connection.connect()

        return self._get_table_or_view_names(connection, "VIEW", schema)

    def do_rollback(self, dbapi_connection):
        # BigQuery has no support for transactions.
        pass

    def _check_unicode_returns(self, connection, additional_tests=None):
        # requests gives back Unicode strings
        return True

    def _check_unicode_description(self, connection):
        # requests gives back Unicode strings
        return True
