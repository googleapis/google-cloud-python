# Copyright 2015 Google Inc. All rights reserved.
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

from gcloud._helpers import _to_bytes
from gcloud.bigtable._generated_v2 import (
    bigtable_pb2 as data_messages_v2_pb2)
from gcloud.bigtable._generated_v2 import (
    bigtable_table_admin_pb2 as table_admin_messages_v2_pb2)
from gcloud.bigtable.column_family import _gc_rule_from_pb
from gcloud.bigtable.column_family import ColumnFamily
from gcloud.bigtable.row import AppendRow
from gcloud.bigtable.row import ConditionalRow
from gcloud.bigtable.row import DirectRow
from gcloud.bigtable.row_data import PartialRowsData


class Table(object):
    """Representation of a Google Cloud Bigtable Table.

    .. note::

        We don't define any properties on a table other than the name. As
        the proto says, in a request:

          The ``name`` field of the Table and all of its ColumnFamilies must
          be left blank, and will be populated in the response.

        This leaves only the ``current_operation`` and ``granularity``
        fields. The ``current_operation`` is only used for responses while
        ``granularity`` is an enum with only one value.

    We can use a :class:`Table` to:

    * :meth:`create` the table
    * :meth:`rename` the table
    * :meth:`delete` the table
    * :meth:`list_column_families` in the table

    :type table_id: str
    :param table_id: The ID of the table.

    :type instance: :class:`Cluster <.instance.Instance>`
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

            ``"projects/../zones/../clusters/../tables/{table_id}"``

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

    def create(self, initial_split_keys=None):
        """Creates this table.

        .. note::

            Though a :class:`._generated_v2.table_pb2.Table` is also
            allowed (as the ``table`` property) in a create table request, we
            do not support it in this method. As mentioned in the
            :class:`Table` docstring, the name is the only useful property in
            the table proto.

        .. note::

            A create request returns a
            :class:`._generated_v2.table_pb2.Table` but we don't use
            this response. The proto definition allows for the inclusion of a
            ``current_operation`` in the response, but it does not appear that
            the Cloud Bigtable API returns any operation.

        :type initial_split_keys: list
        :param initial_split_keys: (Optional) List of row keys that will be
                                   used to initially split the table into
                                   several tablets (Tablets are similar to
                                   HBase regions). Given two split keys,
                                   ``"s1"`` and ``"s2"``, three tablets will be
                                   created, spanning the key ranges:
                                   ``[, s1)``, ``[s1, s2)``, ``[s2, )``.
        """
        split_pb = table_admin_messages_v2_pb2.CreateTableRequest.Split
        if initial_split_keys is not None:
            initial_split_keys = [
                split_pb(key=key) for key in initial_split_keys]
        request_pb = table_admin_messages_v2_pb2.CreateTableRequest(
            initial_splits=initial_split_keys or [],
            parent=self._instance.name,
            table_id=self.table_id,
        )
        client = self._instance._client
        # We expect a `._generated_v2.table_pb2.Table`
        client._table_stub.CreateTable(request_pb, client.timeout_seconds)

    def delete(self):
        """Delete this table."""
        request_pb = table_admin_messages_v2_pb2.DeleteTableRequest(
            name=self.name)
        client = self._instance._client
        # We expect a `google.protobuf.empty_pb2.Empty`
        client._table_stub.DeleteTable(request_pb, client.timeout_seconds)

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
        # We expect a `._generated_v2.table_pb2.Table`
        table_pb = client._table_stub.GetTable(request_pb,
                                               client.timeout_seconds)

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
        response_iterator = client._data_stub.ReadRows(request_pb,
                                                       client.timeout_seconds)
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
        request_pb = _create_row_request(
            self.name, start_key=start_key, end_key=end_key, filter_=filter_,
            limit=limit)
        client = self._instance._client
        response_iterator = client._data_stub.ReadRows(request_pb,
                                                       client.timeout_seconds)
        # We expect an iterator of `data_messages_v2_pb2.ReadRowsResponse`
        return PartialRowsData(response_iterator)

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

        :rtype: :class:`grpc.framework.alpha._reexport._CancellableIterator`
        :returns: A cancel-able iterator. Can be consumed by calling ``next()``
                  or by casting to a :class:`list` and can be cancelled by
                  calling ``cancel()``.
        """
        request_pb = data_messages_v2_pb2.SampleRowKeysRequest(
            table_name=self.name)
        client = self._instance._client
        response_iterator = client._data_stub.SampleRowKeys(
            request_pb, client.timeout_seconds)
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
