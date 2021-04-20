import google.api_core.exceptions
import google.cloud.bigquery.schema
import google.cloud.bigquery.table
import contextlib
import sqlite3


class Connection:

    connection = None

    def __init__(self, client=None, bqstorage_client=None):
        # share a single connection:
        if self.connection is None:
            self.__class__.connection = sqlite3.connect(":memory:")
        self._client = FauxClient(client, self.connection)

    def cursor(self):
        return Cursor(self.connection)

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        self.connection.close()


class Cursor:

    arraysize = 1

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def execute(self, operation, parameters=None):
        if parameters:
            parameters = {
                name: "null" if value is None else repr(value)
                for name, value in parameters.items()
            }
            operation %= parameters
        self.cursor.execute(operation, parameters)
        self.description = self.cursor.description
        self.rowcount = self.cursor.rowcount

    def executemany(self, operation, parameters_list):
        for parameters in parameters_list:
            self.execute(operation, parameters)

    def close(self):
        self.cursor.close()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchmany(self, size=None):
        self.cursor.fetchmany(size or self.arraysize)

    def fetchall(self):
        return self.cursor.fetchall()

    def setinputsizes(self, sizes):
        pass

    def setoutputsize(self, size, column=None):
        pass


class FauxClient:
    def __init__(self, client, connection):
        self._client = client
        self.project = client.project
        self.connection = connection

    def get_table(self, table_ref):
        table_name = table_ref.table_id
        with contextlib.closing(self.connection.cursor()) as cursor:
            cursor.execute(
                f"select name from sqlite_master"
                f" where type='table' and name='{table_name}'"
            )
            if list(cursor):
                cursor.execute("PRAGMA table_info('{table_name}')")
                schema = [
                    google.cloud.bigquery.schema.SchemaField(
                        name=name,
                        field_type=type_,
                        mode="REQUIRED" if notnull else "NULLABLE",
                    )
                    for cid, name, type_, notnull, dflt_value, pk in cursor
                ]
                return google.cloud.bigquery.table.Table(table_ref, schema)
            else:
                raise google.api_core.exceptions.NotFound(table_ref)
