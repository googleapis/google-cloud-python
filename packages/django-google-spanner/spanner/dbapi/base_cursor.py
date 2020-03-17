# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from google.cloud.spanner_v1 import param_types

from .exceptions import InterfaceError, ProgrammingError

_UNSET_COUNT = -1


# This table maps spanner_types to Spanner's data type sizes as per
#   https://cloud.google.com/spanner/docs/data-types#allowable-types
# It is used to map `display_size` to a known type for Cursor.description
# after a row fetch.
# Since ResultMetadata
#   https://cloud.google.com/spanner/docs/reference/rest/v1/ResultSetMetadata
# does not send back the actual size, we have to lookup the respective size.
# Some fields' sizes are dependent upon the dynamic data hence aren't sent back
# by Cloud Spanner.
code_to_display_size = {
    param_types.BOOL.code: 1,
    param_types.DATE.code: 4,
    param_types.FLOAT64.code: 8,
    param_types.INT64.code: 8,
    param_types.TIMESTAMP.code: 12,
}


class BaseCursor(object):
    def __init__(self, connection):
        self._itr = None
        self._res = None
        self._row_count = _UNSET_COUNT
        self._connection = connection
        self._closed = False

        # arraysize is a readable and writable property mandated
        # by PEP-0249 https://www.python.org/dev/peps/pep-0249/#arraysize
        # It determines the results of .fetchmany
        self.arraysize = 1

    @property
    def description(self):
        if not (self._res and self._res.metadata):
            return None

        row_type = self._res.metadata.row_type
        columns = []
        for field in row_type.fields:
            columns.append(
                Column(
                    name=field.name,
                    type_code=field.type.code,
                    # Size of the SQL type of the column.
                    display_size=code_to_display_size.get(field.type.code),
                    # Client perceived size of the column.
                    internal_size=field.ByteSize(),
                )
            )
        return tuple(columns)

    @property
    def rowcount(self):
        return self._row_count

    def _raise_if_already_closed(self):
        """
        Raise an exception if attempting to use an already closed connection.
        """
        if self._closed:
            raise InterfaceError('cursor already closed')

    def close(self):
        self.__clear()
        self._closed = True

    def __discard_aborted_txn(self):
        return self._connection.discard_aborted_txn()

    def __get_txn(self):
        return self._connection.get_txn()

    def executemany(self, operation, seq_of_params):
        if not self._connection:
            raise ProgrammingError('Cursor is not connected to the database')

        raise ProgrammingError('Unimplemented')

    def __next__(self):
        if self._itr is None:
            raise ProgrammingError('no results to return')
        return next(self._itr)

    def __iter__(self):
        if self._itr is None:
            raise ProgrammingError('no results to return')
        return self._itr

    def fetchone(self):
        self._raise_if_already_closed()

        try:
            return next(self)
        except StopIteration:
            return None

    def fetchall(self):
        self._raise_if_already_closed()

        return list(self.__iter__())

    def fetchmany(self, size=None):
        """
        Fetch the next set of rows of a query result, returning a sequence of sequences.
        An empty sequence is returned when no more rows are available.

        Args:
            size: optional integer to determine the maximum number of results to fetch.


        Raises:
            Error if the previous call to .execute*() did not produce any result set
            or if no call was issued yet.
        """
        self._raise_if_already_closed()

        if size is None:
            size = self.arraysize

        items = []
        for i in range(size):
            try:
                items.append(tuple(self.__next__()))
            except StopIteration:
                break

        return items

    @property
    def lastrowid(self):
        return None

    def setinputsizes(sizes):
        raise ProgrammingError('Unimplemented')

    def setoutputsize(size, column=None):
        raise ProgrammingError('Unimplemented')

    def _run_prior_DDL_statements(self):
        return self._connection.run_prior_DDL_statements()

    def list_tables(self):
        return self._connection.list_tables()

    def run_sql_in_snapshot(self, sql):
        return self._connection.run_sql_in_snapshot(sql)

    def get_table_column_schema(self, table_name):
        return self._connection.get_table_column_schema(table_name)


class Column:
    def __init__(self, name, type_code, display_size=None, internal_size=None,
                 precision=None, scale=None, null_ok=False):
        self.name = name
        self.type_code = type_code
        self.display_size = display_size
        self.internal_size = internal_size
        self.precision = precision
        self.scale = scale
        self.null_ok = null_ok

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, index):
        if index == 0:
            return self.name
        elif index == 1:
            return self.type_code
        elif index == 2:
            return self.display_size
        elif index == 3:
            return self.internal_size
        elif index == 4:
            return self.precision
        elif index == 5:
            return self.scale
        elif index == 6:
            return self.null_ok

    def __str__(self):
        rstr = ', '.join([field for field in [
            "name='%s'" % self.name,
            "type_code=%d" % self.type_code,
            None if not self.display_size else "display_size=%d" % self.display_size,
            None if not self.internal_size else "internal_size=%d" % self.internal_size,
            None if not self.precision else "precision='%s'" % self.precision,
            None if not self.scale else "scale='%s'" % self.scale,
            None if not self.null_ok else "null_ok='%s'" % self.null_ok,
        ] if field])

        return 'Column(%s)' % rstr
