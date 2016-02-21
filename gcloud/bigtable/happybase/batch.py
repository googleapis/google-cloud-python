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

from gcloud._helpers import _datetime_from_microseconds
from gcloud.bigtable.row import TimestampRange


_WAL_SENTINEL = object()
# Assumed granularity of timestamps in Cloud Bigtable.
_ONE_MILLISECOND = datetime.timedelta(microseconds=1000)
_WARN = warnings.warn
_WAL_WARNING = ('The wal argument (Write-Ahead-Log) is not '
                'supported by Cloud Bigtable.')


class Batch(object):
    """Batch class for accumulating mutations.

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
