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

"""Google Cloud Bigtable HappyBase batch module."""


import datetime
import warnings

import six

from gcloud._helpers import _datetime_from_microseconds
from gcloud.bigtable.row_filters import TimestampRange


_WAL_SENTINEL = object()
# Assumed granularity of timestamps in Cloud Bigtable.
_ONE_MILLISECOND = datetime.timedelta(microseconds=1000)
_WARN = warnings.warn
_WAL_WARNING = ('The wal argument (Write-Ahead-Log) is not '
                'supported by Cloud Bigtable.')


class Batch(object):
    """Batch class for accumulating mutations.

    .. note::

       When using a batch with ``transaction=False`` as a context manager
       (i.e. in a ``with`` statement), mutations will still be sent as
       row mutations even if the context manager exits with an error.
       This behavior is in place to match the behavior in the HappyBase
       HBase / Thrift implementation.

    :type table: :class:`Table <gcloud.bigtable.happybase.table.Table>`
    :param table: The table where mutations will be applied.

    :type timestamp: int
    :param timestamp: (Optional) Timestamp (in milliseconds since the epoch)
                      that all mutations will be applied at.

    :type batch_size: int
    :param batch_size: (Optional) The maximum number of mutations to allow
                       to accumulate before committing them.

    :type transaction: bool
    :param transaction: Flag indicating if the mutations should be sent
                        transactionally or not. If ``transaction=True`` and
                        an error occurs while a :class:`Batch` is active,
                        then none of the accumulated mutations will be
                        committed. If ``batch_size`` is set, the mutation
                        can't be transactional.

    :type wal: object
    :param wal: Unused parameter (Boolean for using the HBase Write Ahead Log).
                Provided for compatibility with HappyBase, but irrelevant for
                Cloud Bigtable since it does not have a Write Ahead Log.

    :raises: :class:`TypeError <exceptions.TypeError>` if ``batch_size``
             is set and ``transaction=True``.
             :class:`ValueError <exceptions.ValueError>` if ``batch_size``
             is not positive.
    """

    def __init__(self, table, timestamp=None, batch_size=None,
                 transaction=False, wal=_WAL_SENTINEL):
        if wal is not _WAL_SENTINEL:
            _WARN(_WAL_WARNING)

        if batch_size is not None:
            if transaction:
                raise TypeError('When batch_size is set, a Batch cannot be '
                                'transactional')
            if batch_size <= 0:
                raise ValueError('batch_size must be positive')

        self._table = table
        self._batch_size = batch_size
        self._timestamp = self._delete_range = None

        # Timestamp is in milliseconds, convert to microseconds.
        if timestamp is not None:
            self._timestamp = _datetime_from_microseconds(1000 * timestamp)
            # For deletes, we get the very next timestamp (assuming timestamp
            # granularity is milliseconds). This is because HappyBase users
            # expect HBase deletes to go **up to** and **including** the
            # timestamp while Cloud Bigtable Time Ranges **exclude** the
            # final timestamp.
            next_timestamp = self._timestamp + _ONE_MILLISECOND
            self._delete_range = TimestampRange(end=next_timestamp)

        self._transaction = transaction

        # Internal state for tracking mutations.
        self._row_map = {}
        self._mutation_count = 0

    def send(self):
        """Send / commit the batch of mutations to the server."""
        for row in self._row_map.values():
            # commit() does nothing if row hasn't accumulated any mutations.
            row.commit()

        self._row_map.clear()
        self._mutation_count = 0

    def _try_send(self):
        """Send / commit the batch if mutations have exceeded batch size."""
        if self._batch_size and self._mutation_count >= self._batch_size:
            self.send()

    def _get_row(self, row_key):
        """Gets a row that will hold mutations.

        If the row is not already cached on the current batch, a new row will
        be created.

        :type row_key: str
        :param row_key: The row key for a row stored in the map.

        :rtype: :class:`Row <gcloud.bigtable.row.Row>`
        :returns: The newly created or stored row that will hold mutations.
        """
        if row_key not in self._row_map:
            table = self._table._low_level_table
            self._row_map[row_key] = table.row(row_key)

        return self._row_map[row_key]

    def put(self, row, data, wal=_WAL_SENTINEL):
        """Insert data into a row in the table owned by this batch.

        :type row: str
        :param row: The row key where the mutation will be "put".

        :type data: dict
        :param data: Dictionary containing the data to be inserted. The keys
                     are columns names (of the form ``fam:col``) and the values
                     are strings (bytes) to be stored in those columns.

        :type wal: object
        :param wal: Unused parameter (to over-ride the default on the
                    instance). Provided for compatibility with HappyBase, but
                    irrelevant for Cloud Bigtable since it does not have a
                    Write Ahead Log.
        """
        if wal is not _WAL_SENTINEL:
            _WARN(_WAL_WARNING)

        row_object = self._get_row(row)
        # Make sure all the keys are valid before beginning
        # to add mutations.
        column_pairs = _get_column_pairs(six.iterkeys(data),
                                         require_qualifier=True)
        for column_family_id, column_qualifier in column_pairs:
            value = data[column_family_id + ':' + column_qualifier]
            row_object.set_cell(column_family_id, column_qualifier,
                                value, timestamp=self._timestamp)

        self._mutation_count += len(data)
        self._try_send()

    def _delete_columns(self, columns, row_object):
        """Adds delete mutations for a list of columns and column families.

        :type columns: list
        :param columns: Iterable containing column names (as
                        strings). Each column name can be either

                          * an entire column family: ``fam`` or ``fam:``
                          * a single column: ``fam:col``

        :type row_object: :class:`Row <gcloud_bigtable.row.Row>`
        :param row_object: The row which will hold the delete mutations.

        :raises: :class:`ValueError <exceptions.ValueError>` if the delete
                 timestamp range is set on the current batch, but a
                 column family delete is attempted.
        """
        column_pairs = _get_column_pairs(columns)
        for column_family_id, column_qualifier in column_pairs:
            if column_qualifier is None:
                if self._delete_range is not None:
                    raise ValueError('The Cloud Bigtable API does not support '
                                     'adding a timestamp to '
                                     '"DeleteFromFamily" ')
                row_object.delete_cells(column_family_id,
                                        columns=row_object.ALL_COLUMNS)
            else:
                row_object.delete_cell(column_family_id,
                                       column_qualifier,
                                       time_range=self._delete_range)

    def delete(self, row, columns=None, wal=_WAL_SENTINEL):
        """Delete data from a row in the table owned by this batch.

        :type row: str
        :param row: The row key where the delete will occur.

        :type columns: list
        :param columns: (Optional) Iterable containing column names (as
                        strings). Each column name can be either

                          * an entire column family: ``fam`` or ``fam:``
                          * a single column: ``fam:col``

                        If not used, will delete the entire row.

        :type wal: object
        :param wal: Unused parameter (to over-ride the default on the
                    instance). Provided for compatibility with HappyBase, but
                    irrelevant for Cloud Bigtable since it does not have a
                    Write Ahead Log.

        :raises: If the delete timestamp range is set on the
                 current batch, but a full row delete is attempted.
        """
        if wal is not _WAL_SENTINEL:
            _WARN(_WAL_WARNING)

        row_object = self._get_row(row)

        if columns is None:
            # Delete entire row.
            if self._delete_range is not None:
                raise ValueError('The Cloud Bigtable API does not support '
                                 'adding a timestamp to "DeleteFromRow" '
                                 'mutations')
            row_object.delete()
            self._mutation_count += 1
        else:
            self._delete_columns(columns, row_object)
            self._mutation_count += len(columns)

        self._try_send()

    def __enter__(self):
        """Enter context manager, no set-up required."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit context manager, no set-up required.

        :type exc_type: type
        :param exc_type: The type of the exception if one occurred while the
                         context manager was active. Otherwise, :data:`None`.

        :type exc_value: :class:`Exception <exceptions.Exception>`
        :param exc_value: An instance of ``exc_type`` if an exception occurred
                          while the context was active.
                          Otherwise, :data:`None`.

        :type traceback: ``traceback`` type
        :param traceback: The traceback where the exception occurred (if one
                          did occur). Otherwise, :data:`None`.
        """
        # If the context manager encountered an exception and the batch is
        # transactional, we don't commit the mutations.
        if self._transaction and exc_type is not None:
            return

        # NOTE: For non-transactional batches, this will even commit mutations
        #       if an error occurred during the context manager.
        self.send()


def _get_column_pairs(columns, require_qualifier=False):
    """Turns a list of column or column families into parsed pairs.

    Turns a column family (``fam`` or ``fam:``) into a pair such
    as ``['fam', None]`` and turns a column (``fam:col``) into
    ``['fam', 'col']``.

    :type columns: list
    :param columns: Iterable containing column names (as
                    strings). Each column name can be either

                      * an entire column family: ``fam`` or ``fam:``
                      * a single column: ``fam:col``

    :type require_qualifier: bool
    :param require_qualifier: Boolean indicating if the columns should
                              all have a qualifier or not.

    :rtype: list
    :returns: List of pairs, where the first element in each pair is the
              column family and the second is the column qualifier
              (or :data:`None`).
    :raises: :class:`ValueError <exceptions.ValueError>` if any of the columns
             are not of the expected format.
             :class:`ValueError <exceptions.ValueError>` if
             ``require_qualifier`` is :data:`True` and one of the values is
             for an entire column family
    """
    column_pairs = []
    for column in columns:
        if isinstance(column, six.binary_type):
            column = column.decode('utf-8')
        # Remove trailing colons (i.e. for standalone column family).
        if column.endswith(u':'):
            column = column[:-1]
        num_colons = column.count(u':')
        if num_colons == 0:
            # column is a column family.
            if require_qualifier:
                raise ValueError('column does not contain a qualifier',
                                 column)
            else:
                column_pairs.append([column, None])
        elif num_colons == 1:
            column_pairs.append(column.split(u':'))
        else:
            raise ValueError('Column contains the : separator more than once')

    return column_pairs
