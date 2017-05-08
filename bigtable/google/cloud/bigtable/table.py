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

from __future__ import absolute_import
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
from google.cloud.bigtable.retry import ReadRowsIterator, _create_row_request
from grpc import StatusCode

BACKOFF_SETTINGS = BackoffSettings(
    initial_retry_delay_millis=10,
    retry_delay_multiplier=1.3,
    max_retry_delay_millis=30000,
    initial_rpc_timeout_millis=25 * 60 * 1000,
    rpc_timeout_multiplier=1.0,
    max_rpc_timeout_millis=25 * 60 * 1000,
    total_timeout_millis=30 * 60 * 1000
)

RETRY_CODES = [
    StatusCode.DEADLINE_EXCEEDED,
    StatusCode.ABORTED,
    StatusCode.INTERNAL,
    StatusCode.UNAVAILABLE
]


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
                  filter_=None, backoff_settings=None):
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
        client = self._instance._client
        if backoff_settings is None:
            backoff_settings = BACKOFF_SETTINGS
        RETRY_OPTIONS = RetryOptions(
            retry_codes=RETRY_CODES,
            backoff_settings=backoff_settings
        )

        retrying_iterator = ReadRowsIterator(client, self.name, start_key,
                                             end_key, filter_, limit,
                                             RETRY_OPTIONS)
        return PartialRowsData(retrying_iterator)

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
