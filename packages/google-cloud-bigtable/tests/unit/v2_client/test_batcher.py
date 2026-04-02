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


import mock
import time

import pytest

from google.cloud.bigtable.row import DirectRow
from google.cloud.bigtable.batcher import (
    _FlowControl,
    MutationsBatcher,
    MutationsBatchError,
)

TABLE_ID = "table-id"
TABLE_NAME = "/tables/" + TABLE_ID


def test_mutation_batcher_constructor():
    table = _Table(TABLE_NAME)
    with MutationsBatcher(table) as mutation_batcher:
        assert table is mutation_batcher.table


def test_mutation_batcher_w_user_callback():
    table = _Table(TABLE_NAME)

    def callback_fn(response):
        callback_fn.count = len(response)

    with MutationsBatcher(
        table, flush_count=1, batch_completed_callback=callback_fn
    ) as mutation_batcher:
        rows = [
            DirectRow(row_key=b"row_key"),
            DirectRow(row_key=b"row_key_2"),
            DirectRow(row_key=b"row_key_3"),
            DirectRow(row_key=b"row_key_4"),
        ]

        mutation_batcher.mutate_rows(rows)

    assert callback_fn.count == 4


def test_mutation_batcher_mutate_row():
    table = _Table(TABLE_NAME)
    with MutationsBatcher(table=table) as mutation_batcher:
        rows = [
            DirectRow(row_key=b"row_key"),
            DirectRow(row_key=b"row_key_2"),
            DirectRow(row_key=b"row_key_3"),
            DirectRow(row_key=b"row_key_4"),
        ]

        mutation_batcher.mutate_rows(rows)

    assert table.mutation_calls == 1


def test_mutation_batcher_mutate():
    table = _Table(TABLE_NAME)
    with MutationsBatcher(table=table) as mutation_batcher:
        row = DirectRow(row_key=b"row_key")
        row.set_cell("cf1", b"c1", 1)
        row.set_cell("cf1", b"c2", 2)
        row.set_cell("cf1", b"c3", 3)
        row.set_cell("cf1", b"c4", 4)

        mutation_batcher.mutate(row)

    assert table.mutation_calls == 1


def test_mutation_batcher_flush_w_no_rows():
    table = _Table(TABLE_NAME)
    with MutationsBatcher(table=table) as mutation_batcher:
        mutation_batcher.flush()

    assert table.mutation_calls == 0


def test_mutation_batcher_mutate_w_max_flush_count():
    table = _Table(TABLE_NAME)
    with MutationsBatcher(table=table, flush_count=3) as mutation_batcher:
        row_1 = DirectRow(row_key=b"row_key_1")
        row_2 = DirectRow(row_key=b"row_key_2")
        row_3 = DirectRow(row_key=b"row_key_3")

        mutation_batcher.mutate(row_1)
        mutation_batcher.mutate(row_2)
        mutation_batcher.mutate(row_3)

    assert table.mutation_calls == 1


@mock.patch("google.cloud.bigtable.batcher.MAX_OUTSTANDING_ELEMENTS", new=3)
def test_mutation_batcher_mutate_w_max_mutations():
    table = _Table(TABLE_NAME)
    with MutationsBatcher(table=table) as mutation_batcher:
        row = DirectRow(row_key=b"row_key")
        row.set_cell("cf1", b"c1", 1)
        row.set_cell("cf1", b"c2", 2)
        row.set_cell("cf1", b"c3", 3)

        mutation_batcher.mutate(row)

    assert table.mutation_calls == 1


def test_mutation_batcher_mutate_w_max_row_bytes():
    table = _Table(TABLE_NAME)
    with MutationsBatcher(
        table=table, max_row_bytes=3 * 1024 * 1024
    ) as mutation_batcher:
        number_of_bytes = 1 * 1024 * 1024
        max_value = b"1" * number_of_bytes

        row = DirectRow(row_key=b"row_key")
        row.set_cell("cf1", b"c1", max_value)
        row.set_cell("cf1", b"c2", max_value)
        row.set_cell("cf1", b"c3", max_value)

        mutation_batcher.mutate(row)

    assert table.mutation_calls == 1


def test_mutations_batcher_flushed_when_closed():
    table = _Table(TABLE_NAME)
    mutation_batcher = MutationsBatcher(table=table, max_row_bytes=3 * 1024 * 1024)

    number_of_bytes = 1 * 1024 * 1024
    max_value = b"1" * number_of_bytes

    row = DirectRow(row_key=b"row_key")
    row.set_cell("cf1", b"c1", max_value)
    row.set_cell("cf1", b"c2", max_value)

    mutation_batcher.mutate(row)
    assert table.mutation_calls == 0

    mutation_batcher.close()

    assert table.mutation_calls == 1


def test_mutations_batcher_context_manager_flushed_when_closed():
    table = _Table(TABLE_NAME)
    with MutationsBatcher(
        table=table, max_row_bytes=3 * 1024 * 1024
    ) as mutation_batcher:
        number_of_bytes = 1 * 1024 * 1024
        max_value = b"1" * number_of_bytes

        row = DirectRow(row_key=b"row_key")
        row.set_cell("cf1", b"c1", max_value)
        row.set_cell("cf1", b"c2", max_value)

        mutation_batcher.mutate(row)

    assert table.mutation_calls == 1


@mock.patch("google.cloud.bigtable.batcher.MutationsBatcher.flush")
def test_mutations_batcher_flush_interval(mocked_flush):
    table = _Table(TABLE_NAME)
    flush_interval = 0.5
    mutation_batcher = MutationsBatcher(table=table, flush_interval=flush_interval)

    assert mutation_batcher._timer.interval == flush_interval
    mocked_flush.assert_not_called()

    time.sleep(0.4)
    mocked_flush.assert_not_called()

    time.sleep(0.1)
    mocked_flush.assert_called_once_with()

    mutation_batcher.close()


def test_mutations_batcher_response_with_error_codes():
    from google.rpc.status_pb2 import Status

    mocked_response = [Status(code=1), Status(code=5)]

    with mock.patch("tests.unit.v2_client.test_batcher._Table") as mocked_table:
        table = mocked_table.return_value
        mutation_batcher = MutationsBatcher(table=table)

        row1 = DirectRow(row_key=b"row_key")
        row2 = DirectRow(row_key=b"row_key")
        table.mutate_rows.return_value = mocked_response

        mutation_batcher.mutate_rows([row1, row2])
        with pytest.raises(MutationsBatchError) as exc:
            mutation_batcher.close()
        assert exc.value.message == "Errors in batch mutations."
        assert len(exc.value.exc) == 2

        assert exc.value.exc[0].message == mocked_response[0].message
        assert exc.value.exc[1].message == mocked_response[1].message


def test_flow_control_event_is_set_when_not_blocked():
    flow_control = _FlowControl()

    flow_control.set_flow_control_status()
    assert flow_control.event.is_set()


def test_flow_control_event_is_not_set_when_blocked():
    flow_control = _FlowControl()

    flow_control.inflight_mutations = flow_control.max_mutations
    flow_control.inflight_size = flow_control.max_mutation_bytes

    flow_control.set_flow_control_status()
    assert not flow_control.event.is_set()


@mock.patch("concurrent.futures.ThreadPoolExecutor.submit")
def test_flush_async_batch_count(mocked_executor_submit):
    table = _Table(TABLE_NAME)
    mutation_batcher = MutationsBatcher(table=table, flush_count=2)

    number_of_bytes = 1 * 1024 * 1024
    max_value = b"1" * number_of_bytes
    for index in range(5):
        row = DirectRow(row_key=f"row_key_{index}")
        row.set_cell("cf1", b"c1", max_value)
        mutation_batcher.mutate(row)
    mutation_batcher._flush_async()

    # 3 batches submitted. 2 batches of 2 items, and the last one a single item batch.
    assert mocked_executor_submit.call_count == 3


class _Instance(object):
    def __init__(self, client=None):
        self._client = client


class _Table(object):
    def __init__(self, name, client=None):
        self.name = name
        self._instance = _Instance(client)
        self.mutation_calls = 0

    def mutate_rows(self, rows):
        from google.rpc.status_pb2 import Status

        self.mutation_calls += 1

        return [Status(code=0) for _ in rows]
