# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import spanner_dbapi as Database
from django.db.backends.base.base import BaseDatabaseWrapper
from google.cloud import spanner_v1 as spanner

from .client import DatabaseClient
from .creation import DatabaseCreation
from .features import DatabaseFeatures
from .introspection import DatabaseIntrospection
from .operations import DatabaseOperations
from .schema import DatabaseSchemaEditor
from .validation import DatabaseValidation


class DatabaseWrapper(BaseDatabaseWrapper):
    vendor = 'spanner'
    display_name = 'Cloud Spanner'

    # Mapping of Field objects to their column types.
    # https://cloud.google.com/spanner/docs/data-types#date-type
    data_types = {
        'AutoField': 'INT64',
        'BigAutoField': 'INT64',
        'BinaryField': 'BYTES(MAX)',
        'BooleanField': 'BOOL',
        'CharField': 'STRING(%(max_length)s)',
        'DateField': 'DATE',
        'DateTimeField': 'TIMESTAMP',
        'DecimalField': 'FLOAT64',
        'DurationField': 'INT64',
        'EmailField': 'STRING(%(max_length)s)',
        'FileField': 'STRING(%(max_length)s)',
        'FilePathField': 'STRING(%(max_length)s)',
        'FloatField': 'FLOAT64',
        'IntegerField': 'INT64',
        'BigIntegerField': 'INT64',
        'IPAddressField': 'STRING(15)',
        'GenericIPAddressField': 'STRING(39)',
        'NullBooleanField': 'BOOL',
        'OneToOneField': 'INT64',
        'PositiveIntegerField': 'INT64',
        'PositiveSmallIntegerField': 'INT64',
        'SlugField': 'STRING(%(max_length)s)',
        'SmallAutoField': 'INT64',
        'SmallIntegerField': 'INT64',
        'TextField': 'STRING(MAX)',
        'TimeField': 'TIMESTAMP',
        'UUIDField': 'STRING(32)',
    }

    # TODO: (@odeke-em) examine Spanner's data type constraints.
    data_types_check_constraints = {
    }

    operators = {
        'exact': '= %s',
        'iexact': 'REGEXP_CONTAINS(%s, %%%%s)',
        # contains uses REGEXP_CONTAINS instead of LIKE to allow
        # DatabaseOperations.prep_for_like_query() to do regular expression
        # escaping. prep_for_like_query() is called for all the lookups that
        # use REGEXP_CONTAINS except regex/iregex (see
        # django.db.models.lookups.PatternLookup).
        'contains':  'REGEXP_CONTAINS(%s, %%%%s)',
        'icontains': 'REGEXP_CONTAINS(%s, %%%%s)',
        'gt': '> %s',
        'gte': '>= %s',
        'lt': '< %s',
        'lte': '<= %s',
        # Using REGEXP_CONTAINS instead of STARTS_WITH and ENDS_WITH for the
        # same reasoning as described above for 'contains'.
        'startswith': 'REGEXP_CONTAINS(%s, %%%%s)',
        'endswith': 'REGEXP_CONTAINS(%s, %%%%s)',
        'istartswith': 'REGEXP_CONTAINS(%s, %%%%s)',
        'iendswith': 'REGEXP_CONTAINS(%s, %%%%s)',
        'regex': 'REGEXP_CONTAINS(%s, %%%%s)',
        'iregex': 'REGEXP_CONTAINS(%s, %%%%s)',
    }

    # pattern_esc is used to generate SQL pattern lookup clauses when the
    # right-hand side of the lookup isn't a raw string (it might be an
    # expression or the result of a bilateral transformation). In those cases,
    # special characters for REGEXP_CONTAINS operators (e.g. \, *, _) must be
    # escaped on database side.
    pattern_esc = r'REPLACE(REPLACE(REPLACE({}, "\\", "\\\\"), "%%", r"\%%"), "_", r"\_")'
    # These are all no-ops in favor of using REGEXP_CONTAINS in the customized
    # lookups.
    pattern_ops = {
        'contains': '',
        'icontains': '',
        'startswith': '',
        'istartswith': '',
        'endswith': '',
        'iendswith': '',
    }

    Database = Database
    SchemaEditorClass = DatabaseSchemaEditor
    creation_class = DatabaseCreation
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations
    client_class = DatabaseClient
    validation_class = DatabaseValidation

    @property
    def instance(self):
        return spanner.Client().instance(self.settings_dict['INSTANCE'])

    @property
    def _nodb_connection(self):
        raise NotImplementedError('Spanner does not have a "no db" connection.')

    def get_connection_params(self):
        return {
            'project': self.settings_dict['PROJECT'],
            'instance': self.settings_dict['INSTANCE'],
            'database': self.settings_dict['NAME'],
            'user_agent': 'django_spanner/0.0.1',
            **self.settings_dict['OPTIONS'],
        }

    def get_new_connection(self, conn_params):
        return Database.connect(**conn_params)

    def init_connection_state(self):
        pass

    def create_cursor(self, name=None):
        return self.connection.cursor()

    def _set_autocommit(self, autocommit):
        with self.wrap_database_errors:
            self.connection.autocommit = autocommit

    def is_usable(self):
        if self.connection is None:
            return False
        try:
            # Use a cursor directly, bypassing Django's utilities.
            self.connection.cursor().execute('SELECT 1')
        except Database.Error:
            return False
        else:
            return True
