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

import pytest
import pytest_asyncio
import asyncio
import uuid
import os
from google.api_core import retry
from google.api_core.exceptions import ClientError

from google.cloud.bigtable.data.read_modify_write_rules import _MAX_INCREMENT_VALUE
from google.cloud.environment_vars import BIGTABLE_EMULATOR

TEST_FAMILY = "test-family"
TEST_FAMILY_2 = "test-family-2"


@pytest.fixture(scope="session")
def column_family_config():
    """
    specify column families to create when creating a new test table
    """
    from google.cloud.bigtable_admin_v2 import types

    return {TEST_FAMILY: types.ColumnFamily(), TEST_FAMILY_2: types.ColumnFamily()}


@pytest.fixture(scope="session")
def init_table_id():
    """
    The table_id to use when creating a new test table
    """
    return f"test-table-{uuid.uuid4().hex}"


@pytest.fixture(scope="session")
def cluster_config(project_id):
    """
    Configuration for the clusters to use when creating a new instance
    """
    from google.cloud.bigtable_admin_v2 import types

    cluster = {
        "test-cluster": types.Cluster(
            location=f"projects/{project_id}/locations/us-central1-b",
            serve_nodes=1,
        )
    }
    return cluster


class TempRowBuilder:
    """
    Used to add rows to a table for testing purposes.
    """

    def __init__(self, table):
        self.rows = []
        self.table = table

    async def add_row(
        self, row_key, *, family=TEST_FAMILY, qualifier=b"q", value=b"test-value"
    ):
        if isinstance(value, str):
            value = value.encode("utf-8")
        elif isinstance(value, int):
            value = value.to_bytes(8, byteorder="big", signed=True)
        request = {
            "table_name": self.table.table_name,
            "row_key": row_key,
            "mutations": [
                {
                    "set_cell": {
                        "family_name": family,
                        "column_qualifier": qualifier,
                        "value": value,
                    }
                }
            ],
        }
        await self.table.client._gapic_client.mutate_row(request)
        self.rows.append(row_key)

    async def delete_rows(self):
        if self.rows:
            request = {
                "table_name": self.table.table_name,
                "entries": [
                    {"row_key": row, "mutations": [{"delete_from_row": {}}]}
                    for row in self.rows
                ],
            }
            await self.table.client._gapic_client.mutate_rows(request)


@pytest.mark.usefixtures("table")
async def _retrieve_cell_value(table, row_key):
    """
    Helper to read an individual row
    """
    from google.cloud.bigtable.data import ReadRowsQuery

    row_list = await table.read_rows(ReadRowsQuery(row_keys=row_key))
    assert len(row_list) == 1
    row = row_list[0]
    cell = row.cells[0]
    return cell.value


async def _create_row_and_mutation(
    table, temp_rows, *, start_value=b"start", new_value=b"new_value"
):
    """
    Helper to create a new row, and a sample set_cell mutation to change its value
    """
    from google.cloud.bigtable.data.mutations import SetCell

    row_key = uuid.uuid4().hex.encode()
    family = TEST_FAMILY
    qualifier = b"test-qualifier"
    await temp_rows.add_row(
        row_key, family=family, qualifier=qualifier, value=start_value
    )
    # ensure cell is initialized
    assert (await _retrieve_cell_value(table, row_key)) == start_value

    mutation = SetCell(family=TEST_FAMILY, qualifier=qualifier, new_value=new_value)
    return row_key, mutation


@pytest_asyncio.fixture(scope="function")
async def temp_rows(table):
    builder = TempRowBuilder(table)
    yield builder
    await builder.delete_rows()


@pytest.mark.usefixtures("table")
@pytest.mark.usefixtures("client")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=10)
@pytest.mark.asyncio
async def test_ping_and_warm_gapic(client, table):
    """
    Simple ping rpc test
    This test ensures channels are able to authenticate with backend
    """
    request = {"name": table.instance_name}
    await client._gapic_client.ping_and_warm(request)


@pytest.mark.usefixtures("table")
@pytest.mark.usefixtures("client")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_ping_and_warm(client, table):
    """
    Test ping and warm from handwritten client
    """
    results = await client._ping_and_warm_instances()
    assert len(results) == 1
    assert results[0] is None


@pytest.mark.asyncio
@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
async def test_mutation_set_cell(table, temp_rows):
    """
    Ensure cells can be set properly
    """
    row_key = b"bulk_mutate"
    new_value = uuid.uuid4().hex.encode()
    row_key, mutation = await _create_row_and_mutation(
        table, temp_rows, new_value=new_value
    )
    await table.mutate_row(row_key, mutation)

    # ensure cell is updated
    assert (await _retrieve_cell_value(table, row_key)) == new_value


@pytest.mark.skipif(
    bool(os.environ.get(BIGTABLE_EMULATOR)), reason="emulator doesn't use splits"
)
@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_sample_row_keys(client, table, temp_rows, column_split_config):
    """
    Sample keys should return a single sample in small test tables
    """
    await temp_rows.add_row(b"row_key_1")
    await temp_rows.add_row(b"row_key_2")

    results = await table.sample_row_keys()
    assert len(results) == len(column_split_config) + 1
    # first keys should match the split config
    for idx in range(len(column_split_config)):
        assert results[idx][0] == column_split_config[idx]
        assert isinstance(results[idx][1], int)
    # last sample should be empty key
    assert results[-1][0] == b""
    assert isinstance(results[-1][1], int)


@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("table")
@pytest.mark.asyncio
async def test_bulk_mutations_set_cell(client, table, temp_rows):
    """
    Ensure cells can be set properly
    """
    from google.cloud.bigtable.data.mutations import RowMutationEntry

    new_value = uuid.uuid4().hex.encode()
    row_key, mutation = await _create_row_and_mutation(
        table, temp_rows, new_value=new_value
    )
    bulk_mutation = RowMutationEntry(row_key, [mutation])

    await table.bulk_mutate_rows([bulk_mutation])

    # ensure cell is updated
    assert (await _retrieve_cell_value(table, row_key)) == new_value


@pytest.mark.asyncio
async def test_bulk_mutations_raise_exception(client, table):
    """
    If an invalid mutation is passed, an exception should be raised
    """
    from google.cloud.bigtable.data.mutations import RowMutationEntry, SetCell
    from google.cloud.bigtable.data.exceptions import MutationsExceptionGroup
    from google.cloud.bigtable.data.exceptions import FailedMutationEntryError

    row_key = uuid.uuid4().hex.encode()
    mutation = SetCell(family="nonexistent", qualifier=b"test-qualifier", new_value=b"")
    bulk_mutation = RowMutationEntry(row_key, [mutation])

    with pytest.raises(MutationsExceptionGroup) as exc:
        await table.bulk_mutate_rows([bulk_mutation])
    assert len(exc.value.exceptions) == 1
    entry_error = exc.value.exceptions[0]
    assert isinstance(entry_error, FailedMutationEntryError)
    assert entry_error.index == 0
    assert entry_error.entry == bulk_mutation


@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_mutations_batcher_context_manager(client, table, temp_rows):
    """
    test batcher with context manager. Should flush on exit
    """
    from google.cloud.bigtable.data.mutations import RowMutationEntry

    new_value, new_value2 = [uuid.uuid4().hex.encode() for _ in range(2)]
    row_key, mutation = await _create_row_and_mutation(
        table, temp_rows, new_value=new_value
    )
    row_key2, mutation2 = await _create_row_and_mutation(
        table, temp_rows, new_value=new_value2
    )
    bulk_mutation = RowMutationEntry(row_key, [mutation])
    bulk_mutation2 = RowMutationEntry(row_key2, [mutation2])

    async with table.mutations_batcher() as batcher:
        await batcher.append(bulk_mutation)
        await batcher.append(bulk_mutation2)
    # ensure cell is updated
    assert (await _retrieve_cell_value(table, row_key)) == new_value
    assert len(batcher._staged_entries) == 0


@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_mutations_batcher_timer_flush(client, table, temp_rows):
    """
    batch should occur after flush_interval seconds
    """
    from google.cloud.bigtable.data.mutations import RowMutationEntry

    new_value = uuid.uuid4().hex.encode()
    row_key, mutation = await _create_row_and_mutation(
        table, temp_rows, new_value=new_value
    )
    bulk_mutation = RowMutationEntry(row_key, [mutation])
    flush_interval = 0.1
    async with table.mutations_batcher(flush_interval=flush_interval) as batcher:
        await batcher.append(bulk_mutation)
        await asyncio.sleep(0)
        assert len(batcher._staged_entries) == 1
        await asyncio.sleep(flush_interval + 0.1)
        assert len(batcher._staged_entries) == 0
        # ensure cell is updated
        assert (await _retrieve_cell_value(table, row_key)) == new_value


@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_mutations_batcher_count_flush(client, table, temp_rows):
    """
    batch should flush after flush_limit_mutation_count mutations
    """
    from google.cloud.bigtable.data.mutations import RowMutationEntry

    new_value, new_value2 = [uuid.uuid4().hex.encode() for _ in range(2)]
    row_key, mutation = await _create_row_and_mutation(
        table, temp_rows, new_value=new_value
    )
    bulk_mutation = RowMutationEntry(row_key, [mutation])
    row_key2, mutation2 = await _create_row_and_mutation(
        table, temp_rows, new_value=new_value2
    )
    bulk_mutation2 = RowMutationEntry(row_key2, [mutation2])

    async with table.mutations_batcher(flush_limit_mutation_count=2) as batcher:
        await batcher.append(bulk_mutation)
        assert len(batcher._flush_jobs) == 0
        # should be noop; flush not scheduled
        assert len(batcher._staged_entries) == 1
        await batcher.append(bulk_mutation2)
        # task should now be scheduled
        assert len(batcher._flush_jobs) == 1
        await asyncio.gather(*batcher._flush_jobs)
        assert len(batcher._staged_entries) == 0
        assert len(batcher._flush_jobs) == 0
        # ensure cells were updated
        assert (await _retrieve_cell_value(table, row_key)) == new_value
        assert (await _retrieve_cell_value(table, row_key2)) == new_value2


@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_mutations_batcher_bytes_flush(client, table, temp_rows):
    """
    batch should flush after flush_limit_bytes bytes
    """
    from google.cloud.bigtable.data.mutations import RowMutationEntry

    new_value, new_value2 = [uuid.uuid4().hex.encode() for _ in range(2)]
    row_key, mutation = await _create_row_and_mutation(
        table, temp_rows, new_value=new_value
    )
    bulk_mutation = RowMutationEntry(row_key, [mutation])
    row_key2, mutation2 = await _create_row_and_mutation(
        table, temp_rows, new_value=new_value2
    )
    bulk_mutation2 = RowMutationEntry(row_key2, [mutation2])

    flush_limit = bulk_mutation.size() + bulk_mutation2.size() - 1

    async with table.mutations_batcher(flush_limit_bytes=flush_limit) as batcher:
        await batcher.append(bulk_mutation)
        assert len(batcher._flush_jobs) == 0
        assert len(batcher._staged_entries) == 1
        await batcher.append(bulk_mutation2)
        # task should now be scheduled
        assert len(batcher._flush_jobs) == 1
        assert len(batcher._staged_entries) == 0
        # let flush complete
        await asyncio.gather(*batcher._flush_jobs)
        # ensure cells were updated
        assert (await _retrieve_cell_value(table, row_key)) == new_value
        assert (await _retrieve_cell_value(table, row_key2)) == new_value2


@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("table")
@pytest.mark.asyncio
async def test_mutations_batcher_no_flush(client, table, temp_rows):
    """
    test with no flush requirements met
    """
    from google.cloud.bigtable.data.mutations import RowMutationEntry

    new_value = uuid.uuid4().hex.encode()
    start_value = b"unchanged"
    row_key, mutation = await _create_row_and_mutation(
        table, temp_rows, start_value=start_value, new_value=new_value
    )
    bulk_mutation = RowMutationEntry(row_key, [mutation])
    row_key2, mutation2 = await _create_row_and_mutation(
        table, temp_rows, start_value=start_value, new_value=new_value
    )
    bulk_mutation2 = RowMutationEntry(row_key2, [mutation2])

    size_limit = bulk_mutation.size() + bulk_mutation2.size() + 1
    async with table.mutations_batcher(
        flush_limit_bytes=size_limit, flush_limit_mutation_count=3, flush_interval=1
    ) as batcher:
        await batcher.append(bulk_mutation)
        assert len(batcher._staged_entries) == 1
        await batcher.append(bulk_mutation2)
        # flush not scheduled
        assert len(batcher._flush_jobs) == 0
        await asyncio.sleep(0.01)
        assert len(batcher._staged_entries) == 2
        assert len(batcher._flush_jobs) == 0
        # ensure cells were not updated
        assert (await _retrieve_cell_value(table, row_key)) == start_value
        assert (await _retrieve_cell_value(table, row_key2)) == start_value


@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("table")
@pytest.mark.parametrize(
    "start,increment,expected",
    [
        (0, 0, 0),
        (0, 1, 1),
        (0, -1, -1),
        (1, 0, 1),
        (0, -100, -100),
        (0, 3000, 3000),
        (10, 4, 14),
        (_MAX_INCREMENT_VALUE, -_MAX_INCREMENT_VALUE, 0),
        (_MAX_INCREMENT_VALUE, 2, -_MAX_INCREMENT_VALUE),
        (-_MAX_INCREMENT_VALUE, -2, _MAX_INCREMENT_VALUE),
    ],
)
@pytest.mark.asyncio
async def test_read_modify_write_row_increment(
    client, table, temp_rows, start, increment, expected
):
    """
    test read_modify_write_row
    """
    from google.cloud.bigtable.data.read_modify_write_rules import IncrementRule

    row_key = b"test-row-key"
    family = TEST_FAMILY
    qualifier = b"test-qualifier"
    await temp_rows.add_row(row_key, value=start, family=family, qualifier=qualifier)

    rule = IncrementRule(family, qualifier, increment)
    result = await table.read_modify_write_row(row_key, rule)
    assert result.row_key == row_key
    assert len(result) == 1
    assert result[0].family == family
    assert result[0].qualifier == qualifier
    assert int(result[0]) == expected
    # ensure that reading from server gives same value
    assert (await _retrieve_cell_value(table, row_key)) == result[0].value


@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("table")
@pytest.mark.parametrize(
    "start,append,expected",
    [
        (b"", b"", b""),
        ("", "", b""),
        (b"abc", b"123", b"abc123"),
        (b"abc", "123", b"abc123"),
        ("", b"1", b"1"),
        (b"abc", "", b"abc"),
        (b"hello", b"world", b"helloworld"),
    ],
)
@pytest.mark.asyncio
async def test_read_modify_write_row_append(
    client, table, temp_rows, start, append, expected
):
    """
    test read_modify_write_row
    """
    from google.cloud.bigtable.data.read_modify_write_rules import AppendValueRule

    row_key = b"test-row-key"
    family = TEST_FAMILY
    qualifier = b"test-qualifier"
    await temp_rows.add_row(row_key, value=start, family=family, qualifier=qualifier)

    rule = AppendValueRule(family, qualifier, append)
    result = await table.read_modify_write_row(row_key, rule)
    assert result.row_key == row_key
    assert len(result) == 1
    assert result[0].family == family
    assert result[0].qualifier == qualifier
    assert result[0].value == expected
    # ensure that reading from server gives same value
    assert (await _retrieve_cell_value(table, row_key)) == result[0].value


@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("table")
@pytest.mark.asyncio
async def test_read_modify_write_row_chained(client, table, temp_rows):
    """
    test read_modify_write_row with multiple rules
    """
    from google.cloud.bigtable.data.read_modify_write_rules import AppendValueRule
    from google.cloud.bigtable.data.read_modify_write_rules import IncrementRule

    row_key = b"test-row-key"
    family = TEST_FAMILY
    qualifier = b"test-qualifier"
    start_amount = 1
    increment_amount = 10
    await temp_rows.add_row(
        row_key, value=start_amount, family=family, qualifier=qualifier
    )
    rule = [
        IncrementRule(family, qualifier, increment_amount),
        AppendValueRule(family, qualifier, "hello"),
        AppendValueRule(family, qualifier, "world"),
        AppendValueRule(family, qualifier, "!"),
    ]
    result = await table.read_modify_write_row(row_key, rule)
    assert result.row_key == row_key
    assert result[0].family == family
    assert result[0].qualifier == qualifier
    # result should be a bytes number string for the IncrementRules, followed by the AppendValueRule values
    assert (
        result[0].value
        == (start_amount + increment_amount).to_bytes(8, "big", signed=True)
        + b"helloworld!"
    )
    # ensure that reading from server gives same value
    assert (await _retrieve_cell_value(table, row_key)) == result[0].value


@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("table")
@pytest.mark.parametrize(
    "start_val,predicate_range,expected_result",
    [
        (1, (0, 2), True),
        (-1, (0, 2), False),
    ],
)
@pytest.mark.asyncio
async def test_check_and_mutate(
    client, table, temp_rows, start_val, predicate_range, expected_result
):
    """
    test that check_and_mutate_row works applies the right mutations, and returns the right result
    """
    from google.cloud.bigtable.data.mutations import SetCell
    from google.cloud.bigtable.data.row_filters import ValueRangeFilter

    row_key = b"test-row-key"
    family = TEST_FAMILY
    qualifier = b"test-qualifier"

    await temp_rows.add_row(
        row_key, value=start_val, family=family, qualifier=qualifier
    )

    false_mutation_value = b"false-mutation-value"
    false_mutation = SetCell(
        family=TEST_FAMILY, qualifier=qualifier, new_value=false_mutation_value
    )
    true_mutation_value = b"true-mutation-value"
    true_mutation = SetCell(
        family=TEST_FAMILY, qualifier=qualifier, new_value=true_mutation_value
    )
    predicate = ValueRangeFilter(predicate_range[0], predicate_range[1])
    result = await table.check_and_mutate_row(
        row_key,
        predicate,
        true_case_mutations=true_mutation,
        false_case_mutations=false_mutation,
    )
    assert result == expected_result
    # ensure cell is updated
    expected_value = true_mutation_value if expected_result else false_mutation_value
    assert (await _retrieve_cell_value(table, row_key)) == expected_value


@pytest.mark.skipif(
    bool(os.environ.get(BIGTABLE_EMULATOR)),
    reason="emulator doesn't raise InvalidArgument",
)
@pytest.mark.usefixtures("client")
@pytest.mark.usefixtures("table")
@pytest.mark.asyncio
async def test_check_and_mutate_empty_request(client, table):
    """
    check_and_mutate with no true or fale mutations should raise an error
    """
    from google.api_core import exceptions

    with pytest.raises(exceptions.InvalidArgument) as e:
        await table.check_and_mutate_row(
            b"row_key", None, true_case_mutations=None, false_case_mutations=None
        )
    assert "No mutations provided" in str(e.value)


@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_read_rows_stream(table, temp_rows):
    """
    Ensure that the read_rows_stream method works
    """
    await temp_rows.add_row(b"row_key_1")
    await temp_rows.add_row(b"row_key_2")

    # full table scan
    generator = await table.read_rows_stream({})
    first_row = await generator.__anext__()
    second_row = await generator.__anext__()
    assert first_row.row_key == b"row_key_1"
    assert second_row.row_key == b"row_key_2"
    with pytest.raises(StopAsyncIteration):
        await generator.__anext__()


@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_read_rows(table, temp_rows):
    """
    Ensure that the read_rows method works
    """
    await temp_rows.add_row(b"row_key_1")
    await temp_rows.add_row(b"row_key_2")
    # full table scan
    row_list = await table.read_rows({})
    assert len(row_list) == 2
    assert row_list[0].row_key == b"row_key_1"
    assert row_list[1].row_key == b"row_key_2"


@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_read_rows_sharded_simple(table, temp_rows):
    """
    Test read rows sharded with two queries
    """
    from google.cloud.bigtable.data.read_rows_query import ReadRowsQuery

    await temp_rows.add_row(b"a")
    await temp_rows.add_row(b"b")
    await temp_rows.add_row(b"c")
    await temp_rows.add_row(b"d")
    query1 = ReadRowsQuery(row_keys=[b"a", b"c"])
    query2 = ReadRowsQuery(row_keys=[b"b", b"d"])
    row_list = await table.read_rows_sharded([query1, query2])
    assert len(row_list) == 4
    assert row_list[0].row_key == b"a"
    assert row_list[1].row_key == b"c"
    assert row_list[2].row_key == b"b"
    assert row_list[3].row_key == b"d"


@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_read_rows_sharded_from_sample(table, temp_rows):
    """
    Test end-to-end sharding
    """
    from google.cloud.bigtable.data.read_rows_query import ReadRowsQuery
    from google.cloud.bigtable.data.read_rows_query import RowRange

    await temp_rows.add_row(b"a")
    await temp_rows.add_row(b"b")
    await temp_rows.add_row(b"c")
    await temp_rows.add_row(b"d")

    table_shard_keys = await table.sample_row_keys()
    query = ReadRowsQuery(row_ranges=[RowRange(start_key=b"b", end_key=b"z")])
    shard_queries = query.shard(table_shard_keys)
    row_list = await table.read_rows_sharded(shard_queries)
    assert len(row_list) == 3
    assert row_list[0].row_key == b"b"
    assert row_list[1].row_key == b"c"
    assert row_list[2].row_key == b"d"


@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_read_rows_sharded_filters_limits(table, temp_rows):
    """
    Test read rows sharded with filters and limits
    """
    from google.cloud.bigtable.data.read_rows_query import ReadRowsQuery
    from google.cloud.bigtable.data.row_filters import ApplyLabelFilter

    await temp_rows.add_row(b"a")
    await temp_rows.add_row(b"b")
    await temp_rows.add_row(b"c")
    await temp_rows.add_row(b"d")

    label_filter1 = ApplyLabelFilter("first")
    label_filter2 = ApplyLabelFilter("second")
    query1 = ReadRowsQuery(row_keys=[b"a", b"c"], limit=1, row_filter=label_filter1)
    query2 = ReadRowsQuery(row_keys=[b"b", b"d"], row_filter=label_filter2)
    row_list = await table.read_rows_sharded([query1, query2])
    assert len(row_list) == 3
    assert row_list[0].row_key == b"a"
    assert row_list[1].row_key == b"b"
    assert row_list[2].row_key == b"d"
    assert row_list[0][0].labels == ["first"]
    assert row_list[1][0].labels == ["second"]
    assert row_list[2][0].labels == ["second"]


@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_read_rows_range_query(table, temp_rows):
    """
    Ensure that the read_rows method works
    """
    from google.cloud.bigtable.data import ReadRowsQuery
    from google.cloud.bigtable.data import RowRange

    await temp_rows.add_row(b"a")
    await temp_rows.add_row(b"b")
    await temp_rows.add_row(b"c")
    await temp_rows.add_row(b"d")
    # full table scan
    query = ReadRowsQuery(row_ranges=RowRange(start_key=b"b", end_key=b"d"))
    row_list = await table.read_rows(query)
    assert len(row_list) == 2
    assert row_list[0].row_key == b"b"
    assert row_list[1].row_key == b"c"


@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_read_rows_single_key_query(table, temp_rows):
    """
    Ensure that the read_rows method works with specified query
    """
    from google.cloud.bigtable.data import ReadRowsQuery

    await temp_rows.add_row(b"a")
    await temp_rows.add_row(b"b")
    await temp_rows.add_row(b"c")
    await temp_rows.add_row(b"d")
    # retrieve specific keys
    query = ReadRowsQuery(row_keys=[b"a", b"c"])
    row_list = await table.read_rows(query)
    assert len(row_list) == 2
    assert row_list[0].row_key == b"a"
    assert row_list[1].row_key == b"c"


@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.asyncio
async def test_read_rows_with_filter(table, temp_rows):
    """
    ensure filters are applied
    """
    from google.cloud.bigtable.data import ReadRowsQuery
    from google.cloud.bigtable.data.row_filters import ApplyLabelFilter

    await temp_rows.add_row(b"a")
    await temp_rows.add_row(b"b")
    await temp_rows.add_row(b"c")
    await temp_rows.add_row(b"d")
    # retrieve keys with filter
    expected_label = "test-label"
    row_filter = ApplyLabelFilter(expected_label)
    query = ReadRowsQuery(row_filter=row_filter)
    row_list = await table.read_rows(query)
    assert len(row_list) == 4
    for row in row_list:
        assert row[0].labels == [expected_label]


@pytest.mark.usefixtures("table")
@pytest.mark.asyncio
async def test_read_rows_stream_close(table, temp_rows):
    """
    Ensure that the read_rows_stream can be closed
    """
    from google.cloud.bigtable.data import ReadRowsQuery

    await temp_rows.add_row(b"row_key_1")
    await temp_rows.add_row(b"row_key_2")
    # full table scan
    query = ReadRowsQuery()
    generator = await table.read_rows_stream(query)
    # grab first row
    first_row = await generator.__anext__()
    assert first_row.row_key == b"row_key_1"
    # close stream early
    await generator.aclose()
    with pytest.raises(StopAsyncIteration):
        await generator.__anext__()


@pytest.mark.usefixtures("table")
@pytest.mark.asyncio
async def test_read_row(table, temp_rows):
    """
    Test read_row (single row helper)
    """
    from google.cloud.bigtable.data import Row

    await temp_rows.add_row(b"row_key_1", value=b"value")
    row = await table.read_row(b"row_key_1")
    assert isinstance(row, Row)
    assert row.row_key == b"row_key_1"
    assert row.cells[0].value == b"value"


@pytest.mark.skipif(
    bool(os.environ.get(BIGTABLE_EMULATOR)),
    reason="emulator doesn't raise InvalidArgument",
)
@pytest.mark.usefixtures("table")
@pytest.mark.asyncio
async def test_read_row_missing(table):
    """
    Test read_row when row does not exist
    """
    from google.api_core import exceptions

    row_key = "row_key_not_exist"
    result = await table.read_row(row_key)
    assert result is None
    with pytest.raises(exceptions.InvalidArgument) as e:
        await table.read_row("")
    assert "Row keys must be non-empty" in str(e)


@pytest.mark.usefixtures("table")
@pytest.mark.asyncio
async def test_read_row_w_filter(table, temp_rows):
    """
    Test read_row (single row helper)
    """
    from google.cloud.bigtable.data import Row
    from google.cloud.bigtable.data.row_filters import ApplyLabelFilter

    await temp_rows.add_row(b"row_key_1", value=b"value")
    expected_label = "test-label"
    label_filter = ApplyLabelFilter(expected_label)
    row = await table.read_row(b"row_key_1", row_filter=label_filter)
    assert isinstance(row, Row)
    assert row.row_key == b"row_key_1"
    assert row.cells[0].value == b"value"
    assert row.cells[0].labels == [expected_label]


@pytest.mark.skipif(
    bool(os.environ.get(BIGTABLE_EMULATOR)),
    reason="emulator doesn't raise InvalidArgument",
)
@pytest.mark.usefixtures("table")
@pytest.mark.asyncio
async def test_row_exists(table, temp_rows):
    from google.api_core import exceptions

    """Test row_exists with rows that exist and don't exist"""
    assert await table.row_exists(b"row_key_1") is False
    await temp_rows.add_row(b"row_key_1")
    assert await table.row_exists(b"row_key_1") is True
    assert await table.row_exists("row_key_1") is True
    assert await table.row_exists(b"row_key_2") is False
    assert await table.row_exists("row_key_2") is False
    assert await table.row_exists("3") is False
    await temp_rows.add_row(b"3")
    assert await table.row_exists(b"3") is True
    with pytest.raises(exceptions.InvalidArgument) as e:
        await table.row_exists("")
    assert "Row keys must be non-empty" in str(e)


@pytest.mark.usefixtures("table")
@retry.AsyncRetry(predicate=retry.if_exception_type(ClientError), initial=1, maximum=5)
@pytest.mark.parametrize(
    "cell_value,filter_input,expect_match",
    [
        (b"abc", b"abc", True),
        (b"abc", "abc", True),
        (b".", ".", True),
        (".*", ".*", True),
        (".*", b".*", True),
        ("a", ".*", False),
        (b".*", b".*", True),
        (r"\a", r"\a", True),
        (b"\xe2\x98\x83", "☃", True),
        ("☃", "☃", True),
        (r"\C☃", r"\C☃", True),
        (1, 1, True),
        (2, 1, False),
        (68, 68, True),
        ("D", 68, False),
        (68, "D", False),
        (-1, -1, True),
        (2852126720, 2852126720, True),
        (-1431655766, -1431655766, True),
        (-1431655766, -1, False),
    ],
)
@pytest.mark.asyncio
async def test_literal_value_filter(
    table, temp_rows, cell_value, filter_input, expect_match
):
    """
    Literal value filter does complex escaping on re2 strings.
    Make sure inputs are properly interpreted by the server
    """
    from google.cloud.bigtable.data.row_filters import LiteralValueFilter
    from google.cloud.bigtable.data import ReadRowsQuery

    f = LiteralValueFilter(filter_input)
    await temp_rows.add_row(b"row_key_1", value=cell_value)
    query = ReadRowsQuery(row_filter=f)
    row_list = await table.read_rows(query)
    assert len(row_list) == bool(
        expect_match
    ), f"row {type(cell_value)}({cell_value}) not found with {type(filter_input)}({filter_input}) filter"
