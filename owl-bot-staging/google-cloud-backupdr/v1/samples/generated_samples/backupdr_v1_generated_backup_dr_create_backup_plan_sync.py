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
# Snippet for CreateBackupPlan
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-backupdr


# [START backupdr_v1_generated_BackupDR_CreateBackupPlan_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import backupdr_v1


def sample_create_backup_plan():
    # Create a client
    client = backupdr_v1.BackupDRClient()

    # Initialize request argument(s)
    backup_plan = backupdr_v1.BackupPlan()
    backup_plan.backup_rules.standard_schedule.recurrence_type = "YEARLY"
    backup_plan.backup_rules.standard_schedule.backup_window.start_hour_of_day = 1820
    backup_plan.backup_rules.standard_schedule.backup_window.end_hour_of_day = 1573
    backup_plan.backup_rules.standard_schedule.time_zone = "time_zone_value"
    backup_plan.backup_rules.rule_id = "rule_id_value"
    backup_plan.backup_rules.backup_retention_days = 2237
    backup_plan.resource_type = "resource_type_value"
    backup_plan.backup_vault = "backup_vault_value"

    request = backupdr_v1.CreateBackupPlanRequest(
        parent="parent_value",
        backup_plan_id="backup_plan_id_value",
        backup_plan=backup_plan,
    )

    # Make the request
    operation = client.create_backup_plan(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)

# [END backupdr_v1_generated_BackupDR_CreateBackupPlan_sync]
