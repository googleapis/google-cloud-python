# Copyright 2015 Google LLC
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

"""User-friendly container for Google Cloud Bigtable Table."""


from grpc import StatusCode

from google.api_core import timeout
from google.api_core.exceptions import RetryError
from google.api_core.exceptions import NotFound
from google.api_core.retry import if_exception_type
from google.api_core.retry import Retry
from google.api_core.gapic_v1.method import wrap_method
from google.cloud._helpers import _to_bytes
from google.cloud.bigtable.column_family import _gc_rule_from_pb
from google.cloud.bigtable.column_family import ColumnFamily
from google.cloud.bigtable.batcher import MutationsBatcher
from google.cloud.bigtable.batcher import FLUSH_COUNT, MAX_ROW_BYTES
from google.cloud.bigtable.row import AppendRow
from google.cloud.bigtable.row import ConditionalRow
from google.cloud.bigtable.row import DirectRow
from google.cloud.bigtable.row_data import PartialRowsData
from google.cloud.bigtable.row_data import DEFAULT_RETRY_READ_ROWS
from google.cloud.bigtable.row_set import RowSet
from google.cloud.bigtable.row_set import RowRange
from google.cloud.bigtable import enums
from google.cloud.bigtable_v2.proto import bigtable_pb2 as data_messages_v2_pb2
from google.cloud.bigtable_admin_v2.proto import table_pb2 as admin_messages_v2_pb2
from google.cloud.bigtable_admin_v2.proto import (
    bigtable_table_admin_pb2 as table_admin_messages_v2_pb2,
)

import warnings


# Maximum number of mutations in bulk (MutateRowsRequest message):
# (https://cloud.google.com/bigtable/docs/reference/data/rpc/
#  google.bigtable.v2#google.bigtable.v2.MutateRowRequest)
_MAX_BULK_MUTATIONS = 100000
VIEW_NAME_ONLY = enums.Table.View.NAME_ONLY


class _BigtableRetryableError(Exception):
    """Retry-able error expected by the default retry strategy."""


DEFAULT_RETRY = Retry(
    predicate=if_exception_type(_BigtableRetryableError),
    initial=1.0,
    maximum=15.0,
    multiplier=2.0,
    deadline=120.0,  # 2 minutes
)
"""The default retry strategy to be used on retry-able errors.

Used by :meth:`~google.cloud.bigtable.table.Table.mutate_rows`.
"""


class TableMismatchError(ValueError):
    """Row from another table."""


class TooManyMutationsError(ValueError):
    """The number of mutations for bulk request is too big."""


class Table(object):
    """Representation of a Google Cloud Bigtable Table.

    .. note::

        We don't define any properties on a table other than the name.
        The only other fields are ``column_families`` and ``granularity``,
        The ``column_families`` are not stored locally and
        ``granularity`` is an enum with only one value.

    We can use a :class:`Table` to:

    * :meth:`create` the table
    * :meth:`delete` the table
    * :meth:`list_column_families` in the table

    :type table_id: str
    :param table_id: The ID of the table.

    :type instance: :class:`~google.cloud.bigtable.instance.Instance`
    :param instance: The instance that owns the table.

    :type app_profile_id: str
    :param app_profile_id: (Optional) The unique name of the AppProfile.
    """

    def __init__(self, table_id, instance, mutation_timeout=None, app_profile_id=None):
        self.table_id = table_id
        self._instance = instance
        self._app_profile_id = app_profile_id
        self.mutation_timeout = mutation_timeout

    @property
    def name(self):
        """Table name used in requests.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_table_name]
            :end-before: [END bigtable_table_name]

        .. note::

          This property will not change if ``table_id`` does not, but the
          return value is not cached.

        The table name is of the form

            ``"projects/../instances/../tables/{table_id}"``

        :rtype: str
        :returns: The table name.
        """
        project = self._instance._client.project
        instance_id = self._instance.instance_id
        table_client = self._instance._client.table_data_client
        return table_client.table_path(
            project=project, instance=instance_id, table=self.table_id
        )

    def column_family(self, column_family_id, gc_rule=None):
        """Factory to create a column family associated with this table.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_table_column_family]
            :end-before: [END bigtable_table_column_family]

        :type column_family_id: str
        :param column_family_id: The ID of the column family. Must be of the
                                 form ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.

        :type gc_rule: :class:`.GarbageCollectionRule`
        :param gc_rule: (Optional) The garbage collection settings for this
                        column family.

        :rtype: :class:`.ColumnFamily`
        :returns: A column family owned by this table.
        """
        return ColumnFamily(column_family_id, self, gc_rule=gc_rule)

    def row(self, row_key, filter_=None, append=False):
        """Factory to create a row associated with this table.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_table_row]
            :end-before: [END bigtable_table_row]

        .. warning::

           At most one of ``filter_`` and ``append`` can be used in a
           :class:`~google.cloud.bigtable.row.Row`.

        :type row_key: bytes
        :param row_key: The key for the row being created.

        :type filter_: :class:`.RowFilter`
        :param filter_: (Optional) Filter to be used for conditional mutations.
                        See :class:`.ConditionalRow` for more details.

        :type append: bool
        :param append: (Optional) Flag to determine if the row should be used
                       for append mutations.

        :rtype: :class:`~google.cloud.bigtable.row.Row`
        :returns: A row owned by this table.
        :raises: :class:`ValueError <exceptions.ValueError>` if both
                 ``filter_`` and ``append`` are used.
        """
        if append and filter_ is not None:
            raise ValueError("At most one of filter_ and append can be set")
        if append:
            return AppendRow(row_key, self)
        elif filter_ is not None:
            return ConditionalRow(row_key, self, filter_=filter_)
        else:
            return DirectRow(row_key, self)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return other.table_id == self.table_id and other._instance == self._instance

    def __ne__(self, other):
        return not self == other

    def create(self, initial_split_keys=[], column_families={}):
        """Creates this table.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_create_table]
            :end-before: [END bigtable_create_table]

        .. note::

            A create request returns a
            :class:`._generated.table_pb2.Table` but we don't use
            this response.

        :type initial_split_keys: list
        :param initial_split_keys: (Optional) list of row keys in bytes that
                                   will be used to initially split the table
                                   into several tablets.

        :type column_families: dict
        :param column_failies: (Optional) A map columns to create.  The key is
                               the column_id str and the value is a
                               :class:`GarbageCollectionRule`
        """
        table_client = self._instance._client.table_admin_client
        instance_name = self._instance.name

        families = {
            id: ColumnFamily(id, self, rule).to_pb()
            for (id, rule) in column_families.items()
        }
        table = admin_messages_v2_pb2.Table(column_families=families)

        split = table_admin_messages_v2_pb2.CreateTableRequest.Split
        splits = [split(key=_to_bytes(key)) for key in initial_split_keys]

        table_client.create_table(
            parent=instance_name,
            table_id=self.table_id,
            table=table,
            initial_splits=splits,
        )

    def exists(self):
        """Check whether the table exists.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_check_table_exists]
            :end-before: [END bigtable_check_table_exists]

        :rtype: bool
        :returns: True if the table exists, else False.
        """
        table_client = self._instance._client.table_admin_client
        try:
            table_client.get_table(name=self.name, view=VIEW_NAME_ONLY)
            return True
        except NotFound:
            return False

    def delete(self):
        """Delete this table.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_delete_table]
            :end-before: [END bigtable_delete_table]

        """
        table_client = self._instance._client.table_admin_client
        table_client.delete_table(name=self.name)

    def list_column_families(self):
        """List the column families owned by this table.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_list_column_families]
            :end-before: [END bigtable_list_column_families]

        :rtype: dict
        :returns: Dictionary of column families attached to this table. Keys
                  are strings (column family names) and values are
                  :class:`.ColumnFamily` instances.
        :raises: :class:`ValueError <exceptions.ValueError>` if the column
                 family name from the response does not agree with the computed
                 name from the column family ID.
        """
        table_client = self._instance._client.table_admin_client
        table_pb = table_client.get_table(self.name)

        result = {}
        for column_family_id, value_pb in table_pb.column_families.items():
            gc_rule = _gc_rule_from_pb(value_pb.gc_rule)
            column_family = self.column_family(column_family_id, gc_rule=gc_rule)
            result[column_family_id] = column_family
        return result

    def get_cluster_states(self):
        """List the cluster states owned by this table.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_get_cluster_states]
            :end-before: [END bigtable_get_cluster_states]

        :rtype: dict
        :returns: Dictionary of cluster states for this table.
                  Keys are cluster ids and values are
                  :class: 'ClusterState' instances.
        """

        REPLICATION_VIEW = enums.Table.View.REPLICATION_VIEW
        table_client = self._instance._client.table_admin_client
        table_pb = table_client.get_table(self.name, view=REPLICATION_VIEW)

        return {
            cluster_id: ClusterState(value_pb.replication_state)
            for cluster_id, value_pb in table_pb.cluster_states.items()
        }

    def read_row(self, row_key, filter_=None):
        """Read a single row from this table.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_read_row]
            :end-before: [END bigtable_read_row]

        :type row_key: bytes
        :param row_key: The key of the row to read from.

        :type filter_: :class:`.RowFilter`
        :param filter_: (Optional) The filter to apply to the contents of the
                        row. If unset, returns the entire row.

        :rtype: :class:`.PartialRowData`, :data:`NoneType <types.NoneType>`
        :returns: The contents of the row if any chunks were returned in
                  the response, otherwise :data:`None`.
        :raises: :class:`ValueError <exceptions.ValueError>` if a commit row
                 chunk is never encountered.
        """
        row_set = RowSet()
        row_set.add_row_key(row_key)
        result_iter = iter(self.read_rows(filter_=filter_, row_set=row_set))
        row = next(result_iter, None)
        if next(result_iter, None) is not None:
            raise ValueError("More than one row was returned.")
        return row

    def read_rows(
        self,
        start_key=None,
        end_key=None,
        limit=None,
        filter_=None,
        end_inclusive=False,
        row_set=None,
        retry=DEFAULT_RETRY_READ_ROWS,
    ):
        """Read rows from this table.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_read_rows]
            :end-before: [END bigtable_read_rows]

        :type start_key: bytes
        :param start_key: (Optional) The beginning of a range of row keys to
                          read from. The range will include ``start_key``. If
                          left empty, will be interpreted as the empty string.

        :type end_key: bytes
        :param end_key: (Optional) The end of a range of row keys to read from.
                        The range will not include ``end_key``. If left empty,
                        will be interpreted as an infinite string.

        :type limit: int
        :param limit: (Optional) The read will terminate after committing to N
                      rows' worth of results. The default (zero) is to return
                      all results.

        :type filter_: :class:`.RowFilter`
        :param filter_: (Optional) The filter to apply to the contents of the
                        specified row(s). If unset, reads every column in
                        each row.

        :type end_inclusive: bool
        :param end_inclusive: (Optional) Whether the ``end_key`` should be
                      considered inclusive. The default is False (exclusive).

        :type row_set: :class:`row_set.RowSet`
        :param row_set: (Optional) The row set containing multiple row keys and
                        row_ranges.

        :type retry: :class:`~google.api_core.retry.Retry`
        :param retry:
            (Optional) Retry delay and deadline arguments. To override, the
            default value :attr:`DEFAULT_RETRY_READ_ROWS` can be used and
            modified with the :meth:`~google.api_core.retry.Retry.with_delay`
            method or the :meth:`~google.api_core.retry.Retry.with_deadline`
            method.

        :rtype: :class:`.PartialRowsData`
        :returns: A :class:`.PartialRowsData` a generator for consuming
                  the streamed results.
        """
        request_pb = _create_row_request(
            self.name,
            start_key=start_key,
            end_key=end_key,
            filter_=filter_,
            limit=limit,
            end_inclusive=end_inclusive,
            app_profile_id=self._app_profile_id,
            row_set=row_set,
        )
        data_client = self._instance._client.table_data_client
        return PartialRowsData(data_client.transport.read_rows, request_pb, retry)

    def yield_rows(self, **kwargs):
        """Read rows from this table.

        .. warning::
           This method will be removed in future releases.  Please use
           ``read_rows`` instead.

        :type start_key: bytes
        :param start_key: (Optional) The beginning of a range of row keys to
                          read from. The range will include ``start_key``. If
                          left empty, will be interpreted as the empty string.

        :type end_key: bytes
        :param end_key: (Optional) The end of a range of row keys to read from.
                        The range will not include ``end_key``. If left empty,
                        will be interpreted as an infinite string.

        :type limit: int
        :param limit: (Optional) The read will terminate after committing to N
                      rows' worth of results. The default (zero) is to return
                      all results.

        :type filter_: :class:`.RowFilter`
        :param filter_: (Optional) The filter to apply to the contents of the
                        specified row(s). If unset, reads every column in
                        each row.

        :type row_set: :class:`row_set.RowSet`
        :param row_set: (Optional) The row set containing multiple row keys and
                        row_ranges.

        :rtype: :class:`.PartialRowData`
        :returns: A :class:`.PartialRowData` for each row returned
        """
        warnings.warn(
            "`yield_rows()` is deprecated; use `read_rows()` instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.read_rows(**kwargs)

    def mutate_rows(self, rows, retry=DEFAULT_RETRY):
        """Mutates multiple rows in bulk.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_mutate_rows]
            :end-before: [END bigtable_mutate_rows]

        The method tries to update all specified rows.
        If some of the rows weren't updated, it would not remove mutations.
        They can be applied to the row separately.
        If row mutations finished successfully, they would be cleaned up.

        Optionally, a ``retry`` strategy can be specified to re-attempt
        mutations on rows that return transient errors. This method will retry
        until all rows succeed or until the request deadline is reached. To
        specify a ``retry`` strategy of "do-nothing", a deadline of ``0.0``
        can be specified.

        :type rows: list
        :param rows: List or other iterable of :class:`.DirectRow` instances.

        :type retry: :class:`~google.api_core.retry.Retry`
        :param retry:
            (Optional) Retry delay and deadline arguments. To override, the
            default value :attr:`DEFAULT_RETRY` can be used and modified with
            the :meth:`~google.api_core.retry.Retry.with_delay` method or the
            :meth:`~google.api_core.retry.Retry.with_deadline` method.

        :rtype: list
        :returns: A list of response statuses (`google.rpc.status_pb2.Status`)
                  corresponding to success or failure of each row mutation
                  sent. These will be in the same order as the `rows`.
        """
        retryable_mutate_rows = _RetryableMutateRowsWorker(
            self._instance._client,
            self.name,
            rows,
            app_profile_id=self._app_profile_id,
            timeout=self.mutation_timeout,
        )
        return retryable_mutate_rows(retry=retry)

    def sample_row_keys(self):
        """Read a sample of row keys in the table.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_sample_row_keys]
            :end-before: [END bigtable_sample_row_keys]

        The returned row keys will delimit contiguous sections of the table of
        approximately equal size, which can be used to break up the data for
        distributed tasks like mapreduces.

        The elements in the iterator are a SampleRowKeys response and they have
        the properties ``offset_bytes`` and ``row_key``. They occur in sorted
        order. The table might have contents before the first row key in the
        list and after the last one, but a key containing the empty string
        indicates "end of table" and will be the last response given, if
        present.

        .. note::

            Row keys in this list may not have ever been written to or read
            from, and users should therefore not make any assumptions about the
            row key structure that are specific to their use case.

        The ``offset_bytes`` field on a response indicates the approximate
        total storage space used by all rows in the table which precede
        ``row_key``. Buffering the contents of all rows between two subsequent
        samples would require space roughly equal to the difference in their
        ``offset_bytes`` fields.

        :rtype: :class:`~google.cloud.exceptions.GrpcRendezvous`
        :returns: A cancel-able iterator. Can be consumed by calling ``next()``
                  or by casting to a :class:`list` and can be cancelled by
                  calling ``cancel()``.
        """
        data_client = self._instance._client.table_data_client
        response_iterator = data_client.sample_row_keys(
            self.name, app_profile_id=self._app_profile_id
        )

        return response_iterator

    def truncate(self, timeout=None):
        """Truncate the table

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_truncate_table]
            :end-before: [END bigtable_truncate_table]

        :type timeout: float
        :param timeout: (Optional) The amount of time, in seconds, to wait
                        for the request to complete.

        :raise: google.api_core.exceptions.GoogleAPICallError: If the
                request failed for any reason.
                google.api_core.exceptions.RetryError: If the request failed
                due to a retryable error and retry attempts failed.
                ValueError: If the parameters are invalid.
        """
        client = self._instance._client
        table_admin_client = client.table_admin_client
        if timeout:
            table_admin_client.drop_row_range(
                self.name, delete_all_data_from_table=True, timeout=timeout
            )
        else:
            table_admin_client.drop_row_range(
                self.name, delete_all_data_from_table=True
            )

    def drop_by_prefix(self, row_key_prefix, timeout=None):
        """

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_drop_by_prefix]
            :end-before: [END bigtable_drop_by_prefix]

        :type row_prefix: bytes
        :param row_prefix: Delete all rows that start with this row key
                            prefix. Prefix cannot be zero length.

        :type timeout: float
        :param timeout: (Optional) The amount of time, in seconds, to wait
                        for the request to complete.

        :raise: google.api_core.exceptions.GoogleAPICallError: If the
                request failed for any reason.
                google.api_core.exceptions.RetryError: If the request failed
                due to a retryable error and retry attempts failed.
                ValueError: If the parameters are invalid.
        """
        client = self._instance._client
        table_admin_client = client.table_admin_client
        if timeout:
            table_admin_client.drop_row_range(
                self.name, row_key_prefix=_to_bytes(row_key_prefix), timeout=timeout
            )
        else:
            table_admin_client.drop_row_range(
                self.name, row_key_prefix=_to_bytes(row_key_prefix)
            )

    def mutations_batcher(self, flush_count=FLUSH_COUNT, max_row_bytes=MAX_ROW_BYTES):
        """Factory to create a mutation batcher associated with this instance.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_mutations_batcher]
            :end-before: [END bigtable_mutations_batcher]

        :type table: class
        :param table: class:`~google.cloud.bigtable.table.Table`.

        :type flush_count: int
        :param flush_count: (Optional) Maximum number of rows per batch. If it
                reaches the max number of rows it calls finish_batch() to
                mutate the current row batch. Default is FLUSH_COUNT (1000
                rows).

        :type max_row_bytes: int
        :param max_row_bytes: (Optional) Max number of row mutations size to
                flush. If it reaches the max number of row mutations size it
                calls finish_batch() to mutate the current row batch.
                Default is MAX_ROW_BYTES (5 MB).
        """
        return MutationsBatcher(self, flush_count, max_row_bytes)


class _RetryableMutateRowsWorker(object):
    """A callable worker that can retry to mutate rows with transient errors.

    This class is a callable that can retry mutating rows that result in
    transient errors. After all rows are successful or none of the rows
    are retryable, any subsequent call on this callable will be a no-op.
    """

    # pylint: disable=unsubscriptable-object
    RETRY_CODES = (
        StatusCode.DEADLINE_EXCEEDED.value[0],
        StatusCode.ABORTED.value[0],
        StatusCode.UNAVAILABLE.value[0],
    )
    # pylint: enable=unsubscriptable-object

    def __init__(self, client, table_name, rows, app_profile_id=None, timeout=None):
        self.client = client
        self.table_name = table_name
        self.rows = rows
        self.app_profile_id = app_profile_id
        self.responses_statuses = [None] * len(self.rows)
        self.timeout = timeout

    def __call__(self, retry=DEFAULT_RETRY):
        """Attempt to mutate all rows and retry rows with transient errors.

        Will retry the rows with transient errors until all rows succeed or
        ``deadline`` specified in the `retry` is reached.

        :rtype: list
        :returns: A list of response statuses (`google.rpc.status_pb2.Status`)
                  corresponding to success or failure of each row mutation
                  sent. These will be in the same order as the ``rows``.
        """
        mutate_rows = self._do_mutate_retryable_rows
        if retry:
            mutate_rows = retry(self._do_mutate_retryable_rows)

        try:
            mutate_rows()
        except (_BigtableRetryableError, RetryError):
            # - _BigtableRetryableError raised when no retry strategy is used
            #   and a retryable error on a mutation occurred.
            # - RetryError raised when retry deadline is reached.
            # In both cases, just return current `responses_statuses`.
            pass

        return self.responses_statuses

    @staticmethod
    def _is_retryable(status):
        return status is None or status.code in _RetryableMutateRowsWorker.RETRY_CODES

    def _do_mutate_retryable_rows(self):
        """Mutate all the rows that are eligible for retry.

        A row is eligible for retry if it has not been tried or if it resulted
        in a transient error in a previous call.

        :rtype: list
        :return: The responses statuses, which is a list of
                 :class:`~google.rpc.status_pb2.Status`.
        :raises: One of the following:

                 * :exc:`~.table._BigtableRetryableError` if any
                   row returned a transient error.
                 * :exc:`RuntimeError` if the number of responses doesn't
                   match the number of rows that were retried
        """
        retryable_rows = []
        index_into_all_rows = []
        for index, status in enumerate(self.responses_statuses):
            if self._is_retryable(status):
                retryable_rows.append(self.rows[index])
                index_into_all_rows.append(index)

        if not retryable_rows:
            # All mutations are either successful or non-retryable now.
            return self.responses_statuses

        mutate_rows_request = _mutate_rows_request(
            self.table_name, retryable_rows, app_profile_id=self.app_profile_id
        )
        data_client = self.client.table_data_client
        inner_api_calls = data_client._inner_api_calls
        if "mutate_rows" not in inner_api_calls:
            default_retry = (data_client._method_configs["MutateRows"].retry,)
            if self.timeout is None:
                default_timeout = data_client._method_configs["MutateRows"].timeout
            else:
                default_timeout = timeout.ExponentialTimeout(deadline=self.timeout)
            data_client._inner_api_calls["mutate_rows"] = wrap_method(
                data_client.transport.mutate_rows,
                default_retry=default_retry,
                default_timeout=default_timeout,
                client_info=data_client._client_info,
            )

        responses = data_client._inner_api_calls["mutate_rows"](
            mutate_rows_request, retry=None
        )

        num_responses = 0
        num_retryable_responses = 0
        for response in responses:
            for entry in response.entries:
                num_responses += 1
                index = index_into_all_rows[entry.index]
                self.responses_statuses[index] = entry.status
                if self._is_retryable(entry.status):
                    num_retryable_responses += 1
                if entry.status.code == 0:
                    self.rows[index].clear()

        if len(retryable_rows) != num_responses:
            raise RuntimeError(
                "Unexpected number of responses",
                num_responses,
                "Expected",
                len(retryable_rows),
            )

        if num_retryable_responses:
            raise _BigtableRetryableError

        return self.responses_statuses


class ClusterState(object):
    """Representation of a Cluster State.

    :type replication_state: int
    :param replication_state: enum value for cluster state
        Possible replications_state values are
        0 for STATE_NOT_KNOWN: The replication state of the table is
        unknown in this cluster.
        1 for INITIALIZING: The cluster was recently created, and the
        table must finish copying
        over pre-existing data from other clusters before it can
        begin receiving live replication updates and serving
        ``Data API`` requests.
        2 for PLANNED_MAINTENANCE: The table is temporarily unable to
        serve
        ``Data API`` requests from this
        cluster due to planned internal maintenance.
        3 for UNPLANNED_MAINTENANCE: The table is temporarily unable
        to serve
        ``Data API`` requests from this
        cluster due to unplanned or emergency maintenance.
        4 for READY: The table can serve
        ``Data API`` requests from this
        cluster. Depending on replication delay, reads may not
        immediately reflect the state of the table in other clusters.
    """

    def __init__(self, replication_state):
        self.replication_state = replication_state

    def __repr__(self):
        """Representation of  cluster state instance as string value
        for cluster state.

        :rtype: ClusterState instance
        :returns: ClusterState instance as representation of string
                  value for cluster state.
        """
        replication_dict = {
            enums.Table.ReplicationState.STATE_NOT_KNOWN: "STATE_NOT_KNOWN",
            enums.Table.ReplicationState.INITIALIZING: "INITIALIZING",
            enums.Table.ReplicationState.PLANNED_MAINTENANCE: "PLANNED_MAINTENANCE",
            enums.Table.ReplicationState.UNPLANNED_MAINTENANCE: "UNPLANNED_MAINTENANCE",
            enums.Table.ReplicationState.READY: "READY",
        }
        return replication_dict[self.replication_state]

    def __eq__(self, other):
        """Checks if two ClusterState instances(self and other) are
        equal on the basis of instance variable 'replication_state'.

        :type other: ClusterState
        :param other: ClusterState instance to compare with.

        :rtype: Boolean value
        :returns: True if  two cluster state instances have same
                  replication_state.
        """
        if not isinstance(other, self.__class__):
            return False
        return self.replication_state == other.replication_state

    def __ne__(self, other):
        """Checks if two ClusterState instances(self and other) are
        not equal.

        :type other: ClusterState.
        :param other: ClusterState instance to compare with.

        :rtype: Boolean value.
        :returns: True if  two cluster state instances are not equal.
        """
        return not self == other


def _create_row_request(
    table_name,
    start_key=None,
    end_key=None,
    filter_=None,
    limit=None,
    end_inclusive=False,
    app_profile_id=None,
    row_set=None,
):
    """Creates a request to read rows in a table.

    :type table_name: str
    :param table_name: The name of the table to read from.

    :type start_key: bytes
    :param start_key: (Optional) The beginning of a range of row keys to
                      read from. The range will include ``start_key``. If
                      left empty, will be interpreted as the empty string.

    :type end_key: bytes
    :param end_key: (Optional) The end of a range of row keys to read from.
                    The range will not include ``end_key``. If left empty,
                    will be interpreted as an infinite string.

    :type filter_: :class:`.RowFilter`
    :param filter_: (Optional) The filter to apply to the contents of the
                    specified row(s). If unset, reads the entire table.

    :type limit: int
    :param limit: (Optional) The read will terminate after committing to N
                  rows' worth of results. The default (zero) is to return
                  all results.

    :type end_inclusive: bool
    :param end_inclusive: (Optional) Whether the ``end_key`` should be
                  considered inclusive. The default is False (exclusive).

    :type: app_profile_id: str
    :param app_profile_id: (Optional) The unique name of the AppProfile.

    :type row_set: :class:`row_set.RowSet`
    :param row_set: (Optional) The row set containing multiple row keys and
                    row_ranges.

    :rtype: :class:`data_messages_v2_pb2.ReadRowsRequest`
    :returns: The ``ReadRowsRequest`` protobuf corresponding to the inputs.
    :raises: :class:`ValueError <exceptions.ValueError>` if both
             ``row_set`` and one of ``start_key`` or ``end_key`` are set
    """
    request_kwargs = {"table_name": table_name}
    if (start_key is not None or end_key is not None) and row_set is not None:
        raise ValueError("Row range and row set cannot be " "set simultaneously")

    if filter_ is not None:
        request_kwargs["filter"] = filter_.to_pb()
    if limit is not None:
        request_kwargs["rows_limit"] = limit
    if app_profile_id is not None:
        request_kwargs["app_profile_id"] = app_profile_id

    message = data_messages_v2_pb2.ReadRowsRequest(**request_kwargs)

    if start_key is not None or end_key is not None:
        row_set = RowSet()
        row_set.add_row_range(RowRange(start_key, end_key, end_inclusive=end_inclusive))

    if row_set is not None:
        row_set._update_message_request(message)

    return message


def _mutate_rows_request(table_name, rows, app_profile_id=None):
    """Creates a request to mutate rows in a table.

    :type table_name: str
    :param table_name: The name of the table to write to.

    :type rows: list
    :param rows: List or other iterable of :class:`.DirectRow` instances.

    :type: app_profile_id: str
    :param app_profile_id: (Optional) The unique name of the AppProfile.

    :rtype: :class:`data_messages_v2_pb2.MutateRowsRequest`
    :returns: The ``MutateRowsRequest`` protobuf corresponding to the inputs.
    :raises: :exc:`~.table.TooManyMutationsError` if the number of mutations is
             greater than 100,000
    """
    request_pb = data_messages_v2_pb2.MutateRowsRequest(
        table_name=table_name, app_profile_id=app_profile_id
    )
    mutations_count = 0
    for row in rows:
        _check_row_table_name(table_name, row)
        _check_row_type(row)
        mutations = row._get_mutations()
        request_pb.entries.add(row_key=row.row_key, mutations=mutations)
        mutations_count += len(mutations)
    if mutations_count > _MAX_BULK_MUTATIONS:
        raise TooManyMutationsError(
            "Maximum number of mutations is %s" % (_MAX_BULK_MUTATIONS,)
        )
    return request_pb


def _check_row_table_name(table_name, row):
    """Checks that a row belongs to a table.

    :type table_name: str
    :param table_name: The name of the table.

    :type row: :class:`~google.cloud.bigtable.row.Row`
    :param row: An instance of :class:`~google.cloud.bigtable.row.Row`
                subclasses.

    :raises: :exc:`~.table.TableMismatchError` if the row does not belong to
             the table.
    """
    if row.table is not None and row.table.name != table_name:
        raise TableMismatchError(
            "Row %s is a part of %s table. Current table: %s"
            % (row.row_key, row.table.name, table_name)
        )


def _check_row_type(row):
    """Checks that a row is an instance of :class:`.DirectRow`.

    :type row: :class:`~google.cloud.bigtable.row.Row`
    :param row: An instance of :class:`~google.cloud.bigtable.row.Row`
                subclasses.

    :raises: :class:`TypeError <exceptions.TypeError>` if the row is not an
             instance of DirectRow.
    """
    if not isinstance(row, DirectRow):
        raise TypeError(
            "Bulk processing can not be applied for " "conditional or append mutations."
        )
