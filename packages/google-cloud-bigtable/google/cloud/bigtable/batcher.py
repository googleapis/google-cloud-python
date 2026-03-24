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
<<<<<<< ours

import atexit
import concurrent.futures
import queue
import threading
from dataclasses import dataclass
=======
import queue
import atexit


from google.cloud.bigtable.data.exceptions import MutationsExceptionGroup
from google.cloud.bigtable.data.mutations import RowMutationEntry
>>>>>>> theirs

from google.api_core.exceptions import from_grpc_status

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
    must be guaranteed to be sent, since calling :func:`mutate()` may only
    result in an in-memory change. Rows are only sent to the service when a size
    limit is reached, when :func:`flush()` is called explicitly, or when the
    batcher is closed (:func:`close()` is also registered to run at interpreter
    exit). There is no time-based background flush. As a result, if the process
    terminates abruptly -- e.g. a crash, ``SIGKILL``, or ``os._exit`` where the
    ``atexit`` handler never runs -- any :class:`DirectRow` still buffered in
    memory is silently dropped and never sent, even after :func:`mutate()`
    returned.

    Note on thread safety: The same :class:`MutationBatcher` cannot be shared by multiple end-user threads.

    .. warning::

       If using ``MutationsBatcher``, please ensure you are using
       ``google-cloud-bigtable >= 2.42.0``, or consider migrating to the
       batcher provided by the synchronous/asynchronous data client
       (:mod:`google.cloud.bigtable.data`).

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
    :param flush_interval: (Deprecated) No longer used. Retained only for
        backwards compatibility. There is no time-based background flush; see the
        class docstring for when rows are sent.

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
<<<<<<< ours
        self._executor = concurrent.futures.ThreadPoolExecutor()
        atexit.register(self.close)
        # ``flush_interval`` is retained for backwards compatibility but is no
        # longer used: the previous background ``threading.Timer`` was one-shot
        # (never re-armed), so it fired at most once and could silently drop the
        # rows it dequeued if that single flush raised on the timer thread.
        # Flushing now happens only on size thresholds, explicit ``flush()``,
        # or ``close()`` (also registered via ``atexit``).
        self.flow_control = _FlowControl(
            max_mutations=MAX_OUTSTANDING_ELEMENTS,
            max_mutation_bytes=MAX_OUTSTANDING_BYTES,
        )
        self.futures_mapping = {}
        self.exceptions = queue.Queue()
=======
        self._batcher_kwargs = {
            "flush_interval": flush_interval,
            "flush_limit_mutation_count": flush_count,
            "flush_limit_bytes": max_row_bytes,
            "flow_control_max_mutation_count": MAX_OUTSTANDING_ELEMENTS,
            "flow_control_max_bytes": MAX_OUTSTANDING_BYTES,
        }
>>>>>>> theirs
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
<<<<<<< ours
            * :exc:`.batcherMutationsBatchError` if there's any error in the mutations.
        """
        rows_to_flush = []
        row = self._rows.get()
        while row is not None:
            rows_to_flush.append(row)
            row = self._rows.get()
        response = self._flush_rows(rows_to_flush)
        return response

    def _flush_async(self):
        """Sends the current batch to Cloud Bigtable asynchronously.

        :raises:
            * :exc:`.batcherMutationsBatchError` if there's any error in the mutations.
        """
        next_row = self._rows.get()
        while next_row is not None:
            # start a new batch
            rows_to_flush = [next_row]
            batch_info = _BatchInfo(
                mutations_count=len(next_row._get_mutations()),
                rows_count=1,
                mutations_size=next_row.get_mutations_size(),
            )
            # fill up batch with rows
            next_row = self._rows.get()
            while next_row is not None and self._row_fits_in_batch(
                next_row, batch_info
            ):
                rows_to_flush.append(next_row)
                batch_info.mutations_count += len(next_row._get_mutations())
                batch_info.rows_count += 1
                batch_info.mutations_size += next_row.get_mutations_size()
                next_row = self._rows.get()
            # send batch over network
            # wait for resources to become available
            self.flow_control.wait()
            # once unblocked, submit the batch
            # event flag will be set by control_flow to block subsequent thread, but not blocking this one
            self.flow_control.control_flow(batch_info)
            future = self._executor.submit(self._flush_rows, rows_to_flush)
            # schedule release of resources from flow control
            self.futures_mapping[future] = batch_info
            future.add_done_callback(self._batch_completed_callback)

    def _batch_completed_callback(self, future):
        """Callback for when the mutation has finished to clean up the current batch
        and release items from the flow controller.
        Raise exceptions if there's any.
        Release the resources locked by the flow control and allow enqueued tasks to be run.
        """
        processed_rows = self.futures_mapping[future]
        self.flow_control.release(processed_rows)
        del self.futures_mapping[future]
        # Surface any exception raised inside the async flush. Without this, an
        # exception raised by ``_flush_rows`` (e.g. a non-retryable RPC error, a
        # retry deadline, or a response-count mismatch) would be stored on the
        # future and silently discarded, so the failed mutations would never be
        # reported to the user -- effectively silent data loss. Per-row errors
        # from a successful RPC are already recorded in ``self.exceptions`` by
        # ``_flush_rows``; here the whole batch failed with a single exception,
        # so record it once per row in the batch to keep the reported error
        # count aligned with the number of affected mutations.
        #
        # A cancelled future is "done", so this callback still runs for it, but
        # ``future.exception()`` would raise ``CancelledError``. Nothing here
        # cancels futures today, but guard against it so the callback stays
        # correct if cancellation is ever introduced.
        if future.cancelled():
            return
        exc = future.exception()
        if exc is not None:
            for _ in range(processed_rows.rows_count):
                self.exceptions.put(exc)

    def _row_fits_in_batch(self, row, batch_info):
        """Checks if a row can fit in the current batch.

        :type row: class
        :param row: :class:`~google.cloud.bigtable.row.DirectRow`.

        :type batch_info: :class:`_BatchInfo`
        :param batch_info: Information about the current batch.

        :rtype: bool
        :returns: True if the row can fit in the current batch.
=======
            * :exc:`~batcher.MutationsBatchError` if there's any error in the mutations.
>>>>>>> theirs
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
<<<<<<< ours
        try:
            self.flush()
        except MutationsBatchError as exc:
            for e in exc.exc:
                self.exceptions.put(e)
        except Exception as exc:
            # A failure in this final synchronous flush must not abort cleanup.
            # If it propagated here it would skip the executor shutdown (leaving
            # in-flight async flushes un-awaited) and skip draining
            # self.exceptions, masking every error already captured from
            # earlier async flushes -- silently discarding those failures.
            # Record it like any other batch failure and continue.
            self.exceptions.put(exc)
        self._executor.shutdown(wait=True)
=======
        self._close_batcher()
>>>>>>> theirs
        atexit.unregister(self.close)
        if self._exceptions.qsize() > 0:
            exc = list(self._exceptions.queue)
            raise MutationsBatchError("Errors in batch mutations.", exc=exc)
