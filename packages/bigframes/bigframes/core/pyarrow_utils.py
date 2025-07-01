# Copyright 2025 Google LLC
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
from typing import Iterable, Iterator

import pyarrow as pa


class BatchBuffer:
    """
    FIFO buffer of pyarrow Record batches

    Not thread-safe.
    """

    def __init__(self):
        self._buffer: list[pa.RecordBatch] = []
        self._buffer_size: int = 0

    def __len__(self):
        return self._buffer_size

    def append_batch(self, batch: pa.RecordBatch) -> None:
        self._buffer.append(batch)
        self._buffer_size += batch.num_rows

    def take_as_batches(self, n: int) -> tuple[pa.RecordBatch, ...]:
        if n > len(self):
            raise ValueError(f"Cannot take {n} rows, only {len(self)} rows in buffer.")
        rows_taken = 0
        sub_batches: list[pa.RecordBatch] = []
        while rows_taken < n:
            batch = self._buffer.pop(0)
            if batch.num_rows > (n - rows_taken):
                sub_batches.append(batch.slice(length=n - rows_taken))
                self._buffer.insert(0, batch.slice(offset=n - rows_taken))
                rows_taken += n - rows_taken
            else:
                sub_batches.append(batch)
                rows_taken += batch.num_rows

        self._buffer_size -= n
        return tuple(sub_batches)

    def take_rechunked(self, n: int) -> pa.RecordBatch:
        return (
            pa.Table.from_batches(self.take_as_batches(n))
            .combine_chunks()
            .to_batches()[0]
        )


def chunk_by_row_count(
    batches: Iterable[pa.RecordBatch], page_size: int
) -> Iterator[tuple[pa.RecordBatch, ...]]:
    buffer = BatchBuffer()
    for batch in batches:
        buffer.append_batch(batch)
        while len(buffer) >= page_size:
            yield buffer.take_as_batches(page_size)

    # emit final page, maybe smaller
    if len(buffer) > 0:
        yield buffer.take_as_batches(len(buffer))


def cast_batch(batch: pa.RecordBatch, schema: pa.Schema) -> pa.RecordBatch:
    if batch.schema == schema:
        return batch
    # TODO: Use RecordBatch.cast once min pyarrow>=16.0
    return pa.record_batch(
        [arr.cast(type) for arr, type in zip(batch.columns, schema.types)],
        schema=schema,
    )


def truncate_pyarrow_iterable(
    batches: Iterable[pa.RecordBatch], max_results: int
) -> Iterator[pa.RecordBatch]:
    total_yielded = 0
    for batch in batches:
        if batch.num_rows >= (max_results - total_yielded):
            yield batch.slice(length=max_results - total_yielded)
            return
        else:
            yield batch
            total_yielded += batch.num_rows


def append_offsets(
    pa_table: pa.Table,
    offsets_col: str,
) -> pa.Table:
    return pa_table.append_column(
        offsets_col, pa.array(range(pa_table.num_rows), type=pa.int64())
    )


def as_nullable(pa_table: pa.Table):
    """Normalizes schema to nullable for value-wise comparisons."""
    nullable_schema = pa.schema(field.with_nullable(True) for field in pa_table.schema)
    return pa_table.cast(nullable_schema)
