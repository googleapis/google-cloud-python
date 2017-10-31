# Copyright 2016 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Model a set of read-only queries to a database as a snapshot."""

import functools

from google.protobuf.struct_pb2 import Struct
from google.cloud.spanner_v1.proto.transaction_pb2 import TransactionOptions
from google.cloud.spanner_v1.proto.transaction_pb2 import TransactionSelector

from google.api_core.exceptions import ServiceUnavailable
from google.cloud._helpers import _datetime_to_pb_timestamp
from google.cloud._helpers import _timedelta_to_duration_pb
from google.cloud.spanner_v1._helpers import _make_value_pb
from google.cloud.spanner_v1._helpers import _options_with_prefix
from google.cloud.spanner_v1._helpers import _SessionWrapper
from google.cloud.spanner_v1.streamed import StreamedResultSet


def _restart_on_unavailable(restart):
    """Restart iteration after :exc:`.ServiceUnavailable`.

    :type restart: callable
    :param restart: curried function returning iterator
    """
    resume_token = ''
    item_buffer = []
    iterator = restart()
    while True:
        try:
            for item in iterator:
                item_buffer.append(item)
                if item.resume_token:
                    resume_token = item.resume_token
                    break
        except ServiceUnavailable:
            del item_buffer[:]
            iterator = restart(resume_token=resume_token)
            continue

        if len(item_buffer) == 0:
            break

        for item in item_buffer:
            yield item

        del item_buffer[:]


class _SnapshotBase(_SessionWrapper):
    """Base class for Snapshot.

    Allows reuse of API request methods with different transaction selector.

    :type session: :class:`~google.cloud.spanner_v1.session.Session`
    :param session: the session used to perform the commit
    """
    _multi_use = False
    _transaction_id = None
    _read_request_count = 0

    def _make_txn_selector(self):  # pylint: disable=redundant-returns-doc
        """Helper for :meth:`read` / :meth:`execute_sql`.

        Subclasses must override, returning an instance of
        :class:`transaction_pb2.TransactionSelector`
        appropriate for making ``read`` / ``execute_sql`` requests

        :raises: NotImplementedError, always
        """
        raise NotImplementedError

    def read(self, table, columns, keyset, index='', limit=0):
        """Perform a ``StreamingRead`` API request for rows in a table.

        :type table: str
        :param table: name of the table from which to fetch data

        :type columns: list of str
        :param columns: names of columns to be retrieved

        :type keyset: :class:`~google.cloud.spanner_v1.keyset.KeySet`
        :param keyset: keys / ranges identifying rows to be retrieved

        :type index: str
        :param index: (Optional) name of index to use, rather than the
                      table's primary key

        :type limit: int
        :param limit: (Optional) maxiumn number of rows to return

        :rtype: :class:`~google.cloud.spanner_v1.streamed.StreamedResultSet`
        :returns: a result set instance which can be used to consume rows.
        :raises ValueError:
            for reuse of single-use snapshots, or if a transaction ID is
            already pending for multiple-use snapshots.
        """
        if self._read_request_count > 0:
            if not self._multi_use:
                raise ValueError("Cannot re-use single-use snapshot.")
            if self._transaction_id is None:
                raise ValueError("Transaction ID pending.")

        database = self._session._database
        api = database.spanner_api
        options = _options_with_prefix(database.name)
        transaction = self._make_txn_selector()

        restart = functools.partial(
            api.streaming_read,
            self._session.name, table, columns, keyset.to_pb(),
            transaction=transaction, index=index, limit=limit,
            options=options)

        iterator = _restart_on_unavailable(restart)

        self._read_request_count += 1

        if self._multi_use:
            return StreamedResultSet(iterator, source=self)
        else:
            return StreamedResultSet(iterator)

    def execute_sql(self, sql, params=None, param_types=None, query_mode=None):
        """Perform an ``ExecuteStreamingSql`` API request for rows in a table.

        :type sql: str
        :param sql: SQL query statement

        :type params: dict, {str -> column value}
        :param params: values for parameter replacement.  Keys must match
                       the names used in ``sql``.

        :type param_types: dict
        :param param_types:
            (Optional) maps explicit types for one or more param values;
            required if parameters are passed.

        :type query_mode:
            :class:`google.cloud.spanner_v1.proto.ExecuteSqlRequest.QueryMode`
        :param query_mode: Mode governing return of results / query plan. See
            https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.ExecuteSqlRequest.QueryMode1

        :rtype: :class:`~google.cloud.spanner_v1.streamed.StreamedResultSet`
        :returns: a result set instance which can be used to consume rows.
        :raises ValueError:
            for reuse of single-use snapshots, or if a transaction ID is
            already pending for multiple-use snapshots.
        """
        if self._read_request_count > 0:
            if not self._multi_use:
                raise ValueError("Cannot re-use single-use snapshot.")
            if self._transaction_id is None:
                raise ValueError("Transaction ID pending.")

        if params is not None:
            if param_types is None:
                raise ValueError(
                    "Specify 'param_types' when passing 'params'.")
            params_pb = Struct(fields={
                key: _make_value_pb(value) for key, value in params.items()})
        else:
            params_pb = None

        database = self._session._database
        options = _options_with_prefix(database.name)
        transaction = self._make_txn_selector()
        api = database.spanner_api

        restart = functools.partial(
            api.execute_streaming_sql,
            self._session.name, sql,
            transaction=transaction, params=params_pb, param_types=param_types,
            query_mode=query_mode, options=options)

        iterator = _restart_on_unavailable(restart)

        self._read_request_count += 1

        if self._multi_use:
            return StreamedResultSet(iterator, source=self)
        else:
            return StreamedResultSet(iterator)


class Snapshot(_SnapshotBase):
    """Allow a set of reads / SQL statements with shared staleness.

    See
    https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.TransactionOptions.ReadOnly

    If no options are passed, reads will use the ``strong`` model, reading
    at a timestamp where all previously committed transactions are visible.

    :type session: :class:`~google.cloud.spanner_v1.session.Session`
    :param session: the session used to perform the commit.

    :type read_timestamp: :class:`datetime.datetime`
    :param read_timestamp: Execute all reads at the given timestamp.

    :type min_read_timestamp: :class:`datetime.datetime`
    :param min_read_timestamp: Execute all reads at a
                               timestamp >= ``min_read_timestamp``.

    :type max_staleness: :class:`datetime.timedelta`
    :param max_staleness: Read data at a
                          timestamp >= NOW - ``max_staleness`` seconds.

    :type exact_staleness: :class:`datetime.timedelta`
    :param exact_staleness: Execute all reads at a timestamp that is
                            ``exact_staleness`` old.

    :type multi_use: :class:`bool`
    :param multi_use: If true, multipl :meth:`read` / :meth:`execute_sql`
                      calls can be performed with the snapshot in the
                      context of a read-only transaction, used to ensure
                      isolation / consistency. Incompatible with
                      ``max_staleness`` and ``min_read_timestamp``.
    """
    def __init__(self, session, read_timestamp=None, min_read_timestamp=None,
                 max_staleness=None, exact_staleness=None, multi_use=False):
        super(Snapshot, self).__init__(session)
        opts = [
            read_timestamp, min_read_timestamp, max_staleness, exact_staleness]
        flagged = [opt for opt in opts if opt is not None]

        if len(flagged) > 1:
            raise ValueError("Supply zero or one options.")

        if multi_use:
            if min_read_timestamp is not None or max_staleness is not None:
                raise ValueError(
                    "'multi_use' is incompatible with "
                    "'min_read_timestamp' / 'max_staleness'")

        self._strong = len(flagged) == 0
        self._read_timestamp = read_timestamp
        self._min_read_timestamp = min_read_timestamp
        self._max_staleness = max_staleness
        self._exact_staleness = exact_staleness
        self._multi_use = multi_use

    def _make_txn_selector(self):
        """Helper for :meth:`read`."""
        if self._transaction_id is not None:
            return TransactionSelector(id=self._transaction_id)

        if self._read_timestamp:
            key = 'read_timestamp'
            value = _datetime_to_pb_timestamp(self._read_timestamp)
        elif self._min_read_timestamp:
            key = 'min_read_timestamp'
            value = _datetime_to_pb_timestamp(self._min_read_timestamp)
        elif self._max_staleness:
            key = 'max_staleness'
            value = _timedelta_to_duration_pb(self._max_staleness)
        elif self._exact_staleness:
            key = 'exact_staleness'
            value = _timedelta_to_duration_pb(self._exact_staleness)
        else:
            key = 'strong'
            value = True

        options = TransactionOptions(
            read_only=TransactionOptions.ReadOnly(**{key: value}))

        if self._multi_use:
            return TransactionSelector(begin=options)
        else:
            return TransactionSelector(single_use=options)

    def begin(self):
        """Begin a read-only transaction on the database.

        :rtype: bytes
        :returns: the ID for the newly-begun transaction.
        :raises ValueError:
            if the transaction is already begun, committed, or rolled back.
        """
        if not self._multi_use:
            raise ValueError("Cannot call 'begin' single-use snapshots")

        if self._transaction_id is not None:
            raise ValueError("Read-only transaction already begun")

        if self._read_request_count > 0:
            raise ValueError("Read-only transaction already pending")

        database = self._session._database
        api = database.spanner_api
        options = _options_with_prefix(database.name)
        txn_selector = self._make_txn_selector()
        response = api.begin_transaction(
            self._session.name, txn_selector.begin, options=options)
        self._transaction_id = response.id
        return self._transaction_id
