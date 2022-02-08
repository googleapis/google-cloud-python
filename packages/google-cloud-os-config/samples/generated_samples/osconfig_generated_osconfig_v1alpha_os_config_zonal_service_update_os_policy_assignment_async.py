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
# Snippet for UpdateOSPolicyAssignment
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-os-config


# [START osconfig_generated_osconfig_v1alpha_OsConfigZonalService_UpdateOSPolicyAssignment_async]
from google.cloud import osconfig_v1alpha


async def sample_update_os_policy_assignment():
    # Create a client
    client = osconfig_v1alpha.OsConfigZonalServiceAsyncClient()

    # Initialize request argument(s)
    os_policy_assignment = osconfig_v1alpha.OSPolicyAssignment()
    os_policy_assignment.os_policies.id = "id_value"
    os_policy_assignment.os_policies.mode = "ENFORCEMENT"
    os_policy_assignment.os_policies.resource_groups.resources.pkg.apt.name = "name_value"
    os_policy_assignment.os_policies.resource_groups.resources.pkg.desired_state = "REMOVED"
    os_policy_assignment.os_policies.resource_groups.resources.id = "id_value"
    os_policy_assignment.rollout.disruption_budget.fixed = 528

    request = osconfig_v1alpha.UpdateOSPolicyAssignmentRequest(
        os_policy_assignment=os_policy_assignment,
    )

    # Make the request
    operation = client.update_os_policy_assignment(request=request)

    print("Waiting for operation to complete...")

    response = await operation.result()
    print(response)

# [END osconfig_generated_osconfig_v1alpha_OsConfigZonalService_UpdateOSPolicyAssignment_async]
