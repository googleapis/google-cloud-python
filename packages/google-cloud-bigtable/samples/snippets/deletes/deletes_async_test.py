# Copyright 2024, Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import datetime
import os
from typing import AsyncGenerator

from google.cloud._helpers import _microseconds_from_datetime
import pytest, pytest_asyncio

import deletes_snippets_async

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BIGTABLE_INSTANCE = os.environ["BIGTABLE_INSTANCE"]
TABLE_ID_PREFIX = "mobile-time-series-{}"


@pytest_asyncio.fixture
async def table_id() -> AsyncGenerator[str, None]:
    table_id = _create_table()
    await _populate_table(table_id)
    yield table_id
    _delete_table(table_id)


def _create_table():
    from google.cloud import bigtable
    import uuid

    client = bigtable.Client(project=PROJECT, admin=True)
    instance = client.instance(BIGTABLE_INSTANCE)

    table_id = TABLE_ID_PREFIX.format(str(uuid.uuid4())[:16])
    table = instance.table(table_id)
    if table.exists():
        table.delete()

    table.create(column_families={"stats_summary": None, "cell_plan": None})
    client.close()
    return table_id


def _delete_table(table_id: str):
    from google.cloud import bigtable

    client = bigtable.Client(project=PROJECT, admin=True)
    instance = client.instance(BIGTABLE_INSTANCE)
    table = instance.table(table_id)
    table.delete()
    client.close()


async def _populate_table(table_id):
    from google.cloud.bigtable.data import (
        BigtableDataClientAsync,
        RowMutationEntry,
        SetCell,
    )

    timestamp = datetime.datetime(2019, 5, 1)
    timestamp_minus_hr = timestamp - datetime.timedelta(hours=1)

    async with (BigtableDataClientAsync(project=PROJECT) as client):
        async with client.get_table(BIGTABLE_INSTANCE, table_id) as table:
            async with table.mutations_batcher() as batcher:
                await batcher.append(
                    RowMutationEntry(
                        "phone#4c410523#20190501",
                        [
                            SetCell(
                                "stats_summary",
                                "connected_cell",
                                1,
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "stats_summary",
                                "connected_cell",
                                1,
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "stats_summary",
                                "connected_wifi",
                                1,
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "stats_summary",
                                "os_build",
                                "PQ2A.190405.003",
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "cell_plan",
                                "data_plan_01gb",
                                "true",
                                _microseconds_from_datetime(timestamp_minus_hr),
                            ),
                            SetCell(
                                "cell_plan",
                                "data_plan_01gb",
                                "false",
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "cell_plan",
                                "data_plan_05gb",
                                "true",
                                _microseconds_from_datetime(timestamp),
                            ),
                        ],
                    )
                )
                await batcher.append(
                    RowMutationEntry(
                        "phone#4c410523#20190502",
                        [
                            SetCell(
                                "stats_summary",
                                "connected_cell",
                                1,
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "stats_summary",
                                "connected_wifi",
                                1,
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "stats_summary",
                                "os_build",
                                "PQ2A.190405.004",
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "cell_plan",
                                "data_plan_05gb",
                                "true",
                                _microseconds_from_datetime(timestamp),
                            ),
                        ],
                    )
                )
                await batcher.append(
                    RowMutationEntry(
                        "phone#4c410523#20190505",
                        [
                            SetCell(
                                "stats_summary",
                                "connected_cell",
                                0,
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "stats_summary",
                                "connected_wifi",
                                1,
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "stats_summary",
                                "os_build",
                                "PQ2A.190406.000",
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "cell_plan",
                                "data_plan_05gb",
                                "true",
                                _microseconds_from_datetime(timestamp),
                            ),
                        ],
                    )
                )
                await batcher.append(
                    RowMutationEntry(
                        "phone#5c10102#20190501",
                        [
                            SetCell(
                                "stats_summary",
                                "connected_cell",
                                1,
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "stats_summary",
                                "connected_wifi",
                                1,
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "stats_summary",
                                "os_build",
                                "PQ2A.190401.002",
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "cell_plan",
                                "data_plan_10gb",
                                "true",
                                _microseconds_from_datetime(timestamp),
                            ),
                        ],
                    )
                )
                await batcher.append(
                    RowMutationEntry(
                        "phone#5c10102#20190502",
                        [
                            SetCell(
                                "stats_summary",
                                "connected_cell",
                                1,
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "stats_summary",
                                "connected_wifi",
                                0,
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "stats_summary",
                                "os_build",
                                "PQ2A.190406.000",
                                _microseconds_from_datetime(timestamp),
                            ),
                            SetCell(
                                "cell_plan",
                                "data_plan_10gb",
                                "true",
                                _microseconds_from_datetime(timestamp),
                            ),
                        ],
                    )
                )


def assert_output_match(capsys, expected):
    out, _ = capsys.readouterr()
    assert out == expected


@pytest.mark.asyncio
async def test_delete_from_column(capsys, table_id):
    await deletes_snippets_async.delete_from_column(
        PROJECT, BIGTABLE_INSTANCE, table_id
    )
    assert_output_match(capsys, "")


@pytest.mark.asyncio
async def test_delete_from_column_family(capsys, table_id):
    await deletes_snippets_async.delete_from_column_family(
        PROJECT, BIGTABLE_INSTANCE, table_id
    )
    assert_output_match(capsys, "")


@pytest.mark.asyncio
async def test_delete_from_row(capsys, table_id):
    await deletes_snippets_async.delete_from_row(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_output_match(capsys, "")


@pytest.mark.asyncio
async def test_streaming_and_batching(capsys, table_id):
    await deletes_snippets_async.streaming_and_batching(
        PROJECT, BIGTABLE_INSTANCE, table_id
    )
    assert_output_match(capsys, "")


@pytest.mark.asyncio
async def test_check_and_mutate(capsys, table_id):
    await deletes_snippets_async.check_and_mutate(PROJECT, BIGTABLE_INSTANCE, table_id)
    assert_output_match(capsys, "")
