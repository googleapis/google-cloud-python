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

from .parse_utils import (
        resolve_project_id,
        parse_spanner_url
)


class DatabaseWrapper(BaseDatabaseWrapper):
    vendor = 'spanner'
    display_name = 'Spanner'

    # Mapping of Field objects to their column types.
    data_types = dict(
            AutoField='',  # Spanner does not support Auto increment as per
                           # https://cloud.google.com/spanner/docs/migrating-postgres-spanner#data_types
            BigAutoField='',

            BinaryField='BYTES',
            BooleanField='BOOL',
            CharField='STRING',

            DateField='DATE',        # Date with a zone is supported.
                                     # https://cloud.google.com/spanner/docs/data-types#date-type
            DateTimeField='STRING',  # DateTimeField produces a timestamp with a timezone
                                     # but Spanneronly supports timestamps without a timezone, see
                                     #    https://cloud.google.com/spanner/docs/migrating-postgres-spanner#data_types
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
            UUIDField='STRING',
    )

    # TODO: (@odeke-em) examine Spanner's data type constraints.
    data_types_check_constraints = {}

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
        # We'll expect settings in the form of either:
        # {
        #   "NAME":         "spanner",
        #   "INSTANCE":     "instance",
        #   "AUTOCOMMIT":   True or False,
        #   "READ_ONLY":    True or False,
        #   "PROJECT_ID":   "<project_id>",
        # }
        #
        # OR
        # {
        #   "SPANNER_URL":  "cloudspanner:[//host[:port]]/project/<project_id>/instances/<instance-id>/databases/<database-name>?property-name=property-value
        # }
        settings_dict = self.settings_dict

        if settings_dict['SPANNER_URL']:
            return parse_spanner_url(settings_dict['SPANNER_URL'])
        else:
            return dict(
                auto_commit=settings_dict['AUTO_COMMIT'],
                database=settings_dict['NAME'] or 'spanner',
                instance=settings_dict['INSTANCE'],
                project_id=resolve_project_id(settings_dict['PROJECT_ID']),
                read_only=settings_dict['READ_ONLY'],
            )
