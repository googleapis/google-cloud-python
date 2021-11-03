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

from google.cloud.bigtable.row import DirectRow

TABLE_ID = "table-id"
TABLE_NAME = "/tables/" + TABLE_ID


def _make_mutation_batcher(table, **kw):
    from google.cloud.bigtable.batcher import MutationsBatcher

    return MutationsBatcher(table, **kw)


def test_mutation_batcher_constructor():
    table = _Table(TABLE_NAME)

    mutation_batcher = _make_mutation_batcher(table)
    assert table is mutation_batcher.table


def test_mutation_batcher_mutate_row():
    table = _Table(TABLE_NAME)
    mutation_batcher = _make_mutation_batcher(table=table)

    rows = [
        DirectRow(row_key=b"row_key"),
        DirectRow(row_key=b"row_key_2"),
        DirectRow(row_key=b"row_key_3"),
        DirectRow(row_key=b"row_key_4"),
    ]

    mutation_batcher.mutate_rows(rows)
    mutation_batcher.flush()

    assert table.mutation_calls == 1


def test_mutation_batcher_mutate():
    table = _Table(TABLE_NAME)
    mutation_batcher = _make_mutation_batcher(table=table)

    row = DirectRow(row_key=b"row_key")
    row.set_cell("cf1", b"c1", 1)
    row.set_cell("cf1", b"c2", 2)
    row.set_cell("cf1", b"c3", 3)
    row.set_cell("cf1", b"c4", 4)

    mutation_batcher.mutate(row)

    mutation_batcher.flush()

    assert table.mutation_calls == 1


def test_mutation_batcher_flush_w_no_rows():
    table = _Table(TABLE_NAME)
    mutation_batcher = _make_mutation_batcher(table=table)
    mutation_batcher.flush()

    assert table.mutation_calls == 0


def test_mutation_batcher_mutate_w_max_flush_count():
    table = _Table(TABLE_NAME)
    mutation_batcher = _make_mutation_batcher(table=table, flush_count=3)

    row_1 = DirectRow(row_key=b"row_key_1")
    row_2 = DirectRow(row_key=b"row_key_2")
    row_3 = DirectRow(row_key=b"row_key_3")

    mutation_batcher.mutate(row_1)
    mutation_batcher.mutate(row_2)
    mutation_batcher.mutate(row_3)

    assert table.mutation_calls == 1


@mock.patch("google.cloud.bigtable.batcher.MAX_MUTATIONS", new=3)
def test_mutation_batcher_mutate_with_max_mutations_failure():
    from google.cloud.bigtable.batcher import MaxMutationsError

    table = _Table(TABLE_NAME)
    mutation_batcher = _make_mutation_batcher(table=table)

    row = DirectRow(row_key=b"row_key")
    row.set_cell("cf1", b"c1", 1)
    row.set_cell("cf1", b"c2", 2)
    row.set_cell("cf1", b"c3", 3)
    row.set_cell("cf1", b"c4", 4)

    with pytest.raises(MaxMutationsError):
        mutation_batcher.mutate(row)


@mock.patch("google.cloud.bigtable.batcher.MAX_MUTATIONS", new=3)
def test_mutation_batcher_mutate_w_max_mutations():
    table = _Table(TABLE_NAME)
    mutation_batcher = _make_mutation_batcher(table=table)

    row = DirectRow(row_key=b"row_key")
    row.set_cell("cf1", b"c1", 1)
    row.set_cell("cf1", b"c2", 2)
    row.set_cell("cf1", b"c3", 3)

    mutation_batcher.mutate(row)
    mutation_batcher.flush()

    assert table.mutation_calls == 1


def test_mutation_batcher_mutate_w_max_row_bytes():
    table = _Table(TABLE_NAME)
    mutation_batcher = _make_mutation_batcher(
        table=table, max_row_bytes=3 * 1024 * 1024
    )

    number_of_bytes = 1 * 1024 * 1024
    max_value = b"1" * number_of_bytes

    row = DirectRow(row_key=b"row_key")
    row.set_cell("cf1", b"c1", max_value)
    row.set_cell("cf1", b"c2", max_value)
    row.set_cell("cf1", b"c3", max_value)

    mutation_batcher.mutate(row)

    assert table.mutation_calls == 1


class _Instance(object):
    def __init__(self, client=None):
        self._client = client


class _Table(object):
    def __init__(self, name, client=None):
        self.name = name
        self._instance = _Instance(client)
        self.mutation_calls = 0

    def mutate_rows(self, rows):
        self.mutation_calls += 1
        return rows
