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
from datetime import datetime

from google.api_core.exceptions import Aborted
from google.api_core.exceptions import GoogleAPICallError
from google.api_core.exceptions import NotFound
from google.api_core.gapic_v1 import method
from google.cloud.spanner_v1._helpers import _delay_until_retry
from google.cloud.spanner_v1._helpers import _get_retry_delay

from google.cloud.spanner_v1 import ExecuteSqlRequest
from google.cloud.spanner_v1 import CreateSessionRequest
from google.cloud.spanner_v1._helpers import (
    _metadata_with_prefix,
    _metadata_with_leader_aware_routing,
)
from google.cloud.spanner_v1._opentelemetry_tracing import (
    add_span_event,
    get_current_span,
    trace_call,
)
from google.cloud.spanner_v1.batch import Batch
from google.cloud.spanner_v1.snapshot import Snapshot
from google.cloud.spanner_v1.transaction import Transaction
from google.cloud.spanner_v1.metrics.metrics_capture import MetricsCapture


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

    :type labels: dict (str -> str)
    :param labels: (Optional) User-assigned labels for the session.

    :type database_role: str
    :param database_role: (Optional) user-assigned database_role for the session.
    """

    _session_id = None
    _transaction = None

    def __init__(self, database, labels=None, database_role=None):
        self._database = database
        if labels is None:
            labels = {}
        self._labels = labels
        self._database_role = database_role
        self._last_use_time = datetime.utcnow()

    def __lt__(self, other):
        return self._session_id < other._session_id

    @property
    def session_id(self):
        """Read-only ID, set by the back-end during :meth:`create`."""
        return self._session_id

    @property
    def last_use_time(self):
        """ "Approximate last use time of this session

        :rtype: datetime
        :returns: the approximate last use time of this session"""
        return self._last_use_time

    @property
    def database_role(self):
        """User-assigned database-role for the session.

        :rtype: str
        :returns: the database role str (None if no database role were assigned)."""
        return self._database_role

    @property
    def labels(self):
        """User-assigned labels for the session.

        :rtype: dict (str -> str)
        :returns: the labels dict (empty if no labels were assigned.
        """
        return self._labels

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
            raise ValueError("No session ID set by back-end")
        return self._database.name + "/sessions/" + self._session_id

    def create(self):
        """Create this session, bound to its database.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.Spanner.CreateSession

        :raises ValueError: if :attr:`session_id` is already set.
        """
        current_span = get_current_span()
        add_span_event(current_span, "Creating Session")

        if self._session_id is not None:
            raise ValueError("Session ID already set by back-end")
        api = self._database.spanner_api
        metadata = _metadata_with_prefix(self._database.name)
        if self._database._route_to_leader_enabled:
            metadata.append(
                _metadata_with_leader_aware_routing(
                    self._database._route_to_leader_enabled
                )
            )

        request = CreateSessionRequest(database=self._database.name)
        if self._database.database_role is not None:
            request.session.creator_role = self._database.database_role

        if self._labels:
            request.session.labels = self._labels

        observability_options = getattr(self._database, "observability_options", None)
        with trace_call(
            "CloudSpanner.CreateSession",
            self,
            self._labels,
            observability_options=observability_options,
            metadata=metadata,
        ), MetricsCapture():
            session_pb = api.create_session(
                request=request,
                metadata=metadata,
            )
        self._session_id = session_pb.name.split("/")[-1]

    def exists(self):
        """Test for the existence of this session.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.Spanner.GetSession

        :rtype: bool
        :returns: True if the session exists on the back-end, else False.
        """
        current_span = get_current_span()
        if self._session_id is None:
            add_span_event(
                current_span,
                "Checking session existence: Session does not exist as it has not been created yet",
            )
            return False

        add_span_event(
            current_span, "Checking if Session exists", {"session.id": self._session_id}
        )

        api = self._database.spanner_api
        metadata = _metadata_with_prefix(self._database.name)
        if self._database._route_to_leader_enabled:
            metadata.append(
                _metadata_with_leader_aware_routing(
                    self._database._route_to_leader_enabled
                )
            )

        observability_options = getattr(self._database, "observability_options", None)
        with trace_call(
            "CloudSpanner.GetSession",
            self,
            observability_options=observability_options,
            metadata=metadata,
        ) as span, MetricsCapture():
            try:
                api.get_session(name=self.name, metadata=metadata)
                if span:
                    span.set_attribute("session_found", True)
            except NotFound:
                if span:
                    span.set_attribute("session_found", False)
                return False

        return True

    def delete(self):
        """Delete this session.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.Spanner.GetSession

        :raises ValueError: if :attr:`session_id` is not already set.
        :raises NotFound: if the session does not exist
        """
        current_span = get_current_span()
        if self._session_id is None:
            add_span_event(
                current_span, "Deleting Session failed due to unset session_id"
            )
            raise ValueError("Session ID not set by back-end")

        add_span_event(
            current_span, "Deleting Session", {"session.id": self._session_id}
        )

        api = self._database.spanner_api
        metadata = _metadata_with_prefix(self._database.name)
        observability_options = getattr(self._database, "observability_options", None)
        with trace_call(
            "CloudSpanner.DeleteSession",
            self,
            extra_attributes={
                "session.id": self._session_id,
                "session.name": self.name,
            },
            observability_options=observability_options,
            metadata=metadata,
        ), MetricsCapture():
            api.delete_session(name=self.name, metadata=metadata)

    def ping(self):
        """Ping the session to keep it alive by executing "SELECT 1".

        :raises ValueError: if :attr:`session_id` is not already set.
        """
        if self._session_id is None:
            raise ValueError("Session ID not set by back-end")
        api = self._database.spanner_api
        metadata = _metadata_with_prefix(self._database.name)
        request = ExecuteSqlRequest(session=self.name, sql="SELECT 1")
        api.execute_sql(request=request, metadata=metadata)
        self._last_use_time = datetime.now()

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

    def read(self, table, columns, keyset, index="", limit=0, column_info=None):
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
        :param limit: (Optional) maximum number of rows to return

        :type column_info: dict
        :param column_info: (Optional) dict of mapping between column names and additional column information.
            An object where column names as keys and custom objects as corresponding
            values for deserialization. It's specifically useful for data types like
            protobuf where deserialization logic is on user-specific code. When provided,
            the custom object enables deserialization of backend-received column data.
            If not provided, data remains serialized as bytes for Proto Messages and
            integer for Proto Enums.

        :rtype: :class:`~google.cloud.spanner_v1.streamed.StreamedResultSet`
        :returns: a result set instance which can be used to consume rows.
        """
        return self.snapshot().read(
            table, columns, keyset, index, limit, column_info=column_info
        )

    def execute_sql(
        self,
        sql,
        params=None,
        param_types=None,
        query_mode=None,
        query_options=None,
        request_options=None,
        retry=method.DEFAULT,
        timeout=method.DEFAULT,
        column_info=None,
    ):
        """Perform an ``ExecuteStreamingSql`` API request.

        :type sql: str
        :param sql: SQL query statement

        :type params: dict, {str -> column value}
        :param params: values for parameter replacement.  Keys must match
                       the names used in ``sql``.

        :type param_types:
            dict, {str -> :class:`~google.spanner.v1.types.TypeCode`}
        :param param_types: (Optional) explicit types for one or more param
                            values;  overrides default type detection on the
                            back-end.

        :type query_mode:
            :class:`~google.spanner.v1.types.ExecuteSqlRequest.QueryMode`
        :param query_mode: Mode governing return of results / query plan. See:
            `QueryMode <https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.ExecuteSqlRequest.QueryMode>`_.

        :type query_options:
            :class:`~google.cloud.spanner_v1.types.ExecuteSqlRequest.QueryOptions`
            or :class:`dict`
        :param query_options: (Optional) Options that are provided for query plan stability.

        :type request_options:
            :class:`google.cloud.spanner_v1.types.RequestOptions`
        :param request_options:
                (Optional) Common options for this request.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_v1.types.RequestOptions`.

        :type retry: :class:`~google.api_core.retry.Retry`
        :param retry: (Optional) The retry settings for this request.

        :type timeout: float
        :param timeout: (Optional) The timeout for this request.

        :type column_info: dict
        :param column_info: (Optional) dict of mapping between column names and additional column information.
            An object where column names as keys and custom objects as corresponding
            values for deserialization. It's specifically useful for data types like
            protobuf where deserialization logic is on user-specific code. When provided,
            the custom object enables deserialization of backend-received column data.
            If not provided, data remains serialized as bytes for Proto Messages and
            integer for Proto Enums.

        :rtype: :class:`~google.cloud.spanner_v1.streamed.StreamedResultSet`
        :returns: a result set instance which can be used to consume rows.
        """
        return self.snapshot().execute_sql(
            sql,
            params,
            param_types,
            query_mode,
            query_options=query_options,
            request_options=request_options,
            retry=retry,
            timeout=timeout,
            column_info=column_info,
        )

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
            self._transaction.rolled_back = True
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
        :param kw: (Optional) keyword arguments to be passed to ``func``.
                   If passed:
                   "timeout_secs" will be removed and used to
                   override the default retry timeout which defines maximum timestamp
                   to continue retrying the transaction.
                   "commit_request_options" will be removed and used to set the
                   request options for the commit request.
                   "max_commit_delay" will be removed and used to set the max commit delay for the request.
                   "transaction_tag" will be removed and used to set the transaction tag for the request.
                   "exclude_txn_from_change_streams" if true, instructs the transaction to be excluded
                   from being recorded in change streams with the DDL option `allow_txn_exclusion=true`.
                   This does not exclude the transaction from being recorded in the change streams with
                   the DDL option `allow_txn_exclusion` being false or unset.
                   "isolation_level" sets the isolation level for the transaction.

        :rtype: Any
        :returns: The return value of ``func``.

        :raises Exception:
            reraises any non-ABORT exceptions raised by ``func``.
        """
        deadline = time.time() + kw.pop("timeout_secs", DEFAULT_RETRY_TIMEOUT_SECS)
        commit_request_options = kw.pop("commit_request_options", None)
        max_commit_delay = kw.pop("max_commit_delay", None)
        transaction_tag = kw.pop("transaction_tag", None)
        exclude_txn_from_change_streams = kw.pop(
            "exclude_txn_from_change_streams", None
        )
        isolation_level = kw.pop("isolation_level", None)

        attempts = 0

        observability_options = getattr(self._database, "observability_options", None)
        with trace_call(
            "CloudSpanner.Session.run_in_transaction",
            self,
            observability_options=observability_options,
        ) as span, MetricsCapture():
            while True:
                if self._transaction is None:
                    txn = self.transaction()
                    txn.transaction_tag = transaction_tag
                    txn.exclude_txn_from_change_streams = (
                        exclude_txn_from_change_streams
                    )
                    txn.isolation_level = isolation_level
                else:
                    txn = self._transaction

                span_attributes = dict()

                try:
                    attempts += 1
                    span_attributes["attempt"] = attempts
                    txn_id = getattr(txn, "_transaction_id", "") or ""
                    if txn_id:
                        span_attributes["transaction.id"] = txn_id

                    return_value = func(txn, *args, **kw)

                except Aborted as exc:
                    del self._transaction
                    if span:
                        delay_seconds = _get_retry_delay(exc.errors[0], attempts)
                        attributes = dict(delay_seconds=delay_seconds, cause=str(exc))
                        attributes.update(span_attributes)
                        add_span_event(
                            span,
                            "Transaction was aborted in user operation, retrying",
                            attributes,
                        )

                    _delay_until_retry(exc, deadline, attempts)
                    continue
                except GoogleAPICallError:
                    del self._transaction
                    add_span_event(
                        span,
                        "User operation failed due to GoogleAPICallError, not retrying",
                        span_attributes,
                    )
                    raise
                except Exception:
                    add_span_event(
                        span,
                        "User operation failed. Invoking Transaction.rollback(), not retrying",
                        span_attributes,
                    )
                    txn.rollback()
                    raise

                try:
                    txn.commit(
                        return_commit_stats=self._database.log_commit_stats,
                        request_options=commit_request_options,
                        max_commit_delay=max_commit_delay,
                    )
                except Aborted as exc:
                    del self._transaction
                    if span:
                        delay_seconds = _get_retry_delay(exc.errors[0], attempts)
                        attributes = dict(delay_seconds=delay_seconds)
                        attributes.update(span_attributes)
                        add_span_event(
                            span,
                            "Transaction got aborted during commit, retrying afresh",
                            attributes,
                        )

                    _delay_until_retry(exc, deadline, attempts)
                except GoogleAPICallError:
                    del self._transaction
                    add_span_event(
                        span,
                        "Transaction.commit failed due to GoogleAPICallError, not retrying",
                        span_attributes,
                    )
                    raise
                else:
                    if self._database.log_commit_stats and txn.commit_stats:
                        self._database.logger.info(
                            "CommitStats: {}".format(txn.commit_stats),
                            extra={"commit_stats": txn.commit_stats},
                        )
                    return return_value
