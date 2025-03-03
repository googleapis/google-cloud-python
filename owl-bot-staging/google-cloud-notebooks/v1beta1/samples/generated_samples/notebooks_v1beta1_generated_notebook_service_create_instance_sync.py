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
# Snippet for CreateInstance
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-notebooks


# [START notebooks_v1beta1_generated_NotebookService_CreateInstance_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import notebooks_v1beta1


def sample_create_instance():
    # Create a client
    client = notebooks_v1beta1.NotebookServiceClient()

    # Initialize request argument(s)
    instance = notebooks_v1beta1.Instance()
    instance.vm_image.image_name = "image_name_value"
    instance.vm_image.project = "project_value"
    instance.machine_type = "machine_type_value"

    request = notebooks_v1beta1.CreateInstanceRequest(
        parent="parent_value",
        instance_id="instance_id_value",
        instance=instance,
    )

    # Make the request
    operation = client.create_instance(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)

# [END notebooks_v1beta1_generated_NotebookService_CreateInstance_sync]
