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
# Snippet for UpdateModel
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-retail


# [START retail_v2beta_generated_ModelService_UpdateModel_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import retail_v2beta


def sample_update_model():
    # Create a client
    client = retail_v2beta.ModelServiceClient()

    # Initialize request argument(s)
    model = retail_v2beta.Model()
    model.name = "name_value"
    model.display_name = "display_name_value"
    model.type_ = "type__value"

    request = retail_v2beta.UpdateModelRequest(
        model=model,
    )

    # Make the request
    response = client.update_model(request=request)

    # Handle the response
    print(response)

# [END retail_v2beta_generated_ModelService_UpdateModel_sync]
