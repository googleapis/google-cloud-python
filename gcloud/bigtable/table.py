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


from gcloud.bigtable._generated import (
    bigtable_table_service_messages_pb2 as messages_pb2)
from gcloud.bigtable._generated import (
    bigtable_service_messages_pb2 as data_messages_pb2)
from gcloud.bigtable.column_family import _gc_rule_from_pb
from gcloud.bigtable.column_family import ColumnFamily
from gcloud.bigtable.row import Row


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

    :type cluster: :class:`.cluster.Cluster`
    :param cluster: The cluster that owns the table.
    """

    def __init__(self, table_id, cluster):
        self.table_id = table_id
        self._cluster = cluster

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
        return self._cluster.name + '/tables/' + self.table_id

    def column_family(self, column_family_id, gc_rule=None):
        """Factory to create a column family associated with this table.

        :type column_family_id: str
        :param column_family_id: The ID of the column family. Must be of the
                                 form ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.

        :type gc_rule: :class:`.column_family.GarbageCollectionRule`
        :param gc_rule: (Optional) The garbage collection settings for this
                        column family.

        :rtype: :class:`.column_family.ColumnFamily`
        :returns: A column family owned by this table.
        """
        return ColumnFamily(column_family_id, self, gc_rule=gc_rule)

    def row(self, row_key, filter_=None):
        """Factory to create a row associated with this table.

        :type row_key: bytes
        :param row_key: The key for the row being created.

        :type filter_: :class:`.RowFilter`
        :param filter_: (Optional) Filter to be used for conditional mutations.
                        See :class:`.Row` for more details.

        :rtype: :class:`.Row`
        :returns: A row owned by this table.
        """
        return Row(row_key, self, filter_=filter_)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.table_id == self.table_id and
                other._cluster == self._cluster)

    def __ne__(self, other):
        return not self.__eq__(other)

    def create(self, initial_split_keys=None):
        """Creates this table.

        .. note::

            Though a :class:`._generated.bigtable_table_data_pb2.Table` is also
            allowed (as the ``table`` property) in a create table request, we
            do not support it in this method. As mentioned in the
            :class:`Table` docstring, the name is the only useful property in
            the table proto.

        .. note::

            A create request returns a
            :class:`._generated.bigtable_table_data_pb2.Table` but we don't use
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
        request_pb = messages_pb2.CreateTableRequest(
            initial_split_keys=initial_split_keys or [],
            name=self._cluster.name,
            table_id=self.table_id,
        )
        client = self._cluster._client
        # We expect a `._generated.bigtable_table_data_pb2.Table`
        client._table_stub.CreateTable(request_pb, client.timeout_seconds)

    def rename(self, new_table_id):
        """Rename this table.

        .. note::

            This cannot be used to move tables between clusters,
            zones, or projects.

        .. note::

            The Bigtable Table Admin API currently (``v1``) returns

                ``BigtableTableService.RenameTable is not yet implemented``

            when this method is used. It's unclear when this method will
            actually be supported by the API.

        :type new_table_id: str
        :param new_table_id: The new name table ID.
        """
        request_pb = messages_pb2.RenameTableRequest(
            name=self.name,
            new_id=new_table_id,
        )
        client = self._cluster._client
        # We expect a `google.protobuf.empty_pb2.Empty`
        client._table_stub.RenameTable(request_pb, client.timeout_seconds)

        self.table_id = new_table_id

    def delete(self):
        """Delete this table."""
        request_pb = messages_pb2.DeleteTableRequest(name=self.name)
        client = self._cluster._client
        # We expect a `google.protobuf.empty_pb2.Empty`
        client._table_stub.DeleteTable(request_pb, client.timeout_seconds)

    def list_column_families(self):
        """List the column families owned by this table.

        :rtype: dict
        :returns: Dictionary of column families attached to this table. Keys
                  are strings (column family names) and values are
                  :class:`.column_family.ColumnFamily` instances.
        :raises: :class:`ValueError <exceptions.ValueError>` if the column
                 family name from the response does not agree with the computed
                 name from the column family ID.
        """
        request_pb = messages_pb2.GetTableRequest(name=self.name)
        client = self._cluster._client
        # We expect a `._generated.bigtable_table_data_pb2.Table`
        table_pb = client._table_stub.GetTable(request_pb,
                                               client.timeout_seconds)

        result = {}
        for column_family_id, value_pb in table_pb.column_families.items():
            gc_rule = _gc_rule_from_pb(value_pb.gc_rule)
            column_family = self.column_family(column_family_id,
                                               gc_rule=gc_rule)
            if column_family.name != value_pb.name:
                raise ValueError('Column family name %s does not agree with '
                                 'name from request: %s.' % (
                                     column_family.name, value_pb.name))
            result[column_family_id] = column_family
        return result

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
        request_pb = data_messages_pb2.SampleRowKeysRequest(
            table_name=self.name)
        client = self._cluster._client
        response_iterator = client._data_stub.SampleRowKeys(
            request_pb, client.timeout_seconds)
        return response_iterator
