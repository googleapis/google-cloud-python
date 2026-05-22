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
    MutationsBatcher,
    MutationsBatchError,
)

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
