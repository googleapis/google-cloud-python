# Copyright 2018 Google LLC
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

"""User friendly container for Google Cloud Bigtable MutationBatcher."""
import queue
import atexit


from google.cloud.bigtable.data.exceptions import MutationsExceptionGroup
from google.cloud.bigtable.data.mutations import RowMutationEntry


FLUSH_COUNT = 100  # after this many elements, send out the batch

MAX_MUTATION_SIZE = 20 * 1024 * 1024  # 20MB # after this many bytes, send out the batch

MAX_OUTSTANDING_BYTES = 100 * 1024 * 1024  # 100MB # max inflight byte size.

MAX_OUTSTANDING_ELEMENTS = 100000  # max inflight mutations.


class MutationsBatchError(Exception):
    """Error in the batch request"""

    def __init__(self, message, exc):
        self.exc = exc
        self.message = message
        super().__init__(self.message)


class MutationsBatcher(object):
    """A MutationsBatcher is used in batch cases where the number of mutations
    is large or unknown. It will store :class:`DirectRow` in memory until one of the
    size limits is reached, or an explicit call to :func:`flush()` is performed. When
    a flush event occurs, the :class:`DirectRow` in memory will be sent to Cloud
    Bigtable. Batching mutations is more efficient than sending individual
    request.

    This class is not suited for usage in systems where each mutation
    must be guaranteed to be sent, since calling mutate may only result in an
    in-memory change. In a case of a system crash, any :class:`DirectRow` remaining in
    memory will not necessarily be sent to the service, even after the
    completion of the :func:`mutate()` method.

    Note on thread safety: The same :class:`MutationBatcher` cannot be shared by multiple end-user threads.

    :type table: class
    :param table: class:`~google.cloud.bigtable.table.Table`.

    :type flush_count: int
    :param flush_count: (Optional) Max number of rows to flush. If it
        reaches the max number of rows it calls finish_batch() to mutate the
        current row batch. Default is FLUSH_COUNT (1000 rows).

    :type max_row_bytes: int
    :param max_row_bytes: (Optional) Max number of row mutations size to
        flush. If it reaches the max number of row mutations size it calls
        finish_batch() to mutate the current row batch. Default is MAX_ROW_BYTES
        (5 MB).

    :type flush_interval: float
    :param flush_interval: (Optional) The interval (in seconds) between asynchronous flush.
        Default is 1 second.

    :type batch_completed_callback: Callable[list:[`~google.rpc.status_pb2.Status`]] = None
    :param batch_completed_callback: (Optional) A callable for handling responses
        after the current batch is sent. The callable function expect a list of grpc
        Status.
    """

    def __init__(
        self,
        table,
        flush_count=FLUSH_COUNT,
        max_row_bytes=MAX_MUTATION_SIZE,
        flush_interval=1,
        batch_completed_callback=None,
    ):
        self.table = table
        self._batcher_kwargs = {
            "flush_interval": flush_interval,
            "flush_limit_mutation_count": flush_count,
            "flush_limit_bytes": max_row_bytes,
            "flow_control_max_mutation_count": MAX_OUTSTANDING_ELEMENTS,
            "flow_control_max_bytes": MAX_OUTSTANDING_BYTES,
        }
        self._user_batch_completed_callback = batch_completed_callback
        self._init_batcher()
        atexit.register(self.close)
        self._exceptions = queue.Queue()

    @property
    def flush_count(self):
        return self._flush_count

    @property
    def max_row_bytes(self):
        return self._max_row_bytes

    def _init_batcher(self):
        self._batcher = self.table._table_impl.mutations_batcher(**self._batcher_kwargs)
        self._batcher._user_batch_completed_callback = (
            self._user_batch_completed_callback
        )

    def _close_batcher(self):
        try:
            self._batcher.close()
        except MutationsExceptionGroup as exc_group:
            for error in exc_group.exceptions:
                # Unpack the root cause of the FailedMutationEntryError
                # and return that error to the user.
                self._exceptions.put(error.__cause__)

    def __enter__(self):
        """Starting the MutationsBatcher as a context manager"""
        return self

    def mutate(self, row):
        """Add a row to the batch. If the current batch meets one of the size
        limits, the batch is sent asynchronously.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_api_batcher_mutate]
            :end-before: [END bigtable_api_batcher_mutate]
            :dedent: 4

        :type row: class
        :param row: :class:`~google.cloud.bigtable.row.DirectRow`.

        :raises: One of the following:
            * :exc:`~.table._BigtableRetryableError` if any row returned a transient error.
            * :exc:`RuntimeError` if the number of responses doesn't match the number of rows that were retried
        """
        self._batcher.append(RowMutationEntry(row.row_key, row._get_mutations()))

    def mutate_rows(self, rows):
        """Add multiple rows to the batch. If the current batch meets one of the size
        limits, the batch is sent asynchronously.

        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_api_batcher_mutate_rows]
            :end-before: [END bigtable_api_batcher_mutate_rows]
            :dedent: 4

        :type rows: list:[`~google.cloud.bigtable.row.DirectRow`]
        :param rows: list:[`~google.cloud.bigtable.row.DirectRow`].

        :raises: One of the following:
            * :exc:`~.table._BigtableRetryableError` if any row returned a transient error.
            * :exc:`RuntimeError` if the number of responses doesn't match the number of rows that were retried
        """
        for row in rows:
            self.mutate(row)

    def flush(self):
        """Sends the current batch to Cloud Bigtable synchronously.
        For example:

        .. literalinclude:: snippets_table.py
            :start-after: [START bigtable_api_batcher_flush]
            :end-before: [END bigtable_api_batcher_flush]
            :dedent: 4

        :raises:
            * :exc:`~batcher.MutationsBatchError` if there's any error in the mutations.
        """
        self._close_batcher()
        self._init_batcher()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Clean up resources. Flush and shutdown the ThreadPoolExecutor."""
        self.close()

    def close(self):
        """Clean up resources. Flush and shutdown the ThreadPoolExecutor.
        Any errors will be raised.

        :raises:
            * :exc:`~batcher.MutationsBatchError` if there's any error in the mutations.
        """
        self._close_batcher()
        atexit.unregister(self.close)
        if self._exceptions.qsize() > 0:
            exc = list(self._exceptions.queue)
            raise MutationsBatchError("Errors in batch mutations.", exc=exc)
