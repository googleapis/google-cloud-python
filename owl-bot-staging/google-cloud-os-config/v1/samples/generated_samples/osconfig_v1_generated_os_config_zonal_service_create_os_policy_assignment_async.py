# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
# Snippet for CreateOSPolicyAssignment
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-os-config


# [START osconfig_v1_generated_OsConfigZonalService_CreateOSPolicyAssignment_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import osconfig_v1


async def sample_create_os_policy_assignment():
    # Create a client
    client = osconfig_v1.OsConfigZonalServiceAsyncClient()

    # Initialize request argument(s)
    os_policy_assignment = osconfig_v1.OSPolicyAssignment()
    os_policy_assignment.os_policies.id = "id_value"
    os_policy_assignment.os_policies.mode = "ENFORCEMENT"
    os_policy_assignment.os_policies.resource_groups.resources.pkg.apt.name = "name_value"
    os_policy_assignment.os_policies.resource_groups.resources.pkg.desired_state = "REMOVED"
    os_policy_assignment.os_policies.resource_groups.resources.id = "id_value"
    os_policy_assignment.rollout.disruption_budget.fixed = 528

    request = osconfig_v1.CreateOSPolicyAssignmentRequest(
        parent="parent_value",
        os_policy_assignment=os_policy_assignment,
        os_policy_assignment_id="os_policy_assignment_id_value",
    )

    # Make the request
    operation = client.create_os_policy_assignment(request=request)

    print("Waiting for operation to complete...")

    response = (await operation).result()

    # Handle the response
    print(response)

# [END osconfig_v1_generated_OsConfigZonalService_CreateOSPolicyAssignment_async]
