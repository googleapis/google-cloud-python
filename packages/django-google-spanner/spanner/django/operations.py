from datetime import datetime

from django.conf import settings
from django.db.backends.base.operations import BaseDatabaseOperations
from django.utils import timezone
from spanner.dbapi.parse_utils import TimestampStr


class DatabaseOperations(BaseDatabaseOperations):
    # Django's lookup names that require a different name in Spanner's
    # EXTRACT() function.
    # https://cloud.google.com/spanner/docs/functions-and-operators#extract
    extract_names = {
        'week_day': 'dayofweek',
        'iso_week': 'isoweek',
        'iso_year': 'isoyear',
    }

    def quote_name(self, name):
        if '-' in name:
            return '`' + name + '`'
        return name

    def bulk_insert_sql(self, fields, placeholder_rows):
        placeholder_rows_sql = (", ".join(row) for row in placeholder_rows)
        values_sql = ", ".join("(%s)" % sql for sql in placeholder_rows_sql)
        return "VALUES " + values_sql

    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        # Cloud Spanner doesn't support TRUNCATE so DELETE instead.
        # A dummy WHERE clause is required.
        if tables:
            delete_sql = '%s %s %%s;' % (
                style.SQL_KEYWORD('DELETE'),
                style.SQL_KEYWORD('FROM'),
            )
            return [
                delete_sql % style.SQL_FIELD(self.quote_name(table))
                for table in tables
            ]
        else:
            return []

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
                raise ValueError("Cloud Spanner does not support timezone-aware datetimes when USE_TZ is False.")
        return TimestampStr(value.isoformat(timespec='microseconds') + 'Z')

    def get_db_converters(self, expression):
        converters = super().get_db_converters(expression)
        internal_type = expression.output_field.get_internal_type()
        if internal_type == 'DateTimeField':
            converters.append(self.convert_datetimefield_value)
        return converters

    def convert_datetimefield_value(self, value, expression, connection):
        if value is None:
            return value
        # Cloud Spanner returns the
        # google.api_core.datetime_helpers.DatetimeWithNanoseconds subclass
        # of datetime with tzinfo=UTC (which should be replaced with the
        # connection's timezone). Django doesn't support nanoseconds so that
        # part is ignored.
        return datetime(
            value.year, value.month, value.day,
            value.hour, value.minute, value.second, value.microsecond,
            self.connection.timezone,
        )

    def date_extract_sql(self, lookup_type, field_name):
        lookup_type = self.extract_names.get(lookup_type, lookup_type)
        return 'EXTRACT(%s FROM %s)' % (lookup_type, field_name)

    def datetime_extract_sql(self, lookup_type, field_name, tzname):
        tzname = self.connection.timezone if settings.USE_TZ else 'UTC'
        lookup_type = self.extract_names.get(lookup_type, lookup_type)
        return 'EXTRACT(%s FROM %s AT TIME ZONE "%s")' % (lookup_type, field_name, tzname)
