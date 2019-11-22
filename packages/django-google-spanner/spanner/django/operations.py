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
