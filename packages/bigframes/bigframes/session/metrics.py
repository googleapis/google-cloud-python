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
import datetime
import os
from typing import Any, Mapping, Optional, Tuple, Union

import google.cloud.bigquery as bigquery
from google.cloud.bigquery.job.load import LoadJob
from google.cloud.bigquery.job.query import QueryJob
import google.cloud.bigquery.table as bq_table

LOGGING_NAME_ENV_VAR = "BIGFRAMES_PERFORMANCE_LOG_NAME"


@dataclasses.dataclass
class JobMetadata:
    job_id: Optional[str] = None
    query_id: Optional[str] = None
    location: Optional[str] = None
    project: Optional[str] = None
    creation_time: Optional[datetime.datetime] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    duration_seconds: Optional[float] = None
    status: Optional[str] = None
    total_bytes_processed: Optional[int] = None
    total_slot_ms: Optional[int] = None
    job_type: Optional[str] = None
    error_result: Optional[Mapping[str, Any]] = None
    cached: Optional[bool] = None
    job_url: Optional[str] = None
    query: Optional[str] = None
    destination_table: Optional[str] = None
    source_uris: Optional[list[str]] = None
    input_files: Optional[int] = None
    input_bytes: Optional[int] = None
    output_rows: Optional[int] = None
    source_format: Optional[str] = None

    @classmethod
    def from_job(
        cls, query_job: Union[QueryJob, LoadJob], exec_seconds: Optional[float] = None
    ) -> "JobMetadata":
        query_text = getattr(query_job, "query", None)
        if query_text and len(query_text) > 1024:
            query_text = query_text[:1021] + "..."

        job_id = getattr(query_job, "job_id", None)
        job_url = None
        if job_id:
            job_url = f"https://console.cloud.google.com/bigquery?project={query_job.project}&j=bq:{query_job.location}:{job_id}&page=queryresults"

        metadata = cls(
            job_id=query_job.job_id,
            location=query_job.location,
            project=query_job.project,
            creation_time=query_job.created,
            start_time=query_job.started,
            end_time=query_job.ended,
            duration_seconds=exec_seconds,
            status=query_job.state,
            job_type=query_job.job_type,
            error_result=query_job.error_result,
            query=query_text,
            job_url=job_url,
        )
        if isinstance(query_job, QueryJob):
            metadata.cached = getattr(query_job, "cache_hit", None)
            metadata.destination_table = (
                str(query_job.destination) if query_job.destination else None
            )
            metadata.total_bytes_processed = getattr(
                query_job, "total_bytes_processed", None
            )
            metadata.total_slot_ms = getattr(query_job, "slot_millis", None)
        elif isinstance(query_job, LoadJob):
            metadata.output_rows = getattr(query_job, "output_rows", None)
            metadata.input_files = getattr(query_job, "input_files", None)
            metadata.input_bytes = getattr(query_job, "input_bytes", None)
            metadata.destination_table = (
                str(query_job.destination)
                if getattr(query_job, "destination", None)
                else None
            )
            if getattr(query_job, "source_uris", None):
                metadata.source_uris = list(query_job.source_uris)
            if query_job.configuration and hasattr(
                query_job.configuration, "source_format"
            ):
                metadata.source_format = query_job.configuration.source_format

        return metadata

    @classmethod
    def from_row_iterator(
        cls, row_iterator: bq_table.RowIterator, exec_seconds: Optional[float] = None
    ) -> "JobMetadata":
        query_text = getattr(row_iterator, "query", None)
        if query_text and len(query_text) > 1024:
            query_text = query_text[:1021] + "..."

        job_id = getattr(row_iterator, "job_id", None)
        job_url = None
        if job_id:
            project = getattr(row_iterator, "project", "")
            location = getattr(row_iterator, "location", "")
            job_url = f"https://console.cloud.google.com/bigquery?project={project}&j=bq:{location}:{job_id}&page=queryresults"

        return cls(
            job_id=job_id,
            query_id=getattr(row_iterator, "query_id", None),
            location=getattr(row_iterator, "location", None),
            project=getattr(row_iterator, "project", None),
            creation_time=getattr(row_iterator, "created", None),
            start_time=getattr(row_iterator, "started", None),
            end_time=getattr(row_iterator, "ended", None),
            duration_seconds=exec_seconds,
            status="DONE",
            total_bytes_processed=getattr(row_iterator, "total_bytes_processed", None),
            total_slot_ms=getattr(row_iterator, "slot_millis", None),
            job_type="query",
            cached=getattr(row_iterator, "cache_hit", None),
            query=query_text,
            job_url=job_url,
        )


@dataclasses.dataclass
class ExecutionMetrics:
    execution_count: int = 0
    slot_millis: int = 0
    bytes_processed: int = 0
    execution_secs: float = 0
    query_char_count: int = 0
    jobs: list[JobMetadata] = dataclasses.field(default_factory=list)

    def count_job_stats(
        self,
        query_job: Optional[Union[QueryJob, LoadJob]] = None,
        row_iterator: Optional[bq_table.RowIterator] = None,
    ):
        if query_job is None:
            assert row_iterator is not None

            # TODO(tswast): Pass None after making benchmark publishing robust to missing data.
            bytes_processed = getattr(row_iterator, "total_bytes_processed", 0) or 0
            query_char_count = len(getattr(row_iterator, "query", "") or "")
            slot_millis = getattr(row_iterator, "slot_millis", 0) or 0
            created = getattr(row_iterator, "created", None)
            ended = getattr(row_iterator, "ended", None)
            exec_seconds = (
                (ended - created).total_seconds() if created and ended else 0.0
            )

            self.execution_count += 1
            self.query_char_count += query_char_count
            self.bytes_processed += bytes_processed
            self.slot_millis += slot_millis
            self.execution_secs += exec_seconds

            self.jobs.append(
                JobMetadata.from_row_iterator(row_iterator, exec_seconds=exec_seconds)
            )

        elif isinstance(query_job, QueryJob) and query_job.configuration.dry_run:
            query_char_count = len(getattr(query_job, "query", ""))

            # TODO(tswast): Pass None after making benchmark publishing robust to missing data.
            bytes_processed = 0
            slot_millis = 0
            exec_seconds = 0.0

        elif isinstance(query_job, bigquery.QueryJob):
            if (stats := get_performance_stats(query_job)) is not None:
                query_char_count, bytes_processed, slot_millis, exec_seconds = stats
                self.execution_count += 1
                self.query_char_count += query_char_count or 0
                self.bytes_processed += bytes_processed or 0
                self.slot_millis += slot_millis or 0
                self.execution_secs += exec_seconds or 0

                metadata = JobMetadata.from_job(query_job, exec_seconds=exec_seconds)
                metadata.total_bytes_processed = bytes_processed
                metadata.total_slot_ms = slot_millis
                self.jobs.append(metadata)

        else:
            self.execution_count += 1
            duration = (
                (query_job.ended - query_job.created).total_seconds()
                if query_job.ended and query_job.created
                else None
            )
            self.jobs.append(JobMetadata.from_job(query_job, exec_seconds=duration))

        # For pytest runs only, log information about the query job
        # to a file in order to create a performance report.
        if (
            isinstance(query_job, bigquery.QueryJob)
            and not query_job.configuration.dry_run
        ):
            stats = get_performance_stats(query_job)
            if stats:
                write_stats_to_disk(
                    query_char_count=stats[0],
                    bytes_processed=stats[1],
                    slot_millis=stats[2],
                    exec_seconds=stats[3],
                )
        elif row_iterator is not None:
            bytes_processed = getattr(row_iterator, "total_bytes_processed", 0) or 0
            query_char_count = len(getattr(row_iterator, "query", "") or "")
            slot_millis = getattr(row_iterator, "slot_millis", 0) or 0
            created = getattr(row_iterator, "created", None)
            ended = getattr(row_iterator, "ended", None)
            exec_seconds = (
                (ended - created).total_seconds() if created and ended else 0.0
            )
            write_stats_to_disk(
                query_char_count=query_char_count,
                bytes_processed=bytes_processed,
                slot_millis=slot_millis,
                exec_seconds=exec_seconds,
            )

    def on_event(self, event: Any):
        try:
            import bigframes.core.events
            from bigframes.session.executor import LocalExecuteResult
        except ImportError:
            return

        if isinstance(event, bigframes.core.events.ExecutionFinished):
            if event.result and isinstance(event.result, LocalExecuteResult):
                self.execution_count += 1
                bytes_processed = event.result.total_bytes_processed or 0

                metadata = JobMetadata(
                    job_type="polars",
                    status="DONE",
                    total_bytes_processed=bytes_processed,
                )
                self.jobs.append(metadata)


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
    *,
    query_char_count: int,
    bytes_processed: int,
    slot_millis: int,
    exec_seconds: float,
):
    """For pytest runs only, log information about the query job
    to a file in order to create a performance report.
    """
    if LOGGING_NAME_ENV_VAR not in os.environ:
        return

    # when running notebooks via pytest nbmake and running benchmarks
    test_name = os.environ[LOGGING_NAME_ENV_VAR]
    current_directory = os.getcwd()

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
