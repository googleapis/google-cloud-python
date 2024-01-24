# Copyright 2024 Google LLC All rights reserved.
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
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from queue import Queue
from typing import Any, TYPE_CHECKING
from threading import Lock, Event

if TYPE_CHECKING:
    from google.cloud.spanner_v1.database import BatchSnapshot

QUEUE_SIZE_PER_WORKER = 32
MAX_PARALLELISM = 16


class PartitionExecutor:
    """
    Executor that executes single partition on a separate thread and inserts
    rows in the queue
    """

    def __init__(self, batch_snapshot, partition_id, merged_result_set):
        self._batch_snapshot: BatchSnapshot = batch_snapshot
        self._partition_id = partition_id
        self._merged_result_set: MergedResultSet = merged_result_set
        self._queue: Queue[PartitionExecutorResult] = merged_result_set._queue

    def run(self):
        results = None
        try:
            results = self._batch_snapshot.process_query_batch(self._partition_id)
            for row in results:
                if self._merged_result_set._metadata is None:
                    self._set_metadata(results)
                self._queue.put(PartitionExecutorResult(data=row))
            # Special case: The result set did not return any rows.
            # Push the metadata to the merged result set.
            if self._merged_result_set._metadata is None:
                self._set_metadata(results)
        except Exception as ex:
            if self._merged_result_set._metadata is None:
                self._set_metadata(results, True)
            self._queue.put(PartitionExecutorResult(exception=ex))
        finally:
            # Emit a special 'is_last' result to ensure that the MergedResultSet
            # is not blocked on a queue that never receives any more results.
            self._queue.put(PartitionExecutorResult(is_last=True))

    def _set_metadata(self, results, is_exception=False):
        self._merged_result_set.metadata_lock.acquire()
        try:
            if not is_exception:
                self._merged_result_set._metadata = results.metadata
        finally:
            self._merged_result_set.metadata_lock.release()
            self._merged_result_set.metadata_event.set()


@dataclass
class PartitionExecutorResult:
    data: Any = None
    exception: Exception = None
    is_last: bool = False


class MergedResultSet:
    """
    Executes multiple partitions on different threads and then combines the
    results from multiple queries using a synchronized queue. The order of the
    records in the MergedResultSet is not guaranteed.
    """

    def __init__(self, batch_snapshot, partition_ids, max_parallelism):
        self._exception = None
        self._metadata = None
        self.metadata_event = Event()
        self.metadata_lock = Lock()

        partition_ids_count = len(partition_ids)
        self._finished_count_down_latch = partition_ids_count
        parallelism = min(MAX_PARALLELISM, partition_ids_count)
        if max_parallelism != 0:
            parallelism = min(partition_ids_count, max_parallelism)
        self._queue = Queue(maxsize=QUEUE_SIZE_PER_WORKER * parallelism)

        partition_executors = []
        for partition_id in partition_ids:
            partition_executors.append(
                PartitionExecutor(batch_snapshot, partition_id, self)
            )
        executor = ThreadPoolExecutor(max_workers=parallelism)
        for partition_executor in partition_executors:
            executor.submit(partition_executor.run)
        executor.shutdown(False)

    def __iter__(self):
        return self

    def __next__(self):
        if self._exception is not None:
            raise self._exception
        while True:
            partition_result = self._queue.get()
            if partition_result.is_last:
                self._finished_count_down_latch -= 1
                if self._finished_count_down_latch == 0:
                    raise StopIteration
            elif partition_result.exception is not None:
                self._exception = partition_result.exception
                raise self._exception
            else:
                return partition_result.data

    @property
    def metadata(self):
        self.metadata_event.wait()
        return self._metadata

    @property
    def stats(self):
        # TODO: Implement
        return None
