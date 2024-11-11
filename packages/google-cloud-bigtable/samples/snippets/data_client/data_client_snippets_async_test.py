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
import pytest
import pytest_asyncio
import os
import uuid

from . import data_client_snippets_async as data_snippets
from ...utils import create_table_cm


PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BIGTABLE_INSTANCE = os.environ["BIGTABLE_INSTANCE"]
TABLE_ID = f"data-client-{str(uuid.uuid4())[:16]}"


@pytest.fixture(scope="session")
def table_id():
    with create_table_cm(PROJECT, BIGTABLE_INSTANCE, TABLE_ID, {"family": None, "stats_summary": None}):
        yield TABLE_ID


@pytest_asyncio.fixture
async def table(table_id):
    from google.cloud.bigtable.data import BigtableDataClientAsync

    async with BigtableDataClientAsync(project=PROJECT) as client:
        async with client.get_table(BIGTABLE_INSTANCE, table_id) as table:
            yield table


@pytest.mark.asyncio
async def test_write_simple(table):
    await data_snippets.write_simple(table)


@pytest.mark.asyncio
async def test_write_batch(table):
    await data_snippets.write_batch(table)


@pytest.mark.asyncio
async def test_write_increment(table):
    await data_snippets.write_increment(table)


@pytest.mark.asyncio
async def test_write_conditional(table):
    await data_snippets.write_conditional(table)


@pytest.mark.asyncio
async def test_read_row(table):
    await data_snippets.read_row(table)


@pytest.mark.asyncio
async def test_read_row_partial(table):
    await data_snippets.read_row_partial(table)


@pytest.mark.asyncio
async def test_read_rows_multiple(table):
    await data_snippets.read_rows_multiple(table)


@pytest.mark.asyncio
async def test_read_row_range(table):
    await data_snippets.read_row_range(table)


@pytest.mark.asyncio
async def test_read_with_prefix(table):
    await data_snippets.read_with_prefix(table)


@pytest.mark.asyncio
async def test_read_with_filter(table):
    await data_snippets.read_with_filter(table)


@pytest.mark.asyncio
async def test_execute_query(table):
    await data_snippets.execute_query(table)
