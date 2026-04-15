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

from google.api_core import datetime_helpers
from google.api_core.exceptions import AlreadyExists, ResourceExhausted
from google.cloud.spanner_v1 import Client
from google.cloud.spanner_v1.database import Database
from google.cloud.spanner_v1.instance import Instance

from create_test_config import set_test_config

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
    """Delete stale or excessive test databases.

    Deletes stale test databases that are older than 4 hours and
    ensures we don't hit the 100 database limit per spanner instance by
    deleting the oldest databases if we are near the limit.
    """
    cutoff = (int(time.time()) - 4 * 60 * 60) * 1000
    instance = CLIENT.instance("sqlalchemy-dialect-test")
    if not instance.exists():
        return
        
    # Convert iterator to list to allow multiple passes and length check
    database_pbs = list(instance.list_databases())
    
    # First pass: Delete stale databases
    remaining_dbs = []
    for database_pb in database_pbs:
        database = Database.from_pb(database_pb, instance)
        # The emulator does not return a create_time for databases.
        if database.create_time is None:
            remaining_dbs.append(database_pb)
            continue
            
        create_time = datetime_helpers.to_milliseconds(database_pb.create_time)
        if create_time > cutoff:
            remaining_dbs.append(database_pb)
            continue
            
        try:
            database.drop()
            print(f"Dropped stale database '{database.database_id}'")
        except ResourceExhausted:
            print(
                "Unable to drop stale database '{}'. May need manual delete.".format(
                    database.database_id
                )
            )
            remaining_dbs.append(database_pb) # Still there

    # Second pass: If we are still near the limit (e.g., 90+ databases),
    # delete the oldest ones regardless of age to free up slots.
    # Spanner instances have a hard limit of 100 databases.
    LIMIT = 90
    if len(remaining_dbs) >= LIMIT:
        print(f"Database count ({len(remaining_dbs)}) is near limit. Cleaning up oldest databases.")
        
        # Sort by creation time
        dbs_with_time = []
        for db_pb in remaining_dbs:
            if db_pb.create_time:
                dbs_with_time.append((db_pb.create_time, db_pb.name))
                
        dbs_with_time.sort() # Sorts by time ascending (oldest first)
        
        # Delete enough to get below the limit
        to_delete = len(remaining_dbs) - (LIMIT - 10) # Aim for 80
        deleted_count = 0
        
        for create_time, full_name in dbs_with_time:
            if deleted_count >= to_delete:
                break
            db_id = full_name.split('/')[-1]
            try:
                instance.database(db_id).drop()
                print(f"Dropped oldest database '{db_id}' to prevent resource exhaustion.")
                deleted_count += 1
            except Exception as e:
                print(f"Failed to drop database '{db_id}': {e}")


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
