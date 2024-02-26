#!/usr/bin/env python

# Copyright 2024 Google, Inc.
#
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

"""This application demonstrates how to do basic operations using Cloud
Spanner.
For more information, see the README.rst under /spanner.
"""

import time

from google.cloud import spanner
from google.cloud.spanner_admin_database_v1.types import spanner_database_admin
from google.cloud.spanner_admin_instance_v1.types import spanner_instance_admin

OPERATION_TIMEOUT_SECONDS = 240


# [START spanner_create_instance]
def create_instance(instance_id):
    """Creates an instance."""
    spanner_client = spanner.Client()

    config_name = "{}/instanceConfigs/regional-us-central1".format(
        spanner_client.project_name
    )

    operation = spanner_client.instance_admin_api.create_instance(
        parent="projects/{}".format(spanner_client.project),
        instance_id=instance_id,
        instance=spanner_instance_admin.Instance(
            config=config_name,
            display_name="This is a display name.",
            node_count=1,
            labels={
                "cloud_spanner_samples": "true",
                "sample_name": "snippets-create_instance-explicit",
                "created": str(int(time.time())),
            },
        ),
    )

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print("Created instance {}".format(instance_id))


# [END spanner_create_instance]


# [START spanner_create_database_with_default_leader]
def create_database_with_default_leader(instance_id, database_id, default_leader):
    """Creates a database with tables with a default leader."""
    spanner_client = spanner.Client()
    operation = spanner_client.database_admin_api.create_database(
        request=spanner_database_admin.CreateDatabaseRequest(
            parent="projects/{}/instances/{}".format(
                spanner_client.project, instance_id
            ),
            create_statement="CREATE DATABASE {}".format(database_id),
            extra_statements=[
                """CREATE TABLE Singers (
                    SingerId     INT64 NOT NULL,
                    FirstName    STRING(1024),
                    LastName     STRING(1024),
                    SingerInfo   BYTES(MAX)
                ) PRIMARY KEY (SingerId)""",
                """CREATE TABLE Albums (
                    SingerId     INT64 NOT NULL,
                    AlbumId      INT64 NOT NULL,
                    AlbumTitle   STRING(MAX)
                ) PRIMARY KEY (SingerId, AlbumId),
                INTERLEAVE IN PARENT Singers ON DELETE CASCADE""",
                "ALTER DATABASE {}"
                " SET OPTIONS (default_leader = '{}')".format(
                    database_id, default_leader
                ),
            ],
        )
    )

    print("Waiting for operation to complete...")
    database = operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        "Database {} created with default leader {}".format(
            database.name, database.default_leader
        )
    )


# [END spanner_create_database_with_default_leader]
