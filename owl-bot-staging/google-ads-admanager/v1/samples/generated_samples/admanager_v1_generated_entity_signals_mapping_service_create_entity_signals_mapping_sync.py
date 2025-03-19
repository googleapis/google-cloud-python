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
# Snippet for CreateEntitySignalsMapping
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-ads-admanager


# [START admanager_v1_generated_EntitySignalsMappingService_CreateEntitySignalsMapping_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.ads import admanager_v1


def sample_create_entity_signals_mapping():
    # Create a client
    client = admanager_v1.EntitySignalsMappingServiceClient()

    # Initialize request argument(s)
    entity_signals_mapping = admanager_v1.EntitySignalsMapping()
    entity_signals_mapping.audience_segment_id = 1980
    entity_signals_mapping.taxonomy_category_ids = [2268, 2269]

    request = admanager_v1.CreateEntitySignalsMappingRequest(
        parent="parent_value",
        entity_signals_mapping=entity_signals_mapping,
    )

    # Make the request
    response = client.create_entity_signals_mapping(request=request)

    # Handle the response
    print(response)

# [END admanager_v1_generated_EntitySignalsMappingService_CreateEntitySignalsMapping_sync]
