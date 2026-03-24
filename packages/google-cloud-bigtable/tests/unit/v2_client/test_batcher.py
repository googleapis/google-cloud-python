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
import pytest

from google.cloud.bigtable.batcher import (
    MutationsBatcher,
    MutationsBatchError,
    _FlowControl,
)
from google.cloud.bigtable.row import DirectRow

from ._testing import _make_credentials

PROJECT = "PROJECT"
INSTANCE_ID = "instance-id"
TABLE_ID = "table-id"
TABLE_NAME = "/tables/" + TABLE_ID


@pytest.fixture
def _setup_batcher():
    from google.cloud.bigtable.client import Client
    from google.cloud.bigtable.table import Table

    import google.cloud.bigtable.data._sync_autogen.mutations_batcher

    client = Client(project=PROJECT, credentials=_make_credentials())
    instance = client.instance(INSTANCE_ID)

    with mock.patch.object(
        google.cloud.bigtable.data._sync_autogen.mutations_batcher.CrossSync._Sync_Impl,
        "_MutateRowsOperation",
    ) as operation_mock:
        yield Table(TABLE_ID, instance=instance), operation_mock


@pytest.fixture
def _atexit_mock():
    atexit_mock = _AtexitMock()
    with mock.patch.multiple(
        "atexit", register=atexit_mock.register, unregister=atexit_mock.unregister
    ):
        yield atexit_mock


def test_mutations_batcher_constructor(_setup_batcher, _atexit_mock):
    from google.cloud.bigtable.batcher import MAX_OUTSTANDING_ELEMENTS
    from google.cloud.bigtable.batcher import MAX_OUTSTANDING_BYTES

    flush_count = 5
    flush_interval = 0.1
    max_row_bytes = 10000
    table, _ = _setup_batcher
    with mock.patch.object(
        table._table_impl, "mutations_batcher"
    ) as batcher_impl_constructor:
        with MutationsBatcher(
            table,
            flush_count=flush_count,
            flush_interval=flush_interval,
            max_row_bytes=max_row_bytes,
        ) as mutation_batcher:
            assert table is mutation_batcher.table
            batcher_impl_constructor.assert_called_once_with(
                flush_interval=flush_interval,
                flush_limit_mutation_count=flush_count,
                flush_limit_bytes=max_row_bytes,
                flow_control_max_mutation_count=MAX_OUTSTANDING_ELEMENTS,
                flow_control_max_bytes=MAX_OUTSTANDING_BYTES,
            )
            assert mutation_batcher.close in _atexit_mock._functions


def test_mutations_batcher_w_user_callback(_setup_batcher):
    table, _ = _setup_batcher

    callback_fn = mock.Mock()
    batch_size = 4

    with MutationsBatcher(
        table, flush_count=batch_size, batch_completed_callback=callback_fn
    ) as mutation_batcher:
        rows = [DirectRow(row_key=f"row_key_{i}".encode()) for i in range(batch_size)]
        for row in rows:
            row.delete()

        mutation_batcher.mutate_rows(rows)

    assert len(callback_fn.call_args[0][0]) == batch_size


def test_mutations_batcher_mutate_row(_setup_batcher):
    table, operation_mock = _setup_batcher
    batch_size = 4

    with MutationsBatcher(table, flush_count=batch_size) as mutation_batcher:
        rows = [DirectRow(row_key=f"row_key_{i}".encode()) for i in range(batch_size)]
        for row in rows:
            row.delete()

        mutation_batcher.mutate_rows(rows)

    operation_mock.assert_called_once()


def test_mutations_batcher_mutate(_setup_batcher):
    table, operation_mock = _setup_batcher
    with MutationsBatcher(table=table, flush_count=1) as mutation_batcher:
        row = DirectRow(row_key=b"row_key")
        row.set_cell("cf1", b"c1", 1)
        row.set_cell("cf1", b"c2", 2)
        row.set_cell("cf1", b"c3", 3)
        row.set_cell("cf1", b"c4", 4)

        mutation_batcher.mutate(row)

    operation_mock.assert_called_once()


def test_mutations_batcher_manual_flush(_setup_batcher, _atexit_mock):
    table, operation_mock = _setup_batcher
    with MutationsBatcher(table=table) as mutation_batcher:
        original_batcher_impl = mutation_batcher._batcher
        assert original_batcher_impl._on_exit in _atexit_mock._functions

        row = DirectRow(row_key=b"row_key")
        row.set_cell("cf1", b"c1", 1)
        mutation_batcher.mutate(row)

        mutation_batcher.flush()

        operation_mock.assert_called_once()
        assert mutation_batcher._batcher != original_batcher_impl
        assert original_batcher_impl._on_exit not in _atexit_mock._functions


def test_mutations_batcher_flush_w_no_rows(_setup_batcher):
    table, operation_mock = _setup_batcher
    with MutationsBatcher(table=table) as mutation_batcher:
        mutation_batcher.flush()

    operation_mock.assert_not_called()


def test_mutations_batcher_mutate_w_max_row_bytes(_setup_batcher):
    table, operation_mock = _setup_batcher
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

    operation_mock.assert_called_once()


def test_mutations_batcher_flushed_when_closed(_setup_batcher):
    table, operation_mock = _setup_batcher
    mutation_batcher = MutationsBatcher(table=table, max_row_bytes=3 * 1024 * 1024)

    number_of_bytes = 1 * 1024 * 1024
    max_value = b"1" * number_of_bytes

    row = DirectRow(row_key=b"row_key")
    row.set_cell("cf1", b"c1", max_value)
    row.set_cell("cf1", b"c2", max_value)

    mutation_batcher.mutate(row)
    operation_mock.assert_not_called()

    mutation_batcher.close()

    operation_mock.assert_called_once()


def test_mutations_batcher_context_manager_flushed_when_closed(_setup_batcher):
    table, operation_mock = _setup_batcher
    with MutationsBatcher(
        table=table, max_row_bytes=3 * 1024 * 1024
    ) as mutation_batcher:
        number_of_bytes = 1 * 1024 * 1024
        max_value = b"1" * number_of_bytes

        row = DirectRow(row_key=b"row_key")
        row.set_cell("cf1", b"c1", max_value)
        row.set_cell("cf1", b"c2", max_value)

        mutation_batcher.mutate(row)
        operation_mock.assert_not_called()

    operation_mock.assert_called_once()


<<<<<<< ours
@mock.patch("google.cloud.bigtable.batcher.threading.Timer")
@mock.patch("google.cloud.bigtable.batcher.MutationsBatcher.flush")
def test_mutations_batcher_flush_interval_does_not_start_timer(
    mocked_flush, mocked_timer
):
    # ``flush_interval`` is accepted for backwards compatibility but no longer
    # starts a background timer. Constructing the batcher must not create a
    # timer or trigger a flush.
    table = _Table(TABLE_NAME)
    MutationsBatcher(table=table, flush_interval=0.5)

    mocked_timer.assert_not_called()
    mocked_flush.assert_not_called()


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


def test_mutations_batcher_asynchronous_flush_exception_is_surfaced():
    """An exception raised by the underlying ``mutate_rows`` call (e.g. a
    non-retryable RPC error or a response-count mismatch) is raised inside the
    async flush task. It must be captured and re-raised at ``close()`` rather
    than being silently swallowed by the executor -- otherwise the failed
    mutations are never reported to the user (silent data loss)."""
    from google.api_core.exceptions import PermissionDenied

    with mock.patch("tests.unit.v2_client.test_batcher._Table") as mocked_table:
        table = mocked_table.return_value
        # flush_count=2 forces the batch to flush asynchronously (through the
        # executor) as soon as the second row is added
        mutation_batcher = MutationsBatcher(table=table, flush_count=2)

        row1 = DirectRow(row_key=b"row_key")
        row1.set_cell("cf1", b"c1", b"1")
        row2 = DirectRow(row_key=b"row_key")
        row2.set_cell("cf1", b"c1", b"2")
        table.mutate_rows.side_effect = PermissionDenied("denied")

        mutation_batcher.mutate_rows([row1, row2])
        with pytest.raises(MutationsBatchError) as exc:
            mutation_batcher.close()
        assert exc.value.message == "Errors in batch mutations."
        # the whole batch (both rows) failed, so both are reported -- the error
        # count stays aligned with the number of affected mutations
        assert len(exc.value.exc) == 2
        assert all(isinstance(e, PermissionDenied) for e in exc.value.exc)


def test_batch_completed_callback_ignores_cancelled_future():
    """A cancelled future is still "done", so the completion callback runs for
    it, but ``future.exception()`` would raise ``CancelledError``. The callback
    must short-circuit on a cancelled future instead of letting that propagate."""
    from google.cloud.bigtable.batcher import _BatchInfo

    table = _Table(TABLE_NAME)
    with MutationsBatcher(table=table) as mutation_batcher:
        batch_info = _BatchInfo(rows_count=2, mutations_count=2, mutations_size=0)

        cancelled_future = mock.Mock()
        cancelled_future.cancelled.return_value = True
        cancelled_future.exception.side_effect = AssertionError(
            "exception() must not be called on a cancelled future"
        )
        mutation_batcher.futures_mapping[cancelled_future] = batch_info

        # Should not raise, should not record any exceptions
        mutation_batcher._batch_completed_callback(cancelled_future)

        assert cancelled_future not in mutation_batcher.futures_mapping
        assert mutation_batcher.exceptions.qsize() == 0


def test_mutations_batcher_close_surfaces_errors_when_final_flush_raises():
    """If the final flush in ``close()`` raises, ``close()`` must still shut
    down the executor and surface every accumulated error -- including ones
    already captured from async flushes -- instead of letting the flush
    exception mask them and abort cleanup (silent data loss)."""
    from google.api_core.exceptions import PermissionDenied, ServiceUnavailable

    with mock.patch("tests.unit.v2_client.test_batcher._Table") as mocked_table:
        table = mocked_table.return_value
        mutation_batcher = MutationsBatcher(table=table)

        # Simulate an error already captured earlier (e.g. from an async flush).
        prior_error = ServiceUnavailable("earlier async failure")
        mutation_batcher.exceptions.put(prior_error)

        # The row stays queued (below flush_count), so it is only flushed by
        # close(); make that final flush raise.
        row = DirectRow(row_key=b"row_key")
        row.set_cell("cf1", b"c1", b"1")
        mutation_batcher.mutate(row)
        table.mutate_rows.side_effect = PermissionDenied("denied")

        with pytest.raises(MutationsBatchError) as exc:
            mutation_batcher.close()

        # both the pre-existing and the flush-time errors are reported
        assert prior_error in exc.value.exc
        assert any(isinstance(e, PermissionDenied) for e in exc.value.exc)
        # cleanup still ran despite the flush raising
        assert mutation_batcher._executor._shutdown is True


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
=======
def test_mutations_batcher_flush_interval(_setup_batcher):
    table, operation_mock = _setup_batcher
    flush_interval = 0.5
    mutation_batcher = MutationsBatcher(table=table, flush_interval=flush_interval)
    row = DirectRow(row_key=b"row_key")
    row.set_cell("cf1", b"c1", b"1")
    mutation_batcher.mutate(row)
    operation_mock.assert_not_called()

    time.sleep(0.4)
    operation_mock.assert_not_called()

    # Test could be flaky, so giving the thread some extra buffer time
    time.sleep(0.25)
    operation_mock.assert_called_once()

    mutation_batcher.close()


def test_mutations_batcher_response_with_error_codes(_setup_batcher):
    from google.api_core import exceptions
    from google.cloud.bigtable.data.exceptions import FailedMutationEntryError
    from google.cloud.bigtable.data.exceptions import MutationsExceptionGroup

    table, operation_mock = _setup_batcher

    causes = [
        exceptions.InternalServerError("Something happened"),
        exceptions.DataLoss("Data loss"),
    ]
    excs = [
        FailedMutationEntryError(
            failed_idx=i, failed_mutation_entry=mock.Mock(), cause=cause
        )
        for i, cause in enumerate(causes)
    ]
    error = MutationsExceptionGroup(excs=excs, total_entries=len(excs))

    operation_mock.return_value.start.side_effect = error

    mutations_batcher = MutationsBatcher(table=table)
    row1 = DirectRow(row_key=b"row_key")
    row1.set_cell("cf1", b"c1", b"1")
    row2 = DirectRow(row_key=b"row_key_2")
    row2.set_cell("cf1", b"c1", b"1")
    mutations_batcher.mutate_rows([row1, row2])
    mutations_batcher.flush()

    with pytest.raises(MutationsBatchError) as raised_error:
        mutations_batcher.close()
    assert raised_error.value.message == "Errors in batch mutations."
    assert len(raised_error.value.exc) == 2

    assert raised_error.value.exc[0].message == causes[0].message
    assert raised_error.value.exc[1].message == causes[1].message


def test_mutations_batcher_response_with_error_codes_multiple_flushes(_setup_batcher):
    from google.api_core import exceptions
    from google.cloud.bigtable.data.exceptions import FailedMutationEntryError
    from google.cloud.bigtable.data.exceptions import MutationsExceptionGroup

    table, operation_mock = _setup_batcher

    causes = [
        exceptions.InternalServerError("Something happened"),
        exceptions.DataLoss("Data loss"),
    ]
    excs = [
        FailedMutationEntryError(
            failed_idx=i, failed_mutation_entry=mock.Mock(), cause=cause
        )
        for i, cause in enumerate(causes)
    ]
    error1 = MutationsExceptionGroup(excs=excs[0:1], total_entries=1)
    error2 = MutationsExceptionGroup(excs=excs[1:2], total_entries=1)

    operation_mock.return_value.start.side_effect = error1

    mutations_batcher = MutationsBatcher(table=table)
    row1 = DirectRow(row_key=b"row_key")
    row1.set_cell("cf1", b"c1", b"1")
    mutations_batcher.mutate(row1)
    mutations_batcher.flush()

    operation_mock.return_value.start.side_effect = error2

    row2 = DirectRow(row_key=b"row_key_2")
    row2.set_cell("cf1", b"c1", b"1")
    mutations_batcher.mutate(row2)
    mutations_batcher.flush()

    with pytest.raises(MutationsBatchError) as raised_error:
        mutations_batcher.close()
    assert raised_error.value.message == "Errors in batch mutations."
    assert len(raised_error.value.exc) == 2

    assert raised_error.value.exc[0].message == causes[0].message
    assert raised_error.value.exc[1].message == causes[1].message


class _AtexitMock:
    def __init__(self):
        self._functions = set()

    def register(self, func):
        self._functions.add(func)

    def unregister(self, func):
        self._functions.remove(func)
>>>>>>> theirs
