# Copyright 2021 Google LLC All rights reserved.
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

import time
import uuid

import pytest

from google.api_core import exceptions
from google.cloud import spanner_v1
from . import _helpers
from . import _sample_data


DBAPI_OPERATION_TIMEOUT = 240  # seconds


@pytest.fixture(scope="module")
def multiregion_instance(spanner_client, instance_operation_timeout, not_postgres):
    multi_region_instance_id = _helpers.unique_id("multi-region")
    multi_region_config = "nam3"
    config_name = "{}/instanceConfigs/{}".format(
        spanner_client.project_name, multi_region_config
    )
    create_time = str(int(time.time()))
    labels = {"python-spanner-systests": "true", "created": create_time}
    multiregion_instance = spanner_client.instance(
        instance_id=multi_region_instance_id,
        configuration_name=config_name,
        labels=labels,
    )
    operation = _helpers.retry_429_503(multiregion_instance.create)()
    operation.result(instance_operation_timeout)

    yield multiregion_instance

    _helpers.retry_429_503(multiregion_instance.delete)()


def test_list_databases(shared_instance, shared_database):
    # Since `shared_instance` is newly created in `setUpModule`, the
    # database created in `setUpClass` here will be the only one.
    database_names = [database.name for database in shared_instance.list_databases()]
    assert shared_database.name in database_names


def test_create_database(shared_instance, databases_to_delete, database_dialect):
    pool = spanner_v1.BurstyPool(labels={"testcase": "create_database"})
    temp_db_id = _helpers.unique_id("temp_db")
    temp_db = shared_instance.database(
        temp_db_id, pool=pool, database_dialect=database_dialect
    )
    operation = temp_db.create()
    databases_to_delete.append(temp_db)

    # We want to make sure the operation completes.
    operation.result(DBAPI_OPERATION_TIMEOUT)  # raises on failure / timeout.

    database_ids = [database.name for database in shared_instance.list_databases()]
    assert temp_db.name in database_ids


def test_create_database_pitr_invalid_retention_period(
    not_emulator,  # PITR-lite features are not supported by the emulator
    not_postgres,
    shared_instance,
):
    pool = spanner_v1.BurstyPool(labels={"testcase": "create_database_pitr"})
    temp_db_id = _helpers.unique_id("pitr_inv_db", separator="_")
    retention_period = "0d"
    ddl_statements = [
        f"ALTER DATABASE {temp_db_id}"
        f" SET OPTIONS (version_retention_period = '{retention_period}')"
    ]
    temp_db = shared_instance.database(
        temp_db_id, pool=pool, ddl_statements=ddl_statements
    )
    with pytest.raises(exceptions.InvalidArgument):
        temp_db.create()


def test_create_database_pitr_success(
    not_emulator,  # PITR-lite features are not supported by the emulator
    not_postgres,
    shared_instance,
    databases_to_delete,
):
    pool = spanner_v1.BurstyPool(labels={"testcase": "create_database_pitr"})
    temp_db_id = _helpers.unique_id("pitr_db", separator="_")
    retention_period = "7d"
    ddl_statements = [
        f"ALTER DATABASE {temp_db_id}"
        f" SET OPTIONS (version_retention_period = '{retention_period}')"
    ]
    temp_db = shared_instance.database(
        temp_db_id, pool=pool, ddl_statements=ddl_statements
    )
    operation = temp_db.create()
    databases_to_delete.append(temp_db)
    operation.result(DBAPI_OPERATION_TIMEOUT)  # raises on failure / timeout.

    database_ids = [database.name for database in shared_instance.list_databases()]
    assert temp_db.name in database_ids

    temp_db.reload()
    temp_db.version_retention_period == retention_period

    with temp_db.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT OPTION_VALUE AS version_retention_period "
            "FROM INFORMATION_SCHEMA.DATABASE_OPTIONS "
            "WHERE SCHEMA_NAME = '' "
            "AND OPTION_NAME = 'version_retention_period'"
        )
        for result in results:
            assert result[0] == retention_period


def test_create_database_with_default_leader_success(
    not_emulator,  # Default leader setting not supported by the emulator
    not_postgres,
    multiregion_instance,
    databases_to_delete,
):
    pool = spanner_v1.BurstyPool(labels={"testcase": "create_database_default_leader"})

    temp_db_id = _helpers.unique_id("dflt_ldr_db", separator="_")
    default_leader = "us-east4"
    ddl_statements = [
        f"ALTER DATABASE {temp_db_id}"
        f" SET OPTIONS (default_leader = '{default_leader}')"
    ]
    temp_db = multiregion_instance.database(
        temp_db_id, pool=pool, ddl_statements=ddl_statements
    )
    operation = temp_db.create()
    databases_to_delete.append(temp_db)
    operation.result(30)  # raises on failure / timeout.

    database_ids = [database.name for database in multiregion_instance.list_databases()]
    assert temp_db.name in database_ids

    temp_db.reload()
    assert temp_db.default_leader == default_leader

    with temp_db.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT OPTION_VALUE AS default_leader "
            "FROM INFORMATION_SCHEMA.DATABASE_OPTIONS "
            "WHERE SCHEMA_NAME = '' AND OPTION_NAME = 'default_leader'"
        )
        for result in results:
            assert result[0] == default_leader


def test_table_not_found(shared_instance):
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

    temp_db = shared_instance.database(
        temp_db_id, ddl_statements=[create_table, create_index]
    )
    with pytest.raises(exceptions.NotFound):
        temp_db.create()


def test_update_ddl_w_operation_id(
    shared_instance, databases_to_delete, database_dialect
):
    # We used to have:
    # @pytest.mark.skip(
    #    reason="'Database.update_ddl' has a flaky timeout.  See: "
    #    https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5629
    # )
    pool = spanner_v1.BurstyPool(labels={"testcase": "update_database_ddl"})
    temp_db_id = _helpers.unique_id("update_ddl", separator="_")
    temp_db = shared_instance.database(
        temp_db_id, pool=pool, database_dialect=database_dialect
    )
    create_op = temp_db.create()
    databases_to_delete.append(temp_db)
    create_op.result(DBAPI_OPERATION_TIMEOUT)  # raises on failure / timeout.

    # random but shortish always start with letter
    operation_id = f"a{str(uuid.uuid4())[:8]}"
    operation = temp_db.update_ddl(_helpers.DDL_STATEMENTS, operation_id=operation_id)

    assert operation_id == operation.operation.name.split("/")[-1]

    operation.result(DBAPI_OPERATION_TIMEOUT)  # raises on failure / timeout.

    temp_db.reload()

    assert len(temp_db.ddl_statements) == len(_helpers.DDL_STATEMENTS)


def test_update_ddl_w_pitr_invalid(
    not_emulator,
    not_postgres,
    shared_instance,
    databases_to_delete,
):
    pool = spanner_v1.BurstyPool(labels={"testcase": "update_database_ddl_pitr"})
    temp_db_id = _helpers.unique_id("pitr_upd_ddl_inv", separator="_")
    retention_period = "0d"
    temp_db = shared_instance.database(temp_db_id, pool=pool)

    create_op = temp_db.create()
    databases_to_delete.append(temp_db)
    create_op.result(DBAPI_OPERATION_TIMEOUT)  # raises on failure / timeout.

    assert temp_db.version_retention_period is None

    ddl_statements = _helpers.DDL_STATEMENTS + [
        f"ALTER DATABASE {temp_db_id}"
        f" SET OPTIONS (version_retention_period = '{retention_period}')"
    ]
    with pytest.raises(exceptions.InvalidArgument):
        temp_db.update_ddl(ddl_statements)


def test_update_ddl_w_pitr_success(
    not_emulator,
    not_postgres,
    shared_instance,
    databases_to_delete,
):
    pool = spanner_v1.BurstyPool(labels={"testcase": "update_database_ddl_pitr"})
    temp_db_id = _helpers.unique_id("pitr_upd_ddl_inv", separator="_")
    retention_period = "7d"
    temp_db = shared_instance.database(temp_db_id, pool=pool)

    create_op = temp_db.create()
    databases_to_delete.append(temp_db)
    create_op.result(DBAPI_OPERATION_TIMEOUT)  # raises on failure / timeout.

    assert temp_db.version_retention_period is None

    ddl_statements = _helpers.DDL_STATEMENTS + [
        f"ALTER DATABASE {temp_db_id}"
        f" SET OPTIONS (version_retention_period = '{retention_period}')"
    ]
    operation = temp_db.update_ddl(ddl_statements)
    operation.result(DBAPI_OPERATION_TIMEOUT)  # raises on failure / timeout.

    temp_db.reload()
    assert temp_db.version_retention_period == retention_period
    assert len(temp_db.ddl_statements) == len(ddl_statements)


def test_update_ddl_w_default_leader_success(
    not_emulator,
    not_postgres,
    multiregion_instance,
    databases_to_delete,
):
    pool = spanner_v1.BurstyPool(
        labels={"testcase": "update_database_ddl_default_leader"},
    )

    temp_db_id = _helpers.unique_id("dfl_ldrr_upd_ddl", separator="_")
    default_leader = "us-east4"
    temp_db = multiregion_instance.database(temp_db_id, pool=pool)

    create_op = temp_db.create()
    databases_to_delete.append(temp_db)
    create_op.result(DBAPI_OPERATION_TIMEOUT)  # raises on failure / timeout.

    assert temp_db.default_leader is None

    ddl_statements = _helpers.DDL_STATEMENTS + [
        f"ALTER DATABASE {temp_db_id}"
        f" SET OPTIONS (default_leader = '{default_leader}')"
    ]
    operation = temp_db.update_ddl(ddl_statements)
    operation.result(DBAPI_OPERATION_TIMEOUT)  # raises on failure / timeout.

    temp_db.reload()
    assert temp_db.default_leader == default_leader
    assert len(temp_db.ddl_statements) == len(ddl_statements)


def test_db_batch_insert_then_db_snapshot_read(shared_database):
    _helpers.retry_has_all_dll(shared_database.reload)()
    sd = _sample_data

    with shared_database.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)
        batch.insert(sd.TABLE, sd.COLUMNS, sd.ROW_DATA)

    with shared_database.snapshot(read_timestamp=batch.committed) as snapshot:
        from_snap = list(snapshot.read(sd.TABLE, sd.COLUMNS, sd.ALL))

    sd._check_rows_data(from_snap)


def test_db_run_in_transaction_then_snapshot_execute_sql(shared_database):
    _helpers.retry_has_all_dll(shared_database.reload)()
    sd = _sample_data

    with shared_database.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    def _unit_of_work(transaction, test):
        rows = list(transaction.read(test.TABLE, test.COLUMNS, sd.ALL))
        assert rows == []

        transaction.insert_or_update(test.TABLE, test.COLUMNS, test.ROW_DATA)

    shared_database.run_in_transaction(_unit_of_work, test=sd)

    with shared_database.snapshot() as after:
        rows = list(after.execute_sql(sd.SQL))

    sd._check_rows_data(rows)


def test_db_run_in_transaction_twice(shared_database):
    _helpers.retry_has_all_dll(shared_database.reload)()
    sd = _sample_data

    with shared_database.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    def _unit_of_work(transaction, test):
        transaction.insert_or_update(test.TABLE, test.COLUMNS, test.ROW_DATA)

    shared_database.run_in_transaction(_unit_of_work, test=sd)
    shared_database.run_in_transaction(_unit_of_work, test=sd)

    with shared_database.snapshot() as after:
        rows = list(after.execute_sql(sd.SQL))
    sd._check_rows_data(rows)


def test_db_run_in_transaction_twice_4181(shared_database):
    # See https://github.com/googleapis/google-cloud-python/issues/4181
    _helpers.retry_has_all_dll(shared_database.reload)()
    sd = _sample_data

    with shared_database.batch() as batch:
        batch.delete(sd.COUNTERS_TABLE, sd.ALL)

    def _unit_of_work(transaction, name):
        transaction.insert(sd.COUNTERS_TABLE, sd.COUNTERS_COLUMNS, [[name, 0]])

    shared_database.run_in_transaction(_unit_of_work, name="id_1")

    with pytest.raises(exceptions.AlreadyExists):
        shared_database.run_in_transaction(_unit_of_work, name="id_1")

    shared_database.run_in_transaction(_unit_of_work, name="id_2")

    with shared_database.snapshot() as after:
        rows = list(after.read(sd.COUNTERS_TABLE, sd.COUNTERS_COLUMNS, sd.ALL))

    assert len(rows) == 2
