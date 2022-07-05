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

import operator
import os
import time

from google.api_core import exceptions
from google.cloud.spanner_v1 import instance as instance_mod
from tests import _fixtures
from test_utils import retry
from test_utils import system


CREATE_INSTANCE_ENVVAR = "GOOGLE_CLOUD_TESTS_CREATE_SPANNER_INSTANCE"
CREATE_INSTANCE = os.getenv(CREATE_INSTANCE_ENVVAR) is not None

INSTANCE_ID_ENVVAR = "GOOGLE_CLOUD_TESTS_SPANNER_INSTANCE"
INSTANCE_ID_DEFAULT = "google-cloud-python-systest"
INSTANCE_ID = os.environ.get(INSTANCE_ID_ENVVAR, INSTANCE_ID_DEFAULT)

SKIP_BACKUP_TESTS_ENVVAR = "SKIP_BACKUP_TESTS"
SKIP_BACKUP_TESTS = os.getenv(SKIP_BACKUP_TESTS_ENVVAR) is not None

INSTANCE_OPERATION_TIMEOUT_IN_SECONDS = int(
    os.getenv("SPANNER_INSTANCE_OPERATION_TIMEOUT_IN_SECONDS", 560)
)
DATABASE_OPERATION_TIMEOUT_IN_SECONDS = int(
    os.getenv("SPANNER_DATABASE_OPERATION_TIMEOUT_IN_SECONDS", 120)
)
BACKUP_OPERATION_TIMEOUT_IN_SECONDS = int(
    os.getenv("SPANNER_BACKUP_OPERATION_TIMEOUT_IN_SECONDS", 1200)
)

USE_EMULATOR_ENVVAR = "SPANNER_EMULATOR_HOST"
USE_EMULATOR = os.getenv(USE_EMULATOR_ENVVAR) is not None

DATABASE_DIALECT_ENVVAR = "SPANNER_DATABASE_DIALECT"
DATABASE_DIALECT = os.getenv(DATABASE_DIALECT_ENVVAR)

EMULATOR_PROJECT_ENVVAR = "GCLOUD_PROJECT"
EMULATOR_PROJECT_DEFAULT = "emulator-test-project"
EMULATOR_PROJECT = os.getenv(EMULATOR_PROJECT_ENVVAR, EMULATOR_PROJECT_DEFAULT)


DDL_STATEMENTS = (
    _fixtures.PG_DDL_STATEMENTS
    if DATABASE_DIALECT == "POSTGRESQL"
    else (
        _fixtures.EMULATOR_DDL_STATEMENTS if USE_EMULATOR else _fixtures.DDL_STATEMENTS
    )
)

retry_true = retry.RetryResult(operator.truth)
retry_false = retry.RetryResult(operator.not_)

retry_503 = retry.RetryErrors(exceptions.ServiceUnavailable)
retry_429_503 = retry.RetryErrors(
    exceptions.TooManyRequests, exceptions.ServiceUnavailable, 8
)
retry_mabye_aborted_txn = retry.RetryErrors(exceptions.ServerError, exceptions.Aborted)
retry_mabye_conflict = retry.RetryErrors(exceptions.ServerError, exceptions.Conflict)


def _has_all_ddl(database):
    # Predicate to test for EC completion.
    return len(database.ddl_statements) == len(DDL_STATEMENTS)


retry_has_all_dll = retry.RetryInstanceState(_has_all_ddl)


def scrub_referencing_databases(to_scrub, db_list):
    for db_name in db_list:
        db = to_scrub.database(db_name.split("/")[-1])
        try:
            retry_429_503(db.delete)()
        except exceptions.NotFound:  # lost the race
            pass


def scrub_instance_backups(to_scrub):
    try:
        for backup_pb in to_scrub.list_backups():
            # Backup cannot be deleted while referencing databases exist.
            scrub_referencing_databases(to_scrub, backup_pb.referencing_databases)
            bkp = instance_mod.Backup.from_pb(backup_pb, to_scrub)
            try:
                # Instance cannot be deleted while backups exist.
                retry_429_503(bkp.delete)()
            except exceptions.NotFound:  # lost the race
                pass
    except exceptions.MethodNotImplemented:
        # The CI emulator raises 501:  local versions seem fine.
        pass


def scrub_instance_ignore_not_found(to_scrub):
    """Helper for func:`cleanup_old_instances`"""
    scrub_instance_backups(to_scrub)

    try:
        retry_429_503(to_scrub.delete)()
    except exceptions.NotFound:  # lost the race
        pass


def cleanup_old_instances(spanner_client):
    cutoff = int(time.time()) - 3 * 60 * 60  # three hour ago
    instance_filter = "labels.python-spanner-systests:true"

    for instance_pb in spanner_client.list_instances(filter_=instance_filter):
        instance = instance_mod.Instance.from_pb(instance_pb, spanner_client)

        if "created" in instance.labels:
            create_time = int(instance.labels["created"])

            if create_time <= cutoff:
                scrub_instance_ignore_not_found(instance)


def unique_id(prefix, separator="-"):
    return f"{prefix}{system.unique_resource_id(separator)}"
