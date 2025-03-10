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
# Snippet for BatchOptimizeTours
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-maps-routeoptimization


# [START routeoptimization_v1_generated_RouteOptimization_BatchOptimizeTours_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.maps import routeoptimization_v1


async def sample_batch_optimize_tours():
    # Create a client
    client = routeoptimization_v1.RouteOptimizationAsyncClient()

    # Initialize request argument(s)
    model_configs = routeoptimization_v1.AsyncModelConfig()
    model_configs.input_config.gcs_source.uri = "uri_value"
    model_configs.input_config.data_format = "PROTO_TEXT"
    model_configs.output_config.gcs_destination.uri = "uri_value"
    model_configs.output_config.data_format = "PROTO_TEXT"

    request = routeoptimization_v1.BatchOptimizeToursRequest(
        parent="parent_value",
        model_configs=model_configs,
    )

    # Make the request
    operation = client.batch_optimize_tours(request=request)

    print("Waiting for operation to complete...")

    response = (await operation).result()

    # Handle the response
    print(response)

# [END routeoptimization_v1_generated_RouteOptimization_BatchOptimizeTours_async]
