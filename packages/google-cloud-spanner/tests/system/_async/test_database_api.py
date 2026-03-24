# Copyright 2024 Google LLC All rights reserved.
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

from google.cloud import exceptions, spanner_v1

from .. import _helpers, _sample_data

DBAPI_OPERATION_TIMEOUT = 240  # seconds


@pytest.mark.asyncio
async def test_table_not_found(shared_instance):
    temp_db_id = _helpers.unique_id("tbl_not_found", separator="_")

    correct_table = "MyTable"
    incorrect_table = "NotMyTable"

    create_table = (
        f"CREATE TABLE {correct_table} (\n"
        f"    Id      STRING(36) NOT NULL,\n"
        f"    Field1  STRING(36) NOT NULL\n"
        f") PRIMARY KEY (Id)"
    )
    create_index = f"CREATE INDEX IDX ON {incorrect_table} (Field1)"

    temp_db = await shared_instance.database(
        temp_db_id, ddl_statements=[create_table, create_index]
    )
    with pytest.raises(exceptions.NotFound):
        await temp_db.create()


@pytest.mark.asyncio
async def test_list_databases(shared_instance, shared_database):
    database_names = []
    async for database in await shared_instance.list_databases():
        database_names.append(database.name)
    assert shared_database.name in database_names


@pytest.mark.asyncio
async def test_create_database(shared_instance, databases_to_delete, database_dialect):
    pool = spanner_v1.AsyncBurstyPool(labels={"testcase": "create_database_async"})
    temp_db_id = _helpers.unique_id("temp_db_async")
    temp_db = await shared_instance.database(
        temp_db_id, pool=pool, database_dialect=database_dialect
    )
    operation = await temp_db.create()
    databases_to_delete.append(temp_db)

    await operation.result(DBAPI_OPERATION_TIMEOUT)

    database_names = []
    async for database in await shared_instance.list_databases():
        database_names.append(database.name)
    assert temp_db.name in database_names


@pytest.mark.asyncio
async def test_db_batch_insert_then_db_snapshot_read(shared_database):
    await shared_database.reload()
    sd = _sample_data

    async with shared_database.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)
        batch.insert(sd.TABLE, sd.COLUMNS, sd.ROW_DATA)

    async with shared_database.snapshot(read_timestamp=batch.committed) as snapshot:
        results = await snapshot.read(sd.TABLE, sd.COLUMNS, sd.ALL)
        from_snap = []
        async for row in results:
            from_snap.append(row)

    sd._check_rows_data(from_snap)


@pytest.mark.asyncio
async def test_db_run_in_transaction_then_snapshot_execute_sql(shared_database):
    await shared_database.reload()
    sd = _sample_data

    async with shared_database.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    async def _unit_of_work(transaction, test):
        results = await transaction.execute_sql(sd.SQL)
        rows = []
        async for row in results:
            rows.append(row)
        assert rows == []

        transaction.insert_or_update(test.TABLE, test.COLUMNS, test.ROW_DATA)

    await shared_database.run_in_transaction(_unit_of_work, test=sd)

    async with shared_database.snapshot() as after:
        results = await after.execute_sql(sd.SQL)
        rows = []
        async for row in results:
            rows.append(row)

    sd._check_rows_data(rows)


@pytest.mark.asyncio
async def test_db_run_in_transaction_twice(shared_database):
    await shared_database.reload()
    sd = _sample_data

    async with shared_database.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    async def _unit_of_work(transaction, test):
        transaction.insert_or_update(test.TABLE, test.COLUMNS, test.ROW_DATA)

    await shared_database.run_in_transaction(_unit_of_work, test=sd)
    await shared_database.run_in_transaction(_unit_of_work, test=sd)

    async with shared_database.snapshot() as after:
        results = await after.execute_sql(sd.SQL)
        rows = []
        async for row in results:
            rows.append(row)

    sd._check_rows_data(rows)


@pytest.mark.asyncio
async def test_db_batch_insert_then_read_all_datatypes(shared_database):
    sd = _sample_data

    async with shared_database.batch() as batch:
        batch.delete(sd.ALL_TYPES_TABLE, sd.ALL)
        batch.insert(
            sd.ALL_TYPES_TABLE, sd.ALL_TYPES_COLUMNS, sd.EMULATOR_ALL_TYPES_ROWDATA
        )

    async with shared_database.snapshot(read_timestamp=batch.committed) as snapshot:
        results = await snapshot.read(sd.ALL_TYPES_TABLE, sd.ALL_TYPES_COLUMNS, sd.ALL)
        rows = []
        async for row in results:
            rows.append(row)

    sd._check_rows_data(rows, expected=sd.EMULATOR_ALL_TYPES_ROWDATA)


@pytest.mark.asyncio
async def test_transaction_manual_abort_retry(shared_database):
    sd = _sample_data
    await shared_database.reload()

    attempts = 0

    async def _unit_of_work(transaction):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            from google.api_core import exceptions
            from google.rpc import status_pb2

            # Create an Aborted error with at least one error in 'errors'
            # to avoid IndexError in the retry logic.
            status = status_pb2.Status(code=10, message="Simulated abort")
            raise exceptions.Aborted("Simulated abort", errors=[status])

        transaction.insert_or_update(sd.TABLE, sd.COLUMNS, sd.ROW_DATA)

    await shared_database.run_in_transaction(_unit_of_work)
    assert attempts == 2


@pytest.mark.asyncio
async def test_partitioned_update(shared_database):
    sd = _sample_data
    await shared_database.reload()

    # Partitioned DML
    row_count = await shared_database.execute_partitioned_dml(
        f"DELETE FROM {sd.TABLE} WHERE first_name = 'NonExistent'"
    )
    assert row_count == 0
