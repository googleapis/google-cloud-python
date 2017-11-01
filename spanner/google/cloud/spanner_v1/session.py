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

"""Wrapper for Cloud Spanner Session objects."""

from functools import total_ordering
import time

from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from google.rpc.error_details_pb2 import RetryInfo
from grpc import StatusCode

# pylint: disable=ungrouped-imports
from google.cloud.exceptions import NotFound
from google.cloud.exceptions import GrpcRendezvous
from google.cloud.spanner_v1._helpers import _options_with_prefix
from google.cloud.spanner_v1.batch import Batch
from google.cloud.spanner_v1.snapshot import Snapshot
from google.cloud.spanner_v1.transaction import Transaction
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

    :type database: :class:`~google.cloud.spanner_v1.database.Database`
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
        :raises ValueError: if session is not yet created
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
        :raises GaxError:
            for errors other than ``NOT_FOUND`` returned from the call
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

        :raises ValueError: if :attr:`session_id` is not already set.
        :raises NotFound: if the session does not exist
        :raises GaxError:
            for errors other than ``NOT_FOUND`` returned from the call
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

    def snapshot(self, **kw):
        """Create a snapshot to perform a set of reads with shared staleness.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.TransactionOptions.ReadOnly

        :type kw: dict
        :param kw: Passed through to
                   :class:`~google.cloud.spanner_v1.snapshot.Snapshot` ctor.

        :rtype: :class:`~google.cloud.spanner_v1.snapshot.Snapshot`
        :returns: a snapshot bound to this session
        :raises ValueError: if the session has not yet been created.
        """
        if self._session_id is None:
            raise ValueError("Session has not been created.")

        return Snapshot(self, **kw)

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
        """
        return self.snapshot().read(table, columns, keyset, index, limit)

    def execute_sql(self, sql, params=None, param_types=None, query_mode=None):
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

        :rtype: :class:`~google.cloud.spanner_v1.streamed.StreamedResultSet`
        :returns: a result set instance which can be used to consume rows.
        """
        return self.snapshot().execute_sql(
            sql, params, param_types, query_mode)

    def batch(self):
        """Factory to create a batch for this session.

        :rtype: :class:`~google.cloud.spanner_v1.batch.Batch`
        :returns: a batch bound to this session
        :raises ValueError: if the session has not yet been created.
        """
        if self._session_id is None:
            raise ValueError("Session has not been created.")

        return Batch(self)

    def transaction(self):
        """Create a transaction to perform a set of reads with shared staleness.

        :rtype: :class:`~google.cloud.spanner_v1.transaction.Transaction`
        :returns: a transaction bound to this session
        :raises ValueError: if the session has not yet been created.
        """
        if self._session_id is None:
            raise ValueError("Session has not been created.")

        if self._transaction is not None:
            self._transaction._rolled_back = True
            del self._transaction

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

        :rtype: Any
        :returns: The return value of ``func``.

        :raises Exception:
            reraises any non-ABORT execptions raised by ``func``.
        """
        deadline = time.time() + kw.pop(
            'timeout_secs', DEFAULT_RETRY_TIMEOUT_SECS)

        while True:
            if self._transaction is None:
                txn = self.transaction()
            else:
                txn = self._transaction
            if txn._transaction_id is None:
                txn.begin()
            try:
                return_value = func(txn, *args, **kw)
            except (GaxError, GrpcRendezvous) as exc:
                del self._transaction
                _delay_until_retry(exc, deadline)
                continue
            except Exception:
                txn.rollback()
                raise

            try:
                txn.commit()
            except GaxError as exc:
                del self._transaction
                _delay_until_retry(exc, deadline)
            else:
                return return_value


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
    if isinstance(exc, GrpcRendezvous):  # pragma: NO COVER  see #3663
        cause = exc
    else:
        cause = exc.cause

    if exc_to_code(cause) != StatusCode.ABORTED:
        raise

    now = time.time()

    if now >= deadline:
        raise

    delay = _get_retry_delay(cause)
    if delay is not None:

        if now + delay > deadline:
            raise

        time.sleep(delay)
# pylint: enable=misplaced-bare-raise


def _get_retry_delay(cause):
    """Helper for :func:`_delay_until_retry`.

    :type exc: :class:`google.gax.errors.GaxError`
    :param exc: exception for aborted transaction

    :rtype: float
    :returns: seconds to wait before retrying the transaction.
    """
    metadata = dict(cause.trailing_metadata())
    retry_info_pb = metadata.get('google.rpc.retryinfo-bin')
    if retry_info_pb is not None:
        retry_info = RetryInfo()
        retry_info.ParseFromString(retry_info_pb)
        nanos = retry_info.retry_delay.nanos
        return retry_info.retry_delay.seconds + nanos / 1.0e9
