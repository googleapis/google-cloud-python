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
# Snippet for CreateControl
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-retail


# [START retail_v2alpha_generated_ControlService_CreateControl_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import retail_v2alpha


async def sample_create_control():
    # Create a client
    client = retail_v2alpha.ControlServiceAsyncClient()

    # Initialize request argument(s)
    control = retail_v2alpha.Control()
    control.facet_spec.facet_key.key = "key_value"
    control.display_name = "display_name_value"
    control.solution_types = ['SOLUTION_TYPE_SEARCH']

    request = retail_v2alpha.CreateControlRequest(
        parent="parent_value",
        control=control,
        control_id="control_id_value",
    )

    # Make the request
    response = await client.create_control(request=request)

    # Handle the response
    print(response)

# [END retail_v2alpha_generated_ControlService_CreateControl_async]
