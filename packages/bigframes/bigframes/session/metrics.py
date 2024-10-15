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

LOGGING_NAME_ENV_VAR = "BIGFRAMES_PERFORMANCE_LOG_NAME"


@dataclasses.dataclass
class ExecutionMetrics:
    execution_count: int = 0
    slot_millis: int = 0
    bytes_processed: int = 0

    def count_job_stats(self, query_job: bq_job.QueryJob):
        stats = get_performance_stats(query_job)
        if stats is not None:
            bytes_processed, slot_millis, exec_seconds = stats
            self.execution_count += 1
            self.bytes_processed += bytes_processed
            self.slot_millis += slot_millis
            if LOGGING_NAME_ENV_VAR in os.environ:
                # when running notebooks via pytest nbmake
                write_stats_to_disk(bytes_processed, slot_millis, exec_seconds)


def get_performance_stats(
    query_job: bigquery.QueryJob,
) -> Optional[Tuple[int, int, Optional[float]]]:
    """Parse the query job for performance stats.

    Return None if the stats do not reflect real work done in bigquery.
    """
    bytes_processed = query_job.total_bytes_processed
    if not isinstance(bytes_processed, int):
        return None  # filter out mocks
    if query_job.configuration.dry_run:
        # dry run stats are just predictions of the real run
        bytes_processed = 0

    slot_millis = query_job.slot_millis
    if not isinstance(slot_millis, int):
        return None  # filter out mocks

    if query_job.configuration.dry_run:
        # dry run stats are just predictions of the real run
        slot_millis = 0

    exec_seconds = (
        (query_job.ended - query_job.created).total_seconds()
        if query_job.created is not None and query_job.ended is not None
        else None
    )

    return bytes_processed, slot_millis, exec_seconds


def write_stats_to_disk(
    bytes_processed: int, slot_millis: int, exec_seconds: Optional[float]
):
    """For pytest runs only, log information about the query job
    to a file in order to create a performance report.
    """
    if LOGGING_NAME_ENV_VAR not in os.environ:
        raise EnvironmentError(
            "Environment variable {env_var} is not set".format(
                env_var=LOGGING_NAME_ENV_VAR
            )
        )
    test_name = os.environ[LOGGING_NAME_ENV_VAR]
    current_directory = os.getcwd()

    # store bytes processed
    bytes_file = os.path.join(current_directory, test_name + ".bytesprocessed")
    with open(bytes_file, "a") as f:
        f.write(str(bytes_processed) + "\n")

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
