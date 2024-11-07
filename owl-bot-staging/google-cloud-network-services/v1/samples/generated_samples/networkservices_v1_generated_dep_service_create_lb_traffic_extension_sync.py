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
# Snippet for CreateLbTrafficExtension
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-network-services


# [START networkservices_v1_generated_DepService_CreateLbTrafficExtension_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import network_services_v1


def sample_create_lb_traffic_extension():
    # Create a client
    client = network_services_v1.DepServiceClient()

    # Initialize request argument(s)
    lb_traffic_extension = network_services_v1.LbTrafficExtension()
    lb_traffic_extension.name = "name_value"
    lb_traffic_extension.forwarding_rules = ['forwarding_rules_value1', 'forwarding_rules_value2']
    lb_traffic_extension.extension_chains.name = "name_value"
    lb_traffic_extension.extension_chains.match_condition.cel_expression = "cel_expression_value"
    lb_traffic_extension.extension_chains.extensions.name = "name_value"
    lb_traffic_extension.extension_chains.extensions.service = "service_value"
    lb_traffic_extension.load_balancing_scheme = "EXTERNAL_MANAGED"

    request = network_services_v1.CreateLbTrafficExtensionRequest(
        parent="parent_value",
        lb_traffic_extension_id="lb_traffic_extension_id_value",
        lb_traffic_extension=lb_traffic_extension,
    )

    # Make the request
    operation = client.create_lb_traffic_extension(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)

# [END networkservices_v1_generated_DepService_CreateLbTrafficExtension_sync]
