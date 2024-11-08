# -*- coding: utf-8 -*-
#
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time

from create_test_config import set_test_config
from google.api_core import datetime_helpers
from google.api_core.exceptions import AlreadyExists, ResourceExhausted
from google.cloud.spanner_v1 import Client
from google.cloud.spanner_v1.instance import Instance
from google.cloud.spanner_v1.database import Database


USE_EMULATOR = os.getenv("SPANNER_EMULATOR_HOST") is not None

PROJECT = os.getenv(
    "GOOGLE_CLOUD_PROJECT",
    os.getenv("PROJECT_ID", "emulator-test-project"),
)
CLIENT = None

if USE_EMULATOR:
    from google.auth.credentials import AnonymousCredentials

    CLIENT = Client(project=PROJECT, credentials=AnonymousCredentials())
else:
    CLIENT = Client(project=PROJECT)


def delete_stale_test_instances():
    """Delete test instances that are older than four hours."""
    cutoff = int(time.time()) - 4 * 60 * 60
    instances_pbs = CLIENT.list_instances(
        "labels.python-spanner-sqlalchemy-systest:true"
    )
    for instance_pb in instances_pbs:
        instance = Instance.from_pb(instance_pb, CLIENT)
        if "created" not in instance.labels:
            continue
        create_time = int(instance.labels["created"])
        if create_time > cutoff:
            continue
        # Backups are not used in sqlalchemy dialect test,
        # therefore instance can just be deleted.
        try:
            instance.delete()
            time.sleep(5)  # Sleep for 5 seconds to give time for cooldown.
        except ResourceExhausted:
            print(
                "Unable to drop stale instance '{}'. May need manual delete.".format(
                    instance.instance_id
                )
            )


def delete_stale_test_databases():
    """Delete test databases that are older than four hours."""
    cutoff = (int(time.time()) - 4 * 60 * 60) * 1000
    instance = CLIENT.instance("sqlalchemy-dialect-test")
    if not instance.exists():
        return
    database_pbs = instance.list_databases()
    for database_pb in database_pbs:
        database = Database.from_pb(database_pb, instance)
        # The emulator does not return a create_time for databases.
        if database.create_time is None:
            continue
        create_time = datetime_helpers.to_milliseconds(database_pb.create_time)
        if create_time > cutoff:
            continue
        try:
            database.drop()
        except ResourceExhausted:
            print(
                "Unable to drop stale database '{}'. May need manual delete.".format(
                    database.database_id
                )
            )


def create_test_instance():
    instance_id = "sqlalchemy-dialect-test"
    instance = CLIENT.instance(instance_id)
    if not instance.exists():
        instance_config = f"projects/{PROJECT}/instanceConfigs/regional-us-east1"
        if USE_EMULATOR:
            configs = list(CLIENT.list_instance_configs())
            instance_config = configs[0].name
        create_time = str(int(time.time()))
        labels = {"python-spanner-sqlalchemy-systest": "true", "created": create_time}

        instance = CLIENT.instance(instance_id, instance_config, labels=labels)

        try:
            created_op = instance.create()
            created_op.result(1800)  # block until completion
        except AlreadyExists:
            pass  # instance was already created

    unique_resource_id = "%s%d" % ("-", 1000 * time.time())
    database_id = "sqlalchemy-test" + unique_resource_id

    try:
        database = instance.database(database_id)
        created_op = database.create()
        created_op.result(1800)
    except AlreadyExists:
        pass  # database was already created

    set_test_config(PROJECT, instance_id, database_id)


delete_stale_test_databases()
create_test_instance()
