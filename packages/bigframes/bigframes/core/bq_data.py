# Copyright 2023 Google LLC
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

import concurrent.futures
import dataclasses
import datetime
import functools
import os
import queue
import threading
import typing
from typing import Any, Iterator, Optional, Sequence, Tuple

from google.cloud import bigquery_storage_v1
import google.cloud.bigquery as bq
import google.cloud.bigquery_storage_v1.types as bq_storage_types
from google.protobuf import timestamp_pb2
import pyarrow as pa

from bigframes.core import pyarrow_utils
import bigframes.core.schema

if typing.TYPE_CHECKING:
    import bigframes.core.ordering as orderings


@dataclasses.dataclass(frozen=True)
class GbqTable:
    project_id: str = dataclasses.field()
    dataset_id: str = dataclasses.field()
    table_id: str = dataclasses.field()
    physical_schema: Tuple[bq.SchemaField, ...] = dataclasses.field()
    is_physically_stored: bool = dataclasses.field()
    cluster_cols: typing.Optional[Tuple[str, ...]]

    @staticmethod
    def from_table(table: bq.Table, columns: Sequence[str] = ()) -> GbqTable:
        # Subsetting fields with columns can reduce cost of row-hash default ordering
        if columns:
            schema = tuple(item for item in table.schema if item.name in columns)
        else:
            schema = tuple(table.schema)
        return GbqTable(
            project_id=table.project,
            dataset_id=table.dataset_id,
            table_id=table.table_id,
            physical_schema=schema,
            is_physically_stored=(table.table_type in ["TABLE", "MATERIALIZED_VIEW"]),
            cluster_cols=None
            if table.clustering_fields is None
            else tuple(table.clustering_fields),
        )

    @staticmethod
    def from_ref_and_schema(
        table_ref: bq.TableReference,
        schema: Sequence[bq.SchemaField],
        cluster_cols: Optional[Sequence[str]] = None,
    ) -> GbqTable:
        return GbqTable(
            project_id=table_ref.project,
            dataset_id=table_ref.dataset_id,
            table_id=table_ref.table_id,
            physical_schema=tuple(schema),
            is_physically_stored=True,
            cluster_cols=tuple(cluster_cols) if cluster_cols else None,
        )

    def get_table_ref(self) -> bq.TableReference:
        return bq.TableReference(
            bq.DatasetReference(self.project_id, self.dataset_id), self.table_id
        )

    @property
    @functools.cache
    def schema_by_id(self):
        return {col.name: col for col in self.physical_schema}


@dataclasses.dataclass(frozen=True)
class BigqueryDataSource:
    """
    Google BigQuery Data source.

    This should not be modified once defined, as all attributes contribute to the default ordering.
    """

    def __post_init__(self):
        # not all columns need be in schema, eg so can exclude unsupported column types (eg RANGE)
        assert set(field.name for field in self.table.physical_schema).issuperset(
            self.schema.names
        )

    table: GbqTable
    schema: bigframes.core.schema.ArraySchema
    at_time: typing.Optional[datetime.datetime] = None
    # Added for backwards compatibility, not validated
    sql_predicate: typing.Optional[str] = None
    ordering: typing.Optional[orderings.RowOrdering] = None
    # Optimization field
    n_rows: Optional[int] = None


_WORKER_TIME_INCREMENT = 0.05


def _iter_stream(
    stream_name: str,
    storage_read_client: bigquery_storage_v1.BigQueryReadClient,
    result_queue: queue.Queue,
    stop_event: threading.Event,
):
    reader = storage_read_client.read_rows(stream_name)
    for page in reader.rows().pages:
        while True:  # Alternate between put attempt and checking stop event
            try:
                result_queue.put(page.to_arrow(), timeout=_WORKER_TIME_INCREMENT)
                break
            except queue.Full:
                if stop_event.is_set():
                    return
                continue


def _iter_streams(
    streams: Sequence[bq_storage_types.ReadStream],
    storage_read_client: bigquery_storage_v1.BigQueryReadClient,
) -> Iterator[pa.RecordBatch]:
    stop_event = threading.Event()
    result_queue: queue.Queue = queue.Queue(
        len(streams)
    )  # each response is large, so small queue is appropriate

    in_progress: list[concurrent.futures.Future] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(streams)) as pool:
        try:
            for stream in streams:
                in_progress.append(
                    pool.submit(
                        _iter_stream,
                        stream.name,
                        storage_read_client,
                        result_queue,
                        stop_event,
                    )
                )

            while in_progress:
                try:
                    yield result_queue.get(timeout=0.1)
                except queue.Empty:
                    new_in_progress = []
                    for future in in_progress:
                        if future.done():
                            # Call to raise any exceptions
                            future.result()
                        else:
                            new_in_progress.append(future)
                    in_progress = new_in_progress
        finally:
            stop_event.set()


@dataclasses.dataclass
class ReadResult:
    iter: Iterator[pa.RecordBatch]
    approx_rows: int
    approx_bytes: int


def get_arrow_batches(
    data: BigqueryDataSource,
    columns: Sequence[str],
    storage_read_client: bigquery_storage_v1.BigQueryReadClient,
    project_id: str,
    sample_rate: Optional[float] = None,
) -> ReadResult:
    table_mod_options = {}
    read_options_dict: dict[str, Any] = {"selected_fields": list(columns)}

    predicates = []
    if data.sql_predicate:
        predicates.append(data.sql_predicate)
    if sample_rate is not None:
        assert isinstance(sample_rate, float)
        predicates.append(f"RAND() < {sample_rate}")

    if predicates:
        full_predicates = " AND ".join(f"( {pred} )" for pred in predicates)
        read_options_dict["row_restriction"] = full_predicates

    read_options = bq_storage_types.ReadSession.TableReadOptions(**read_options_dict)

    if data.at_time:
        snapshot_time = timestamp_pb2.Timestamp()
        snapshot_time.FromDatetime(data.at_time)
        table_mod_options["snapshot_time"] = snapshot_time
    table_mods = bq_storage_types.ReadSession.TableModifiers(**table_mod_options)

    requested_session = bq_storage_types.stream.ReadSession(
        table=data.table.get_table_ref().to_bqstorage(),
        data_format=bq_storage_types.DataFormat.ARROW,
        read_options=read_options,
        table_modifiers=table_mods,
    )
    if data.ordering is not None:
        max_streams = 1
    else:
        max_streams = os.cpu_count() or 8

    # Single stream to maintain ordering
    request = bq_storage_types.CreateReadSessionRequest(
        parent=f"projects/{project_id}",
        read_session=requested_session,
        max_stream_count=max_streams,
    )

    session = storage_read_client.create_read_session(request=request)

    if not session.streams:
        batches: Iterator[pa.RecordBatch] = iter([])
    else:
        batches = _iter_streams(session.streams, storage_read_client)

        def process_batch(pa_batch):
            return pyarrow_utils.cast_batch(
                pa_batch.select(columns), data.schema.select(columns).to_pyarrow()
            )

        batches = map(process_batch, batches)

    return ReadResult(
        batches, session.estimated_row_count, session.estimated_total_bytes_scanned
    )
