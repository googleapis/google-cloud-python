from datetime import datetime

from django.db.backends.base.operations import BaseDatabaseOperations


class DatabaseOperations(BaseDatabaseOperations):
    def quote_name(self, name):
        return name

    def bulk_insert_sql(self, fields, placeholder_rows):
        placeholder_rows_sql = (", ".join(row) for row in placeholder_rows)
        values_sql = ", ".join("(%s)" % sql for sql in placeholder_rows_sql)
        return "VALUES " + values_sql

    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        # TODO: Cloud Spanner doesn't support TRUNCATE, however, this will
        # need to be implemented somehow to support the normal way of testing
        # in Django: https://github.com/orijtech/spanner-orm/issues/67
        return []

    def get_db_converters(self, expression):
        converters = super().get_db_converters(expression)
        internal_type = expression.output_field.get_internal_type()
        if internal_type == 'DateTimeField':
            converters.append(self.convert_datetimefield_value)
        return converters

    def convert_datetimefield_value(self, value, expression, connection):
        if value is not None:
            try:
                value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:  # time data does not match format (no microsecond?)
                value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return value
