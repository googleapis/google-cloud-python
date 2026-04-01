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
from typing import Any, Iterator, List, Literal, Optional, Sequence, Tuple, Union

from google.cloud import bigquery_storage_v1
import google.cloud.bigquery as bq
import google.cloud.bigquery_storage_v1.types as bq_storage_types
from google.protobuf import timestamp_pb2
import pyarrow as pa

import bigframes.constants
from bigframes.core import pyarrow_utils
import bigframes.core.schema

if typing.TYPE_CHECKING:
    import bigframes.core.ordering as orderings


def _resolve_standard_gcp_region(bq_region: str):
    """
    Resolve bq regions to standardized
    """
    if bq_region.casefold() == "US":
        return "us-central1"
    elif bq_region.casefold() == "EU":
        return "europe-west4"
    return bq_region


def is_irc_table(table_id: str):
    """
    Determines if a table id should be resolved through the iceberg rest catalog.
    """
    return len(table_id.split(".")) == 4


def is_compatible(
    data_region: Union[GcsRegion, BigQueryRegion], session_location: str
) -> bool:
    # based on https://docs.cloud.google.com/bigquery/docs/locations#storage-location-considerations
    if isinstance(data_region, BigQueryRegion):
        return data_region.name == session_location
    else:
        assert isinstance(data_region, GcsRegion)
        # TODO(b/463675088): Multi-regions don't yet support rest catalog tables
        if session_location in bigframes.constants.BIGQUERY_MULTIREGIONS:
            return False
        return _resolve_standard_gcp_region(session_location) in data_region.included


def get_default_bq_region(data_region: Union[GcsRegion, BigQueryRegion]) -> str:
    if isinstance(data_region, BigQueryRegion):
        return data_region.name
    elif isinstance(data_region, GcsRegion):
        # should maybe try to track and prefer primary replica?
        return data_region.included[0]


@dataclasses.dataclass(frozen=True)
class BigQueryRegion:
    name: str


@dataclasses.dataclass(frozen=True)
class GcsRegion:
    # this is the name of gcs regions, which may be names for multi-regions, so shouldn't be compared with non-gcs locations
    storage_regions: tuple[str, ...]
    # this tracks all the included standard, specific regions (eg us-east1), and should be comparable to bq regions (except non-standard US, EU, omni regions)
    included: tuple[str, ...]


# what is the line between metadata and core fields? Mostly metadata fields are optional or unreliable, but its fuzzy
@dataclasses.dataclass(frozen=True)
class TableMetadata:
    # this size metadata might be stale, don't use where strict correctness is needed
    location: Union[BigQueryRegion, GcsRegion]
    type: Literal["TABLE", "EXTERNAL", "VIEW", "MATERIALIZE_VIEW", "SNAPSHOT"]
    numBytes: Optional[int] = None
    numRows: Optional[int] = None
    created_time: Optional[datetime.datetime] = None
    modified_time: Optional[datetime.datetime] = None


@dataclasses.dataclass(frozen=True)
class GbqNativeTable:
    project_id: str = dataclasses.field()
    dataset_id: str = dataclasses.field()
    table_id: str = dataclasses.field()
    physical_schema: Tuple[bq.SchemaField, ...] = dataclasses.field()
    metadata: TableMetadata = dataclasses.field()
    partition_col: Optional[str] = None
    cluster_cols: typing.Optional[Tuple[str, ...]] = None
    primary_key: Optional[Tuple[str, ...]] = None

    @staticmethod
    def from_table(table: bq.Table, columns: Sequence[str] = ()) -> GbqNativeTable:
        # Subsetting fields with columns can reduce cost of row-hash default ordering
        if columns:
            schema = tuple(item for item in table.schema if item.name in columns)
        else:
            schema = tuple(table.schema)

        metadata = TableMetadata(
            numBytes=table.num_bytes,
            numRows=table.num_rows,
            location=BigQueryRegion(table.location),  # type: ignore
            type=table.table_type or "TABLE",  # type: ignore
            created_time=table.created,
            modified_time=table.modified,
        )
        partition_col = None
        if table.range_partitioning:
            partition_col = table.range_partitioning.field
        elif table.time_partitioning:
            partition_col = table.time_partitioning.field

        return GbqNativeTable(
            project_id=table.project,
            dataset_id=table.dataset_id,
            table_id=table.table_id,
            physical_schema=schema,
            partition_col=partition_col,
            cluster_cols=None
            if (table.clustering_fields is None)
            else tuple(table.clustering_fields),
            primary_key=tuple(_get_primary_keys(table)),
            metadata=metadata,
        )

    @staticmethod
    def from_ref_and_schema(
        table_ref: bq.TableReference,
        schema: Sequence[bq.SchemaField],
        location: str,
        table_type: Literal["TABLE"] = "TABLE",
        cluster_cols: Optional[Sequence[str]] = None,
    ) -> GbqNativeTable:
        return GbqNativeTable(
            project_id=table_ref.project,
            dataset_id=table_ref.dataset_id,
            table_id=table_ref.table_id,
            metadata=TableMetadata(location=BigQueryRegion(location), type=table_type),
            physical_schema=tuple(schema),
            cluster_cols=tuple(cluster_cols) if cluster_cols else None,
        )

    @property
    def is_physically_stored(self) -> bool:
        return self.metadata.type in ["TABLE", "MATERIALIZED_VIEW"]

    def get_table_ref(self) -> bq.TableReference:
        return bq.TableReference(
            bq.DatasetReference(self.project_id, self.dataset_id), self.table_id
        )

    def get_full_id(self, quoted: bool = False) -> str:
        if quoted:
            return f"`{self.project_id}`.`{self.dataset_id}`.`{self.table_id}`"
        return f"{self.project_id}.{self.dataset_id}.{self.table_id}"

    @property
    @functools.cache
    def schema_by_id(self):
        return {col.name: col for col in self.physical_schema}


@dataclasses.dataclass(frozen=True)
class BiglakeIcebergTable:
    project_id: str = dataclasses.field()
    catalog_id: str = dataclasses.field()
    namespace_id: str = dataclasses.field()
    table_id: str = dataclasses.field()
    physical_schema: Tuple[bq.SchemaField, ...] = dataclasses.field()
    cluster_cols: typing.Optional[Tuple[str, ...]]
    metadata: TableMetadata

    def get_full_id(self, quoted: bool = False) -> str:
        if quoted:
            return f"`{self.project_id}`.`{self.catalog_id}`.`{self.namespace_id}`.`{self.table_id}`"
        return (
            f"{self.project_id}.{self.catalog_id}.{self.namespace_id}.{self.table_id}"
        )

    @property
    @functools.cache
    def schema_by_id(self):
        return {col.name: col for col in self.physical_schema}

    @property
    def partition_col(self) -> Optional[str]:
        # TODO: Use iceberg partition metadata
        return None

    @property
    def dataset_id(self) -> str:
        """
        Not a true dataset, but serves as the dataset component of the identifer in sql queries
        """
        return f"{self.catalog_id}.{self.namespace_id}"

    @property
    def primary_key(self) -> Optional[Tuple[str, ...]]:
        return None

    def get_table_ref(self) -> bq.TableReference:
        return bq.TableReference(
            bq.DatasetReference(self.project_id, self.dataset_id), self.table_id
        )


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

    table: Union[GbqNativeTable, BiglakeIcebergTable]
    schema: bigframes.core.schema.ArraySchema
    at_time: typing.Optional[datetime.datetime] = None
    # Added for backwards compatibility, not validated
    sql_predicate: typing.Optional[str] = None
    ordering: typing.Optional[orderings.RowOrdering] = None
    # Optimization field, must be correct if set, don't put maybe-stale number here
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
    assert isinstance(data.table, GbqNativeTable)

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


def _get_primary_keys(
    table: bq.Table,
) -> List[str]:
    """Get primary keys from table if they are set."""

    primary_keys: List[str] = []
    if (
        (table_constraints := getattr(table, "table_constraints", None)) is not None
        and (primary_key := table_constraints.primary_key) is not None
        # This will be False for either None or empty list.
        # We want primary_keys = None if no primary keys are set.
        and (columns := primary_key.columns)
    ):
        primary_keys = columns if columns is not None else []

    return primary_keys
