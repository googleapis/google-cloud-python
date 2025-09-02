# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
# Snippet for CreateBackupPlanAssociation
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-backupdr


# [START backupdr_v1_generated_BackupDR_CreateBackupPlanAssociation_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import backupdr_v1


async def sample_create_backup_plan_association():
    # Create a client
    client = backupdr_v1.BackupDRAsyncClient()

    # Initialize request argument(s)
    backup_plan_association = backupdr_v1.BackupPlanAssociation()
    backup_plan_association.resource_type = "resource_type_value"
    backup_plan_association.resource = "resource_value"
    backup_plan_association.backup_plan = "backup_plan_value"

    request = backupdr_v1.CreateBackupPlanAssociationRequest(
        parent="parent_value",
        backup_plan_association_id="backup_plan_association_id_value",
        backup_plan_association=backup_plan_association,
    )

    # Make the request
    operation = client.create_backup_plan_association(request=request)

    print("Waiting for operation to complete...")

    response = (await operation).result()

    # Handle the response
    print(response)

# [END backupdr_v1_generated_BackupDR_CreateBackupPlanAssociation_async]
