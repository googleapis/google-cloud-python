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
# Snippet for CreateClientConnectorService
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-beyondcorp-clientconnectorservices


# [START beyondcorp_v1_generated_ClientConnectorServicesService_CreateClientConnectorService_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import beyondcorp_clientconnectorservices_v1


def sample_create_client_connector_service():
    # Create a client
    client = beyondcorp_clientconnectorservices_v1.ClientConnectorServicesServiceClient()

    # Initialize request argument(s)
    client_connector_service = beyondcorp_clientconnectorservices_v1.ClientConnectorService()
    client_connector_service.name = "name_value"
    client_connector_service.ingress.config.transport_protocol = "TCP"
    client_connector_service.ingress.config.destination_routes.address = "address_value"
    client_connector_service.ingress.config.destination_routes.netmask = "netmask_value"
    client_connector_service.egress.peered_vpc.network_vpc = "network_vpc_value"

    request = beyondcorp_clientconnectorservices_v1.CreateClientConnectorServiceRequest(
        parent="parent_value",
        client_connector_service=client_connector_service,
    )

    # Make the request
    operation = client.create_client_connector_service(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)

# [END beyondcorp_v1_generated_ClientConnectorServicesService_CreateClientConnectorService_sync]
