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

from django.db.backends.base.base import BaseDatabaseWrapper
from django.utils.functional import cached_property

from .parse_utils import (
        extract_connection_params
)

from google.cloud import spanner_v1 as spanner


class DatabaseWrapper(BaseDatabaseWrapper):
    vendor = 'google'
    display_name = 'Cloud Spanner'

    # Mapping of Field objects to their column types.
    data_types = dict(
            AutoField='',  # Spanner does not support Auto increment as per
                           # https://cloud.google.com/spanner/docs/migrating-postgres-spanner#data_types
            BigAutoField='',

            BinaryField='BYTES',
            BooleanField='BOOL',
            CharField='STRING(%(max_length)s)',

            DateField='DATE',        # Date with a zone is supported.
                                     # https://cloud.google.com/spanner/docs/data-types#date-type
            DateTimeField='STRING',  # DateTimeField produces a timestamp with a timezone
                                     # but Spanneronly supports timestamps without a timezone, see
                                     #    https://cloud.google.com/spanner/docs/migrating-postgres-spanner#data_types
            DecimalField='FLOAT64',
            DurationField='STRING',  # Django extracts this field with parse_duration by invoking
                                     #   https://docs.djangoproject.com/en/2.2/_modules/django/utils/dateparse/#parse_duration
                                     # starting from
                                     #   https://docs.djangoproject.com/en/2.2/_modules/django/db/models/fields/#DurationField
                                     # expecting format "[DD] [HH:[MM:]]ss[.uuuuuu]"
                                     # also see
                                     #   https://cloud.google.com/spanner/docs/migrating-postgres-spanner#data_types
                                     # which recommends either:
                                     #   "INT64" if storing the value in milliseconds
                                     #  OR
                                     #   "STRING" if storing the value in an application-defined interval format.

            EmailField='STRING',
            FileField='STRING',
            FilePathField='STRING',
            FloatField='FLOAT64',
            IntegerField='INT64',
            BigIntegerField='INT64',

            IPAddressField='STRING',  # IP addresses are directly translated to
                                      # STRING, despite being say "inet" in Postgres.
            GenericIPAddressField='STRING',

            NullBooleanField='BOOL',
            OneToOneField='INT64',
            PositiveIntegerField='INT64',
            PositiveSmallIntegerField='INT64',
            SlugField='STRING',
            SmallAutoField='INT64',
            SmallIntegerField='INT64',
            TextField='STRING',
            TimeField='STRING',  # With or without the time zone, Spanner
                                 # expects the time field as a string.
            UUIDField='STRING(36)',  # A UUID4 like 'd9c388b1-184d-4511-a818-3d598cc2f847', 16 bytes, with 4 dashes.
    )

    # TODO: (@odeke-em) examine Spanner's data type constraints.
    data_types_check_constraints = {
    }

    operators = { 
            'exact': '= %s',
            'iexact': '= %s',  # Spanner String comparison are case sensitive,
                               # but it doesn't have a case insensitive
                               # matching.
            'contains': 'IN %s',
            'icontains': 'LIKE %s',
            'gt': '> %s',
            'gte': '>= %s',
            'lt': '< %s',
            'lte': '<= %s',
            'startswith': 'STARTS_WITH(%s, %s)',
            'endswith': 'ENDS_WITH(%s, %s)',
            'istartswith': 'STARTS_WITH(%s, %s)',
            'iendswith': 'ENDS_WITH(%s, %s)',
    }


    def get_connection_params(self):
        return extract_connection_params(self.settings_dict)


    def get_new_connection(self, conn_params):
        kwargs = dict(
            project=conn_params.get('project_id'),
            user_agent='spanner-django/v1',
        )

        credentials_uri = conn_params.get('credentials_uri')
        client = None

        if credentials_uri:
            client = spanner.Client.from_service_account_json(credentials_uri, **kwargs)
        else:
            client = spanner.Client(**kwargs)

        return client


    def create_cursor(self, name=None):
        raise Exception('unimplemented')


    def disable_constraint_checking(self):
        raise Exception('unimplemented')


    def enable_constraint_checking(self):
        raise Exception('unimplemented')


    def check_constraints(self, table_names=None):
        raise Exception('unimplemented')


    def is_usable(self):
        raise Exception('unimplemented')

    @cached_property
    def display_name(self):
        return 'Spanner'

    @cached_property
    def data_type_check_constraints(self):
        raise Exception('unimplemented')
