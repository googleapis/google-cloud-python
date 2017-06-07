"""Connection for the Google BigQuery DB-API."""

from google.cloud import bigquery
from bigquery import cursor


class Connection(object):
    """Connection to Google BigQuery."""

    def __init__(self, client):
        self._client = client

    def close(self):
        """No-op."""
        pass

    def commit(self):
        """No-op."""
        pass

    def cursor(self):
        """Return a new cursor object."""
        return cursor.Cursor(self)


def connect(*args, **kwargs):
    """Construct a connection to Google BigQuery."""
    client = bigquery.Client(project=args[0])
    return Connection(client)
