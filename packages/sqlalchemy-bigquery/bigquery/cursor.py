"""Cursor for the Google BigQuery DB-API."""

import collections
import bigquery.exceptions as exc
from bigquery import formatter
_escaper = formatter.ParamEscaper()


class Cursor:
    """Cursor to Google BigQuery."""

    _STATE_NONE = 0
    _STATE_RUNNING = 1
    _STATE_FINISHED = 2

    def __init__(self, connection):
        self.connection = connection
        self.arraysize = 1

    def _reset_state(self):
        self.rowcount = -1
        self.description = None
        self.rownumber = 0

        # Internal helper state
        self._state = self._STATE_NONE
        self._data = collections.deque()

    def close(self):
        """No-op."""
        pass

    def cancel(self):
        """Not implemented."""
        pass

    def _set_description(self, schema):
        """Set description from schema."""
        if schema is None:
            self.description = None
            return

        desc = []
        for field in schema:
            desc.append(tuple([
                field.name,
                None,
                None,
                None,
                None,
                None,
                field.mode == 'NULLABLE']))
        self.description = tuple(desc)

    def execute(self, operation, parameters=None):
        """Prepare and execute a database operation."""
        client = self.connection._client

        # Prepare statement
        if parameters is None:
            sql = operation
        else:
            sql = operation % _escaper.escape_args(parameters)

        query = client.run_sync_query(sql)

        query.use_legacy_sql = False
        query.timeout_ms = 180000

        # Begin execution
        self._reset_state()
        self._state = self._STATE_RUNNING
        query.run()

        # Get results
        total_rows = query.total_rows if query.total_rows is not None else -1
        self.rowcount = total_rows
        self._set_description(query.schema)
        self._data += map(tuple, query.rows)
        self._state = self._STATE_FINISHED

    def executemany(self, operation, seq_of_parameters):
        """Not imlemented. AFAIK this is used for executing multiple DML statements."""
        pass

    def fetchone(self):
        """Fetch the next row of a query result set."""
        if self._state == self._STATE_NONE:
            raise exc.ProgrammingError("No query yet")

        if not self._data:
            return None
        else:
            self.rownumber += 1
            return self._data.popleft()

    def fetchmany(self, size=None):
        """Fetch the next set of rows of a query result."""

        if size is None:
            size = self.arraysize
        result = []

        for _ in range(size):
            one = self.fetchone()
            if one is None:
                break
            else:
                result.append(one)
        return result

    def fetchall(self):
        """Fetch all (remaining) rows of a query result."""
        result = []
        while True:
            one = self.fetchone()
            if one is None:
                break
            else:
                result.append(one)
        return result

    def setinputsizes(self, sizes):
        """Does nothing by default."""
        pass

    def setoutputsize(self, size, column=None):
        """Does nothing by default."""
        pass

    def __next__(self):
        """Return the next row from."""
        one = self.fetchone()
        if one is None:
            raise StopIteration
        else:
            return one

    next = __next__

    def __iter__(self):
        """Return self to make cursors compatible to the iteration protocol."""
        return self
