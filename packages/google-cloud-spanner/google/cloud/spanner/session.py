# Copyright 2016 Google Inc. All rights reserved.
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

"""Wrapper for Cloud Spanner Session objects."""

from functools import total_ordering
import time

from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from google.rpc.error_details_pb2 import RetryInfo
from grpc import StatusCode

# pylint: disable=ungrouped-imports
from google.cloud.exceptions import NotFound
from google.cloud.spanner._helpers import _options_with_prefix
from google.cloud.spanner.batch import Batch
from google.cloud.spanner.snapshot import Snapshot
from google.cloud.spanner.transaction import Transaction
# pylint: enable=ungrouped-imports


DEFAULT_RETRY_TIMEOUT_SECS = 30
"""Default timeout used by :meth:`Session.run_in_transaction`."""


@total_ordering
class Session(object):
    """Representation of a Cloud Spanner Session.

    We can use a :class:`Session` to:

    * :meth:`create` the session
    * Use :meth:`exists` to check for the existence of the session
    * :meth:`drop` the session

    :type database: :class:`~google.cloud.spanner.database.Database`
    :param database: The database to which the session is bound.
    """

    _session_id = None
    _transaction = None

    def __init__(self, database):
        self._database = database

    def __lt__(self, other):
        return self._session_id < other._session_id

    @property
    def session_id(self):
        """Read-only ID, set by the back-end during :meth:`create`."""
        return self._session_id

    @property
    def name(self):
        """Session name used in requests.

        .. note::

          This property will not change if ``session_id`` does not, but the
          return value is not cached.

        The session name is of the form

            ``"projects/../instances/../databases/../sessions/{session_id}"``

        :rtype: str
        :returns: The session name.
        """
        if self._session_id is None:
            raise ValueError('No session ID set by back-end')
        return self._database.name + '/sessions/' + self._session_id

    def create(self):
        """Create this session, bound to its database.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.Spanner.CreateSession

        :raises: :exc:`ValueError` if :attr:`session_id` is already set.
        """
        if self._session_id is not None:
            raise ValueError('Session ID already set by back-end')
        api = self._database.spanner_api
        options = _options_with_prefix(self._database.name)
        session_pb = api.create_session(self._database.name, options=options)
        self._session_id = session_pb.name.split('/')[-1]

    def exists(self):
        """Test for the existence of this session.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.Spanner.GetSession

        :rtype: bool
        :returns: True if the session exists on the back-end, else False.
        """
        if self._session_id is None:
            return False
        api = self._database.spanner_api
        options = _options_with_prefix(self._database.name)
        try:
            api.get_session(self.name, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                return False
            raise
        else:
            return True

    def delete(self):
        """Delete this session.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.Spanner.GetSession

        :raises: :exc:`ValueError` if :attr:`session_id` is not already set.
        """
        if self._session_id is None:
            raise ValueError('Session ID not set by back-end')
        api = self._database.spanner_api
        options = _options_with_prefix(self._database.name)
        try:
            api.delete_session(self.name, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(self.name)
            raise

    def snapshot(self, read_timestamp=None, min_read_timestamp=None,
                 max_staleness=None, exact_staleness=None):
        """Create a snapshot to perform a set of reads with shared staleness.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.TransactionOptions.ReadOnly

        If no options are passed, reads will use the ``strong`` model, reading
        at a timestamp where all previously committed transactions are visible.

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

        :rtype: :class:`~google.cloud.spanner.snapshot.Snapshot`
        :returns: a snapshot bound to this session
        :raises: :exc:`ValueError` if the session has not yet been created.
        """
        if self._session_id is None:
            raise ValueError("Session has not been created.")

        return Snapshot(self,
                        read_timestamp=read_timestamp,
                        min_read_timestamp=min_read_timestamp,
                        max_staleness=max_staleness,
                        exact_staleness=exact_staleness)

    def read(self, table, columns, keyset, index='', limit=0,
             resume_token=b''):
        """Perform a ``StreamingRead`` API request for rows in a table.

        :type table: str
        :param table: name of the table from which to fetch data

        :type columns: list of str
        :param columns: names of columns to be retrieved

        :type keyset: :class:`~google.cloud.spanner.keyset.KeySet`
        :param keyset: keys / ranges identifying rows to be retrieved

        :type index: str
        :param index: (Optional) name of index to use, rather than the
                      table's primary key

        :type limit: int
        :param limit: (Optional) maxiumn number of rows to return

        :type resume_token: bytes
        :param resume_token: token for resuming previously-interrupted read

        :rtype: :class:`~google.cloud.spanner.streamed.StreamedResultSet`
        :returns: a result set instance which can be used to consume rows.
        """
        return self.snapshot().read(
            table, columns, keyset, index, limit, resume_token)

    def execute_sql(self, sql, params=None, param_types=None, query_mode=None,
                    resume_token=b''):
        """Perform an ``ExecuteStreamingSql`` API request.

        :type sql: str
        :param sql: SQL query statement

        :type params: dict, {str -> column value}
        :param params: values for parameter replacement.  Keys must match
                       the names used in ``sql``.

        :type param_types:
            dict, {str -> :class:`google.spanner.v1.type_pb2.TypeCode`}
        :param param_types: (Optional) explicit types for one or more param
                            values;  overrides default type detection on the
                            back-end.

        :type query_mode:
            :class:`google.spanner.v1.spanner_pb2.ExecuteSqlRequest.QueryMode`
        :param query_mode: Mode governing return of results / query plan. See
            https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.ExecuteSqlRequest.QueryMode1

        :type resume_token: bytes
        :param resume_token: token for resuming previously-interrupted query

        :rtype: :class:`~google.cloud.spanner.streamed.StreamedResultSet`
        :returns: a result set instance which can be used to consume rows.
        """
        return self.snapshot().execute_sql(
            sql, params, param_types, query_mode, resume_token)

    def batch(self):
        """Factory to create a batch for this session.

        :rtype: :class:`~google.cloud.spanner.batch.Batch`
        :returns: a batch bound to this session
        :raises: :exc:`ValueError` if the session has not yet been created.
        """
        if self._session_id is None:
            raise ValueError("Session has not been created.")

        return Batch(self)

    def transaction(self):
        """Create a transaction to perform a set of reads with shared staleness.

        :rtype: :class:`~google.cloud.spanner.transaction.Transaction`
        :returns: a transaction bound to this session
        :raises: :exc:`ValueError` if the session has not yet been created.
        """
        if self._session_id is None:
            raise ValueError("Session has not been created.")

        if self._transaction is not None:
            self._transaction._rolled_back = True

        txn = self._transaction = Transaction(self)
        return txn

    def run_in_transaction(self, func, *args, **kw):
        """Perform a unit of work in a transaction, retrying on abort.

        :type func: callable
        :param func: takes a required positional argument, the transaction,
                     and additional positional / keyword arguments as supplied
                     by the caller.

        :type args: tuple
        :param args: additional positional arguments to be passed to ``func``.

        :type kw: dict
        :param kw: optional keyword arguments to be passed to ``func``.
                   If passed, "timeout_secs" will be removed and used to
                   override the default timeout.

        :rtype: :class:`datetime.datetime`
        :returns: timestamp of committed transaction
        """
        deadline = time.time() + kw.pop(
            'timeout_secs', DEFAULT_RETRY_TIMEOUT_SECS)

        while True:
            if self._transaction is None:
                txn = self.transaction()
            else:
                txn = self._transaction
            if txn._id is None:
                txn.begin()
            try:
                func(txn, *args, **kw)
            except GaxError as exc:
                _delay_until_retry(exc, deadline)
                del self._transaction
                continue
            except Exception:
                txn.rollback()
                del self._transaction
                raise

            try:
                txn.commit()
            except GaxError as exc:
                _delay_until_retry(exc, deadline)
                del self._transaction
            else:
                committed = txn.committed
                del self._transaction
                return committed


# pylint: disable=misplaced-bare-raise
#
# Rational:  this function factors out complex shared deadline / retry
#            handling from two `except:` clauses.
def _delay_until_retry(exc, deadline):
    """Helper for :meth:`Session.run_in_transaction`.

    Detect retryable abort, and impose server-supplied delay.

    :type exc: :class:`google.gax.errors.GaxError`
    :param exc: exception for aborted transaction

    :type deadline: float
    :param deadline: maximum timestamp to continue retrying the transaction.
    """
    if exc_to_code(exc.cause) != StatusCode.ABORTED:
        raise

    now = time.time()

    if now >= deadline:
        raise

    delay = _get_retry_delay(exc)
    if delay is not None:

        if now + delay > deadline:
            raise

        time.sleep(delay)
# pylint: enable=misplaced-bare-raise


def _get_retry_delay(exc):
    """Helper for :func:`_delay_until_retry`.

    :type exc: :class:`google.gax.errors.GaxError`
    :param exc: exception for aborted transaction

    :rtype: float
    :returns: seconds to wait before retrying the transaction.
    """
    metadata = dict(exc.cause.trailing_metadata())
    retry_info_pb = metadata.get('google.rpc.retryinfo-bin')
    if retry_info_pb is not None:
        retry_info = RetryInfo()
        retry_info.ParseFromString(retry_info_pb)
        nanos = retry_info.retry_delay.nanos
        return retry_info.retry_delay.seconds + nanos / 1.0e9
