# Copyright 2020 Google Inc. All Rights Reserved.
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

from google.api_core.exceptions import DeadlineExceeded
from google.cloud import spanner
import pytest
from test_utils.retry import RetryErrors

import backup_sample
from snippets_test import cleanup_old_instances


def unique_instance_id():
    """ Creates a unique id for the database. """
    return f"test-instance-{uuid.uuid4().hex[:10]}"


def unique_database_id():
    """ Creates a unique id for the database. """
    return f"test-db-{uuid.uuid4().hex[:10]}"


def unique_backup_id():
    """ Creates a unique id for the backup. """
    return f"test-backup-{uuid.uuid4().hex[:10]}"


INSTANCE_ID = unique_instance_id()
DATABASE_ID = unique_database_id()
RESTORE_DB_ID = unique_database_id()
BACKUP_ID = unique_backup_id()
CMEK_RESTORE_DB_ID = unique_database_id()
CMEK_BACKUP_ID = unique_backup_id()
RETENTION_DATABASE_ID = unique_database_id()
RETENTION_PERIOD = "7d"


@pytest.fixture(scope="module")
def spanner_instance():
    spanner_client = spanner.Client()
    cleanup_old_instances(spanner_client)
    instance_config = "{}/instanceConfigs/{}".format(
        spanner_client.project_name, "regional-us-central1"
    )
    instance = spanner_client.instance(
        INSTANCE_ID,
        instance_config,
        labels={
           "cloud_spanner_samples": "true",
           "created": str(int(time.time()))
        }
    )
    op = instance.create()
    op.result(120)  # block until completion
    yield instance
    for database_pb in instance.list_databases():
        database = instance.database(database_pb.name.split("/")[-1])
        database.drop()
    for backup_pb in instance.list_backups():
        backup = instance.backup(backup_pb.name.split("/")[-1])
        backup.delete()
    instance.delete()


@pytest.fixture(scope="module")
def database(spanner_instance):
    """ Creates a temporary database that is removed after testing. """
    db = spanner_instance.database(DATABASE_ID)
    db.create()
    yield db
    db.drop()


def test_create_backup(capsys, database):
    version_time = None
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql("SELECT CURRENT_TIMESTAMP()")
        version_time = list(results)[0][0]

    backup_sample.create_backup(INSTANCE_ID, DATABASE_ID, BACKUP_ID, version_time)
    out, _ = capsys.readouterr()
    assert BACKUP_ID in out


def test_create_backup_with_encryption_key(capsys, spanner_instance, database):
    kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
        spanner_instance._client.project, "us-central1", "spanner-test-keyring", "spanner-test-cmek"
    )
    backup_sample.create_backup_with_encryption_key(INSTANCE_ID, DATABASE_ID, CMEK_BACKUP_ID, kms_key_name)
    out, _ = capsys.readouterr()
    assert CMEK_BACKUP_ID in out
    assert kms_key_name in out


# Depends on test_create_backup having run first
@RetryErrors(exception=DeadlineExceeded, max_tries=2)
def test_restore_database(capsys):
    backup_sample.restore_database(INSTANCE_ID, RESTORE_DB_ID, BACKUP_ID)
    out, _ = capsys.readouterr()
    assert (DATABASE_ID + " restored to ") in out
    assert (RESTORE_DB_ID + " from backup ") in out
    assert BACKUP_ID in out


# Depends on test_create_backup having run first
@RetryErrors(exception=DeadlineExceeded, max_tries=2)
def test_restore_database_with_encryption_key(capsys, spanner_instance):
    kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
        spanner_instance._client.project, "us-central1", "spanner-test-keyring", "spanner-test-cmek"
    )
    backup_sample.restore_database_with_encryption_key(INSTANCE_ID, CMEK_RESTORE_DB_ID, CMEK_BACKUP_ID, kms_key_name)
    out, _ = capsys.readouterr()
    assert (DATABASE_ID + " restored to ") in out
    assert (CMEK_RESTORE_DB_ID + " from backup ") in out
    assert CMEK_BACKUP_ID in out
    assert kms_key_name in out


# Depends on test_create_backup having run first
def test_list_backup_operations(capsys, spanner_instance):
    backup_sample.list_backup_operations(INSTANCE_ID, DATABASE_ID)
    out, _ = capsys.readouterr()
    assert BACKUP_ID in out
    assert DATABASE_ID in out


# Depends on test_create_backup having run first
def test_list_backups(capsys, spanner_instance):
    backup_sample.list_backups(INSTANCE_ID, DATABASE_ID, BACKUP_ID)
    out, _ = capsys.readouterr()
    id_count = out.count(BACKUP_ID)
    assert id_count == 7


# Depends on test_create_backup having run first
def test_update_backup(capsys):
    backup_sample.update_backup(INSTANCE_ID, BACKUP_ID)
    out, _ = capsys.readouterr()
    assert BACKUP_ID in out


# Depends on test_create_backup having run first
def test_delete_backup(capsys, spanner_instance):
    backup_sample.delete_backup(INSTANCE_ID, BACKUP_ID)
    out, _ = capsys.readouterr()
    assert BACKUP_ID in out


# Depends on test_create_backup having run first
def test_cancel_backup(capsys):
    backup_sample.cancel_backup(INSTANCE_ID, DATABASE_ID, BACKUP_ID)
    out, _ = capsys.readouterr()
    cancel_success = "Backup creation was successfully cancelled." in out
    cancel_failure = ("Backup was created before the cancel completed." in out) and (
        "Backup deleted." in out
    )
    assert cancel_success or cancel_failure


@RetryErrors(exception=DeadlineExceeded, max_tries=2)
def test_create_database_with_retention_period(capsys, spanner_instance):
    backup_sample.create_database_with_version_retention_period(INSTANCE_ID, RETENTION_DATABASE_ID, RETENTION_PERIOD)
    out, _ = capsys.readouterr()
    assert (RETENTION_DATABASE_ID + " created with ") in out
    assert ("retention period " + RETENTION_PERIOD) in out
    database = spanner_instance.database(RETENTION_DATABASE_ID)
    database.drop()
