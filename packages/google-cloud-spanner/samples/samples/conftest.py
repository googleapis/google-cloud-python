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
""" Shared pytest fixtures."""

import time
import uuid

import pytest
from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1
from google.cloud.spanner_admin_database_v1.types.common import DatabaseDialect
from google.cloud.spanner_v1 import backup, client, database, instance
from test_utils import retry

INSTANCE_CREATION_TIMEOUT = 560  # seconds

OPERATION_TIMEOUT_SECONDS = 120  # seconds

retry_429 = retry.RetryErrors(exceptions.ResourceExhausted, delay=15)


@pytest.fixture(scope="module")
def sample_name():
    """Sample testcase modules must define this fixture.

    The name is used to label the instance created by the sample, to
    aid in debugging leaked instances.
    """
    raise NotImplementedError("Define 'sample_name' fixture in sample test driver")


@pytest.fixture(scope="module")
def database_dialect():
    """Database dialect to be used for this sample.

    The dialect is used to initialize the dialect for the database.
    It can either be GoogleStandardSql or PostgreSql.
    """
    # By default, we consider GOOGLE_STANDARD_SQL dialect. Other specific tests
    # can override this if required.
    return DatabaseDialect.GOOGLE_STANDARD_SQL


@pytest.fixture(scope="session")
def spanner_client():
    """Shared client used across all samples in a session."""
    return client.Client()


def scrub_instance_ignore_not_found(to_scrub):
    """Helper for func:`cleanup_old_instances`"""
    try:
        for backup_pb in to_scrub.list_backups():
            backup.Backup.from_pb(backup_pb, to_scrub).delete()

        retry_429(to_scrub.delete)()
    except exceptions.NotFound:
        pass


@pytest.fixture(scope="session")
def cleanup_old_instances(spanner_client):
    """Delete instances, created by samples, that are older than an hour."""
    cutoff = int(time.time()) - 1 * 60 * 60
    instance_filter = "labels.cloud_spanner_samples:true"

    for instance_pb in spanner_client.list_instances(filter_=instance_filter):
        inst = instance.Instance.from_pb(instance_pb, spanner_client)

        if "created" in inst.labels:
            create_time = int(inst.labels["created"])

            if create_time <= cutoff:
                scrub_instance_ignore_not_found(inst)


@pytest.fixture(scope="module")
def instance_id():
    """Unique id for the instance used in samples."""
    return f"test-instance-{uuid.uuid4().hex[:10]}"


@pytest.fixture(scope="module")
def multi_region_instance_id():
    """Unique id for the multi-region instance used in samples."""
    return f"multi-instance-{uuid.uuid4().hex[:10]}"


@pytest.fixture(scope="module")
def instance_config(spanner_client):
    return "{}/instanceConfigs/{}".format(
        spanner_client.project_name, "regional-us-central1"
    )


@pytest.fixture(scope="module")
def multi_region_instance_config(spanner_client):
    return "{}/instanceConfigs/{}".format(spanner_client.project_name, "nam3")


@pytest.fixture(scope="module")
def proto_descriptor_file():
    import os

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "testdata/descriptors.pb")
    file = open(filename, "rb")
    yield file.read()
    file.close()


@pytest.fixture(scope="module")
def sample_instance(
    spanner_client,
    cleanup_old_instances,
    instance_id,
    instance_config,
    sample_name,
):
    sample_instance = spanner_client.instance(
        instance_id,
        instance_config,
        labels={
            "cloud_spanner_samples": "true",
            "sample_name": sample_name,
            "created": str(int(time.time())),
        },
    )
    op = retry_429(sample_instance.create)()
    op.result(INSTANCE_CREATION_TIMEOUT)  # block until completion

    # Eventual consistency check
    retry_found = retry.RetryResult(bool)
    retry_found(sample_instance.exists)()

    yield sample_instance

    for database_pb in sample_instance.list_databases():
        database.Database.from_pb(database_pb, sample_instance).drop()

    for backup_pb in sample_instance.list_backups():
        backup.Backup.from_pb(backup_pb, sample_instance).delete()

    sample_instance.delete()


@pytest.fixture(scope="module")
def multi_region_instance(
    spanner_client,
    cleanup_old_instances,
    multi_region_instance_id,
    multi_region_instance_config,
    sample_name,
):
    multi_region_instance = spanner_client.instance(
        multi_region_instance_id,
        multi_region_instance_config,
        labels={
            "cloud_spanner_samples": "true",
            "sample_name": sample_name,
            "created": str(int(time.time())),
        },
    )
    op = retry_429(multi_region_instance.create)()
    op.result(INSTANCE_CREATION_TIMEOUT)  # block until completion

    # Eventual consistency check
    retry_found = retry.RetryResult(bool)
    retry_found(multi_region_instance.exists)()

    yield multi_region_instance

    for database_pb in multi_region_instance.list_databases():
        database.Database.from_pb(database_pb, multi_region_instance).drop()

    for backup_pb in multi_region_instance.list_backups():
        backup.Backup.from_pb(backup_pb, multi_region_instance).delete()

    multi_region_instance.delete()


@pytest.fixture(scope="module")
def database_id():
    """Id for the database used in samples.

    Sample testcase modules can override as needed.
    """
    return "my-database-id"


@pytest.fixture(scope="module")
def proto_columns_database(
    spanner_client,
    sample_instance,
    proto_columns_database_id,
    proto_columns_database_ddl,
    database_dialect,
):
    if database_dialect == DatabaseDialect.GOOGLE_STANDARD_SQL:
        sample_database = sample_instance.database(
            proto_columns_database_id,
            ddl_statements=proto_columns_database_ddl,
        )

        if not sample_database.exists():
            operation = sample_database.create()
            operation.result(OPERATION_TIMEOUT_SECONDS)

        yield sample_database

        sample_database.drop()


@pytest.fixture(scope="module")
def bit_reverse_sequence_database_id():
    """Id for the database used in bit reverse sequence samples.

    Sample testcase modules can override as needed.
    """
    return "sequence-database-id"


@pytest.fixture(scope="module")
def database_ddl():
    """Sequence of DDL statements used to set up the database.

    Sample testcase modules can override as needed.
    """
    return []


@pytest.fixture(scope="module")
def sample_database(
    spanner_client, sample_instance, database_id, database_ddl, database_dialect
):
    if database_dialect == DatabaseDialect.POSTGRESQL:
        sample_database = sample_instance.database(
            database_id,
            database_dialect=DatabaseDialect.POSTGRESQL,
        )

        if not sample_database.exists():
            operation = sample_database.create()
            operation.result(OPERATION_TIMEOUT_SECONDS)

        request = spanner_admin_database_v1.UpdateDatabaseDdlRequest(
            database=sample_database.name,
            statements=database_ddl,
        )

        operation = spanner_client.database_admin_api.update_database_ddl(request)
        operation.result(OPERATION_TIMEOUT_SECONDS)

        yield sample_database

        sample_database.drop()
        return

    sample_database = sample_instance.database(
        database_id,
        ddl_statements=database_ddl,
    )

    if not sample_database.exists():
        operation = sample_database.create()
        operation.result(OPERATION_TIMEOUT_SECONDS)

    yield sample_database

    sample_database.drop()


@pytest.fixture(scope="module")
def bit_reverse_sequence_database(
    spanner_client, sample_instance, bit_reverse_sequence_database_id, database_dialect
):
    if database_dialect == DatabaseDialect.POSTGRESQL:
        bit_reverse_sequence_database = sample_instance.database(
            bit_reverse_sequence_database_id,
            database_dialect=DatabaseDialect.POSTGRESQL,
        )

        if not bit_reverse_sequence_database.exists():
            operation = bit_reverse_sequence_database.create()
            operation.result(OPERATION_TIMEOUT_SECONDS)

        yield bit_reverse_sequence_database

        bit_reverse_sequence_database.drop()
        return

    bit_reverse_sequence_database = sample_instance.database(
        bit_reverse_sequence_database_id
    )

    if not bit_reverse_sequence_database.exists():
        operation = bit_reverse_sequence_database.create()
        operation.result(OPERATION_TIMEOUT_SECONDS)

    yield bit_reverse_sequence_database

    bit_reverse_sequence_database.drop()


@pytest.fixture(scope="module")
def kms_key_name(spanner_client):
    return "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
        spanner_client.project,
        "us-central1",
        "spanner-test-keyring",
        "spanner-test-cmek",
    )
