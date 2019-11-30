from django.conf import settings
from django.db.backends.base.operations import BaseDatabaseOperations
from django.utils import timezone
from spanner.dbapi.parse_utils import TimestampStr


class DatabaseOperations(BaseDatabaseOperations):
    def quote_name(self, name):
        return name

    def bulk_insert_sql(self, fields, placeholder_rows):
        placeholder_rows_sql = (", ".join(row) for row in placeholder_rows)
        values_sql = ", ".join("(%s)" % sql for sql in placeholder_rows_sql)
        return "VALUES " + values_sql

    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        # Cloud Spanner doesn't support TRUNCATE so DELETE instead.
        # A dummy WHERE clause is required.
        if tables:
            delete_sql = '%s %s %%s %s 1=1;' % (
                style.SQL_KEYWORD('DELETE'),
                style.SQL_KEYWORD('FROM'),
                style.SQL_KEYWORD('WHERE'),
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
        if timezone.is_aware(value):
            return value
        return timezone.make_aware(value, self.connection.timezone)
