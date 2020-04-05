# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import os
import re
from base64 import b64decode
from datetime import datetime, time
from decimal import Decimal
from uuid import UUID

from django.conf import settings
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.utils import DatabaseError
from django.utils import timezone
from django.utils.duration import duration_microseconds
from spanner_dbapi.parse_utils import DateStr, TimestampStr, escape_name


class DatabaseOperations(BaseDatabaseOperations):
    cast_data_types = {
        'CharField': 'STRING',
        'TextField': 'STRING',
    }
    cast_char_field_without_max_length = 'STRING'
    compiler_module = 'django_spanner.compiler'
    # Django's lookup names that require a different name in Spanner's
    # EXTRACT() function.
    # https://cloud.google.com/spanner/docs/functions-and-operators#extract
    extract_names = {
        'iso_year': 'isoyear',
        'week': 'isoweek',
        'week_day': 'dayofweek',
    }

    def max_name_length(self):
        # https://cloud.google.com/spanner/quotas#tables
        return 128

    def quote_name(self, name):
        # Spanner says "column name not valid" if spaces or hyphens are present
        # (although according the docs, any character should be allowed in
        # quoted identifiers). Replace problematic characters when running the
        # Django tests to prevent crashes. (Don't modify names in normal
        # operation to prevent the possibility of colliding with another
        # column.) https://github.com/orijtech/spanner-orm/issues/204
        if os.environ.get('RUNNING_SPANNER_BACKEND_TESTS') == '1':
            name = name.replace(' ', '_').replace('-', '_')
        return escape_name(name)

    def bulk_batch_size(self, fields, objs):
        return self.connection.features.max_query_params

    def bulk_insert_sql(self, fields, placeholder_rows):
        placeholder_rows_sql = (", ".join(row) for row in placeholder_rows)
        values_sql = ", ".join("(%s)" % sql for sql in placeholder_rows_sql)
        return "VALUES " + values_sql

    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        # Cloud Spanner doesn't support TRUNCATE so DELETE instead.
        # A dummy WHERE clause is required.
        if tables:
            delete_sql = '%s %s %%s' % (
                style.SQL_KEYWORD('DELETE'),
                style.SQL_KEYWORD('FROM'),
            )
            return [
                delete_sql % style.SQL_FIELD(self.quote_name(table))
                for table in tables
            ]
        else:
            return []

    def adapt_datefield_value(self, value):
        if value is None:
            return None
        return DateStr(str(value))

    def adapt_datetimefield_value(self, value):
        if value is None:
            return None
        # Expression values are adapted by the database.
        if hasattr(value, 'resolve_expression'):
            return value
        # Cloud Spanner doesn't support tz-aware datetimes
        if timezone.is_aware(value):
            if settings.USE_TZ:
                value = timezone.make_naive(value, self.connection.timezone)
            else:
                raise ValueError(
                    "The Cloud Spanner backend does not support "
                    "timezone-aware datetimes when USE_TZ is False."
                )
        return TimestampStr(value.isoformat(timespec='microseconds') + 'Z')

    def adapt_decimalfield_value(self, value, max_digits=None, decimal_places=None):
        """
        Convert value from decimal.Decimal into float, for a direct mapping
        and correct serialization with RPCs to Cloud Spanner.
        """
        if value is None:
            return None
        return float(value)

    def adapt_timefield_value(self, value):
        if value is None:
            return None
        # Expression values are adapted by the database.
        if hasattr(value, 'resolve_expression'):
            return value
        # Column is TIMESTAMP, so prefix a dummy date to the datetime.time.
        return TimestampStr('0001-01-01T' + value.isoformat(timespec='microseconds') + 'Z')

    def get_db_converters(self, expression):
        converters = super().get_db_converters(expression)
        internal_type = expression.output_field.get_internal_type()
        if internal_type == 'DateTimeField':
            converters.append(self.convert_datetimefield_value)
        elif internal_type == 'DecimalField':
            converters.append(self.convert_decimalfield_value)
        elif internal_type == 'TimeField':
            converters.append(self.convert_timefield_value)
        elif internal_type == 'BinaryField':
            converters.append(self.convert_binaryfield_value)
        elif internal_type == 'UUIDField':
            converters.append(self.convert_uuidfield_value)
        return converters

    def convert_binaryfield_value(self, value, expression, connection):
        if value is None:
            return value
        # Cloud Spanner stores bytes base64 encoded.
        return b64decode(value)

    def convert_datetimefield_value(self, value, expression, connection):
        if value is None:
            return value
        # Cloud Spanner returns the
        # google.api_core.datetime_helpers.DatetimeWithNanoseconds subclass
        # of datetime with tzinfo=UTC (which should be replaced with the
        # connection's timezone). Django doesn't support nanoseconds so that
        # part is ignored.
        dt = datetime(
            value.year, value.month, value.day,
            value.hour, value.minute, value.second, value.microsecond,
        )
        return timezone.make_aware(dt, self.connection.timezone) if settings.USE_TZ else dt

    def convert_decimalfield_value(self, value, expression, connection):
        if value is None:
            return value
        # Cloud Spanner returns a float.
        return Decimal(str(value))

    def convert_timefield_value(self, value, expression, connection):
        if value is None:
            return value
        # Convert DatetimeWithNanoseconds to time.
        return time(value.hour, value.minute, value.second, value.microsecond)

    def convert_uuidfield_value(self, value, expression, connection):
        if value is not None:
            value = UUID(value)
        return value

    def date_extract_sql(self, lookup_type, field_name):
        lookup_type = self.extract_names.get(lookup_type, lookup_type)
        return 'EXTRACT(%s FROM %s)' % (lookup_type, field_name)

    def datetime_extract_sql(self, lookup_type, field_name, tzname):
        tzname = tzname if settings.USE_TZ else 'UTC'
        lookup_type = self.extract_names.get(lookup_type, lookup_type)
        return 'EXTRACT(%s FROM %s AT TIME ZONE "%s")' % (lookup_type, field_name, tzname)

    def time_extract_sql(self, lookup_type, field_name):
        # Time is stored as TIMESTAMP with UTC time zone.
        return 'EXTRACT(%s FROM %s AT TIME ZONE "UTC")' % (lookup_type, field_name)

    def date_trunc_sql(self, lookup_type, field_name):
        # https://cloud.google.com/spanner/docs/functions-and-operators#date_trunc
        if lookup_type == 'week':
            # Spanner truncates to Sunday but Django expects Monday. First,
            # subtract a day so that a Sunday will be truncated to the previous
            # week...
            field_name = 'DATE_SUB(CAST(' + field_name + ' AS DATE), INTERVAL 1 DAY)'
        sql = 'DATE_TRUNC(CAST(%s AS DATE), %s)' % (field_name, lookup_type)
        if lookup_type == 'week':
            # ...then add a day to get from Sunday to Monday.
            sql = 'DATE_ADD(CAST(' + sql + ' AS DATE), INTERVAL 1 DAY)'
        return sql

    def datetime_trunc_sql(self, lookup_type, field_name, tzname):
        # https://cloud.google.com/spanner/docs/functions-and-operators#timestamp_trunc
        tzname = tzname if settings.USE_TZ else 'UTC'
        if lookup_type == 'week':
            # Spanner truncates to Sunday but Django expects Monday. First,
            # subtract a day so that a Sunday will be truncated to the previous
            # week...
            field_name = 'TIMESTAMP_SUB(' + field_name + ', INTERVAL 1 DAY)'
        sql = 'TIMESTAMP_TRUNC(%s, %s, "%s")' % (field_name, lookup_type, tzname)
        if lookup_type == 'week':
            # ...then add a day to get from Sunday to Monday.
            sql = 'TIMESTAMP_ADD(' + sql + ', INTERVAL 1 DAY)'
        return sql

    def time_trunc_sql(self, lookup_type, field_name):
        # https://cloud.google.com/spanner/docs/functions-and-operators#timestamp_trunc
        return 'TIMESTAMP_TRUNC(%s, %s, "UTC")' % (field_name, lookup_type)

    def datetime_cast_date_sql(self, field_name, tzname):
        # https://cloud.google.com/spanner/docs/functions-and-operators#date
        tzname = tzname if settings.USE_TZ else 'UTC'
        return 'DATE(%s, "%s")' % (field_name, tzname)

    def datetime_cast_time_sql(self, field_name, tzname):
        tzname = tzname if settings.USE_TZ else 'UTC'
        # Cloud Spanner doesn't have a function for converting
        # TIMESTAMP to another time zone.
        return "TIMESTAMP(FORMAT_TIMESTAMP('%%Y-%%m-%%d %%R:%%E9S %%Z', %s, '%s'))" % (field_name, tzname)

    def date_interval_sql(self, timedelta):
        return 'INTERVAL %s MICROSECOND' % duration_microseconds(timedelta)

    def format_for_duration_arithmetic(self, sql):
        return 'INTERVAL %s MICROSECOND' % sql

    def combine_expression(self, connector, sub_expressions):
        if connector == '%%':
            return 'MOD(%s)' % ', '.join(sub_expressions)
        elif connector == '^':
            return 'POWER(%s)' % ', '.join(sub_expressions)
        elif connector == '>>':
            lhs, rhs = sub_expressions
            # Use an alternate computation because Cloud Sapnner's '>>' operator does not do
            # sign bit extension with a signed type (i.e. produces different results for
            # negative numbers than what Django's tests expect). Cast float result as INT64 to
            # allow assigning to both INT64 and FLOAT64 columns (otherwise the FLOAT result
            # couldn't be assigned to INT64 columns).
            return 'CAST(FLOOR(%(lhs)s / POW(2, %(rhs)s)) AS INT64)' % {'lhs': lhs, 'rhs': rhs}
        return super().combine_expression(connector, sub_expressions)

    def combine_duration_expression(self, connector, sub_expressions):
        if connector == '+':
            return 'TIMESTAMP_ADD(' + ', '.join(sub_expressions) + ')'
        elif connector == '-':
            return 'TIMESTAMP_SUB(' + ', '.join(sub_expressions) + ')'
        else:
            raise DatabaseError('Invalid connector for timedelta: %s.' % connector)

    def lookup_cast(self, lookup_type, internal_type=None):
        # Cast text lookups to string to allow things like filter(x__contains=4)
        if lookup_type in ('contains', 'icontains', 'startswith', 'istartswith',
                           'endswith', 'iendswith', 'regex', 'iregex', 'iexact'):
            return 'CAST(%s AS STRING)'
        return '%s'

    def prep_for_like_query(self, x):
        """Lookups that use this method use REGEXP_CONTAINS instead of LIKE."""
        return re.escape(str(x))

    prep_for_iexact_query = prep_for_like_query

    def no_limit_value(self):
        """The largest INT64: (2**63) - 1"""
        return 9223372036854775807

    def _get_limit_offset_params(self, low_mark, high_mark):
        limit, offset = super()._get_limit_offset_params(low_mark, high_mark)
        if offset and limit == self.connection.ops.no_limit_value():
            # Subtract offset from the limit to avoid an INT64 overflow error
            # from Cloud Spanner.
            limit -= offset
        return limit, offset
