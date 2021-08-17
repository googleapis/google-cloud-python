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

import pytest

from google.cloud import spanner_v1
from . import _helpers


@pytest.fixture(scope="function")
def if_create_instance():
    if not _helpers.CREATE_INSTANCE:
        pytest.skip(f"{_helpers.CREATE_INSTANCE_ENVVAR} not set in environment.")


@pytest.fixture(scope="function")
def no_create_instance():
    if _helpers.CREATE_INSTANCE:
        pytest.skip(f"{_helpers.CREATE_INSTANCE_ENVVAR} set in environment.")


@pytest.fixture(scope="function")
def if_backup_tests():
    if _helpers.SKIP_BACKUP_TESTS:
        pytest.skip(f"{_helpers.SKIP_BACKUP_TESTS_ENVVAR} set in environment.")


@pytest.fixture(scope="function")
def not_emulator():
    if _helpers.USE_EMULATOR:
        pytest.skip(f"{_helpers.USE_EMULATOR_ENVVAR} set in environment.")


@pytest.fixture(scope="session")
def spanner_client():
    if _helpers.USE_EMULATOR:
        from google.auth.credentials import AnonymousCredentials

        credentials = AnonymousCredentials()
        return spanner_v1.Client(
            project=_helpers.EMULATOR_PROJECT, credentials=credentials,
        )
    else:
        return spanner_v1.Client()  # use google.auth.default credentials


@pytest.fixture(scope="session")
def instance_operation_timeout():
    return _helpers.INSTANCE_OPERATION_TIMEOUT_IN_SECONDS


@pytest.fixture(scope="session")
def database_operation_timeout():
    return _helpers.DATABASE_OPERATION_TIMEOUT_IN_SECONDS


@pytest.fixture(scope="session")
def shared_instance_id():
    if _helpers.CREATE_INSTANCE:
        return f"{_helpers.unique_id('google-cloud')}"

    return _helpers.INSTANCE_ID


@pytest.fixture(scope="session")
def instance_configs(spanner_client):
    configs = list(_helpers.retry_503(spanner_client.list_instance_configs)())

    if not _helpers.USE_EMULATOR:

        # Defend against back-end returning configs for regions we aren't
        # actually allowed to use.
        configs = [config for config in configs if "-us-" in config.name]

    yield configs


@pytest.fixture(scope="session")
def instance_config(instance_configs):
    if not instance_configs:
        raise ValueError("No instance configs found.")

    yield instance_configs[0]


@pytest.fixture(scope="session")
def existing_instances(spanner_client):
    instances = list(_helpers.retry_503(spanner_client.list_instances)())

    yield instances


@pytest.fixture(scope="session")
def shared_instance(
    spanner_client,
    instance_operation_timeout,
    shared_instance_id,
    instance_config,
    existing_instances,  # evalutate before creating one
):
    _helpers.cleanup_old_instances(spanner_client)

    if _helpers.CREATE_INSTANCE:
        create_time = str(int(time.time()))
        labels = {"python-spanner-systests": "true", "created": create_time}

        instance = spanner_client.instance(
            shared_instance_id, instance_config.name, labels=labels
        )
        created_op = _helpers.retry_429_503(instance.create)()
        created_op.result(instance_operation_timeout)  # block until completion

    else:  # reuse existing instance
        instance = spanner_client.instance(shared_instance_id)
        instance.reload()

    yield instance

    if _helpers.CREATE_INSTANCE:
        _helpers.retry_429_503(instance.delete)()


@pytest.fixture(scope="session")
def shared_database(shared_instance, database_operation_timeout):
    database_name = _helpers.unique_id("test_database")
    pool = spanner_v1.BurstyPool(labels={"testcase": "database_api"})
    database = shared_instance.database(
        database_name, ddl_statements=_helpers.DDL_STATEMENTS, pool=pool
    )
    operation = database.create()
    operation.result(database_operation_timeout)  # raises on failure / timeout.

    yield database

    database.drop()


@pytest.fixture(scope="function")
def databases_to_delete():
    to_delete = []

    yield to_delete

    for database in to_delete:
        database.drop()
