# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
#
# Generated code. DO NOT EDIT!
#
# Snippet for CreateMigrationJob
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-dms


# [START datamigration_generated_clouddms_v1_DataMigrationService_CreateMigrationJob_async]
from google.cloud import clouddms_v1


async def sample_create_migration_job():
    # Create a client
    client = clouddms_v1.DataMigrationServiceAsyncClient()

    # Initialize request argument(s)
    migration_job = clouddms_v1.MigrationJob()
    migration_job.reverse_ssh_connectivity.vm_ip = "vm_ip_value"
    migration_job.reverse_ssh_connectivity.vm_port = 775
    migration_job.type_ = "CONTINUOUS"
    migration_job.source = "source_value"
    migration_job.destination = "destination_value"

    request = clouddms_v1.CreateMigrationJobRequest(
        parent="parent_value",
        migration_job_id="migration_job_id_value",
        migration_job=migration_job,
    )

    # Make the request
    operation = client.create_migration_job(request=request)

    print("Waiting for operation to complete...")

    response = await operation.result()

    # Handle the response
    print(response)

# [END datamigration_generated_clouddms_v1_DataMigrationService_CreateMigrationJob_async]
