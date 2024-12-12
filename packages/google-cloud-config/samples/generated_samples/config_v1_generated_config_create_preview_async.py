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
# Snippet for CreatePreview
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-config


# [START config_v1_generated_Config_CreatePreview_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import config_v1


async def sample_create_preview():
    # Create a client
    client = config_v1.ConfigAsyncClient()

    # Initialize request argument(s)
    preview = config_v1.Preview()
    preview.terraform_blueprint.gcs_source = "gcs_source_value"
    preview.service_account = "service_account_value"

    request = config_v1.CreatePreviewRequest(
        parent="parent_value",
        preview=preview,
    )

    # Make the request
    operation = client.create_preview(request=request)

    print("Waiting for operation to complete...")

    response = (await operation).result()

    # Handle the response
    print(response)

# [END config_v1_generated_Config_CreatePreview_async]
