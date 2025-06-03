# Copyright 2024 Google LLC
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

from __future__ import annotations

import dataclasses
import os
from typing import Optional, Tuple

import google.cloud.bigquery as bigquery
import google.cloud.bigquery.job as bq_job
import google.cloud.bigquery.table as bq_table

LOGGING_NAME_ENV_VAR = "BIGFRAMES_PERFORMANCE_LOG_NAME"


@dataclasses.dataclass
class ExecutionMetrics:
    execution_count: int = 0
    slot_millis: int = 0
    bytes_processed: int = 0
    execution_secs: float = 0
    query_char_count: int = 0

    def count_job_stats(
        self,
        query_job: Optional[bq_job.QueryJob] = None,
        row_iterator: Optional[bq_table.RowIterator] = None,
    ):
        if query_job is None:
            assert row_iterator is not None
            total_bytes_processed = getattr(row_iterator, "total_bytes_processed", None)
            query = getattr(row_iterator, "query", None)
            if total_bytes_processed is None or query is None:
                return

            self.execution_count += 1
            self.query_char_count += len(query)
            self.bytes_processed += total_bytes_processed
            write_stats_to_disk(len(query), total_bytes_processed)
            return

        stats = get_performance_stats(query_job)
        if stats is not None:
            query_char_count, bytes_processed, slot_millis, execution_secs = stats
            self.execution_count += 1
            self.query_char_count += query_char_count
            self.bytes_processed += bytes_processed
            self.slot_millis += slot_millis
            self.execution_secs += execution_secs
            write_stats_to_disk(
                query_char_count, bytes_processed, slot_millis, execution_secs
            )


def get_performance_stats(
    query_job: bigquery.QueryJob,
) -> Optional[Tuple[int, int, int, float]]:
    """Parse the query job for performance stats.

    Return None if the stats do not reflect real work done in bigquery.
    """
    if (
        query_job.configuration.dry_run
        or query_job.created is None
        or query_job.ended is None
    ):
        return None

    bytes_processed = query_job.total_bytes_processed
    if bytes_processed and not isinstance(bytes_processed, int):
        return None  # filter out mocks

    slot_millis = query_job.slot_millis
    if slot_millis and not isinstance(slot_millis, int):
        return None  # filter out mocks

    execution_secs = (query_job.ended - query_job.created).total_seconds()
    query_char_count = len(query_job.query)

    return (
        query_char_count,
        # Not every job populates these. For example, slot_millis is missing
        # from queries that came from cached results.
        bytes_processed if bytes_processed else 0,
        slot_millis if slot_millis else 0,
        execution_secs,
    )


def write_stats_to_disk(
    query_char_count: int,
    bytes_processed: int,
    slot_millis: Optional[int] = None,
    exec_seconds: Optional[float] = None,
):
    """For pytest runs only, log information about the query job
    to a file in order to create a performance report.
    """
    if LOGGING_NAME_ENV_VAR not in os.environ:
        return

    # when running notebooks via pytest nbmake and running benchmarks
    test_name = os.environ[LOGGING_NAME_ENV_VAR]
    current_directory = os.getcwd()

    if (slot_millis is not None) and (exec_seconds is not None):
        # store slot milliseconds
        slot_file = os.path.join(current_directory, test_name + ".slotmillis")
        with open(slot_file, "a") as f:
            f.write(str(slot_millis) + "\n")

        # store execution time seconds
        exec_time_file = os.path.join(
            current_directory, test_name + ".bq_exec_time_seconds"
        )
        with open(exec_time_file, "a") as f:
            f.write(str(exec_seconds) + "\n")

    # store length of query
    query_char_count_file = os.path.join(
        current_directory, test_name + ".query_char_count"
    )
    with open(query_char_count_file, "a") as f:
        f.write(str(query_char_count) + "\n")

    # store bytes processed
    bytes_file = os.path.join(current_directory, test_name + ".bytesprocessed")
    with open(bytes_file, "a") as f:
        f.write(str(bytes_processed) + "\n")
