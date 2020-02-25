# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Connection for the Google BigQuery DB-API."""

from google.cloud import bigquery
from google.cloud.bigquery.dbapi import cursor


class Connection(object):
    """DB-API Connection to Google BigQuery.

    Args:
        client (google.cloud.bigquery.Client): A client used to connect to BigQuery.
        bqstorage_client(\
            Optional[google.cloud.bigquery_storage_v1beta1.BigQueryStorageClient] \
        ):
            [Beta] An alternative client that uses the faster BigQuery Storage
            API to fetch rows from BigQuery. If both clients are given,
            ``bqstorage_client`` is used first to fetch query results,
            with a fallback on ``client``, if necessary.

            .. note::
                There is a known issue with the BigQuery Storage API with small
                anonymous result sets, which results in such fallback.

                https://github.com/googleapis/python-bigquery-storage/issues/2
    """

    def __init__(self, client, bqstorage_client=None):
        self._client = client
        self._bqstorage_client = bqstorage_client

    def close(self):
        """No-op."""

    def commit(self):
        """No-op."""

    def cursor(self):
        """Return a new cursor object.

        Returns:
            google.cloud.bigquery.dbapi.Cursor: A DB-API cursor that uses this connection.
        """
        return cursor.Cursor(self)


def connect(client=None, bqstorage_client=None):
    """Construct a DB-API connection to Google BigQuery.

    Args:
        client (Optional[google.cloud.bigquery.Client]):
            A client used to connect to BigQuery. If not passed, a client is
            created using default options inferred from the environment.
        bqstorage_client(\
            Optional[google.cloud.bigquery_storage_v1beta1.BigQueryStorageClient] \
        ):
            [Beta] An alternative client that uses the faster BigQuery Storage
            API to fetch rows from BigQuery. If both clients are given,
            ``bqstorage_client`` is used first to fetch query results,
            with a fallback on ``client``, if necessary.

            .. note::
                There is a known issue with the BigQuery Storage API with small
                anonymous result sets, which results in such fallback.

                https://github.com/googleapis/python-bigquery-storage/issues/2

    Returns:
        google.cloud.bigquery.dbapi.Connection: A new DB-API connection to BigQuery.
    """
    if client is None:
        client = bigquery.Client()
    return Connection(client, bqstorage_client)
