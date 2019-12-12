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

import spanner.dbapi as Database
from django.db.backends.base.base import BaseDatabaseWrapper

from .client import DatabaseClient
from .creation import DatabaseCreation
from .features import DatabaseFeatures
from .introspection import DatabaseIntrospection
from .operations import DatabaseOperations
from .schema import DatabaseSchemaEditor


class DatabaseWrapper(BaseDatabaseWrapper):
    vendor = 'spanner'
    display_name = 'Cloud Spanner'

    # Mapping of Field objects to their column types.
    # https://cloud.google.com/spanner/docs/data-types#date-type
    # TODO: audit max lengths of all STRING fields.
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
        'IPAddressField': 'STRING(40)',
        'GenericIPAddressField': 'STRING(80)',
        'NullBooleanField': 'BOOL',
        'OneToOneField': 'INT64',
        'PositiveIntegerField': 'INT64',
        'PositiveSmallIntegerField': 'INT64',
        'SlugField': 'STRING(%(max_length)s)',
        'SmallAutoField': 'INT64',
        'SmallIntegerField': 'INT64',
        'TextField': 'STRING(MAX)',
        'TimeField': 'TIMESTAMP',
        # A UUID4 like 'd9c388b1-184d-4511-a818-3d598cc2f847', 16 bytes, with 4 dashes.
        'UUIDField': 'STRING(36)',
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

    Database = Database
    SchemaEditorClass = DatabaseSchemaEditor
    creation_class = DatabaseCreation
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations
    client_class = DatabaseClient

    def get_connection_params(self):
        return {'spanner_url': self.settings_dict['SPANNER_URL']}

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
