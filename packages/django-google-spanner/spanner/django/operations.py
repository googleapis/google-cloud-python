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
