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


import six

from google.api_core.exceptions import RetryError
from google.api_core.exceptions import Aborted
from google.api_core.exceptions import DeadlineExceeded
from google.api_core.exceptions import ServiceUnavailable
from google.api_core.exceptions import from_grpc_status
from google.api_core.retry import Retry
from google.api_core.retry import if_exception_type
from google.cloud._helpers import _to_bytes
from google.cloud.bigtable._generated import (
    bigtable_pb2 as data_messages_v2_pb2)
from google.cloud.bigtable._generated import (
    bigtable_table_admin_pb2 as table_admin_messages_v2_pb2)
from google.cloud.bigtable._generated import (
    table_pb2 as table_v2_pb2)
from google.cloud.bigtable.column_family import _gc_rule_from_pb
from google.cloud.bigtable.column_family import ColumnFamily
from google.cloud.bigtable.row import AppendRow
from google.cloud.bigtable.row import ConditionalRow
from google.cloud.bigtable.row import DirectRow
from google.cloud.bigtable.row_data import PartialRowsData
from grpc import StatusCode


# Maximum number of mutations in bulk (MutateRowsRequest message):
# https://cloud.google.com/bigtable/docs/reference/data/rpc/google.bigtable.v2#google.bigtable.v2.MutateRowRequest
_MAX_BULK_MUTATIONS = 100000

DEFAULT_RETRY = Retry(
        predicate=if_exception_type((Aborted,
                                     DeadlineExceeded,
                                     ServiceUnavailable)),
        initial=1.0,
        maximum=15.0,
        multiplier=2.0,
        deadline=60.0 * 2.0)


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
    * :meth:`rename` the table
    * :meth:`delete` the table
    * :meth:`list_column_families` in the table

    :type table_id: str
    :param table_id: The ID of the table.

    :type instance: :class:`~google.cloud.bigtable.instance.Instance`
    :param instance: The instance that owns the table.
    """

    def __init__(self, table_id, instance):
        self.table_id = table_id
        self._instance = instance

    @property
    def name(self):
        """Table name used in requests.

        .. note::

          This property will not change if ``table_id`` does not, but the
          return value is not cached.

        The table name is of the form

            ``"projects/../instances/../tables/{table_id}"``

        :rtype: str
        :returns: The table name.
        """
        return self._instance.name + '/tables/' + self.table_id

    def column_family(self, column_family_id, gc_rule=None):
        """Factory to create a column family associated with this table.

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

        .. warning::

           At most one of ``filter_`` and ``append`` can be used in a
           :class:`.Row`.

        :type row_key: bytes
        :param row_key: The key for the row being created.

        :type filter_: :class:`.RowFilter`
        :param filter_: (Optional) Filter to be used for conditional mutations.
                        See :class:`.ConditionalRow` for more details.

        :type append: bool
        :param append: (Optional) Flag to determine if the row should be used
                       for append mutations.

        :rtype: :class:`.Row`
        :returns: A row owned by this table.
        :raises: :class:`ValueError <exceptions.ValueError>` if both
                 ``filter_`` and ``append`` are used.
        """
        if append and filter_ is not None:
            raise ValueError('At most one of filter_ and append can be set')
        if append:
            return AppendRow(row_key, self)
        elif filter_ is not None:
            return ConditionalRow(row_key, self, filter_=filter_)
        else:
            return DirectRow(row_key, self)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (other.table_id == self.table_id and
                other._instance == self._instance)

    def __ne__(self, other):
        return not self == other

    def create(self, initial_split_keys=None, column_families=()):
        """Creates this table.

        .. note::

            A create request returns a
            :class:`._generated.table_pb2.Table` but we don't use
            this response.

        :type initial_split_keys: list
        :param initial_split_keys: (Optional) List of row keys that will be
                                   used to initially split the table into
                                   several tablets (Tablets are similar to
                                   HBase regions). Given two split keys,
                                   ``"s1"`` and ``"s2"``, three tablets will be
                                   created, spanning the key ranges:
                                   ``[, s1)``, ``[s1, s2)``, ``[s2, )``.

        :type column_families: list
        :param column_families: (Optional) List or other iterable of
                                :class:`.ColumnFamily` instances.
        """
        if initial_split_keys is not None:
            split_pb = table_admin_messages_v2_pb2.CreateTableRequest.Split
            initial_split_keys = [
                split_pb(key=key) for key in initial_split_keys]

        table_pb = None
        if column_families:
            table_pb = table_v2_pb2.Table()
            for col_fam in column_families:
                curr_id = col_fam.column_family_id
                table_pb.column_families[curr_id].CopyFrom(col_fam.to_pb())

        request_pb = table_admin_messages_v2_pb2.CreateTableRequest(
            initial_splits=initial_split_keys or [],
            parent=self._instance.name,
            table_id=self.table_id,
            table=table_pb,
        )
        client = self._instance._client
        # We expect a `._generated.table_pb2.Table`
        client._table_stub.CreateTable(request_pb)

    def delete(self):
        """Delete this table."""
        request_pb = table_admin_messages_v2_pb2.DeleteTableRequest(
            name=self.name)
        client = self._instance._client
        # We expect a `google.protobuf.empty_pb2.Empty`
        client._table_stub.DeleteTable(request_pb)

    def list_column_families(self):
        """List the column families owned by this table.

        :rtype: dict
        :returns: Dictionary of column families attached to this table. Keys
                  are strings (column family names) and values are
                  :class:`.ColumnFamily` instances.
        :raises: :class:`ValueError <exceptions.ValueError>` if the column
                 family name from the response does not agree with the computed
                 name from the column family ID.
        """
        request_pb = table_admin_messages_v2_pb2.GetTableRequest(
            name=self.name)
        client = self._instance._client
        # We expect a `._generated.table_pb2.Table`
        table_pb = client._table_stub.GetTable(request_pb)

        result = {}
        for column_family_id, value_pb in table_pb.column_families.items():
            gc_rule = _gc_rule_from_pb(value_pb.gc_rule)
            column_family = self.column_family(column_family_id,
                                               gc_rule=gc_rule)
            result[column_family_id] = column_family
        return result

    def read_row(self, row_key, filter_=None):
        """Read a single row from this table.

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
        request_pb = _create_row_request(self.name, row_key=row_key,
                                         filter_=filter_)
        client = self._instance._client
        response_iterator = client._data_stub.ReadRows(request_pb)
        rows_data = PartialRowsData(response_iterator)
        rows_data.consume_all()
        if rows_data.state not in (rows_data.NEW_ROW, rows_data.START):
            raise ValueError('The row remains partial / is not committed.')

        if len(rows_data.rows) == 0:
            return None

        return rows_data.rows[row_key]

    def read_rows(self, start_key=None, end_key=None, limit=None,
                  filter_=None, end_inclusive=False):
        """Read rows from this table.

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

        :rtype: :class:`.PartialRowsData`
        :returns: A :class:`.PartialRowsData` convenience wrapper for consuming
                  the streamed results.
        """
        request_pb = _create_row_request(
            self.name, start_key=start_key, end_key=end_key, filter_=filter_,
            limit=limit, end_inclusive=end_inclusive)
        client = self._instance._client
        response_iterator = client._data_stub.ReadRows(request_pb)
        # We expect an iterator of `data_messages_v2_pb2.ReadRowsResponse`
        return PartialRowsData(response_iterator)

    def mutate_rows(self, rows, retry=DEFAULT_RETRY):
        """Mutates multiple rows in bulk.

        The method tries to update all specified rows.
        If some of the rows weren't updated, it would not remove mutations.
        They can be applied to the row separately.
        If row mutations finished successfully, they would be cleaned up.
        Optionally specify a `retry` to re-attempt rows that return transient
        errors, until all rows succeed or the deadline is reached.

        :type rows: list
        :param rows: List or other iterable of :class:`.DirectRow` instances.

        :type retry: :class:`~google.api_core.retry.Retry`
        :param retry: (Optional) Retry delay and deadline arguments. Can be
                      specified using ``DEFAULT_RETRY.with_delay`` and/or
                      ``DEFAULT_RETRY.with_deadline``.

        :rtype: list
        :returns: A list of response statuses (`google.rpc.status_pb2.Status`)
                  corresponding to success or failure of each row mutation
                  sent. These will be in the same order as the `rows`.
        """
        retryable_mutate_rows = _RetryableMutateRowsWorker(
            self._instance._client, self.name, rows)
        return retryable_mutate_rows(retry=retry)

    def sample_row_keys(self):
        """Read a sample of row keys in the table.

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
        request_pb = data_messages_v2_pb2.SampleRowKeysRequest(
            table_name=self.name)
        client = self._instance._client
        response_iterator = client._data_stub.SampleRowKeys(request_pb)
        return response_iterator


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

    def __init__(self, client, table_name, rows):
        self.client = client
        self.table_name = table_name
        self.rows = rows
        self.responses_statuses = [
            None for _ in six.moves.xrange(len(self.rows))]

    def __call__(self, retry=DEFAULT_RETRY):
        """Attempt to mutate all rows and retry rows with transient errors.

        Will retry the rows with transient errors until all rows succeed or
        ``deadline`` specified in the `retry` is reached.

        :rtype: list
        :returns: A list of response statuses (`google.rpc.status_pb2.Status`)
                  corresponding to success or failure of each row mutation
                  sent. These will be in the same order as the ``rows``.
        """
        try:
            retry(self.__class__._do_mutate_retryable_rows)(self)
        except (RetryError, ValueError) as err:
            # Upon timeout or sleep generator error, return responses_statuses
            pass
        return self.responses_statuses

    def _is_retryable(self, status):  # pylint: disable=no-self-use
        return (status is None or
                status.code in _RetryableMutateRowsWorker.RETRY_CODES)

    def _do_mutate_retryable_rows(self):
        """Mutate all the rows that are eligible for retry.

        A row is eligible for retry if it has not been tried or if it resulted
        in a transient error in a previous call.

        :rtype: list
        :return: ``responses_statuses`` (`google.rpc.status_pb2.Status`)
        :raises: :exc:`~google.api_core.exceptions.ServiceUnavailable` if any
                 row returned a transient error. An artificial exception
                 to work with ``DEFAULT_RETRY``.
        """
        retryable_rows = []
        index_into_all_rows = []
        for i, status in enumerate(self.responses_statuses):
            if self._is_retryable(status):
                retryable_rows.append(self.rows[i])
                index_into_all_rows.append(i)

        if not retryable_rows:
            # All mutations are either successful or non-retryable now.
            return self.responses_statuses

        mutate_rows_request = _mutate_rows_request(
            self.table_name, retryable_rows)
        responses = self.client._data_stub.MutateRows(
            mutate_rows_request)

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

        assert len(retryable_rows) == num_responses

        if num_retryable_responses:
            raise from_grpc_status(StatusCode.UNAVAILABLE,
                                   'MutateRows retryable error.')
        return self.responses_statuses


def _create_row_request(table_name, row_key=None, start_key=None, end_key=None,
                        filter_=None, limit=None, end_inclusive=False):
    """Creates a request to read rows in a table.

    :type table_name: str
    :param table_name: The name of the table to read from.

    :type row_key: bytes
    :param row_key: (Optional) The key of a specific row to read from.

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

    :rtype: :class:`data_messages_v2_pb2.ReadRowsRequest`
    :returns: The ``ReadRowsRequest`` protobuf corresponding to the inputs.
    :raises: :class:`ValueError <exceptions.ValueError>` if both
             ``row_key`` and one of ``start_key`` and ``end_key`` are set
    """
    request_kwargs = {'table_name': table_name}
    if (row_key is not None and
            (start_key is not None or end_key is not None)):
        raise ValueError('Row key and row range cannot be '
                         'set simultaneously')
    range_kwargs = {}
    if start_key is not None or end_key is not None:
        if start_key is not None:
            range_kwargs['start_key_closed'] = _to_bytes(start_key)
        if end_key is not None:
            end_key_key = 'end_key_open'
            if end_inclusive:
                end_key_key = 'end_key_closed'
            range_kwargs[end_key_key] = _to_bytes(end_key)
    if filter_ is not None:
        request_kwargs['filter'] = filter_.to_pb()
    if limit is not None:
        request_kwargs['rows_limit'] = limit

    message = data_messages_v2_pb2.ReadRowsRequest(**request_kwargs)

    if row_key is not None:
        message.rows.row_keys.append(_to_bytes(row_key))

    if range_kwargs:
        message.rows.row_ranges.add(**range_kwargs)

    return message


def _mutate_rows_request(table_name, rows):
    """Creates a request to mutate rows in a table.

    :type table_name: str
    :param table_name: The name of the table to write to.

    :type rows: list
    :param rows: List or other iterable of :class:`.DirectRow` instances.

    :rtype: :class:`data_messages_v2_pb2.MutateRowsRequest`
    :returns: The ``MutateRowsRequest`` protobuf corresponding to the inputs.
    :raises: :exc:`~.table.TooManyMutationsError` if the number of mutations is
             greater than 100,000
    """
    request_pb = data_messages_v2_pb2.MutateRowsRequest(table_name=table_name)
    mutations_count = 0
    for row in rows:
        _check_row_table_name(table_name, row)
        _check_row_type(row)
        entry = request_pb.entries.add()
        entry.row_key = row.row_key
        # NOTE: Since `_check_row_type` has verified `row` is a `DirectRow`,
        #  the mutations have no state.
        for mutation in row._get_mutations(None):
            mutations_count += 1
            entry.mutations.add().CopyFrom(mutation)
    if mutations_count > _MAX_BULK_MUTATIONS:
        raise TooManyMutationsError('Maximum number of mutations is %s' %
                                    (_MAX_BULK_MUTATIONS,))
    return request_pb


def _check_row_table_name(table_name, row):
    """Checks that a row belongs to a table.

    :type table_name: str
    :param table_name: The name of the table.

    :type row: :class:`.Row`
    :param row: An instance of :class:`.Row` subclasses.

    :raises: :exc:`~.table.TableMismatchError` if the row does not belong to
             the table.
    """
    if row.table.name != table_name:
        raise TableMismatchError(
            'Row %s is a part of %s table. Current table: %s' %
            (row.row_key, row.table.name, table_name))


def _check_row_type(row):
    """Checks that a row is an instance of :class:`.DirectRow`.

    :type row: :class:`.Row`
    :param row: An instance of :class:`.Row` subclasses.

    :raises: :class:`TypeError <exceptions.TypeError>` if the row is not an
             instance of DirectRow.
    """
    if not isinstance(row, DirectRow):
        raise TypeError('Bulk processing can not be applied for '
                        'conditional or append mutations.')
