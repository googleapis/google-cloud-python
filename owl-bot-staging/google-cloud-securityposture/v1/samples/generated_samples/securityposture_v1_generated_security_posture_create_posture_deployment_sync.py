# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
# Snippet for CreatePostureDeployment
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-securityposture


# [START securityposture_v1_generated_SecurityPosture_CreatePostureDeployment_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import securityposture_v1


def sample_create_posture_deployment():
    # Create a client
    client = securityposture_v1.SecurityPostureClient()

    # Initialize request argument(s)
    posture_deployment = securityposture_v1.PostureDeployment()
    posture_deployment.name = "name_value"
    posture_deployment.target_resource = "target_resource_value"
    posture_deployment.posture_id = "posture_id_value"
    posture_deployment.posture_revision_id = "posture_revision_id_value"

    request = securityposture_v1.CreatePostureDeploymentRequest(
        parent="parent_value",
        posture_deployment_id="posture_deployment_id_value",
        posture_deployment=posture_deployment,
    )

    # Make the request
    operation = client.create_posture_deployment(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)

# [END securityposture_v1_generated_SecurityPosture_CreatePostureDeployment_sync]
