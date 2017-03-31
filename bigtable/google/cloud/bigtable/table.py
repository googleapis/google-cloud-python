# Copyright 2015 Google Inc.
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

"""User friendly container for Google Cloud Bigtable Table."""
from __future__ import absolute_import, division

import six

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
from google.gax import RetryOptions, BackoffSettings

class IteratorToCallable(object):

    def __init__(self, iterator):
        self.iterator = iterator

    def next(self):
        return self.__call__()

    def __next__(self):
        return self.__call__()

    def __iter__(self):
        return self

    def __call__(self, *args, **kwargs):
        return six.next(self.iterator)


class CallableToIterator(object):

    def __init__(self, c):
        self.c = c

    def next(self, *args, **kwargs):
        return self.__call__(*args, **kwargs)

    def __next__(self, *args, **kwargs):
        return self.__call__(*args, **kwargs)

    def __iter__(self):
        return self

    def __call__(self, *args, **kwargs):
        return self.c(*args, **kwargs)

class ResponseIterator(object):
    def __init__(self, request_pb, client):
        self.client = client
        self.request_pb = request_pb
        self.stream = client._data_stub.ReadRows(request_pb)

    def next(self, *args, **kwargs):
        self.__call__(*args, **kwargs)

    def __next__(self, *args, **kwargs):
        return self.next(*args, **kwargs)

    def __iter__(self):
        return self

    def __call__(self, *args, **kwargs):
        print ">>>>>>>>>>>>>>>>"
        try:
            out = six.next(self.stream)
            print out
            return out
        except Exception as e:
            print e
            self.stream = self.client._data_stub.ReadRows(self.request_pb)
            raise e


DEADLINE_EXCEEDED = 4
ABORTED = 10
INTERNAL = 13
UNAVAILABLE = 14

BACKOFF_SETTINGS = BackoffSettings(
    initial_retry_delay_millis = 10,
    retry_delay_multiplier = 2,
    max_retry_delay_millis = 500,
    initial_rpc_timeout_millis = 10,
    rpc_timeout_multiplier = 2,
    max_rpc_timeout_millis = 1000,
    total_timeout_millis = 500
)

RETRY_OPTIONS = RetryOptions(
    retry_codes = range(100),
    backoff_settings = BACKOFF_SETTINGS
)

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
           :class:`Row`.

        :type row_key: bytes
        :param row_key: The key for the row being created.

        :type filter_: :class:`.RowFilter`
        :param filter_: (Optional) Filter to be used for conditional mutations.
                        See :class:`.DirectRow` for more details.

        :type append: bool
        :param append: (Optional) Flag to determine if the row should be used
                       for append mutations.

        :rtype: :class:`.DirectRow`
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
            return False
        return (other.table_id == self.table_id and
                other._instance == self._instance)

    def __ne__(self, other):
        return not self.__eq__(other)

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
                table_pb.column_families[curr_id].MergeFrom(col_fam.to_pb())

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
                  filter_=None):
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

        :rtype: :class:`.PartialRowsData`
        :returns: A :class:`.PartialRowsData` convenience wrapper for consuming
                  the streamed results.
        """
        print "???????????????????????????????"

        request_pb = _create_row_request(
            self.name, start_key=start_key, end_key=end_key, filter_=filter_,
            limit=limit)
        client = self._instance._client
        response_iterator = ResponseIterator(request_pb, client)
        retryable_iterator = CallableToIterator(
            retryable(
                response_iterator, RETRY_OPTIONS)) 
        # We expect an iterator of `data_messages_v2_pb2.ReadRowsResponse`
        return PartialRowsData(retryable_iterator)

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


def _create_row_request(table_name, row_key=None, start_key=None, end_key=None,
                        filter_=None, limit=None):
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
            range_kwargs['end_key_open'] = _to_bytes(end_key)
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

"""Provides function wrappers that implement retrying."""
import random
import time

from google.gax import config, errors

_MILLIS_PER_SECOND = 1000


def _has_timeout_settings(backoff_settings):
    return (backoff_settings.rpc_timeout_multiplier is not None and
            backoff_settings.max_rpc_timeout_millis is not None and
            backoff_settings.total_timeout_millis is not None and
            backoff_settings.initial_rpc_timeout_millis is not None)


def add_timeout_arg(a_func, timeout, **kwargs):
    """Updates a_func so that it gets called with the timeout as its final arg.
    This converts a callable, a_func, into another callable with an additional
    positional arg.
    Args:
      a_func (callable): a callable to be updated
      timeout (int): to be added to the original callable as it final positional
        arg.
    Returns:
      callable: the original callable updated to the timeout arg
    """

    def inner(*args):
        """Updates args with the timeout."""
        updated_args = args + (timeout,)
        return a_func(*updated_args, **kwargs)

    return inner


def retryable(a_func, retry_options, **kwargs):
    """Creates a function equivalent to a_func, but that retries on certain
    exceptions.
    Args:
      a_func (callable): A callable.
      retry_options (RetryOptions): Configures the exceptions upon which the
        callable should retry, and the parameters to the exponential backoff
        retry algorithm.
    Returns:
      A function that will retry on exception.
    """
    delay_mult = retry_options.backoff_settings.retry_delay_multiplier
    max_delay_millis = retry_options.backoff_settings.max_retry_delay_millis
    has_timeout_settings = _has_timeout_settings(retry_options.backoff_settings)

    if has_timeout_settings:
        timeout_mult = retry_options.backoff_settings.rpc_timeout_multiplier
        max_timeout = (retry_options.backoff_settings.max_rpc_timeout_millis /
                       _MILLIS_PER_SECOND)
        total_timeout = (retry_options.backoff_settings.total_timeout_millis /
                         _MILLIS_PER_SECOND)

    def inner(*args):
        """Equivalent to ``a_func``, but retries upon transient failure.
        Retrying is done through an exponential backoff algorithm configured
        by the options in ``retry``.
        """
        delay = retry_options.backoff_settings.initial_retry_delay_millis
        exc = errors.RetryError('Retry total timeout exceeded before any'
                                'response was received')
        if has_timeout_settings:
            timeout = (
                retry_options.backoff_settings.initial_rpc_timeout_millis /
                _MILLIS_PER_SECOND)

            now = time.time()
            deadline = now + total_timeout
        else:
            timeout = None
            deadline = None
        while deadline is None or now < deadline:
            try:
                to_call = add_timeout_arg(a_func, timeout, **kwargs)
                return to_call(*args)
            except Exception as exception:  # pylint: disable=broad-except
                code = config.exc_to_code(exception)
                if "UNAVAILABLE" not in str(exception):
                    raise errors.RetryError(
                        'Exception occurred in retry method that was not'
                        ' classified as transient', exception)

                # pylint: disable=redefined-variable-type
                exc = errors.RetryError(
                    'Retry total timeout exceeded with exception', exception)

                # Sleep a random number which will, on average, equal the
                # expected delay.
                to_sleep = random.uniform(0, delay * 2)
                time.sleep(to_sleep / _MILLIS_PER_SECOND)
                delay = min(delay * delay_mult, max_delay_millis)

                if has_timeout_settings:
                    now = time.time()
                    timeout = min(
                        timeout * timeout_mult, max_timeout, deadline - now)

        raise exc

    return inner

